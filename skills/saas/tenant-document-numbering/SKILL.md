---
name: tenant-document-numbering
description: Use when designing, retrofitting or reviewing user-facing document numbers such as invoice, receipt, order, purchase-order or journal numbers in a multi-tenant system, so each tenant and document type gets one contiguous, never-reset series. Not for primary keys, ledger posting rules or tax-authority fiscal numbering.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Tenant Document Numbering
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

Every number a person sees, prints, quotes or searches for on a business document is a
control, not a decoration. An auditor reads a missing invoice number as possible
suppressed revenue, and a duplicate one as possible fraud. This skill is the engine
standard (owner rule, 5 Nov 2026) for making those numbers contiguous in every
multi-tenant system, whether it is being designed or already runs in production.

<!-- dual-compat-start -->
## Use When

- Designing any new document type that carries a user-facing number: sales invoice,
  receipt, credit note, bill, kitchen ticket, order, purchase order, goods receipt,
  supplier return, stock transfer, adjustment, count, expense, deposit, withdrawal,
  account transfer, journal entry, payroll run, reservation, folio, prescription.
- Retrofitting numbering in an existing SaaS where numbers come from `COUNT(*)+1`,
  `MAX+1`, `uniqid`, random strings, the row id or a database sequence.
- Reviewing a diff, schema, API or mobile sync flow that creates, deletes or displays
  numbered documents.
- Splitting a shared counter (for example platform invoices consuming a tenant's sales
  series) or adding a separate credit-note series.

## Do Not Use When

- The question is the surrogate key or auto-increment `id` itself. Ids stay separate
  and untouched; use `database-design-engineering`.
- The task is the posting logic behind a journal or invoice; use `accounting-engine`
  or `saas-accounting-system`, and keep this skill only for the number.
- A tax authority issues or prescribes the fiscal number (EFRIS, eTIMS, EFD and
  similar); use `electronic-fiscal-taxing`. Store the authority number in its own
  column. It never replaces or consumes the tenant series.
- The identifier is never shown to a person (correlation ids, idempotency keys, public
  URL slugs). Use random or UUID identifiers there.

## Required Inputs

| Input | Source | If absent |
|---|---|---|
| Document type inventory: every table, column and code path that writes a number | Repository search, schema from `INFORMATION_SCHEMA` (not a schema snapshot) | Stop the retrofit; produce the inventory first |
| The issue event per type (finalised, posted, approved, sent, settled) | Domain owner, existing workflow code | Record as an open question; do not guess a draft-time number |
| Tenant scope column and how the tenant id reaches the service | Auth context, `multi-tenant-saas-architecture` | Stop; never take the tenant id from the request body |
| Production shape: highest existing numbers, duplicates, row counts, peak concurrent writers | Read-only query on a production copy | Design only; mark seeding and capacity `NOT ASSESSED` |
| Database engine and version | Deployment record | Give MySQL 8 and PostgreSQL forms; mark engine-specific checks `NOT ASSESSED` |

## Workflow

1. **Inventory.** List every generator and every numbered table. Classify each:
   counter, COUNT+1, MAX+1, random/uniqid/hash, id-derived, client-assigned, sequence
   object, trigger or stored procedure, none. Note deletes of numbered rows and
   allocations outside the save transaction.
2. **Register the types.** One registry entry per (document type): stable type key,
   scope (tenant or platform), tables and columns in the series, format, parse pattern,
   lock tier and rank, issue event, rollout switch, plain-language label. Load
   [schema and allocator](references/schema-and-allocator.md).
3. **Design the allocator.** One service is the only way to make a number. It runs
   inside the caller's transaction, locks the counter row, probes for clashes and
   returns the formatted number. Same reference.
4. **Fix the lifecycle.** Number at issue time, nullable while draft, never delete a
   numbered row, void instead. Wrap each unit of work in the retry helper.
5. **Close the edges.** Idempotency key on the document row, numbers as strings in
   APIs, provisional tags offline, platform and credit-note series separate. Load
   [API, offline and guardrails](references/api-offline-and-guardrails.md).
6. **Size for decades.** Column widths, padding, sort keys, incremental gap report.
   Load [seeding, clashes and capacity](references/seeding-clashes-and-capacity.md).
7. **Retrofit safely** (existing systems only). History untouched, counters seeded
   past existing numbers before switch-on, unique keys added after a duplicate audit,
   per-type switches. Load [retrofit and rollout](references/retrofit-and-rollout.md).
8. **Prove it.** Run the test and review checklists in the guardrails reference and
   record evidence. An unrun check is `NOT ASSESSED`, never a pass.

## Quality Standards

The eleven rules. A design or diff that breaks one is not done.

1. **One series per (tenant, document type), never reset.** Not per year, branch,
   till or month. A date fragment such as `JE-2026-` is a label; the counter behind it
   keeps counting. Counters are `BIGINT UNSIGNED` (PostgreSQL `bigint` with a
   `CHECK (last_number >= 0)`), in a counter table locked with `SELECT ... FOR UPDATE`.
2. **Allocate inside the save transaction, as late as possible.** After validation,
   stock checks, pricing and approvals; immediately before the document `INSERT`.
   Rollback then returns the number. Forbidden: `COUNT(*)+1`, `MAX+1` without a
   counter, random/`uniqid`/hash numbers, numbers derived from the id, client-assigned
   numbers, allocation in a separate transaction, database sequence objects or
   auto-increment for the visible number (both leave gaps on rollback), and trigger or
   stored-procedure generators hidden from application code.
3. **Number at issue time.** Drafts carry no number (nullable column; a unique key
   allows many NULLs). Drafts may be deleted. A numbered document is never deleted: it
   is voided, keeps its number, stays in the series, and voids are shown (struck
   through with the reason), not hidden.
4. **Handle clashes in three layers.** Seed the counter from the maximum numeric part
   of numbers that match the type's own pattern (never from `COUNT`). While holding the
   counter lock, probe the type's tables and step past any number that already exists
   (an existing document fills that slot, so no gap). Keep `UNIQUE (tenant_id,
   number)` on every numbered table as the backstop. On a duplicate-key error at
   insert, roll back the whole transaction and retry once; if it clashes again, fail
   with a plain message: "We couldn't give this receipt a number just now. Nothing was
   saved. Please try again."
5. **Fixed lock order.** Business-document counters first (ordered by rank), the
   journal-entry counter last. Retry the full transaction on deadlock or lock-wait
   timeout, at most 3 attempts in total. Retries burn no number because the rollback
   undoes the counter update.
6. **Separate series.** The platform's own invoices to tenants use a platform-scope
   counter table and never consume a tenant counter. Credit notes have their own
   series. Imported or supplier-supplied numbers go in their own column (for example
   `supplier_reference`) and never consume or advance the counter.
7. **Durable idempotency.** `idempotency_key` on the document row with `UNIQUE
   (tenant_id, idempotency_key)`, looked up inside the transaction before allocating,
   so a replay at any time returns the same document and number. Numbered create APIs
   require the key. Never invent fallback keys (time buckets, `nokey-` prefixes).
8. **The server issues every number.** Offline documents show a provisional tag that
   cannot be mistaken for a number ("Pending · 7F3KQ9"); printouts say the document is
   not yet confirmed. The server number is written back durably after sync and
   replaces the tag everywhere.
9. **Capacity for decades.** Number columns at least `VARCHAR(40)` (fixed text plus 19
   digits fits). Numbers travel as strings in APIs, never JSON numbers. Padding by
   volume: 8 digits for per-sale types, 6 otherwise; the counter grows past its
   padding. Never `ORDER BY` the number string alone; sort by issue timestamp, then id.
   The gap report is incremental with a watermark.
10. **Retrofit without touching history.** No `UPDATE` of an issued number; backfill
    new columns only with the number the row already displayed. Seed every counter past
    existing numbers before switching on. A format change gets a new counter key; a
    counter is never lowered. Add unique keys only after a duplicate audit, skipping and
    reporting rather than aborting. One switch per type for rollback.
11. **Guardrails.** A CI ratchet bans other generators and `DELETE` of numbered rows; a
    schema test asserts the unique keys; a nightly gap and duplicate report alerts.

## Anti-Patterns

- `SELECT COUNT(*)+1` or `MAX(number)+1` at insert time. Two tills read the same value,
  and a deleted row lets the number be reissued. Fix: counter row with `FOR UPDATE`.
- Using `AUTO_INCREMENT`, a PostgreSQL `SEQUENCE` or `IDENTITY` for the visible
  number. Both are non-transactional and leave gaps on rollback. Fix: counter table.
- Allocating in its own short transaction "to reduce locking". A failed save burns the
  number. Fix: allocate late inside the save transaction and shorten what follows.
- Numbering drafts on open, then deleting abandoned drafts. Fix: number at issue.
- Deleting a voided or mistaken document. Fix: void it, keep the number, show it.
- Per-branch or per-year counters adopted silently. Fix: one series per tenant and
  type; dates are labels.
- Seeding from `COUNT(*)`. It jumps the series past the real highest number and opens
  a gap on day one. Fix: seed from the maximum parsed number that matches the pattern.
- Platform billing sharing the tenant's invoice counter. Fix: platform-scope counter.
- Returning `"invoice_number": 1042` as a JSON number. Fix: always a string.
- Hidden trigger or stored-procedure generators. Fix: one application allocator that
  tests can exercise.

## Outputs

- Generator inventory with method, location and verdict per document type.
- Document type registry (type key, scope, tables, format, pattern, tier, rank, issue
  event, switch, label).
- Counter schema, allocator, retry wrapper and clash-probe design.
- Lifecycle table per type: issue event, delete paths changed to void.
- API and offline contract changes; capacity decisions.
- Retrofit rollout and rollback plan (existing systems).
- Test, CI ratchet and nightly report evidence.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | Generator inventory and type registry | Markdown table plus registry source | `docs/numbering/inventory.md` |
| Data safety | Concurrency, rollback and clash test results | Test report | `evidence/numbering/allocator-tests.txt` |
| Data safety | History checksum before and after rollout | Checksum diff per tenant | `evidence/numbering/rollout-checksums.csv` |
| Performance | Counter lock-wait benchmark at peak writers | Benchmark log with p95 | `evidence/numbering/lock-wait.md` |
| Operability | Nightly gap and duplicate report | Report rows plus alert config | `docs/numbering/gap-report.md` |
| Release evidence | Per-type switch-on record and rollback plan | Markdown checklist | `docs/numbering/rollout.md` |

## References

- [Schema and allocator](references/schema-and-allocator.md): MySQL 8 and PostgreSQL
  counter tables, registry entry, allocator pseudo-code, PHP allocator and retry
  wrapper, issue-time lifecycle, lock order.
- [Seeding, clashes and capacity](references/seeding-clashes-and-capacity.md): seed
  queries, probe, unique-key backstop, column widths, padding, sorting, incremental gap
  report.
- [API, offline and guardrails](references/api-offline-and-guardrails.md): API
  contract, idempotency, offline provisional tags, CI ratchet, test checklist, review
  checklist.
- [Retrofit and rollout](references/retrofit-and-rollout.md): zero-disruption order of
  operations, safe unique-key migration, rollback, client notice.
- Companions: `multi-tenant-saas-architecture` (tenant context),
  `database-design-engineering`, `mysql-engineering`, `postgresql-engineering`,
  `api-design-first`, `saas-accounting-system`, `accounting-engine`,
  `pwa-offline-first`, `android-development`, `code-safety-scanner`,
  `advanced-testing-strategy`.
- Reference implementation plan (Maduuka, 5 Nov 2026): `docs/plans/numbering/` in the
  Maduuka repository, especially `03-architecture.md`, `04-production-rollout.md`,
  `07-capacity-and-field-sizing.md` and `02-kaizen-findings.md`.

<!-- dual-compat-end -->

## Capability and permission contract

Default to read-only analysis and design. Edit schema, migrations or allocator code
only when the task authorises it, in the repository and a disposable environment.
Never run a seed, unique-key or backfill migration against production from this
skill; hand the reviewed migration to the authorised operator. Never print one
tenant's numbers or counts in another tenant's context or error message.

## Degraded mode

Without database access, deliver the registry, allocator and migration as a labelled
design, and mark seeding values, duplicate counts and lock-wait figures
`NOT ASSESSED`. Without execution, return the test list as a plan, not as passed.
Without the domain owner, record each type's issue event as an open question.

## Decision rules

| Condition | Action | Failure avoided |
|---|---|---|
| Users can discard the document before it is final | Number at issue; draft number column nullable | A series full of meaningless voids, or gaps from deleted drafts |
| An existing type keeps its format | Seed from the highest matching number and continue | Reissuing an old number |
| A type changes format | New counter key; old row untouched | Lowering a counter and reissuing numbers |
| Existing duplicates block a unique key | Record them, skip the key for that table, keep the probe | Rollout aborted by historical data |
| Peak lock wait exceeds the target | Move slow work after the insert; keep allocation inside the transaction | Gaps from out-of-transaction allocation |
| A tax authority also numbers the document | Store its number separately; keep the tenant series | Fiscal number consuming or replacing the series |
| A client sends a number on create | Ignore it unless it is a documented external reference column | Forged or duplicate numbers |

## Sources

Checked on 5 Nov 2026 against primary documentation; review by 5 Feb 2027:
PostgreSQL 18 sequence functions (sequences cannot give gapless numbers), PostgreSQL 18
unique indexes (NULLs distinct by default; `NULLS NOT DISTINCT`), PostgreSQL 18 error
codes (`23505`, `40P01`, `40001`, `55P03`), MySQL 8.4 InnoDB locking reads (locks held
to commit or rollback), MySQL 8.4 auto-increment handling (rolled-back values are
lost), MySQL 8.4 `CREATE INDEX` (unique index permits multiple NULLs), MySQL 8.4 server
error reference (`1062`/`23000`, `1205`, `1213`/`40001`), RFC 8259 section 6 (integers
are interoperable only within plus or minus 2^53 - 1). URLs, access dates and scope are
recorded in `docs/updates/2026-11-05-tenant-document-numbering-standard.md`.
