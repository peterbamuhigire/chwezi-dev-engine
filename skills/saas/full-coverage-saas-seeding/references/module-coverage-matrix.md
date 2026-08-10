# Module coverage matrix

Generate rows only for capabilities discovered in the product. A row is not
`SUPPORTED` until its application boundary was executed and its evidence retained.

| Module family | Journey prompts | Minimum evidence prompts |
|---|---|---|
| Identity, tenant, RBAC | onboarding, role grant/deny, suspension, offboarding, facility scope | allowed/forbidden matrix, audit, historical attribution, cross-tenant refusal |
| Core domain | create, update, approve, cancel, complete, search, empty state | state transitions, validation, duplicate/replay, audit, report inclusion |
| People and service delivery | customer/patient/member/staff cohorts, appointments/queues, documents, communications | role access, consent/privacy, source-to-output lineage, failure recovery |
| Purchasing and inventory | supplier, requisition, PO, receipt, batch/expiry, transfer, sale/dispense, adjustment | quantities, approval separation, stock valuation/variance, rollback, expiry |
| Billing and finance | invoice, payment, refund, claim, expense, asset, close, reconciliation | source events, balances, period lock, AR/AP, cash/bank, drilldown, idempotency |
| HR and payroll | employee, attendance, leave, payroll, approval, payslip, payment | preparer/approver, deductions/contributions, register-to-ledger tie-out |
| Reporting and administration | dashboards, exports, audit, settings, support, integrations, webhooks, mobile/offline | filters, empty/large reports, export restriction, lineage, side-effect adapter |

For a hospital, extend the core/service row with appointments, triage, encounters,
diagnoses linked to the default coding catalogue, orders, lab results, prescriptions,
dispensing, claims, billing, payments, stock, and clinical privacy. Do not infer
these capabilities from tables or menu labels.
