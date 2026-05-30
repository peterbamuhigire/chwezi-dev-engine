# EF Core Data Access

Self-contained reference prepared from supplied C#/.NET books and current EF Core documentation. Use for modelling, migrations, queries, transactions, and performance reviews.

## Table Of Contents

- Modelling boundaries
- DbContext lifetime
- Query rules
- Migrations and schema change
- Transactions and concurrency
- EF Core 10 notes
- Anti-patterns

## Modelling Boundaries

EF Core is an infrastructure tool, not the domain model boundary. For small CRUD apps, entities can be close to tables. For business systems, keep domain invariants in domain/application layers and map persistence deliberately.

| Pattern | Use when | Watch for |
|---|---|---|
| Entity as persistence model | Simple CRUD/admin apps | Leaking schema shape into public API |
| Separate domain and EF models | Rich domain rules, long-lived systems | Mapping overhead |
| CQRS read projections | High-read APIs or reporting | Projection staleness and rebuild plan |
| Raw SQL/Dapper beside EF | Hot queries or SQL-specific features | Contract drift and test coverage |

## DbContext Lifetime

- Use scoped `DbContext` per request/unit of work in web apps.
- Use `IDbContextFactory<T>` in background services, Blazor, parallel workflows, and long-lived components.
- Never share a `DbContext` across threads.
- Keep transactions short and explicit.
- Do not inject `DbContext` into singleton services.

## Query Rules

- Project DTOs directly with `Select`; do not load full graphs when the response needs a small shape.
- Use `AsNoTracking` for read-only queries.
- Include only the navigation data needed for a use case.
- Use split queries for multiple collection includes when cartesian explosion appears.
- Page every collection endpoint with stable ordering.
- Inspect generated SQL for complex LINQ; add tests for provider-specific translation.
- Index foreign keys, filters, sort columns, uniqueness constraints, and high-cardinality lookup paths.

## Migrations And Schema Change

- Keep migrations reviewable; avoid dumping unrelated model churn into one migration.
- Use expand-contract for live systems: add nullable/new columns, backfill, dual-read/write if needed, switch, then remove old shape.
- Never rely on automatic production migrations unless the deployment system and rollback model are designed for it.
- Seed reference data deterministically; do not hide business onboarding data in migrations.
- For destructive changes, include backup, rollback, and data validation evidence.

## Transactions And Concurrency

- Use optimistic concurrency tokens for user-editable records.
- Use idempotency keys for externally retried commands such as payments, webhooks, and queue messages.
- Keep isolation level explicit for financial or inventory workflows.
- Use outbox/inbox patterns when database changes and message publication must be coordinated.
- Prefer database constraints for invariants the database can enforce: uniqueness, foreign keys, required values, and check constraints.

## EF Core 10 Notes

When the project targets .NET 10/EF Core 10:

- EF Core 10 requires .NET 10; do not apply it to earlier runtime targets.
- Named query filters can make multi-tenant and soft-delete filters easier to compose and selectively disable.
- SQL Server/Azure SQL support for JSON and vector search can help document/embedding workloads, but model storage, indexing, and query cost explicitly.
- Parameterized collection translation changed; test hot `Contains` queries on production-like data.
- Date/time provider behaviour and SQLite changes can affect tests and migrations; verify provider-specific behaviour.

## Anti-Patterns

- Lazy loading on web request paths.
- Returning tracked EF entities from API endpoints.
- `ToList()` before filtering, sorting, or paging.
- Repository wrappers that only mirror `DbSet<T>` and hide useful EF features.
- Swallowing `DbUpdateConcurrencyException` or retrying writes without idempotency.
- Huge aggregate roots loaded for every operation.
- Provider-agnostic assumptions in queries that use provider-specific functions.

## Data Access Done Checklist

- Schema has indexes and constraints aligned to access patterns.
- Critical queries are projected, paged, and measured.
- Migrations have deploy and rollback notes.
- Concurrency conflicts have user/operator handling.
- Tests cover provider translation, not only in-memory behaviour.
