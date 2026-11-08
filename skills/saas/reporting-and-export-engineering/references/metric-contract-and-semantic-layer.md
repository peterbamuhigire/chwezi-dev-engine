Parent skill: [reporting-and-export-engineering](../SKILL.md)

# Metric contract, semantic layer and reconciliation tests

Load this before a figure reaches a dashboard, report, export, schedule or narrative. It covers
the versioned metric catalogue, the one controlled measure layer, fact and dimension grain,
fan-out tests and the reconciliation harness. Rules: [rules-and-gates.md](rules-and-gates.md).
Self-contained; prepared from Chwezi's own standard and engineering practice.

## 1. Metric contract (RPT-METRIC-001, RPT-METRIC-006, RPT-GATE-02)

One file per measure, versioned with semantic versions, approved by the named business owner,
stored in the product repository (for example `metrics/sales/net_sales.yaml`). A headline,
exported or scheduled figure without an approved contract trips RPT-GATE-02.

```yaml
metric:
  id: sales.net_sales                  # stable, never reused, dotted domain.name
  version: 2.0.0                       # major: definition change; minor: new test; patch: wording
  status: approved                     # draft | approved | withdrawn
  question: "What did we sell, after discounts and returns, before tax?"
  definition: "Issued invoice lines after line and bill discounts, less returns, excluding tax."
  numerator: "sum(net_line_amount) - sum(return_net_amount)"
  denominator: null                    # every ratio names both parts
  includes: [issued, paid, part_paid, credit]
  excludes: [draft, voided, provisional_offline]   # offline rows count once the server issues them
  unit: money                          # money | count | measured_quantity | ratio | percent
  quantity_unit: null                  # for quantities: the one unit; never mixed (RPT-METRIC-003)
  currency: tenant_functional          # never summed across currencies
  rounding: "store exact; round once at display to the ISO 4217 minor unit"
  date_basis: issue_date               # issue_date | payment_date | posting_date - say which
  timezone: tenant                     # resolved per tenant, e.g. Africa/Kampala
  grain: [tenant_id, branch_id, business_date]
  source: [invoices, invoice_lines, returns]
  basis: accrual                       # accrual | cash
  owner: "Finance lead (role, not a person's name in the file)"
  freshness_target: "15 minutes for dashboards (Chwezi value)"
  privacy_class: internal              # public | internal | confidential | restricted
  direction: higher_is_favourable      # drives variance status (RPT-PERIOD-003)
  comparison: "same weekday-aligned range of the prior period; MTD labelled as such"
  tests: [reconcile_detail, reconcile_ledger, fanout_tags, void_excluded,
          return_after_close, zero_day, negative_day, missing_branch, restricted_branch]
  ledger_link: "4000 Sales less 4050 Sales returns, same branch and business date"
```

Contract review checklist:

- Revenue, cash collected and profit are separate contracts with separate labels; gross versus
  net, discounts, tax, refunds, returns, voids, cost of goods and the accrual or cash basis are
  written in each contract that uses them (RPT-METRIC-006).
- The date basis is explicit: issue date, payment date and posting date give three different
  totals for the same day.
- Exclusions name drafts, voids and offline provisional rows.
- A ratio names numerator and denominator and the grain at which it is computed (average of
  ratios and ratio of sums differ).
- A change to the definition bumps the major version; reports record the version they used
  (generation record, [generation-records-and-export-jobs.md](generation-records-and-export-jobs.md)).

## 2. One controlled measure layer (RPT-METRIC-002, RPT-VIEW-007)

| Decision | Do | Failure avoided |
|---|---|---|
| Where a measure is computed | Once, on the server, in the semantic layer (SQL views or a metrics module that reads the contract) | Two screens showing two "net sales" figures |
| What presentation code may do | Format, sort, lay out; never add, net, convert or filter a measure | Screen, PDF and XLSX drifting apart |
| How clients get figures | An API that names `metric_id`, `version`, scope and period and returns values with their unit and currency | Clients re-deriving totals from row lists |
| Where domain arithmetic for variance lives | Server returns actual, baseline, variance and status; the badge renders them | Sign-only red and green colouring |
| How a new report adds a measure | Add or reuse a contract first, then query it | Undefined metrics in exports (RPT-GATE-02) |

Enforce with a guardrail: a CI search that fails on aggregation keywords (`sum(`, `reduce(`,
`SUM(` in client query builders) inside presentation packages, ratcheted to zero. Record its
output as LINT evidence.

## 3. Facts, dimensions and grain (RPT-METRIC-004, RPT-METRIC-005)

- Keep transactional facts (invoice lines, stock movements, payments, postings) apart from
  dimensions (product, category, branch, staff, customer). Declare each fact table's grain in
  one sentence: "one row per invoice line".
- Join a fact only to dimensions that are one-to-one at its grain. A many-valued attribute
  (product tags, multiple categories, split commissions) is either bridged with an allocation
  weight that sums to 1 or reported in its own view.
- Use the dimension and rate valid on the transaction date where a report spans changes in
  price, category, branch or exchange rate (slowly changing dimensions, historical rates).
- Tenant and branch are part of every grain; queries filter on them from the server-side
  context, never from a client parameter alone.

Fan-out and double-count test (run for every join added to a reporting view):

```sql
-- The total at fact grain must equal the total after the join.
SELECT
  (SELECT SUM(l.net_line_amount) FROM invoice_lines l
     WHERE l.tenant_id = :t AND l.business_date = :d) AS fact_total,
  (SELECT SUM(l.net_line_amount) FROM invoice_lines l
     JOIN products p ON p.id = l.product_id AND p.tenant_id = l.tenant_id
     LEFT JOIN product_tags pt ON pt.product_id = p.id          -- many-valued: should fan out
     WHERE l.tenant_id = :t AND l.business_date = :d) AS joined_total;
-- Expect fact_total = joined_total. A difference proves fan-out; remove or bridge the join.
```

Fixture: one product with three tags, one line of 10,000; the test fails if the joined total
reads 30,000.

## 4. Never sum unlike things (RPT-METRIC-003; owner rule, 7 Nov 2026)

- Quantities in different units are never added. "3 kg + 12 pcs + 2 L" is not a figure. Group
  by unit and show one total per unit, or convert to value at a stated cost or price and say
  which.
- The API returns quantity totals keyed by unit (`{"kg": "3.000", "pcs": "12"}`), never one
  bare number for a mixed set.
- Different currencies are never added; a converted total names the rate, its source and time.
- Test: a fixture with three units and two currencies yields no single cross-unit or
  cross-currency total anywhere (screen, PDF, XLSX).

## 5. Reconciliation harness (RPT-RECON-001/002/003, RPT-EXPORT-006, RPT-GATE-01)

Build one automated job per fixed report and per dashboard headline:

1. Headline equals the sum of its detail list for the same scope and period.
2. Detail list equals the ledger postings for the same scope where a ledger exists (sales to
   the sales and returns accounts; stock value to the inventory account; cash to the cash and
   bank accounts).
3. Screen payload, rendered PDF text and XLSX values are equal for the same scope; all three are
   produced from one canonical dataset with a dataset hash recorded in the generation record.
4. Run five fixture classes every time: positive, zero, negative (refund or credit note),
   reversed (void after close, back-dated posting) and missing data (a branch that has not
   synced).

Output a RECON report: scope, period, metric version, each comparison, difference, status.
An unexplained difference is never absorbed or rounded away. The API returns it so the surface
shows a reconciliation warning that cannot be dismissed (RPT-RECON-002, RPT-STATE-003):

```json
{"metric_id": "sales.net_sales", "version": "2.0.0",
 "reconciliation": {"status": "mismatch", "difference": "45000", "currency": "UGX",
   "cause": "2 invoices from Ntinda branch awaiting sync", "last_good_snapshot": "2026-11-03T14:02:00+03:00"}}
```

Amounts travel as decimal strings; the client formats them to the currency's ISO 4217 minor
unit (UGX and RWF 0 decimals, KES, TZS and USD 2).

## 6. Periods and variance (RPT-PERIOD-001..004)

- Compute comparison windows on the server from the contract's `comparison` rule: same
  duration, same cut-off time for an in-progress day, weekday-aligned where trade depends on the
  weekday, the tenant's fiscal calendar and timezone.
- Return `period.complete: false` for an in-progress period; every surface marks it.
- Variance = actual minus baseline. Status comes from `direction`: revenue over budget is
  favourable, expense over budget is adverse. Never colour by sign alone.
- A change from zero returns `change_kind: "new"`, rendered "New this period", never
  "+infinity %". Percentage and percentage-point changes use different fields.

## Worked example (fictional data)

A fictional two-branch hardware shop in Kampala (Kikuubo and Ntinda) closes its business day on
4 Nov 2026. The owner sees "Net sales UGX 3,450,000" on the home tile but "UGX 3,330,000" on the
printed daily close.

Investigation against the contracts:

| Step | Finding |
|---|---|
| Read both queries | The tile summed payments received today (payment date); the close used invoice issue date |
| Find the difference | One credit invoice of UGX 120,000 was issued on 3 Nov and paid on 4 Nov |
| Fix | Both surfaces read `sales.net_sales` 2.0.0 (issue date). The tile gains a second, separately labelled measure `cash.collections` 1.1.0 (payment date): "Received today UGX 3,450,000" |
| Prove | Reconciliation job: tile = close detail = ledger 4000 less 4050 for both branches; PDF and XLSX totals equal the screen. The close lists invoice numbers exactly as issued (for example `INV-00012841`), never renumbered |

The quantity column on the close shows "Cement 50 kg bags: 40 bags; Nails: 25 kg; Paint: 12 L"
and no grand quantity total.
