---
name: accounting-finance-controller
description: Use for accounting, bookkeeping, ERP finance, POS, inventory, payroll, billing, financial reporting, IFRS-aware workflows, management accounting, cost accounting, budgeting, valuation, controls, reconciliations, and finance-system design. Produces controller-grade requirements, implementation guidance, review findings, and financial logic so business software can replace QuickBooks/Tally-class workflows where appropriate.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Accounting Finance Controller

## Use When

- Designing or implementing financial modules for POS, ERP, SaaS, school fees, healthcare billing, inventory, payroll, project accounting, fixed assets, procurement, or mobile-money-heavy systems.
- Reviewing business plans, proposals, dashboards, spreadsheets, or systems where accounting accuracy, financial controls, investor confidence, or management reporting matter.
- The user wants outputs that feel credible to CFOs, accountants, auditors, lenders, investors, or senior executives.

## Core Rule

Every money movement must have a business event, source document, accounting treatment, posting rule, control, reconciliation path, and report destination. If any link is missing, the system is not finance-ready.

## Workflow

1. Identify the entity type, industry, reporting basis, currency, tax context, transaction volumes, user roles, and whether IFRS/statutory reporting is required.
2. Map business events to ledgers: sales, receipts, purchases, payments, inventory, payroll, tax, fixed assets, loans, owner equity, journals, adjustments, accruals, prepayments, and reversals.
3. Define the chart of accounts, accounting dimensions, control accounts, subledgers, fiscal periods, document numbers, posting rules, and period-close workflow.
4. Build management accounting: cost objects, cost drivers, cost centers, profit centers, contribution margin, CVP, budgets, flexible budgets, variance analysis, and responsibility-center reporting.
5. Add controls: segregation of duties, maker-checker approvals, immutable audit logs, period locks, role permissions, exception queues, reconciliation evidence, and reversal-only correction.
6. Design reports: trial balance, general ledger, P&L, balance sheet, cash flow, aging, inventory valuation, tax schedules, management accounts, dashboards, and board packs.
7. Validate with accounting gates: balanced journals, subledger-to-GL reconciliation, tax timing, inventory costing, cash/bank proof, period close, and model checks.

## Accounting Coverage

- Financial accounting: double-entry, accruals, revenue, expenses, assets, liabilities, equity, financial statements, disclosures, consolidation where relevant.
- Cost accounting: direct/indirect costs, fixed/variable costs, cost drivers, job/process/hybrid costing, ABC, standard costing, CVP, margin of safety, transfer pricing.
- Management control: budgets, responsibility centers, KPIs, performance measurement, incentives, project controls, decentralization, and management reporting cadence.
- IFRS-aware design: accounting policies, estimates, errors, events after reporting date, inventories, PPE, leases, impairment, provisions, financial instruments, cash flow, fair value, and disclosure readiness.
- Advanced accounting: business combinations, goodwill, non-controlling interests, intercompany eliminations, equity method, foreign currency, and group reporting where relevant.
- Quantitative finance: NPV, IRR, payback, effective interest rates, discounting, sensitivity analysis, scenario modelling, risk-return logic, and data-driven forecast checks.

## Quality Gates

- No posted transaction can be edited or deleted; corrections use reversals and adjustment entries.
- Debits equal credits at transaction, batch, period, tenant, and consolidated levels.
- Subledgers reconcile to GL control accounts: AR, AP, inventory, fixed assets, payroll, tax, loans, and bank/mobile money.
- Reports must be reproducible from source transactions, not manually typed summaries.
- Financial projections must connect to operational drivers, not arbitrary growth percentages.
- Budgets compare actuals to flexible budgets, not only static targets.
- Investor or lender numbers must reconcile across narrative, tables, cash flow, balance sheet, funding request, and appendices.

## References

- `references/professional-accounting-systems-gate.md` - detailed checklists for system requirements, IFRS-aware reporting, management accounting, projections, controls, and review.
- Companion skill: `saas-accounting-system` for double-entry implementation patterns and schema-level design.
