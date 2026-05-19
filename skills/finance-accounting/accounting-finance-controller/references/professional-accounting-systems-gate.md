# Professional Accounting Systems Gate

Use this reference as the review checklist for software, plans, proposals, dashboards, or spreadsheets involving money.

## 1. Finance System Requirements

| Area | Required capability |
|---|---|
| Entity setup | Legal entity, branch, department, project, cost center, profit center, currency, fiscal year, tax profile |
| Chart of accounts | Account type, normal balance, parent account, posting restrictions, control-account flags, inactive-account protection |
| Source documents | Invoice, receipt, bill, PO, GRN, delivery note, stock count, timesheet, payroll run, bank/mobile money statement |
| Posting engine | Event-based posting rules, balanced journal generation, atomic posting, reversal entries, audit trail |
| Subledgers | AR, AP, inventory, fixed assets, payroll, tax, loans, projects, grants, deferred revenue where relevant |
| Period close | Accruals, prepayments, depreciation, provisions, reconciliations, review signoff, period lock |
| Reporting | GL, trial balance, P&L, balance sheet, cash flow, aging, inventory valuation, tax schedules, management accounts |

## 2. IFRS-Aware Reporting Checks

- State the accounting basis: cash, modified cash, accrual, IFRS, IFRS for SMEs, local GAAP, tax basis, or management-only basis.
- Identify recognition rules for revenue, inventory, PPE, leases, provisions, impairment, financial instruments, foreign currency, grants, and taxes.
- For fair-value or impairment-sensitive balances, keep valuation date, method, assumptions, reviewer, and evidence references. Do not let users overwrite carrying values without an adjustment workflow.
- For interest-bearing instruments, separate principal, interest, fees, maturity, repayment schedule, effective rate where required, and current/non-current classification.
- Keep accounting policies explicit and stable. Changes in policy, estimate, or prior-period error need separate treatment and disclosure.
- Separate accounting profit from cash flow. Cash statements must classify operating, investing, and financing cash flows consistently.
- If group reporting exists, define control, consolidation scope, intercompany balances, unrealized profit eliminations, goodwill/NCI, and currency translation.

## 3. Cost And Management Accounting

- Define cost objects: product, service, customer, project, branch, department, order, route, grant, or contract.
- Classify costs as direct/indirect, fixed/variable, controllable/non-controllable, committed/discretionary, and one-time/recurring.
- Choose costing method by operations: job costing for custom work, process costing for continuous flow, hybrid costing for mixed operations, ABC when overhead is material and diverse.
- Use CVP where pricing, scale, or break-even matters: contribution margin, margin of safety, target profit, sales mix, capacity constraint.
- Use standard costing and variance analysis where repeatable production exists: price/rate, quantity/efficiency, mix/yield, volume/capacity, spending, and overhead variances.
- Use responsibility centers: cost center, revenue center, profit center, investment center. Match KPIs and authority to what managers actually control.
- For internal transfers, define transfer pricing policy, source price, approval, tax/statutory constraints, and impact on both sending and receiving responsibility centers.
- For dashboards, pair financial KPIs with operational drivers: volume, yield, scrap, service time, quality, delivery reliability, retention, utilization, and customer profitability.

## 4. Controls And Assurance

- Segregate creation, approval, custody, posting, reconciliation, and review duties.
- Protect high-risk actions: supplier bank changes, refunds, credit notes, write-offs, stock adjustments, payroll edits, manual journals, period reopenings.
- Use maker-checker approval thresholds, immutable audit logs, attachment evidence, and exception queues.
- Reconcile bank/mobile money daily or weekly for high-volume systems; reconcile AR, AP, inventory, payroll, tax, loans, and fixed assets monthly.
- Preserve documents and logs long enough for tax, audit, donor, investor, or litigation needs.

## 5. Financial Model Review

- Every line item must trace to an operating driver, contract, price, headcount plan, volume assumption, tax rule, or benchmark.
- Keep input cells, calculation cells, and output cells separate. Avoid hard-coded outputs and hidden balancing figures.
- Include checks: balance sheet balances, cash roll-forward works, debt schedule ties to cash flow, depreciation ties to capex, tax ties to profit and timing.
- Run base, downside, upside, and severe downside cases. Change the operating drivers, not only the final totals.
- Test debt service with DSCR, liquidity with runway/current ratio, profitability with contribution margin and break-even, and valuation with sensitivity ranges.

## 6. Red Flags

- Manual journals used to force reports to match.
- Inventory value not tied to stock movement and costing method.
- Revenue recognized before the business has delivered or earned it.
- Positive profit but negative operating cash flow with no working-capital explanation.
- VAT/PAYE/WHT/NSSF or local statutory costs missing from projections.
- A funding request that does not equal the use-of-funds schedule.
- Controls described in prose but absent from roles, workflows, and data model.
