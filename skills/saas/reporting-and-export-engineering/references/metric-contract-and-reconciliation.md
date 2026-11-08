Parent skill: [reporting-and-export-engineering](../SKILL.md)

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

# Metric contract and reconciliation

Use this reference before a figure appears on any dashboard, report or export. A figure without a
contract cannot be checked, so it cannot ship (RPT-GATE-02). Rule IDs are in
[rules-and-gates.md](rules-and-gates.md).

## Task 1: write the metric contract

One contract per measure, versioned, approved by its business owner, stored where engineers and
reviewers can read it (the product repository or the metric catalogue). Template:

```yaml
metric:
  id: sales.net_sales            # stable; never reused
  version: 1.2.0
  question: "How much did we sell, after discounts and returns?"
  definition: "Invoice line amounts after line and bill discounts, less returns, excluding tax."
  numerator: "sum(line_amount - discount_amount) - sum(return_amount)"
  denominator: null              # ratios name both parts
  includes: [paid, credit, partly_paid]
  excludes: [voided, draft, provisional_offline_until_synced]
  unit: money
  currency: tenant_currency      # never summed across currencies
  rounding: "ISO 4217 minor unit of the currency; round once, at display"
  date_basis: invoice_date       # not payment date; say which
  timezone: tenant               # e.g. EAT
  grain: [tenant, branch, day]
  source: invoices, invoice_lines, returns
  owner: "Finance lead (role)"
  freshness_target: "15 minutes for dashboards (Chwezi value)"
  privacy_class: internal
  comparison: "same weekday range of the prior week; MTD is labelled"
  tests: [reconcile_to_ledger, fanout_join, void_excluded, return_after_close, zero_day, restricted_branch]
```

Checks: the numerator and denominator are both named for every ratio; the date basis is stated
(invoice date, payment date and posting date give different totals); exclusions name voids,
drafts and offline provisional records; currency is never mixed (RPT-METRIC-001, RPT-METRIC-006).

## Task 2: keep measures in one place

| Choice | Do | Failure if wrong |
|---|---|---|
| Where a measure is computed | Once, in the semantic or metrics layer on the server | Two screens show two "net sales" figures; the owner stops trusting both |
| Where it is formatted | In presentation, from the same value | Rounding differs between screen and PDF |
| How dimensions join | Declared keys and grain; tested against one-to-many dimensions | Fan-out: a sale counted once per category tag |
| Historical rates and categories | Use the rate or dimension valid on the transaction date | Last year's report changes when a price or rate changes |

(RPT-METRIC-002, RPT-METRIC-004, RPT-METRIC-005)

## Task 3: never sum unlike things

- Quantities in different units are never added: "3 kg + 12 pcs + 2 L" is not a figure. Show a
  total per unit, or convert to value at a stated cost or price (RPT-METRIC-003; owner rule,
  7 November 2026).
- Different currencies are never added; a converted total shows the rate, its source and time.
- Revenue, cash collected and profit are different measures and never share a label
  (RPT-METRIC-006). "Sales 4.8M" and "Received 3.1M" are both true on the same day.

## Task 4: reconcile

Reconciliation runs from the headline down and from the ledger across (RPT-RECON-001/003):

1. Headline figure equals the sum of its detail list for the same scope and period.
2. Detail list equals the ledger postings for the same scope, where a ledger exists (sales to the
   sales and receivables accounts; stock value to the inventory account).
3. Screen, PDF and spreadsheet totals are equal for the same scope (one canonical dataset; only
   formatting differs).
4. Run the five fixture cases every time: positive, zero, negative (refund or credit note),
   reversed (void after close, back-dated posting) and missing data (an outlet that did not sync).

A difference that cannot be explained is shown, not absorbed (RPT-RECON-002):

> Sales do not match the ledger by UGX 45,000 for 3 Nov 2026. Two invoices from Kireka branch are
> waiting to sync. Last good snapshot 14:02. [Retry]

The warning cannot be dismissed until the difference is resolved (RPT-STATE-003, RPT-GATE-08).

## Task 5: variance

| Metric type | Variance (actual minus baseline) | Status |
|---|---|---|
| Revenue, collections, margin | +2,000,000 | Favourable |
| Expense, cost, wastage, refunds | +2,000,000 | Adverse |
| Stock on hand vs target | Depends on the contract: above target may be overstock (adverse) | Rule stated in the contract |

The sign is arithmetic; favourable or adverse comes from the metric's direction rule. Show the
status as a word plus icon, never red alone (RPT-PERIOD-003, RPT-VIEW-003).

## Task 6: comparable periods

| Situation | Correct | Wrong |
|---|---|---|
| Today until 14:00 vs yesterday | "Today to 14:00 vs yesterday to 14:00" | Today so far vs all of yesterday |
| November to date (8 days) vs October | "1-8 Nov vs 1-8 Oct" | 1-8 Nov vs all of October |
| This week vs last week, trade depends on weekday | Same weekdays | Mon-Fri vs Mon-Sun |
| Fiscal year differs from calendar | State the fiscal calendar | Silent calendar year |
| Branches in different timezones | One stated timezone, or per-branch local with a note | Mixed, unlabelled |

Incomplete periods carry an "In progress" mark everywhere they appear (RPT-PERIOD-001/002).
Percentage and percentage-point changes are never mixed; a change from zero reads "New this
period" (RPT-PERIOD-004).

## Task 7: freshness and confidence

Show the snapshot time, the source lag, any integration that has not reported, and whether a
value is estimated or actual. Do not show a bare "data confidence 92%"; say what is missing and
let the user drill to the failed check or the missing feed (RPT-STATE-004).

## Worked example (fictional data)

A fictional Kampala hardware shop with two branches asks "Why is net sales on the home screen
UGX 120,000 higher than the daily sales report?" Investigation against the contract above: the
home tile summed invoices by payment date while the report used invoice date, and one credit sale
of 120,000 was invoiced yesterday and paid today. Fix: both read `sales.net_sales` v1.2.0 from the
metrics layer (date basis invoice date); the home tile gains a second measure "Received today"
(`cash.collections`, date basis payment date) so both truths are visible and labelled.

## Evidence/currentness

No external standard is cited in this reference. The freshness target in the template is a
Chwezi value.
