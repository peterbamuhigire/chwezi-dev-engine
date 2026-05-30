# ASP.NET Core And Services

Self-contained reference prepared from supplied .NET cloud/web books and current Microsoft documentation. Use for APIs, web apps, workers, SignalR, Blazor, Azure Functions, and service hosting.

## Table Of Contents

- Service shape decision
- API architecture
- Minimal APIs vs controllers
- Middleware and filters
- Authentication and authorization
- Configuration and secrets
- Background services and queues
- Azure and cloud integration
- Blazor and SignalR

## Service Shape Decision

| Need | Fit | Notes |
|---|---|---|
| Small internal HTTP API | Minimal APIs | Keep handlers thin; extract use cases into services. |
| Public versioned API | Controllers or endpoint groups | Stronger conventions for filters, versioning, and documentation. |
| Long-running background work | Worker Service | Supervise queues, retries, cancellation, and health. |
| Event-driven serverless | Azure Functions | Good for integration glue; avoid burying domain workflows in function bodies. |
| Real-time bidirectional UI | SignalR | Design reconnect, backpressure, authorization, and message versioning. |
| Interactive web UI | Blazor/ASP.NET Core | Choose server, WASM, or hybrid based on latency, offline, and deployment constraints. |

## API Architecture

Keep transport code thin:

```text
Api endpoint/controller
  -> application use case
  -> domain model/policy
  -> infrastructure adapter (EF, queue, HTTP, storage)
```

Do not put business rules in route handlers, filters, middleware, EF interceptors, or model binders. Use endpoint filters for cross-cutting HTTP concerns only: validation, authorization checks, idempotency lookup, and response mapping.

## Minimal APIs Vs Controllers

Use minimal APIs for concise, cohesive endpoint groups:

```csharp
var group = app.MapGroup("/orders").RequireAuthorization();

group.MapPost("/", async (
    CreateOrderRequest request,
    CreateOrderHandler handler,
    CancellationToken cancellationToken) =>
{
    var result = await handler.HandleAsync(request, cancellationToken);
    return result.ToHttpResult();
});
```

Use controllers when the app needs mature conventions: complex model binding, filters, API versioning, generated clients, or teams already organised around MVC patterns.

## Middleware And Filters

Middleware is for request-pipeline concerns: exception handling, correlation IDs, forwarded headers, authentication, CORS, rate limiting, compression, static files, routing, authorization, and endpoints. Keep ordering deliberate and documented.

Endpoint filters are for endpoint-local policies. Do not hide database writes or business workflows in filters.

## Authentication And Authorization

- Prefer platform auth libraries over custom token/session systems.
- Enforce authorization by policy, resource, tenant, and action. Authentication alone is not enough.
- Validate JWT issuer, audience, lifetime, signing keys, and clock skew.
- Lock down CORS to known origins. Never use permissive CORS with credentials.
- For cookies, use secure, HTTP-only, same-site settings and anti-forgery where browser form posts exist.
- Log authorization denials without leaking sensitive attributes.

## Configuration And Secrets

- Use strongly typed options with validation at startup.
- Keep local secrets in user-secrets or environment variables; production secrets in a managed store such as Azure Key Vault.
- Fail fast on missing required configuration unless degraded mode is explicitly designed.
- Never bind arbitrary config into public response DTOs.

## Background Services And Queues

Use `BackgroundService` for supervised loops:

- Await delays with cancellation tokens.
- Bound queues with `Channel<T>` or a broker; avoid unbounded in-memory growth.
- Make jobs idempotent and retry-safe.
- Emit metrics for queue length, processing latency, success/failure, and dead letters.
- Add shutdown drain rules and document what happens to in-flight work.

## Azure And Cloud Integration

- Azure Functions are best for event handlers, scheduled jobs, integration endpoints, and scale-to-zero workloads. Keep function entrypoints thin.
- Service Bus suits durable commands/events; design duplicate delivery handling.
- Blob Storage suits large immutable objects; store metadata in a database when querying is needed.
- Cosmos DB suits document workloads with known partition keys; do not use it as a relational substitute.
- Key Vault stores secrets/keys/certificates; cache responsibly and rotate.

## Blazor And SignalR

- Blazor Server: low client payload and full .NET server execution, but sensitive to latency and connection state.
- Blazor WebAssembly: offline/client execution potential, but larger payload and exposed client code.
- SignalR: version messages, authorize hub methods, handle reconnect, and avoid broadcasting sensitive data without tenant/user scoping.

## API Done Checklist

- OpenAPI describes stable public contracts.
- Validation errors are machine-readable and user-safe.
- Authn/authz policies are tested.
- Every outbound dependency has timeout, retry/circuit policy where appropriate, and telemetry.
- Health checks distinguish startup readiness, liveness, and dependency health.
- Logs use structured templates and correlation IDs.
