---
name: mysql-engineering
description: Use when designing, implementing, or reviewing MySQL application schemas, SQL, indexes, constraints, stored routines, and production query patterns. Load absorbed MySQL best-practice, data-modeling, and advanced-SQL reference files as needed.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# MySQL Engineering
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

Use this parent skill as the active MySQL engineering entrypoint. It keeps routing narrow while preserving the older MySQL child skills as reference modules.

<!-- dual-compat-start -->
## Use When

- Designing MySQL-backed features, schemas, migrations, indexes, keys, and query paths.
- Reviewing MySQL SQL correctness, transaction behaviour, locking assumptions, or data modelling choices.
- Implementing stored routines, generated columns, JSON usage, or application data-access conventions.

## Do Not Use When

- The task is unrelated to this parent skill or is better handled by a narrower active parent named in the workflow.
- The request only needs a trivial answer and no reference module needs to be loaded.

## Required Inputs

- Gather the concrete system, repository, environment, constraints, and deliverable before loading references.
- Identify which absorbed reference file is needed; do not load every migrated reference by default.
## Workflow

1. Start with `database-design-engineering` for model, integrity, tenancy, migration, and access-pattern framing.
2. Load only the needed reference:
   - `references/mysql-best-practices.md` for MySQL defaults, constraints, engine choices, and safe conventions.
   - `references/mysql-data-modeling.md` for schema and relationship design.
   - `references/mysql-advanced-sql.md` for advanced query and SQL patterns.
3. Pair with `mysql-operations` for administration, performance, backup, restore, or incident work.

## Quality Standards

- Make storage engine, character set, collation, key, and transaction assumptions explicit.
- Prefer integrity in schema constraints and transactional boundaries before application-only enforcement.
- Include migration safety notes for locks, long-running changes, rollback, and data verification.

## Anti-Patterns

- Treating absorbed reference files as active skills or separate routing entrypoints.
- Loading every migrated child reference instead of the one that matches the task.
- Producing generic advice without constraints, evidence, or next verification steps.
## Outputs

- MySQL schema, SQL, migration, or review output with loaded references and validation evidence.

## References

- Load only the references/<old-skill>.md files named in the workflow when their depth is required.
<!-- dual-compat-end -->

## Inputs
| Input | Required | Purpose |
|---|---|---|
| MySQL version and schema | yes | Select valid features |
| Query shapes and cardinalities | yes | Design indexes |
| Migration and availability constraints | yes | Plan safe change |

## Capability contract
Review SQL and propose DDL by default. Execute migrations, routines, or data changes only with authorised credentials, environment scope, backup evidence, and rollback.

## Degraded mode
If EXPLAIN plans or production statistics are unavailable, provide read-only hypotheses and validation SQL; do not claim a query is tuned.

## Decision rules
| Condition | Action |
|---|---|
| Scan is selective and frequent | Evaluate a covering index |
| DDL may lock a hot table | Use an online or staged migration |
| Constraint encodes business truth | Enforce it in the database |

## Domain Anti-Patterns
- Using SELECT star in stable contracts. Fix: name columns.
- Building SQL by interpolation. Fix: bind parameters.
- Adding indexes without write-cost review. Fix: measure both paths.
- Using zero dates as missing values. Fix: use nullable semantics.
- Changing a hot table without lock analysis. Fix: test the DDL plan.
