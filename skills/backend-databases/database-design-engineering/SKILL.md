---
name: database-design-engineering
description: Use when designing or reviewing relational or document-backed data architecture for SaaS platforms, ERP systems, APIs, analytics stores, or mobile sync. Covers domain modeling, tenancy, indexing, migrations, integrity, retention, and performance tradeoffs.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Database Design Engineering
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Use when designing or reviewing relational or document-backed data architecture for SaaS platforms, ERP systems, APIs, analytics stores, or mobile sync. Covers domain modeling, tenancy, indexing, migrations, integrity, retention, and performance tradeoffs.

## Do Not Use When

- The task is query tuning or production incident diagnosis without a schema-design decision; use the database operations or reliability skill.
- The datastore is a search index, cache, or vector store whose source-of-truth semantics belong elsewhere.

## Required Inputs

| Input | Required | Why it matters |
|---|---|---|
| Domain entities, invariants, and lifecycle rules | yes | Determines tables, keys, constraints, and valid state transitions |
| Read and write access patterns | yes | Drives indexes, transaction boundaries, and denormalization choices |
| Data volume, growth, and retention expectations | yes | Exposes scaling and archival constraints |
| Existing schema and migration constraints | conditional | Enables safe evolution without data loss or prolonged locking |

## Workflow

Model invariants and ownership, choose keys and relationships, enforce integrity in the database, design indexes from verified access paths, plan reversible expand-contract migrations, then test concurrency, rollback, and representative query plans.

## Quality Standards

The schema enforces material invariants with types, constraints, and transactions rather than application convention alone. Each index supports a named query, and every migration states lock, backfill, compatibility, rollback, and validation behavior.

## Outputs

| Output | Consumer | Acceptance condition |
|---|---|---|
| Logical and physical schema | Application and data engineers | Identifies ownership, keys, constraints, relationships, types, and intentional denormalization |
| Index and transaction plan | Implementers | Links access patterns to indexes and defines concurrency behavior |
| Migration packet | Release and operations teams | Includes sequencing, compatibility window, backfill, validation, rollback, and risk notes |

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Data safety | Migration plan | Markdown doc per `skill-composition-standards/references/migration-plan-template.md` | `docs/data/migration-2026-04-16-add-tenant-column.md` |
| Data safety | Entity model | Markdown doc per `skill-composition-standards/references/entity-model-template.md` | `docs/data/entity-model-billing.md` |
| Data safety | Access pattern register | Markdown doc per `skill-composition-standards/references/access-patterns-template.md` | `docs/data/access-patterns-billing.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
<!-- dual-compat-end -->
Use this skill when schema choices will shape correctness, performance, or future maintainability. It complements vendor-specific database skills by focusing on design logic that survives framework changes.

## Load Order

1. Load `world-class-engineering`.
2. Load this skill to design the data model and lifecycle.
3. Load engine-specific parent skills afterward: `mysql-engineering`, `mysql-operations`, `postgresql-engineering`, or `postgresql-operations`.

## Database Workflow

### 1. Model the Domain

Define:

- Core entities and their lifecycles.
- Ownership and tenancy boundaries.
- Transactional invariants.
- Reporting and audit requirements.
- Retention, archival, and deletion rules.
- The release and migration constraints for live data.

Model events and states, not just forms and screens.

### 2. Choose the Storage Shape

Prefer relational design when:

- Consistency matters.
- Multi-table invariants exist.
- Reporting and joins are central.

Prefer document or key-value structures for:

- Flexible metadata.
- Cached projections.
- Denormalized read models or unstructured payloads.

Do not use schemaless storage as a substitute for undecided modeling.

### 3. Define Table Boundaries

- One table should represent one durable business concept or event stream.
- Separate current state from append-only history when auditability matters.
- Distinguish master data, transactions, and derived projections.
- Avoid overloading one table with mutually exclusive concepts.

### 4. Design for Scale and Safety

- Add tenant or ownership keys early.
- Design indexes around real query predicates and sort order.
- Keep writes idempotent where retries are possible.
- Plan archival, purging, and partitioning before large-volume tables arrive.
- Use expand-contract migrations for live systems.
- Separate transactional truth from projections, integrations, and analytical read models.
- Design test-data and backfill strategies for major schema evolution before the first risky migration.

## Core Standards

### Integrity

- Enforce invariants at the strongest reasonable layer: schema, transaction, application, worker.
- Use foreign keys where ownership is mandatory and module boundaries permit it.
- Use append-only ledgers for financial and audit-critical domains.
- Never encode important business rules only in UI validation.

### Tenancy

- Every tenant-scoped table must carry the tenant key.
- Every tenant-scoped query must constrain by tenant key.
- Every unique constraint must reflect tenancy where appropriate.
- Cross-tenant analytics should use controlled derived datasets, not raw shared queries.

### Indexing

- Index for the access path, not for column popularity.
- Prefer composite indexes that match filter plus sort order.
- Remove duplicate or low-value indexes that tax writes.
- Validate index usefulness against actual queries and execution plans.

### Migrations

- Make every migration forward-safe and observable.
- Prefer additive changes, backfills, then cutovers, then cleanup.
- Keep application code compatible across deployment overlap where possible.
- Rehearse destructive or high-volume changes before production.
- Tag migrations with rollback posture: reversible, compensating-only, or forward-fix-only.
- For web projects, provide a root pull-time migration script that reads the app's environment database settings, compares tracked migrations with live migration history, and applies only missing migrations.
- Never bundle seeds into the normal migration-apply path. Demo data, reference seeds, fixtures, and production bootstrap scripts must require a separate explicit command.

### Operable Data Systems

- Emit release markers and migration identifiers into logs and dashboards where possible.
- Track replication lag, queue lag, backfill progress, and lock or saturation risk on critical stores.
- Treat long-running migrations and backfills as operational workflows with owners and stop conditions.
- Document how data correctness will be verified after migration, replay, or recovery.

### Scale, Replication, and Change Data

- Know which queries must read current truth and which can tolerate replica lag.
- Design outbox, CDC, or projection pipelines so integration needs do not corrupt the transactional model.
- Budget storage, index, and retention cost for hot tables before volume becomes painful.
- Validate the hottest access paths with execution plans, cardinality assumptions, and realistic filters.

## Decision Heuristics

Normalize when:

- Data duplication would create correctness risk.
- Multiple workflows update the same fact.

Denormalize when:

- Read performance or query simplicity clearly outweighs duplication cost.
- The source of truth remains obvious.
- Refresh or reconciliation strategy is explicit.

Use soft delete when:

- Recovery, auditability, or legal hold matters.

Use hard delete when:

- Data minimization or cost pressure is stronger and downstream references are safely handled.

## Deliverables

For substantive database work, produce:

- Entity and lifecycle summary.
- Table or collection design.
- Index plan.
- Migration strategy.
- Data verification and rollback posture.
- Data retention and audit plan.
- Top 5 critical queries or access patterns.
- Projection, outbox, or replication notes where external reads or integrations exist.

## Review Checklist

- [ ] Domain entities reflect real business concepts.
- [ ] Tenant and ownership boundaries are explicit.
- [ ] Invariants are protected at durable layers.
- [ ] Indexes match real access paths.
- [ ] Migrations support live deployment safety.
- [ ] Migration verification and rollback posture are explicit.
- [ ] Audit, retention, and archival rules are documented.
- [ ] Reporting needs do not distort the transactional model without justification.
- [ ] Replica lag, projections, or CDC assumptions are explicit where they matter.

## References

- [references/data-review-checklist.md](references/data-review-checklist.md): Schema and migration review prompts.
- [references/live-data-evolution.md](references/live-data-evolution.md): Expand-contract, backfills, verification, and rollback posture.
- [../../sdlc-meta/world-class-engineering/references/source-patterns.md](../../sdlc-meta/world-class-engineering/references/source-patterns.md): Source-derived patterns for design quality and website/data analysis.

## Capability contract
Design schemas and migration plans by default. Apply DDL, backfills, retention jobs, or production queries only with explicit database and environment authority.

## Degraded mode
If workload samples or schema access are unavailable, provide a read-only logical design and mark index, capacity, and migration claims unverified.

## Domain Anti-Patterns
- Omitting foreign-key or application integrity rules. Fix: state enforcement explicitly.
- Indexing every column. Fix: derive indexes from measured access paths.
- Mixing tenant data without a tenant key. Fix: enforce isolation in schema and queries.
- Shipping destructive migrations in one step. Fix: use expand-contract.
- Retaining data indefinitely. Fix: define retention and deletion ownership.
