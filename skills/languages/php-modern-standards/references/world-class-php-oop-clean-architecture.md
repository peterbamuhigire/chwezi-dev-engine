# World-Class PHP OOP And Clean Architecture

Use this reference when PHP work needs to remain maintainable for years, survive framework changes, and support safe testing and refactoring.

## Core Direction

- Treat frameworks as delivery mechanisms, not the home of business rules.
- Domain entities, value objects, policies, and use cases should not depend on controllers, HTTP, ORM models, sessions, or views.
- Controllers should coordinate request parsing, authorization handoff, use-case invocation, and response shaping. They should not contain business rules or SQL.
- Dependency direction should point inward: infrastructure depends on application/domain contracts, not the reverse.
- Code that cannot be tested in isolation is usually too coupled.

## PHP 8 OOP Rules

- Use `declare(strict_types=1)` and typed properties/parameters/returns.
- Prefer constructor injection with interfaces for collaborators.
- Use `readonly` value objects where mutation is not part of the model.
- Use union types sparingly; if the type set keeps growing, introduce a value object or interface.
- Use attributes only for metadata that belongs near code; do not turn attributes into hidden business logic.
- Use `match` for exhaustive value selection where it improves clarity.
- Use exceptions for exceptional control flow, not ordinary validation outcomes.

## Domain Model

- Use domain language, not database column names, as the primary model vocabulary.
- Keep invariants inside entities/value objects or use cases, not scattered across controllers and forms.
- Prefer composition over inheritance for domain behavior unless the inheritance relationship is stable and meaningful.
- Traits are acceptable for small technical reuse, but not for hiding domain behavior across unrelated classes.
- Keep factories for object creation that has invariants, defaulting, or dependency-sensitive construction.

## Clean Architecture Layers

| Layer | Owns | Must not know |
|---|---|---|
| Domain | Entities, value objects, domain services, invariants | HTTP, database, framework, UI |
| Application | Use cases, ports/interfaces, transactions, orchestration | Concrete ORM, request globals, views |
| Infrastructure | Repositories, gateways, mailers, queues, files, external APIs | Controller details |
| Interface | Controllers, presenters, serializers, CLI commands | Persistence mechanics |

## Repository And Adapter Rules

- Repositories hide data source mechanics behind interfaces.
- One repository should primarily manage one aggregate/entity family.
- Controllers and use cases should depend on repository interfaces, not concrete ORM/query classes.
- Adapters translate third-party APIs, framework services, or libraries into project-owned interfaces.
- Persistence mapping should not leak into domain entities if the project needs long-term framework/ORM portability.

## Testing Strategy

- Unit-test domain and application layers without a database or framework bootstrap.
- Use mocks/fakes only at ports you do not own or infrastructure boundaries.
- Add integration tests for repositories, controllers, framework wiring, and migrations.
- Seed test data with realistic but non-production records.
- If a controller has too many dependencies to test, split the workflow or introduce a use case/application service.

## Review Checklist

- [ ] Business rules are outside controllers/views.
- [ ] Domain/application code has no framework imports.
- [ ] Dependencies are injected, not instantiated inline.
- [ ] Interfaces exist where implementation swapping or isolated testing matters.
- [ ] Use cases expose business actions in domain language.
- [ ] Repository methods express business access patterns, not arbitrary table operations.
- [ ] Unit tests cover domain/application behavior.
- [ ] Integration tests cover framework, persistence, and HTTP wiring.
