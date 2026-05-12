# Deferred Revenue + Refund Reserves for Agent Products

This reference specifies the **ledger schema, posting rules, and sizing formulas** for the two balance-sheet liabilities that are unique to agent revenue: deferred revenue (prepaid task credits) and the refund reserve (estimated refund liability).

Both are required by ASC 606 / IFRS 15 (see `asc-606-for-agents.md`). Both are auditor-scrutinized. Both fail silently if not engineered: deferred revenue grows unbounded if prepaid credits never expire; the refund reserve is mis-sized if the rolling rate is not recomputed.

---

## 1. Deferred Revenue — Prepaid Task Credits

### 1.1 When deferred revenue is created

A tenant purchases a **prepaid task-credit pack** (e.g., 1,000 resolutions for $9,000, TTL 12 months). At sale:

- Cash collected: $9,000
- Performance obligation satisfied: 0 (no resolutions yet consumed)
- Revenue recognized: $0
- Deferred revenue (liability) booked: $9,000

### 1.2 Ledger schema

```sql
CREATE TABLE deferred_revenue_balances (
  id               BIGSERIAL PRIMARY KEY,
  tenant_id        UUID NOT NULL,
  sku              TEXT NOT NULL,             -- e.g. 'resolution_pack_1000'
  currency         CHAR(3) NOT NULL,
  units_purchased  INTEGER NOT NULL,
  units_consumed   INTEGER NOT NULL DEFAULT 0,
  unit_price_minor BIGINT NOT NULL,           -- minor units
  total_minor      BIGINT NOT NULL,
  purchase_date    DATE NOT NULL,
  expires_at       TIMESTAMPTZ,
  breakage_pct     NUMERIC(5,4),              -- expected non-redemption fraction
  status           TEXT NOT NULL,             -- 'active' | 'expired' | 'depleted'
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE deferred_revenue_postings (
  id                  BIGSERIAL PRIMARY KEY,
  balance_id          BIGINT NOT NULL REFERENCES deferred_revenue_balances(id),
  posting_type        TEXT NOT NULL,         -- 'initial' | 'consumption' | 'breakage' | 'true_up' | 'refund'
  units               INTEGER NOT NULL,
  amount_minor        BIGINT NOT NULL,       -- positive = liability up, negative = liability down
  resolution_event_id UUID,                  -- when posting_type='consumption'
  period_yyyymm       INTEGER NOT NULL,      -- accounting period
  idempotency_key     TEXT UNIQUE NOT NULL,
  posted_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 1.3 Posting rules

**At purchase (event: `prepaid_credit_pack.purchased`):**

```
DR Cash / AR                       $9,000
CR Deferred Revenue (liability)    $9,000

posting_type='initial', amount_minor=+900000
```

**At each resolution that consumes credits (event: `agent.resolution.completed` with `pricing_source='prepaid_pack'`):**

For a $9.00 unit price:

```
DR Deferred Revenue (liability)    $9
CR Revenue — Agent Resolutions     $9

posting_type='consumption', amount_minor=-900,
resolution_event_id=<event_id>, period_yyyymm=current
```

**Idempotency:** `idempotency_key = f"defrev:consume:{resolution_event_id}"`. Retries collapse.

**At TTL with `breakage_pct` applied (event: `prepaid_credit_pack.expired`):**

Two acceptable models — pick one in the policy doc, never mix:

- **Conservative (recommended):** breakage recognized as revenue **only when statutorily allowed** (escheatment rules vary by US state and EU country). If allowed:
  - `DR Deferred Revenue / CR Revenue` for `units_remaining * unit_price`.
- **No-breakage:** balance becomes a long-term liability with periodic review.

**At refund (event: `prepaid_pack.refund.issued`):**

```
DR Deferred Revenue (liability)    $refund_amount
CR Cash / customer balance         $refund_amount
```

The refund flow does **not** touch revenue; it reverses the original liability only.

### 1.4 Reconciliation

A daily reconciliation job:

1. Sum `units_purchased - units_consumed` across active balances per tenant per SKU.
2. Multiply by `unit_price_minor` to get expected liability.
3. Compare to the GL deferred-revenue balance.
4. Tolerance: 0.5% per tenant per period. Out-of-tolerance triggers an ops alert.

### 1.5 Tenant-facing surface

The customer dashboard (see `ai-agent-customer-sla-dashboard`) shows:

- Credits purchased / consumed / remaining
- Expiry date
- Average burn rate (for capacity-planning prompts)

The customer never sees "deferred revenue" — that's an internal accounting view.

---

## 2. Refund Reserve

### 2.1 Why a reserve

ASC 606 requires that variable consideration (refunds, SLA credits) be **estimated and constrained** at recognition time. We cannot wait until the refund happens — by then the revenue has been booked and the books are wrong.

The refund reserve is a balance-sheet liability that absorbs estimated future refunds against revenue **already booked**.

### 2.2 Reserve sizing — rolling 90-day rate

The reserve sits in the GL as a single liability per tenant per currency:

```sql
CREATE TABLE refund_reserve_balances (
  id               BIGSERIAL PRIMARY KEY,
  tenant_id        UUID NOT NULL,
  currency         CHAR(3) NOT NULL,
  balance_minor    BIGINT NOT NULL DEFAULT 0,
  rate_window_days INTEGER NOT NULL DEFAULT 90,
  rolling_rate_pct NUMERIC(6,4) NOT NULL,
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE refund_reserve_postings (
  id              BIGSERIAL PRIMARY KEY,
  balance_id      BIGINT NOT NULL REFERENCES refund_reserve_balances(id),
  posting_type    TEXT NOT NULL,   -- 'accrual' | 'utilization' | 'true_up'
  amount_minor    BIGINT NOT NULL,
  reason_ref      TEXT,            -- billing_event_id, refund_id
  period_yyyymm   INTEGER NOT NULL,
  idempotency_key TEXT UNIQUE NOT NULL,
  posted_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 2.3 Rolling-rate computation

Re-compute daily:

```python
from decimal import Decimal
from datetime import date, timedelta

def compute_rolling_refund_rate(tenant_id: str, currency: str, window_days: int = 90) -> Decimal:
    today = date.today()
    start = today - timedelta(days=window_days)

    # Sum of refunded amounts in window (technical + out-of-scope only — see abandonment-and-refund-policy)
    refunds = sum_refunds_minor(tenant_id, currency, start, today)
    # Sum of agent-resolution revenue billed in window
    revenue = sum_agent_revenue_minor(tenant_id, currency, start, today)

    if revenue == 0:
        # New tenant: fall back to tier default (e.g. 2.5% for Pro, 1.0% for Enterprise)
        return Decimal(get_tier_default_refund_rate(tenant_id))

    rate = Decimal(refunds) / Decimal(revenue)

    # Constraint: floor to the 80th-percentile-conservative figure — see asc-606-for-agents.md.
    # Practical heuristic: take max(rolling_rate, prior_rate * 0.95, tier_floor).
    return max(rate, prior_rate(tenant_id) * Decimal("0.95"), tier_floor(tenant_id))
```

### 2.4 Posting rules

**At each agent revenue booking (event: `revenue.recognized`):**

```
expected_refund_minor = revenue_minor * rolling_rate_pct

DR Refund Expense (contra-revenue)   $expected_refund_minor
CR Refund Reserve (liability)        $expected_refund_minor

posting_type='accrual', idempotency_key=f"reserve:accrue:{revenue_event_id}"
```

**At actual refund (event: `refund.executed`):**

```
DR Refund Reserve (liability)        $actual_refund_minor
CR Cash / customer balance           $actual_refund_minor

posting_type='utilization', idempotency_key=f"reserve:use:{refund_id}"
```

**At month-end true-up:**

If `actual_refunds_in_period > accrued_in_period * 1.20` (over-utilization) or `< accrued_in_period * 0.50` (over-accrual): adjust.

```
DR / CR  Refund Reserve   <delta>
CR / DR  Refund Expense   <delta>

posting_type='true_up', idempotency_key=f"reserve:trueup:{tenant_id}:{period_yyyymm}"
```

### 2.5 Reserve health alerts

Continuous alerts:

| Alert | Threshold | Action |
|---|---|---|
| Over-utilization (period) | actual / accrued > 1.20 | Re-size rolling rate; review per-class refund mix |
| Under-utilization (period) | actual / accrued < 0.50 | Release reserve via true-up; document |
| Reserve depletion | balance < 30-day-forecast | Re-accrue immediately; check for systemic issue |
| Stale rate | rolling_rate not recomputed in 7 days | Page ops; data pipeline broken |

### 2.6 Per-class reserve buckets (optional but recommended)

The four abandonment classes (see `ai-agent-abandonment-and-refund-policy/references/abandonment-taxonomy.md`) have different refund rates. Track them separately:

- `technical_failure` → high refund rate, full refund expected.
- `out_of_scope` → moderate refund rate, full refund expected.
- `user_abort` → no refund. Excluded from reserve.
- `budget_exceeded` → no refund. Excluded from reserve.

Aggregating into one rate hides regressions in one class behind improvements in another.

---

## 3. SLA Credit Reserve (sub-case of refund reserve)

SLA credits are a separate variable-consideration line. They behave like the refund reserve but are sized from the breach forecast rather than refund history:

```python
def sla_credit_reserve_size(tier: str, base_revenue_minor: int) -> int:
    # Pro: 5% of base, Business: 10%, Enterprise: 15% — see sla-class-table.md
    pct = {"pro": Decimal("0.05"), "business": Decimal("0.10"), "enterprise": Decimal("0.15")}[tier]
    return int(Decimal(base_revenue_minor) * pct)
```

Postings mirror the refund-reserve flow (`accrual` / `utilization` / `true_up`) under separate ledger accounts so SLA-credit cost is visible to the P&L.

---

## 4. GL Account Setup (Reference Chart)

| Account | Type | Normal balance |
|---|---|---|
| `2150 Deferred Revenue — Prepaid Agent Credits` | Liability | Credit |
| `2160 Refund Reserve — Agent Resolutions` | Liability | Credit |
| `2170 SLA Credit Reserve — Agent` | Liability | Credit |
| `4100 Revenue — Agent Resolutions` | Revenue | Credit |
| `4110 Revenue — Agent Subscription Base` | Revenue | Credit |
| `4910 Refund Expense — Agent` (contra-revenue) | Contra-revenue | Debit |
| `4920 SLA Credits Issued — Agent` (contra-revenue) | Contra-revenue | Debit |

---

## 5. Common Pitfalls

- Booking prepaid pack to revenue at sale. Inflates the period; auditor finding.
- Single refund reserve aggregated across all classes; technical-failure spike hidden by user-abort drop.
- Rolling rate computed once and forgotten. Reserve drifts; first quarter of growth produces a restatement.
- Breakage recognized without statutory-allowance review. Tax/regulatory risk.
- Refund executed via Stripe Dashboard without GL posting. Liability stays on books forever.
- True-ups posted to *prior* period after close. Reopens audited books. Always post to current.
