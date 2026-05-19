# Month-End Close Pipeline â€” Agent Revenue

This reference specifies the **deterministic, idempotent, auditable** month-end close pipeline for agent revenue. It runs as a sequence of Airflow / Dagster / Prefect tasks (engine-agnostic; the contracts matter, not the orchestrator).

Target: agent-revenue close completes within **3 business days** of period end. Same-day if no exceptions.

---

## 1. Pre-Close Checklist (Day âˆ’3 to Day 0)

Run nightly during the last 3 days of the period. Failures must be resolved before close starts.

| Check | Query | Pass criterion |
|---|---|---|
| Verdict lag | `count(*) where verdict_status='pending' and resolution_at < now() - interval '24h'` | < 0.5% of period resolutions |
| Pricing-rule version drift | `select distinct pricing_rule_version from billing_events where period=P` | Exactly one version per `(tenant, feature)` pair |
| Deferred-revenue reconciliation | per Â§1.4 of `deferred-revenue-and-refund-reserves.md` | Within 0.5% per tenant |
| Reserve rate freshness | `max(updated_at)` on `refund_reserve_balances` | < 24h old |
| Stripe webhook backlog | unprocessed `invoice.*` events | 0 |
| FX rate fixed | `fx_rates_period(period=P)` | All currencies populated |

If any check fails, the close pipeline refuses to start. No "we'll fix it during close."

---

## 2. Close Pipeline â€” Stage by Stage

The pipeline runs as 8 stages, each idempotent on `(period_yyyymm, stage_name, run_id)`.

### Stage 1 â€” Freeze the period

```python
def freeze_period(period_yyyymm: int, run_id: str) -> None:
    with txn() as t:
        existing = t.query("select * from close_runs where period=%s and stage='freeze'", period_yyyymm)
        if existing and existing.status == 'succeeded':
            return  # idempotent

        t.execute("""
          insert into period_locks (period_yyyymm, locked_at, locked_by, status)
          values (%s, now(), %s, 'frozen')
          on conflict (period_yyyymm) do nothing
        """, period_yyyymm, run_id)

        t.execute("""
          insert into close_runs (period_yyyymm, stage, run_id, status, started_at)
          values (%s, 'freeze', %s, 'succeeded', now())
        """, period_yyyymm, run_id)
```

Effect: new billing-event rows for `period_yyyymm` are rejected by the application layer. Late events go to `late_event_quarantine` for triage.

### Stage 2 â€” Drain pending verdicts (3-business-day allowance)

Any resolution event whose verdict is still pending at freeze gets up to **3 business days** to post a verdict that books against the closing period. Verdicts arriving after the allowance book to the current open period (see Â§4).

```python
def drain_pending_verdicts(period: int, run_id: str) -> None:
    deadline = third_business_day_after(period_end(period))
    pending = query("""
      select event_id from billing_events
      where period=%s and verdict_status='pending'
    """, period)

    for ev in pending:
        if now() > deadline:
            move_to_current_period(ev.event_id)
            audit_log("verdict_late", event=ev.event_id, original_period=period)
        # else: wait
```

### Stage 3 â€” Booking journal: per-resolution revenue

For every `billing_event` in the period with `verdict='resolved'`:

```
DR  AR / Stripe Pending (customer balance)   <amount>
CR  4100 Revenue â€” Agent Resolutions          <amount>
```

For `verdict='attempted_only'` (see `ai-agent-attempted-vs-completed-billing`):

```
DR  AR / Stripe Pending                      <attempt_price>
CR  4100 Revenue â€” Agent Resolutions          <attempt_price>
```

Implementation:

```python
def post_resolution_revenue(period: int, run_id: str) -> None:
    events = query("""
      select event_id, tenant_id, currency, amount_minor, verdict
      from billing_events
      where period=%s and verdict in ('resolved','attempted_only')
        and revenue_posted=false
      order by event_id
    """, period)

    for batch in chunks(events, 500):
        with txn() as t:
            for ev in batch:
                idem_key = f"rev:resolution:{ev.event_id}"
                if t.exists("ledger_entries", idempotency_key=idem_key):
                    continue
                t.insert("ledger_entries",
                    idempotency_key=idem_key,
                    period=period,
                    dr_account="1200 AR",
                    cr_account="4100 Revenue â€” Agent Resolutions",
                    amount_minor=ev.amount_minor,
                    currency=ev.currency,
                    source_event=ev.event_id,
                    tenant_id=ev.tenant_id,
                )
                t.update("billing_events", set={"revenue_posted": True}, where={"event_id": ev.event_id})
```

### Stage 4 â€” Deferred revenue consumption journal

For prepaid-pack-funded resolutions (`pricing_source='prepaid_pack'`):

```
DR  2150 Deferred Revenue â€” Prepaid Agent Credits   <amount>
CR  4100 Revenue â€” Agent Resolutions                 <amount>
```

Postings derive from `deferred_revenue_postings` where `posting_type='consumption'` and `period_yyyymm=P`.

### Stage 5 â€” Refund-reserve accrual + utilization

Two sub-stages:

**5a Accrual** â€” for every resolution-revenue line booked in stage 3, accrue the expected refund:

```
DR  4910 Refund Expense â€” Agent (contra-revenue)    <rolling_rate * revenue>
CR  2160 Refund Reserve â€” Agent Resolutions          <rolling_rate * revenue>
```

**5b Utilization** â€” for every refund executed in the period:

```
DR  2160 Refund Reserve                              <refund_amount>
CR  AR / Customer balance                            <refund_amount>
```

Then run the **true-up** logic from `deferred-revenue-and-refund-reserves.md` Â§2.4.

### Stage 6 â€” SLA-credit journal

Mirrors stage 5 but for SLA credits:

```
DR  4920 SLA Credits Issued â€” Agent (contra-revenue) <credit_amount>
CR  2170 SLA Credit Reserve â€” Agent                  <credit_amount>
```

For each credit-note issued via the pipeline in `ai-agent-sla-credit-automation`, post the utilization side.

### Stage 7 â€” FX revaluation (multi-currency tenants)

For each non-base-currency revenue posting in the period:

- Use the **period-end** rate fixed in pre-close.
- Post FX gain/loss to `7100 FX Adjustment â€” Agent`.
- Document the corridor policy (no retroactive re-translation of prior periods).

### Stage 8 â€” Reconciliation + sign-off

Three reconciliations, each producing a delta report:

1. **Stripe â†” GL**: sum of Stripe invoice line items (agent-related SKUs) for the period vs sum of `ledger_entries` revenue lines.
2. **Billing-events ledger â†” GL revenue**: every `billing_events.amount_minor` with `verdict in ('resolved','attempted_only')` must equal the booked revenue.
3. **Deferred-revenue ledger â†” GL liability**: per `deferred-revenue-and-refund-reserves.md` Â§1.4.

Tolerance: 0.1% per reconciliation. Out-of-tolerance fails the close â€” no override without controller approval + audit-log row.

Sign-off artifact: a markdown report committed to `finance/close-runs/{period_yyyymm}.md` with:

- Total agent revenue per feature
- Refund expense + reserve movement
- SLA credits issued + reserve movement
- Deferred revenue movement
- FX impact
- Exceptions and how they were resolved
- Sign-offs: revenue-ops lead, controller, (annual) auditor

---

## 3. Late Verdicts â€” Post-Close Handling

A verdict arriving after the 3-business-day allowance:

- Books to the **current open period**, never to the closed one.
- The original `billing_event` row gets `verdict_late=true` and a pointer to the current-period correction.
- Customer invoice for the closed period is **not re-issued**; a current-period adjustment line item appears instead.
- Audit-log row records the original event, the late verdict, and the correction posting.

If the late-verdict volume per period exceeds 0.5% of total resolutions, escalate to product: the success-tracking cascade is too slow.

---

## 4. Disputes That Cross Close Boundaries

A dispute filed after close (see `ai-agent-task-success-tracking/references/dispute-resolution.md`) that **overturns** a verdict:

```
Period P: revenue $X recognized for event E (verdict='resolved')
Period P+2: dispute upheld â€” verdict flips to 'failed', refund issued

Period P+2 journal:
  DR  4100 Revenue â€” Agent Resolutions    $X      (de-recognition)
  CR  2160 Refund Reserve                 $X      (or DR Refund Reserve / CR Cash if reserve insufficient)
```

The historical period stays untouched. Always post to current. This is the IFRS 15 / ASC 606 prospective adjustment pattern.

---

## 5. Audit Trail Requirements

For every ledger entry produced by the pipeline:

- `idempotency_key` (collision = same entry, not duplicate).
- `source_event` (resolution event, refund id, credit-note id).
- `period_yyyymm`.
- `run_id` (links back to the orchestrator run for replay).
- `pricing_rule_version` (so future audits can reconstruct the price).
- `verdict_ref` (the success-tracking verdict that drove the booking).

Retention: 7 years (SOX-eligible tenants); 10 years (MiFID II); 5 years default. Confirm with `ai-agent-observability-and-replay`.

---

## 6. Orchestration Skeleton (Dagster-style; engine-agnostic)

```python
@graph
def agent_revenue_close(period_yyyymm: int):
    locked = freeze_period(period_yyyymm)
    drained = drain_pending_verdicts(locked)
    revenue = post_resolution_revenue(drained)
    defrev = post_deferred_consumption(revenue)
    reserves = post_refund_reserve_movements(defrev)
    sla = post_sla_credit_movements(reserves)
    fx = revalue_fx(sla)
    recon = reconcile_and_signoff(fx)
    return recon

@op(required_resource_keys={"db", "audit_log"})
def freeze_period(context, period_yyyymm: int) -> int:
    ...
```

Each `@op` is idempotent on `(period_yyyymm, op_name, run_id)` and emits a structured close-event to the audit log.

---

## 7. Common Pitfalls

- Closing a period with pending verdicts. Revenue gets booked to wrong period; restatement risk.
- True-ups posted to historical periods after sign-off. Reopens audited books.
- Multiple `pricing_rule_version` values in one period for one tenant/feature pair. Customer math doesn't reconcile.
- FX rate captured at start of period instead of period-end. Auditor finding.
- Reconciliation tolerance treated as "round-off" â€” material drift hidden.
- Stripe-side adjustments (manual credit notes) not mirrored to GL. Liability ghost.
- Sign-off done verbally / via Slack. No artifact = no audit defense.
- Close pipeline as a single 4-hour script. Debugging a failure means re-running everything; should be 8 idempotent ops.
