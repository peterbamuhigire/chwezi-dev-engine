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

## Use when

- A SaaS needs a believable, end-to-end demo tenant and a repeatable system-test fixture.
- A team needs to discover every supported module, create linked synthetic business journeys, exercise failure paths, and produce evidence before go-live.
- A CLI or runner must orchestrate supported UI actions, APIs, typed application services, commands, workflow handlers, posting services, or event/outbox boundaries.

## Do not use when

- The task is only migrations, schema bootstrap, permanent reference-data installation, or a template setup; use the relevant bootstrap/database skill.
- The target is production, the tenant ownership is ambiguous, or real personal, patient, employee, supplier, payment, or regulated data is supplied.
- The product has no supported application boundary for a required capability. Stop with `BLOCKED_CAPABILITY`; never use SQL or a private persistence shortcut.

## Non-negotiable execution rules

1. Never use direct database injection for business or demo activity: no raw DML, table truncation, manual journals, arbitrary SQL in fixtures, direct database handles, repository shortcuts, or ORM bypasses from the seeding layer.
2. Use the same authenticated UI actions, supported APIs, domain commands, services, workflow handlers, posting services, and event/outbox boundaries available to real users. A CLI may orchestrate them but may not bypass them.
3. Inspect the repository and running product before designing fixtures: routes, contracts, permissions, state machines, migrations for understanding only, reference bootstrap, tests, reports, integrations, and existing seeders.
4. Separate standard/reference data, tenant configuration, disposable demo activity, and isolated fault-probe records. Never delete standard data or unrelated tenant data during reset.
5. Use deterministic manifests, stable natural keys, collision registries, actor/tenant/scenario IDs, idempotency keys, correlation IDs, run and entity ledgers, target guards, dry-run, replay, verification, and controlled reset.
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

## Required outputs

1. Discovery report with scope, capability matrix, dependencies, gaps, and stop conditions.
2. Data classification register for default/reference data, tenant configuration, demo activity, and fault probes.
3. Versioned seed manifest with stable keys, cohorts, prerequisites, actors, expected states, negative cases, invariants, and checksum; never passwords, tokens, numeric foreign keys, SQL, or real regulated data.
4. Facility/organisation roster with hard minimums and target volumes per tenant/facility.
5. Scenario catalogue covering every supported module and its happy, failure, permission, duplicate, replay, boundary, rollback, isolation, reporting, and audit journeys.
6. Application execution plan naming the write boundary and actor for each scenario family.
7. Verification and reconciliation plan, defect loop, refresh/reset runbook, evidence pack, and skill-contract test results.

## Ordered workflow

1. **Establish authority and target.** Refuse production or an ambiguous target. Confirm non-production secrets, encrypted PHI/PII handling, test payment/integration adapters, no real outbound messages or money, ownership, retention, and recoverable reset boundary.
2. **Discover capabilities.** Build the capability matrix from implementation and executed boundary evidence. Distinguish implemented, partial, configured-off, externally dependent, and unimplemented features; create blockers instead of fake rows.
3. **Define data boundaries.** Record standard/reference-data source, version, install path, preservation check, tenant configuration, demo ownership, retention, reset rule, and manifest tags.
4. **Design volumes and cohorts.** Set measurable per-tenant/facility minimums and higher targets. Include new/returning, active/inactive, complete/incomplete, normal/exception, high/low volume, privacy-restricted, and other domain-relevant cohorts. Ensure each later workflow has a valid actor and source entity.
5. **Design identities and separation of duties.** Create fictional stable fixture keys, roles, departments, supervisors, facility grants, account states, preparer/approver pairs, suspension/offboarding cases, and preserved historical attribution.
6. **Design chained scenarios.** For each discovered module record prerequisites, boundary, actor, input, state transitions, entities, audit events, downstream effects, reports, negative cases, duplicate/replay, partial failure, and compensation or rollback. Chain source events into billing, stock, payroll, claims, finance, and reports where supported.
7. **Implement a narrow execution adapter.** Carry actor, tenant, scenario, idempotency, correlation, and manifest checksum through every command. Add a static guard rejecting SQL/DML, table names, direct database handles, arbitrary repositories, and private persistence shortcuts in seeding code.
8. **Preflight and dry-run.** Validate manifest schema, tenant/facility codes, actor permissions, prerequisites, reference data, timezones, amounts/quantities, natural-key collisions, environment, secrets, dependency order, and target safety. Dry-run performs zero business writes and reports planned commands, unsupported capabilities, counts, and invariants.
9. **Execute in dependency order.** Apply configuration, identities, reference links, master data, primary records, source transactions, downstream effects, reports, and verification. Do not parallelise dependent writes. Record results in run and entity ledgers.
10. **Run fault and security probes.** Test invalid input, missing prerequisite, duplicate submit, replay, stale version, forbidden role, cross-tenant ID, locked period, negative stock, expiry, overpayment, failed payment, mismatched documents, unapproved payroll, self-approval, cancellation, empty report, export restriction, timeout/retry, and forced mid-run failure as applicable.
11. **Verify and reconcile.** Check counts, state machines, permissions, idempotency, audit lineage, tenant isolation, privacy, reports, source-to-output links, stock, payroll, AP/AR, cash/bank/mobile money, and accounting invariants. Every pass points to machine-readable evidence or a reproducible route.
12. **Repair and retest.** Fix the owning application module or configuration, never the seeded rows. Rerun the smallest failing scenario, affected journey, and impacted verification set; preserve failed evidence.
13. **Replay, reset, and hand off.** Replay to prove no duplicates. Reset only owned fictional activity through the approved application cleanup boundary, prove standard/reference and unrelated tenant data are unchanged, reproduce on a second clean target, and issue the evidence-backed verdict.

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

## References

- `references/seed-manifest-contract.md` — manifest fields, classifications, keys, and execution metadata.
- `references/module-coverage-matrix.md` — module journey and invariant prompts.
- `references/evidence-pack-contract.md` — reproducible proof and verdict structure.
- `references/contract-test-matrix.md` — routing, refusal, replay, reset, and limited-capability tests.
- `saas/saas-seeder` — legacy/template bootstrap only; do not use it for full-coverage business activity when its boundary conflicts with this skill.
- `saas/multi-tenant-saas-architecture`, `security/vibe-security-skill`, `languages/typescript-full-stack`, and `sdlc-meta/kaizen-improvement-system` as applicable.
