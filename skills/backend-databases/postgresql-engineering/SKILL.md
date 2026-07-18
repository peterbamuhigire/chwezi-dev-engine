---
name: postgresql-engineering
description: Use when designing, implementing, or reviewing PostgreSQL application data models, SQL, indexes, constraints, extensions, server-side routines, and production query patterns. Load the absorbed PostgreSQL reference files for fundamentals, advanced SQL, schema patterns, and server programming.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# PostgreSQL Engineering
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

Use this parent skill as the active PostgreSQL engineering entrypoint. Keep implementation guidance here short; load the relevant reference module only when the task needs that depth.

<!-- dual-compat-start -->
## Use When

- Designing PostgreSQL-backed features, schemas, indexes, constraints, and access paths.
- Reviewing SQL correctness, transaction boundaries, isolation assumptions, or extension usage.
- Implementing functions, triggers, views, materialized views, or server-side routines.
- Consolidating PostgreSQL-specific engineering advice before pairing with `database-design-engineering` or `database-reliability`.

## Do Not Use When

- The task is unrelated to this parent skill or is better handled by a narrower active parent named in the workflow.
- The request only needs a trivial answer and no reference module needs to be loaded.

## Required Inputs

- Gather the concrete system, repository, environment, constraints, and deliverable before loading references.
- Identify which absorbed reference file is needed; do not load every migrated reference by default.
## Workflow

1. Start with `database-design-engineering` for logical model, integrity, tenancy, and migration shape.
2. Load only the reference file matching the task:
   - `references/postgresql-fundamentals.md` for baseline PostgreSQL usage and core concepts.
   - `references/postgresql-patterns.md` for schema and application patterns.
   - `references/postgresql-advanced-sql.md` for advanced query design.
   - `references/postgresql-server-programming.md` for functions, triggers, and server-side behaviour.
3. Pair with `postgresql-operations` for administration, performance incidents, tuning, backups, or production operations.
4. Pair with `postgresql-ai-platform` only when pgvector or AI platform concerns are central.

## Quality Standards

- Preserve data integrity with constraints, types, and transaction design before relying on application checks.
- Make query plans reviewable: expected indexes, cardinality assumptions, and failure cases must be explicit.
- Treat migrations as reversible operational changes with lock, runtime, and rollback impact stated.

## Anti-Patterns

- Treating absorbed reference files as active skills or separate routing entrypoints.
- Loading every migrated child reference instead of the one that matches the task.
- Producing generic advice without constraints, evidence, or next verification steps.
## Outputs

- PostgreSQL schema, SQL, migration, or review notes with integrity and performance evidence.
- Reference files loaded and companion skills used.

## References

- Load only the references/<old-skill>.md files named in the workflow when their depth is required.
<!-- dual-compat-end -->

## Inputs
| Input | Required | Purpose |
|---|---|---|
| PostgreSQL version and schema | yes | Select valid features |
| Query plans and cardinalities | yes | Design indexes |
| Migration and availability constraints | yes | Plan safe change |

## Capability contract
Review SQL and propose DDL by default. Execute migrations, extensions, routines, or data changes only with authorised scope and rollback.

## Degraded mode
If EXPLAIN ANALYZE or statistics are unavailable, provide read-only hypotheses and validation SQL; do not claim measured improvement.

## Decision rules
| Condition | Action |
|---|---|
| Planner estimate is materially wrong | Refresh or improve statistics |
| Index build may block writes | Use a compatible concurrent path |
| Constraint encodes business truth | Enforce it in the database |

## Domain Anti-Patterns
- Running EXPLAIN ANALYZE on unsafe writes. Fix: use a rollback-safe test.
- Adding extensions without trust review. Fix: verify source and privileges.
- Indexing without workload evidence. Fix: compare read and write cost.
- Hiding null semantics in application code. Fix: define them in schema.
- Combining expand and contract in one release. Fix: stage compatibility.
