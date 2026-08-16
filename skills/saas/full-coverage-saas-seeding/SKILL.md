---
name: full-coverage-saas-seeding
description: Use when designing, implementing, executing, replaying, or verifying a realistic synthetic SaaS tenant through the product's supported UI, APIs, application services, commands, and workflow boundaries for both prospect demonstration and full system testing.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Full-Coverage SaaS Seeding

<!-- dual-compat-start -->

## Use when

- A SaaS needs a believable, end-to-end demo tenant and a repeatable system-test fixture.
- A team needs to discover every supported module, create linked synthetic business journeys, exercise failure paths, and produce evidence before go-live.
- A CLI or runner must orchestrate supported UI actions, APIs, typed application services, commands, workflow handlers, posting services, or event/outbox boundaries.

## Do not use when

- The task is only migrations, schema bootstrap, permanent reference-data installation, or a template setup; use the relevant bootstrap/database skill.
- The target is production, the tenant ownership is ambiguous, or real personal, patient, employee, supplier, payment, or regulated data is supplied.
- The product has no supported application boundary for a required capability. Stop with `BLOCKED_CAPABILITY`; never use SQL or a private persistence shortcut.

## Non-negotiable execution rules

1. Never use direct database injection to imitate supported business activity: no raw DML for procurement, stock, production, sales, payroll, billing, payments, approvals, journals, or other stateful workflows; no table truncation or ORM/repository bypass for those journeys.
2. Use the same authenticated UI actions, supported APIs, domain commands, services, workflow handlers, posting services, and event/outbox boundaries available to real users. A CLI may orchestrate them but may not bypass them. For the narrow, classified exception covering reference/bootstrap, tenant configuration, compatibility repair, or missing-writer infrastructure, load `references/operational-seeding-patterns.md` and record the gap and controls.
3. Inspect the repository and running product before designing fixtures: routes, contracts, permissions, state machines, migrations for understanding only, reference bootstrap, tests, reports, integrations, and existing seeders.
4. Separate standard/reference data, tenant configuration, disposable demo activity, and isolated fault-probe records. Never delete standard data or unrelated tenant data during reset.
5. Use deterministic manifests, stable natural keys, collision registries, actor/tenant/scenario IDs, idempotency keys, correlation IDs, explicit as-of windows, schema fingerprints, run and entity ledgers, target guards, dry-run, replay, verification, and controlled reset. Random run IDs are metadata; random business fixtures are not deterministic.
6. Mark capabilities `SUPPORTED`, `PARTIAL`, `BLOCKED`, or `NOT_ASSESSED`. A menu, table, migration, or screenshot alone is not evidence of a working capability.
7. Use fictional, synthetic, culturally appropriate identities. Never store reusable production secrets or real regulated data.

## Default/reference data versus demo data

| Layer | Ownership and examples | Lifecycle and reset rule |
|---|---|---|
| Default/reference data | System-owned, versioned global catalogues and configuration required for the product to function: global categories, ICD or coding catalogues, legitimately supplied medicine lists, laboratory/UOM/status/country lists, permission templates, currencies, tax/status vocabularies, and other standards | Install or bootstrap through the approved reference-data path; record source/version; preserve across demo reset and production deployment; never pretend it is tenant activity |
| Tenant configuration | Fictional organisation/facility, departments, settings, fiscal periods, roles, grants, prices, policies, and integration test adapters | Created through tenant setup boundaries; owned by the target tenant; reset only through its approved lifecycle |
| Demo/business activity | Fictional patients, doctors, staff, members, suppliers, products, appointments, encounters, prescriptions, orders, invoices, payments, reports, and audit events | Disposable, manifest-owned, tenant-scoped, linked into realistic journeys, and recreated through application workflows |
| Fault probes | Clearly tagged invalid, duplicate, replay, forbidden, timeout, partial-failure, rollback, privacy, and cross-tenant attempts | Isolated and retained as test evidence; never mixed into the prospect happy-path tenant unless explicitly labelled |

For a hospital, demo data includes a fictional facility, doctors, nurses, patients,
appointments, encounters, prescriptions, lab orders, invoices, payments, and reports.
Default data includes the supported ICD/coding catalogue, medicine and laboratory
reference lists, global categories, units, countries, statuses, permissions,
currencies, tax configuration, and other system-owned catalogues. The demo patient
must reference the default catalogue; it must not replace or become the catalogue.

## Required inputs

| Input | Required | Purpose |
|---|---:|---|
| Product repository, deployed non-production target, owner, engineering/QA/demo operators, environment, tenant scope, reset authority, and secrets mechanism | Yes | Prove safe authority and target |
| PRD/SRS/HLD, routes/screens, API contracts, application services, permissions, states, reports, integrations, tests, existing seeders, and reference bootstrap | Yes | Discover real capabilities and boundaries |
| Finance/accounting doctrine and jurisdictional source register | When money, tax, payroll, stock, billing, assets, or accounting apply | Preserve financial invariants and current-source controls |

## Outputs

1. Discovery report with scope, capability matrix, dependencies, gaps, and stop conditions.
2. Data classification register for default/reference data, tenant configuration, demo activity, and fault probes.
3. Versioned seed manifest with stable keys, cohorts, prerequisites, actors, expected states, negative cases, invariants, and checksum; never passwords, tokens, numeric foreign keys, SQL, or real regulated data.
4. Facility/organisation roster with hard minimums and target volumes per tenant/facility.
5. Scenario catalogue covering every supported module and its happy, failure, permission, duplicate, replay, boundary, rollback, isolation, reporting, and audit journeys.
6. Application execution plan naming the write boundary and actor for each scenario family.
7. Verification and reconciliation plan, defect loop, refresh/reset runbook, schema-compatibility record, controlled-persistence exception register where needed, evidence pack, and skill-contract test results.

## Workflow

1. **Establish authority and target.** Refuse production or an ambiguous target. Confirm non-production secrets, encrypted PHI/PII handling, test payment/integration adapters, no real outbound messages or money, ownership, retention, and recoverable reset boundary.
2. **Classify the work.** Separate reference bootstrap, tenant configuration, business activity, compatibility repair, and verification/refresh. Split mixed responsibilities into ordered steps with separate evidence and reset rules.
3. **Discover capabilities.** Build the capability matrix from implementation and executed boundary evidence. Distinguish implemented, partial, configured-off, externally dependent, and unimplemented features; create blockers instead of fake rows.
4. **Define data boundaries.** Record standard/reference-data source, version, install path, preservation check, tenant configuration, demo ownership, retention, reset rule, and manifest tags.
5. **Design volumes and cohorts.** Set measurable per-tenant/facility minimums and higher targets. Include new/returning, active/inactive, complete/incomplete, normal/exception, high/low volume, privacy-restricted, and other domain-relevant cohorts. Ensure each later workflow has a valid actor and source entity.
6. **Design identities and separation of duties.** Create fictional stable fixture keys, roles, departments, supervisors, facility grants, account states, preparer/approver pairs, suspension/offboarding cases, and preserved historical attribution.
7. **Design chained scenarios.** For each discovered module record prerequisites, boundary, actor, input, state transitions, entities, audit events, downstream effects, reports, negative cases, duplicate/replay, partial failure, and compensation or rollback. Chain source events into billing, stock, payroll, claims, finance, and reports where supported.
8. **Implement a narrow execution adapter.** Carry actor, tenant, branch/facility, scenario, idempotency, correlation, and manifest checksum through every command. Add a static guard rejecting unclassified SQL/DML, unscoped deletes, hard-coded foreign keys, arbitrary repositories, and private persistence shortcuts in business-activity seeding code.
9. **Run the schema-compatibility gate.** Apply and verify versioned migrations, required columns/indexes/triggers/procedures/enums, tenant ownership of closure or summary tables, and a schema fingerprint before business activity. Do not hide compatibility repair inside a replay.
10. **Preflight and dry-run.** Validate manifest schema, tenant/facility codes, actor permissions, prerequisites, reference data, timezones, explicit as-of windows, amounts/quantities, natural-key collisions, environment, secrets, dependency order, and target safety. Dry-run performs zero business writes and reports planned commands, unsupported capabilities, counts, and invariants.
11. **Execute in dependency order.** Apply configuration, identities, reference links, master data, primary records, source transactions, downstream effects, reports, and verification. Do not parallelise dependent writes. Record results in run and entity ledgers, including committed partial work when services own their transactions.
12. **Run fault and security probes.** Test invalid input, missing prerequisite, duplicate submit, replay, stale version, forbidden role, cross-tenant ID, cross-branch/facility ID, locked period, negative stock, expiry, overpayment, failed payment, mismatched documents, unapproved payroll, self-approval, cancellation, empty report, export restriction, timeout/retry, and forced mid-run failure as applicable.
13. **Verify and reconcile.** Check counts, state machines, permissions, idempotency, audit lineage, tenant and branch isolation, privacy, reports, source-to-output links, stock, payroll, AP/AR, cash/bank/mobile money, hierarchy closure, and accounting invariants. Every pass points to machine-readable evidence or a reproducible route; screenshots are supplementary.
14. **Repair and retest.** Fix the owning application module or configuration, never the seeded rows. Rerun the smallest failing scenario, affected journey, and impacted verification set; preserve failed evidence and classify missing writers or migrations explicitly.
15. **Replay, reset, and hand off.** Replay to prove no duplicates. Reset only owned fictional activity through the approved application cleanup boundary, prove standard/reference and unrelated tenant data are unchanged, reproduce on a second clean target, and issue the evidence-backed verdict.

## Finance, stock, privacy, and side-effect controls

When applicable, load the canonical accounting doctrine and require source events,
balanced immutable idempotent journals, period controls, reversal/compensation,
source-document drilldown, subledger tie-outs, controlled stock variance/expiry,
payroll separation, and current source-register checks. Never hard-code statutory
rates or create posted journals directly. Use test adapters for notifications,
webhooks, payment providers, and external integrations; disable real side effects.

## Output contract and release verdict

Return target and safety decision; capability matrix and blocked list; reference-data
preservation result; manifest/version/checksum and scenario order; planned versus
executed counts by tenant/facility/module/cohort; boundary and actor per scenario;
positive/negative/duplicate/replay/rollback/permission/isolation/privacy/reconciliation
results; defect and retest register; evidence locations and exact commands/routes;
limitations; and one verdict: `PASS`, `PASS_WITH_CAVEATS`, `BLOCKED`, or `FAIL`.

Never claim “fully seeded”, “all modules tested”, “production-ready”, or “accounting
reconciles” without the corresponding measured evidence.

## Quality Standards

Evidence must distinguish application execution from compatibility repair,
show tenant and operational-scope isolation, and include replay, failure,
reconciliation, and reset results where the capability applies.

## Anti-Patterns

- Do not use a screenshot as proof of a workflow; retain machine-readable evidence.
- Do not silently replace a missing writer with direct business-table inserts; classify the gap.
- Do not reset a shared table without proving its ownership scope.
- Do not use wall-clock dates or random business identity in a replayable fixture.
- Do not report a module as supported from schema or menu presence alone.

## References

- `references/operational-seeding-patterns.md` - run classification, controlled persistence exceptions, schema compatibility, temporal determinism, branch/facility scope, hierarchy closure, partial failure, and per-runner tests.

- `references/seed-manifest-contract.md` — manifest fields, classifications, keys, and execution metadata.
- `references/module-coverage-matrix.md` — module journey and invariant prompts.
- `references/evidence-pack-contract.md` — reproducible proof and verdict structure.
- `references/contract-test-matrix.md` — routing, refusal, replay, reset, and limited-capability tests.
- `saas/saas-seeder` — legacy/template bootstrap only; do not use it for full-coverage business activity when its boundary conflicts with this skill.
- `saas/multi-tenant-saas-architecture`, `security/vibe-security-skill`, `languages/typescript-full-stack`, and `sdlc-meta/kaizen-improvement-system` as applicable.

<!-- dual-compat-end -->
