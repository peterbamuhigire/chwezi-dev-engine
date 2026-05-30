# Testing, Packaging, And Operations

Self-contained reference prepared from supplied C#/.NET books and current Microsoft documentation. Use to close implementation work with verification, packaging, and operability evidence.

## Table Of Contents

- Test strategy
- Tooling baseline
- Integration and contract tests
- Packaging and deployment
- Observability
- Release readiness

## Test Strategy

| Layer | Proves | Typical tools |
|---|---|---|
| Unit tests | Domain rules, value objects, pure services | xUnit/NUnit/MSTest, FluentAssertions |
| Component tests | Application use cases with fake adapters | Test doubles, in-memory clocks, fake queues |
| Integration tests | EF provider, HTTP pipeline, auth, serialization | `WebApplicationFactory`, Testcontainers, real provider |
| Contract tests | Public API request/response compatibility | OpenAPI snapshots, approval tests |
| UI tests | Critical user flows | MAUI platform tests, Playwright for web |
| Load/smoke tests | Startup, health, latency, dependency behaviour | k6, NBomber, curl scripts, cloud probes |

Do not rely on EF in-memory provider for relational behaviour. Use SQLite only when it matches the target behaviour closely enough; otherwise use the real database in containers or a test instance.

## Tooling Baseline

- `dotnet restore`
- `dotnet build --no-restore`
- `dotnet test --no-build`
- `dotnet format --verify-no-changes`
- analyzers enabled in build
- dependency vulnerability scan where CI supports it
- code coverage for critical domain/application paths

Microsoft.Testing.Platform support in newer SDKs can improve test execution. Adopt it only after the team confirms framework and CI compatibility.

## Integration And Contract Tests

- Test HTTP status codes, content types, validation payloads, auth failures, and idempotency.
- Test migrations against a real provider before production.
- Use stable test data builders, not large fixture dumps.
- Reset database state deterministically.
- For queues/webhooks, test duplicate delivery, out-of-order delivery, and poison messages.
- For AI features, snapshot safety-critical structured outputs and evaluate refusal/error paths.

## Packaging And Deployment

| Target | Checks |
|---|---|
| ASP.NET/Worker | publish profile, config binding, health endpoints, container base image, non-root user, ports |
| Library/NuGet | semantic version, XML docs, package metadata, symbols, compatibility tests |
| CLI | single-file/trimming/AOT compatibility, config path, exit codes, shell completion |
| MAUI | signing, app IDs, entitlements, store metadata, runtime identifiers |
| Azure Functions | function bindings, app settings, managed identity, cold-start tolerance |

Use trimming and NativeAOT only with explicit compatibility testing. Reflection-heavy serializers, DI scanning, dynamic proxies, and some libraries need annotations or alternatives.

## Observability

- Structured logs with event IDs and scopes.
- Correlation/trace IDs across HTTP, queues, database, and outbound calls.
- Metrics for request duration, error rate, dependency latency, queue depth, job duration, retries, and resource saturation.
- Health checks separated into liveness and readiness.
- Release markers: version, commit SHA, build ID, environment, migration version.
- Operator runbook with common failures and commands.

## Release Readiness

Before calling work done:

- Build/test/analyzer commands pass or skipped commands are justified.
- Runtime smoke test exercises the changed path.
- Config and secret requirements are documented.
- Database migrations have forward and rollback handling.
- Health, logs, and metrics can confirm deployment success.
- Rollback path is realistic for code, config, and schema.
- Ownership and escalation are clear.

## Anti-Patterns

- "Works locally" without build/test evidence.
- Only mocking EF and HTTP while never testing the real pipeline.
- No startup validation for missing configuration.
- Containers running as root by default.
- Publishing self-contained/trimming/AOT builds without executing them.
- Health checks that always return healthy regardless of dependencies.
