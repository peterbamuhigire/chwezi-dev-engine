# Token Accounting Pipeline — Reference

How a request's tokens become a tenant's USD cost in the audit log, the realtime spend gauge, the daily aggregate, and the monthly invoice.

## Five stages

```
[1] Gateway captures        →  [2] Audit row + cost event
                                     │
                                     ├──> [3] Redis realtime counter (per tenant)
                                     ├──> [4] Daily aggregate job (Postgres / warehouse)
                                     └──> [5] Monthly billing rollup (Stripe meter)
```

## Stage 1: Gateway capture

At the close of every provider call, the gateway has:
- `tokens_in` (from provider response headers or the gateway's own tokenizer pre-call)
- `tokens_out` (from provider response or token counter on the streamed deltas)
- `model_used` (after fallback resolution)
- `request_id`, `tenant_id`, `feature`, `region`, `prompt_id`, `prompt_version`
- `usd_cost` (computed from the checked-in price table)

The gateway commits one transactional unit:

```python
async with pg.transaction() as tx:
    await tx.execute(INSERT_AI_REQUEST, ...)
    await redis.hincrby(f"ai:cost:{tenant_id}:{yyyymm}", "usd_micro", int(usd_cost * 1e6))
    await redis.hincrby(f"ai:cost:{tenant_id}:{yyyymm}", "tokens_in", tokens_in)
    await redis.hincrby(f"ai:cost:{tenant_id}:{yyyymm}", "tokens_out", tokens_out)
    await bus.publish("ai.cost.recorded", {
        "tenant_id": tenant_id, "request_id": request_id,
        "usd_cost": str(usd_cost), "tokens_in": tokens_in, "tokens_out": tokens_out,
        "feature": feature, "model_used": model_used, "ts": now,
    })
```

If any sub-step fails, the response is *not* returned. This is non-negotiable.

## Stage 2: Audit row

`ai_requests` is the canonical row. Schema in `ai-on-saas-architecture/references/control-plane-ai-services.md`. Indexed by `(tenant_id, created_at)` for cost queries.

The full prompt + response payload is written to S3 (`ai-audit/<tenant_id>/<yyyy>/<mm>/<dd>/<request_id>.json.zst`) with a per-tenant KMS key. The Postgres row holds the S3 key.

## Stage 3: Realtime tenant counter (Redis)

Hash per tenant per month:

```
ai:cost:8421:202605 = {
  usd_micro: 134821345,    # 134.821345 USD
  tokens_in: 18_204_991,
  tokens_out: 4_120_330,
  reqs: 38_204,
  fallbacks: 47
}
```

Read at the top of every gateway request (cap enforcement); read by the in-product usage panel; read by the budget-threshold sweeper.

## Stage 4: Daily aggregate

A scheduled job rolls Postgres `ai_requests` into a `tenant_ai_daily` materialised table:

```sql
CREATE TABLE tenant_ai_daily (
    tenant_id     BIGINT NOT NULL,
    day           DATE NOT NULL,
    feature       VARCHAR(64) NOT NULL,
    model_used    VARCHAR(64) NOT NULL,
    reqs          BIGINT NOT NULL,
    tokens_in     BIGINT NOT NULL,
    tokens_out    BIGINT NOT NULL,
    usd_cost      DECIMAL(12,6) NOT NULL,
    PRIMARY KEY (tenant_id, day, feature, model_used)
);
```

Daily job runs at 01:00 UTC for previous day; idempotent on (tenant, day, feature, model).

The daily rollup feeds:
- the cost-per-tenant dashboard,
- the cost anomaly detector (see `ai-cost-per-tenant-attribution`),
- the warehouse ELT.

## Stage 5: Monthly billing rollup

For metered plans, daily rolls feed `ai-usage-metering-and-billing`:

```sql
-- usage units for billing
SELECT tenant_id, billing_dimension, SUM(units) AS units
FROM tenant_ai_daily_billable
WHERE month = '2026-05'
GROUP BY tenant_id, billing_dimension;
```

Sent to Stripe via metered billing API at end of period.

## Reconciliation

Nightly: sum Postgres `ai_requests` rows for tenant × month versus Redis counter. Drift > 0.1% pages on-call. Drift > 1% blocks the daily rollup until investigated. Provider-invoice reconciliation runs monthly — drift > 2% triggers a price-table review.

## Backfill

When a new dimension is added (e.g., per-feature cost), backfill from `ai_requests` rows (Postgres has the canonical record). Never backfill from provider invoices — they have a 24–72h lag and aggregate poorly.

## Test patterns

- **Unit**: `cost_calc` with known tokens for every model in the price table; assert exact USD.
- **Integration**: run a synthetic gateway call; assert Postgres row + Redis increment + bus event all written.
- **Soak**: run 10k req/min for 5 minutes; assert zero loss between `ai_requests.count()` and Redis `reqs`.
- **Chaos**: kill Redis mid-pipeline; assert request fails (not returned) and Postgres row is rolled back.
