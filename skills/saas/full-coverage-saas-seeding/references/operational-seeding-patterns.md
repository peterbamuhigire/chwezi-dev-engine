# Operational seeding patterns

Parent skill: [`full-coverage-saas-seeding`](../SKILL.md)

This reference records durable lessons from a phased ERP demo programme that
grew from a tenant contract check into procurement, manufacturing, inventory,
local sales, export, finance, recurring refresh, inventory realism, daily
multi-branch sales, and territory hierarchy work. It is a pattern guide, not a
copy of that project's implementation.

## Classify the run before writing code

Do not call every database population task a business-data seed. Choose one
primary class and keep its permissions and reset policy separate.

| Class | Purpose | Allowed write boundary | Typical modes |
|---|---|---|---|
| `reference-bootstrap` | Install system-owned catalogues, statuses, units, currencies, or permissions | Approved reference-data installer or migration | `dry-run`, `verify`, `apply` |
| `tenant-configuration` | Create fictional tenant structure, branches, facilities, roles, stores, policies, and grants | Tenant onboarding/configuration services; controlled master-data writer only when no writer exists | `dry-run`, `verify`, `apply` |
| `business-activity` | Exercise procurement, stock, production, sales, payroll, billing, payments, and reporting journeys | The same authenticated application services, APIs, commands, posting boundaries, and outbox adapters used by users | `dry-run`, `verify`, `apply`, `replay` |
| `compatibility-repair` | Make a known schema or legacy-data correction safe for the next activity phase | Versioned migration or narrowly scoped repair command; never hidden inside a happy-path activity seed | `dry-run`, `verify`, `apply` |
| `verification-refresh` | Reconcile, refresh a dated activity window, prove replay, or reset owned demo activity | Read-only reports, supported reversal/cleanup workflow, or an explicitly owned reset boundary | `dry-run`, `verify`, `refresh`, `reset-plan`, `reset-test`, `reset` |

If a runner contains more than one class, split it into ordered runners or
expose the classes as explicit steps in its manifest. A procurement phase may
create a missing tenant-local category through a controlled master-data path
and then execute the purchase request -> PO -> receipt -> quality -> invoice
journey, but the two actions must remain distinguishable in its evidence.

## Boundary rule for direct persistence

The default remains strict: do not insert or update business activity directly
to make a screen or report non-empty. Use the real workflow so validation,
permissions, maker-checker, stock movement, audit, posting, and side effects
are exercised.

There is a narrow exception for a writer gap or infrastructure repair. Direct
prepared SQL is acceptable only when all of the following are true:

1. The missing writer is recorded as `PARTIAL` or `BLOCKED`, with an owner and
   a follow-up product task.
2. The operation is classified as reference, tenant configuration,
   compatibility repair, or seed evidence; it is not a substitute for a
   financial, stock, payroll, payment, approval, or other business workflow.
3. The table and column allowlist, expected foreign keys, enum values, and
   tenant/branch scope are checked against the live schema before mutation.
4. Inputs use prepared statements and explicit columns. No interpolated values,
   table truncation, `SELECT *` contract, or arbitrary repository shortcut is
   permitted.
5. The runner sets the audit actor and tenant context expected by triggers,
   records a marker and stable fixture key, runs inside a bounded transaction,
   and verifies the resulting state.
6. The exception, blast radius, reset rule, and evidence locator are returned
   in the run ledger.

Never make an exception merely because a private service is inconvenient. A
missing application boundary is a product finding, not permission to fake a
posted journal or stock ledger entry.

## Schema compatibility comes before activity

Phased ERP seeding repeatedly exposed the need for a compatibility gate before
the next workflow can execute. Before applying a phase:

- run the versioned migration or compatibility command separately;
- fingerprint required tables, columns, indexes, foreign keys, triggers,
  procedures, and enum values;
- fail closed on missing or incompatible schema rather than trying a fallback;
- record the migration version and schema fingerprint in the seed evidence;
- verify the migration in a clean second target before calling the phase
  portable.

Schema repairs such as adding tenant ownership to a closure table, normalising
batch numbers, or adding a missing journal link belong to migrations or repair
runners. They must not be silently bundled into a normal activity replay.

## Tenant, branch, and hierarchy scope

Tenant isolation is necessary but not sufficient for operational data. Resolve
the tenant by a unique approved natural key and refuse zero or multiple matches.
Resolve branch, facility, plant, store, sales point, and actor IDs by stable
fixture keys or validated natural keys. Do not carry numeric IDs from one
environment into another.

Every read and write must carry the narrowest applicable scope:

- `tenant_id` on every tenant-owned table and owned join;
- `branch_id` or `facility_id` on branch-local operational documents;
- plant, store, sales point, territory, or department scope where the workflow
  requires it;
- actor and role grants for the branch/facility being exercised.

Hierarchy closure tables need an explicit policy. If the closure table is
tenant-owned, add and verify `tenant_id` before seeding and rebuild only that
tenant's closure rows. If it is genuinely global, the runner must prove that
the rebuild is a coordinated global operation and must not mix it with a
tenant-local reset. An unscoped `DELETE FROM closure_table` is never an
acceptable tenant seed primitive.

## Determinism has two layers

Use deterministic business identity and deterministic time windows:

- stable fixture keys, natural codes, markers, idempotency keys, and scenario
  keys identify business records;
- explicit historical dates and `--from`/`--to` or `--days` windows make replay
  comparable;
- current time is metadata only, not a business date, expiry date, invoice
  date, or reporting period unless the run explicitly declares an as-of clock;
- random UUIDs are acceptable for a run ID or correlation ID, but never as the
  only way to find a business fixture on replay;
- random assignment, random quantities, and random names are prohibited unless
  a seeded generator value is declared and replayed from the manifest.

Historical continuity and rolling activity are different products. Historical
backfill must preserve chronology and source stock availability. A rolling
refresh appends a bounded window, skips an already materialised idempotency
key, and never rewrites history merely to move a dashboard date.

## Workflow and accounting discipline

Each scenario must name its actor, source records, state transitions, and
downstream effects. Use separate preparer and approver identities wherever the
product enforces separation of duties. Include branch grants and historical
attribution; a root user that can do everything is not evidence of a valid
workflow.

For finance, stock, payroll, and payments, the seed verifies source-to-output
lineage rather than row counts alone:

- procurement documents reconcile to receipts, invoices, approvals, and AP;
- stock quantities reconcile across batch, base UOM, store, ledger, valuation,
  expiry, and transfer state;
- manufacturing output has recipe, material issue, WIP, yield/loss, batch, and
  quality genealogy;
- sales and payments reconcile to invoice state, customer/agent balances,
  cash/bank/mobile-money records, and GL journals;
- payroll and expenses reconcile their registers to approvals and journals;
- period locks, reversals, and failed posting paths are tested where supported.

Do not create a balancing journal directly to repair an attractive dashboard.
Repair the source workflow or record the capability as blocked.

## Run ledger and partial failure

Every apply, replay, refresh, repair, and reset records a run with:

- manifest ID/version/checksum, phase, class, environment, commit, operator,
  tenant, branch/facility scope, and command;
- start, completion, and failure status, current step, counts, and error;
- actor, scenario, fixture key, idempotency key, correlation ID, and server IDs
  for each materialised entity;
- planned, inserted, skipped, reconciled, compensated, and failed counts;
- verification and reset evidence locators.

Do not assume a phase is atomic because its orchestrator opened a transaction.
Application services may commit their own documents, so a later failure can
leave valid partial activity. The runner must either provide compensation,
record the partial state for a retry-safe continuation, or stop with an explicit
reset/recovery instruction. A failed run must not be reported as `SKIPPED`.

## Minimum contract tests per runner

Every entrypoint needs a small test matrix, even when the full database suite
is expensive:

| Check | Required assertion |
|---|---|
| Argument contract | Default is dry-run; unsupported flags and modes fail closed; help is accurate |
| Production guard | Production/live/prod mutation is refused before writes |
| Dry-run | Zero business writes, with planned counts and prerequisites returned |
| Schema gate | Missing table, column, enum, trigger, or procedure produces a named blocker |
| First apply | Expected states, audit rows, postings, and lineage are verified |
| Replay | Same manifest produces no duplicate business effects |
| Scope | Foreign tenant, branch, facility, or actor input is refused |
| Failure | Mid-run failure leaves a ledger entry and a tested recovery or blocker |
| Reset | Only owned synthetic records are removed/reversed; reference and unrelated data remain |
| Domain reconciliation | Counts, balances, quantities, dates, reports, and state transitions tie out |

Structural tests are useful but do not prove the live workflow. At least one
non-trivial phase per module needs a runtime smoke or integration verification
on a clean target.

## Anti-patterns learned from phased ERP seeding

- One giant "seed everything" command. Fix: keep dependency-ordered phase
  runners behind a small orchestrator and expose resumable checkpoints.
- Treating schema repair as demo activity. Fix: version it as a migration or
  compatibility runner and record its fingerprint.
- Directly inserting rows because the UI is slow or a writer is missing. Fix:
  use the supported boundary, or declare a controlled writer exception and a
  product gap.
- Using tenant ID, branch ID, or account ID copied from a local database. Fix:
  resolve by natural key and verify ownership at runtime.
- Rebuilding a shared closure table with a tenant-local delete. Fix: enforce
  tenant ownership first or run a reviewed global rebuild with a distinct scope.
- Using today's date, random quantities, or random fixture assignment. Fix:
  use an explicit as-of clock, date window, and deterministic schedule.
- Calling a screenshot or non-empty table proof of capability. Fix: retain
  machine-readable state, permission, lineage, replay, and reconciliation
  evidence.
- Marking an unavailable module as complete because its tables exist. Fix:
  classify `SUPPORTED`, `PARTIAL`, `BLOCKED`, or `NOT_ASSESSED` from executed
  boundary evidence.
