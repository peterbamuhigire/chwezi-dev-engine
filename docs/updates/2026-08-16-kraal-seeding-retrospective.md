# Kraal Code seeding retrospective - 2026-08-16

## Reason for the update

The Kraal Code demo programme outgrew the original mental model of a seeder as
a one-time database bootstrap. Between the procurement, manufacturing,
inventory, sales, finance, historical-continuity, inventory-realism,
multi-branch daily-sales, and territory-hierarchy phases, the reusable problem
became a controlled synthetic-operations programme.

## Evidence reviewed

- phased runners from `NileHarvestPhase5SeedRunner` through
  `NileHarvestPhase21DailySalesSeedRunner` and the territory hierarchy runner;
- separate schema-compatibility and normalisation migrations;
- Phase 12 refresh, replay, reset-plan, reset-test, and stale-run reconciliation;
- service-backed procurement, stock, manufacturing, sales, posting, payroll,
  and inventory-adjustment workflows;
- natural-key tenant/branch resolution, stable markers, idempotency keys,
  schema assertions, run ledgers, verification audits, and focused runner tests;
- the master plan's historical continuity and evidence requirements.

## Durable lessons promoted

1. Seeding work needs an explicit class: reference bootstrap, tenant
   configuration, business activity, compatibility repair, or verification/
   refresh. Mixed runners must expose the boundary instead of hiding it.
2. Application workflows remain mandatory for business activity. A controlled
   prepared-SQL exception is useful only for missing-writer master data or
   infrastructure repair, and must produce a product-gap/evidence record.
3. Schema compatibility is a prerequisite gate, not a fallback inside a demo
   run. Tenant ownership of closure and summary tables must be proven before a
   hierarchy or reporting rebuild.
4. Tenant scope must be joined by operational scope: branch, facility, plant,
   store, sales point, territory, and actor grants where applicable.
5. Determinism means stable business fixture identity and explicit dates. A
   random run UUID is acceptable metadata; random business data and wall-clock
   activity dates are not.
6. A run ledger must make partial commits visible because domain services can
   own their transactions. Recovery, compensation, and reset are part of the
   seed contract.
7. Counts and screenshots do not prove an ERP journey. Stock, genealogy,
   approvals, cash/AR/AP, GL, permissions, reports, replay, and isolation need
   machine-readable reconciliation.

## Engine changes

- Added `references/operational-seeding-patterns.md` to
  `full-coverage-saas-seeding`.
- Tightened the skill workflow with classification, schema gates, branch/
  facility scope, hierarchy closure, partial-failure evidence, and runner-level
  contract tests.
- Added routing fixtures separating full-coverage seeding from template
  bootstrap.

## Remaining product-side follow-up

The engine can now require these controls, but it cannot make a downstream
product provide missing writers, tenant-owned closure tables, or compensating
workflows. Future projects should record those as explicit blockers rather than
adding a private SQL shortcut to make the demo appear complete.
