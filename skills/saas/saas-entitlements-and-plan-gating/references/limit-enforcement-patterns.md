# Limit Enforcement Patterns - Reference

A feature gate is a boolean: can this tenant use X? A limit is a quantity: has this tenant used more than its allowance of Y this period? Limits are harder than feature gates because they involve counting, the counting races with the action being counted, and the period rolls over. This reference covers atomic counters, period rollover, hard vs soft caps, metering, grace, and the HTTP semantics (402 vs 429) that the wrong choice gets backwards.

## section 1 The Race Condition Is the Whole Problem

The naive limit check is:

```python
# WRONG - races
count = db.execute("SELECT COUNT(*) FROM projects WHERE tenant_id = %s", tenant_id)
if count >= limit:
    deny()
else:
    db.execute("INSERT INTO projects ...")   # two concurrent requests both pass the check
```

Two concurrent requests both read `count = limit - 1`, both pass, both insert, and the tenant now has `limit + 1`. Under load this is not rare - it is the default outcome. Every pattern below exists to make "check and consume" atomic.

## section 2 Choosing the Enforcement Mechanism

| Limit kind | Example | Mechanism | Why |
|---|---|---|---|
| Low-cardinality resource | seats, projects | DB unique constraint or `SELECT ... FOR UPDATE` on a counter row | Correctness matters; volume is low; the DB is the source of truth anyway |
| High-frequency metered | API calls/month, AI tokens | Redis atomic `INCRBY` against a period key, reconciled to DB | Sub-millisecond; the DB cannot take a write per request |
| Storage / continuous | storage GB | Maintained running total updated on upload/delete + periodic reconciliation | Cannot COUNT(*) bytes per request; drift corrected by a sweep |
| Burst rate | requests/second | Token bucket (see `saas-rate-limiting-and-quotas`) | This is a rate, not a quota; different concern, different HTTP code |

The wrong choice is using `SELECT COUNT(*)` on the hot path for a high-frequency limit: it is both slow and racy, and it gets slower as the tenant's data grows.

## section 3 Atomic Counter Patterns

### Pattern A - DB transactional counter (correctness-first)

```sql
-- one row per (tenant, limit, period); the counter is the truth
UPDATE tenant_usage_counters
   SET used = used + :amount, updated_at = NOW()
 WHERE tenant_id = :t AND limit_code = :l AND period_key = :p
   AND used + :amount <= :limit_value;          -- atomic check-and-consume
-- rows_affected = 0  ->  limit would be exceeded; reject
```

A single conditional UPDATE both checks and consumes; if zero rows change, the limit is hit. No read-then-write gap. For resources that are also real rows (seats), a unique constraint per `(tenant_id, slot)` is an additional belt-and-braces guard.

### Pattern B - Redis atomic counter (speed-first)

```python
def consume(tenant_id, limit_code, period_key, amount, limit_value):
    key = f"usage:{tenant_id}:{limit_code}:{period_key}"
    new_val = redis.incrby(key, amount)          # atomic
    redis.expire(key, ttl_for(period_key))       # auto-cleans after period
    if new_val > limit_value:
        redis.decrby(key, amount)                # roll back the over-consume
        return Denied()
    return Allowed(remaining=limit_value - new_val)
```

Redis is the hot-path source for high-frequency limits; the database is reconciled asynchronously (write-behind) for billing accuracy and durability. If Redis is unavailable, fail according to policy (section 7) - not silently open.

## section 4 Period Rollover

A monthly limit resets each month; the counter must roll over without a cron job racing the first request of the new period.

- Encode the period in the key: `period_key = '2026-05'` (monthly), `'2026-05-30'` (daily), `'lifetime'`.
- The first consume in a new period naturally creates a fresh key/row at zero - no reset job required.
- Set a TTL on Redis keys slightly longer than the period so late reconciliation can still read the prior period.
- Anchor the period to the tenant's billing cycle, not the calendar, if the plan is billed on a rolling date. A calendar-month reset on a tenant billed on the 14th gives them a free top-up mid-cycle - a metering-revenue leak.

The wrong choice - a nightly "reset all counters to zero" job - has a window where the job has not yet run but the new period has begun, and either over-counts (old period's usage blocks new period) or under-counts (reset early gives free usage).

## section 5 Hard Caps vs Soft Caps

| Cap type | Behaviour at limit | Use for | Failure mode of wrong choice |
|---|---|---|---|
| **Hard cap** | Action blocked outright | Seats, security-relevant limits, free-tier abuse prevention | A soft cap on free-tier seats lets a free tenant invite 10,000 users and abuse the platform |
| **Soft cap** | Action allowed; overage metered and billed or flagged | Usage-based paid limits (API calls, AI tokens) where blocking a paying customer mid-workflow is worse than billing overage | A hard cap on a paying customer's API at midnight on the last day of the month breaks their production integration and generates a support escalation instead of revenue |

Decide per limit, store it as `enforcement: 'hard' | 'soft'` on the limit definition, and make it overridable per tenant (an enterprise contract may convert a hard cap to soft with negotiated overage pricing - see `enterprise-override-model.md`).

## section 6 Grace

Grace softens the edge of a hard cap so a customer is not abruptly cut off.

- **Approaching-limit signals**: 70% passive indicator, 80% in-app banner, 95% stronger CTA + email, 100% block (matches the upgrade-discovery UX in the parent skill).
- **Grace overage**: allow a small percentage over the hard cap (for example 10%) for a grace period (for example 72 hours) while prompting upgrade, then enforce. Record `grace_started_at`; the block engages when grace expires or the grace overage is exhausted.
- Grace is a per-plan policy, not a code constant. Free tier may get zero grace; paid tiers get a softer landing.

## section 7 HTTP Semantics - Get 402 vs 429 Right

This is the most common confusion and getting it wrong sends the customer down the wrong path.

| Code | Meaning | Use when | Client should |
|---|---|---|---|
| **402 Payment Required** | You are out of *quota/entitlement*; the fix is commercial | Tenant exceeded a plan limit (API calls/month, seats, projects) | Show an upgrade prompt; retrying without upgrading will not help |
| **429 Too Many Requests** | You are going too *fast*; the fix is to slow down | Tenant exceeded a rate limit (requests/second burst) | Back off and retry after `Retry-After`; the request will succeed later |

Returning 429 for a monthly-quota exhaustion tells the client "retry later" - so it retries forever and never upgrades, and the limit never converts to revenue. Returning 402 for a per-second rate limit tells a well-behaved client "go upgrade" when all it needed was to slow down. Both responses carry structured context:

```json
{
  "error": {
    "code": "LIMIT_EXCEEDED",
    "limit": "api_calls_monthly",
    "used": 100000,
    "allowance": 100000,
    "period_resets_at": "2026-06-01T00:00:00Z",
    "enforcement": "hard",
    "upgrade_url": "https://app.example.com/billing/upgrade?target=scale&context=api_calls"
  }
}
```

429 responses additionally carry a `Retry-After` header; 402 responses do not (waiting does not help).

## section 8 Where to Enforce

- **API gate** is primary enforcement: the conditional consume in section 3 runs here.
- **Worker gate**: background jobs that consume quota (a queued bulk import burning API calls) must consume against the same counter. A job that bypasses the API gate by inserting straight onto the queue must not bypass metering - or it becomes the exploit path.
- **UI**: mirrors remaining quota for UX; never the enforcement boundary.
- **DB constraint**: belt-and-braces for hard, low-cardinality caps (unique seat slots).

## section 9 Metering and Reconciliation

For billing-relevant limits, the counter is also the billing meter. Keep it honest:

- Emit a `limit.consumed` event per consume for the analytics/PQL pipeline and for usage-based billing aggregation.
- Reconcile Redis hot counters to the durable store on a schedule; the durable store is what bills.
- On reconciliation drift beyond a threshold, alert - drift means either lost events (under-billing) or double counting (over-billing), both of which are revenue/trust problems.

## section 9a Failure Policy When the Counter Store Is Down

Redis (or the hot counter) will be unavailable at some point. Decide the policy per limit class in advance, because the default - whatever the code happens to do - is almost always wrong.

| Limit class | On counter outage | Rationale |
|---|---|---|
| Abuse-prevention hard cap (free-tier) | Fail closed (deny) | Failing open lets an outage become a free-for-all for abusers |
| Paying-customer usage-based (soft) | Fail open + record unmetered usage to reconcile later | Blocking a paying customer's production traffic during your outage is worse than briefly under-metering |
| Security-relevant limit | Fail closed | The limit exists for safety; an outage must not relax it |

Whatever the choice, emit an alert when the fallback path is taken and reconcile when the store recovers. Silently failing open on everything turns a cache blip into unlimited free usage; silently failing closed on everything turns a cache blip into a platform-wide outage for paying customers.

## section 9b Worked Example - Concurrent Consume

Two requests for the same tenant arrive at the same instant; the tenant has 1 API call left of its monthly allowance.

```text
allowance = 100000, used = 99999

Request A: redis.incrby(key, 1) -> 100000   (<= allowance) -> Allowed, remaining 0
Request B: redis.incrby(key, 1) -> 100001   (>  allowance) -> decrby(key,1) -> Denied (402)
```

Because `INCRBY` is atomic, exactly one request wins; there is no interleaving where both read 99999 and both pass. The denied request gets a 402 with `period_resets_at`, not a 429 - it is out of quota, not going too fast. Contrast the naive read-then-write (section 1), where both requests read 99999, both pass, and the tenant lands at 100001 - one call of unbilled overage per race, multiplied across every high-traffic tenant.

## section 10 Anti-Patterns

- **`SELECT COUNT(*)` per request** - slow and racy; gets worse as data grows.
- **Read-then-write limit check** - two concurrent requests both pass.
- **Nightly reset job for period rollover** - racy window at the boundary.
- **Calendar-month reset on a non-calendar billing cycle** - free mid-cycle top-up.
- **429 for quota exhaustion** - client retries forever, never upgrades.
- **402 for a rate limit** - client told to pay when it just needed to slow down.
- **Hard cap on a paying customer's usage-based limit with no grace** - production breakage instead of overage revenue.
- **Worker path bypasses metering** - direct queue insertion is an unmetered exploit.
- **Fail-open when the counter store is down** - unlimited free usage during an outage.

## See Also

- `saas-entitlements-and-plan-gating` section 5-section 6 - resolution strategies and gate placement.
- `references/enterprise-override-model.md` - per-tenant limit overrides and hard-to-soft conversion.
- `saas-rate-limiting-and-quotas` - token-bucket rate limiting (the 429 side).
- `subscription-billing` - usage-based billing aggregation of metered limits.
- `ai-usage-metering-and-billing` - token metering specifics for AI limits.
