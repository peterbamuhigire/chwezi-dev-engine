# Evidence pack contract

The pack must let a reviewer reproduce what was inspected, executed, blocked, and
verified without trusting a populated screen.

## Required contents

- target/environment/commit, owner, operator, manifest checksum, run ID, and command or route log;
- capability matrix with evidence locator and `SUPPORTED`, `PARTIAL`, `BLOCKED`, or `NOT_ASSESSED` status;
- reference-data version and before/after preservation result;
- planned versus executed counts by classification, tenant, facility, module, and cohort;
- entity/run ledgers with actor, scenario, idempotency, correlation, response status, and server identifiers;
- state, permission, duplicate/replay, rollback, isolation, privacy, report-lineage, integration, stock, payroll, and accounting results where applicable;
- defect register linking scenario, route/service, evidence, severity, owner, fix, and retest;
- reset/replay results, known limitations, unassessed dependencies, and final verdict.

Screenshots are supplementary. They cannot prove isolation, balances, idempotency,
rollback, privacy, or a complete module journey without machine-readable evidence.
