# API And Container Sidecar Engineering For Python

Use this reference when Python supports PHP-backed SaaS as a FastAPI sidecar, worker, analytics service, document generator, ML service, or integration job.

## API Contract Discipline

- Python services must consume and produce documented contracts. Do not let Pydantic models drift away from OpenAPI schemas or queue payload schemas.
- Validate every external payload with Pydantic v2 before domain logic sees it.
- Use stable machine-readable error codes at service boundaries.
- Include request/correlation IDs in logs and responses where appropriate.
- Make idempotency explicit for jobs that create documents, send messages, charge money, move inventory, call external APIs, or mutate tenant-visible state.

## Runtime Boundaries

- Keep domain logic pure and testable; adapters own HTTP, database, file, queue, and shell interactions.
- Python services should not reach into PHP internals or database tables casually. Use APIs, queues, or documented shared database contracts.
- Use repositories/gateways for external systems and keep retries/timeouts there.
- Treat long-running jobs as resumable or idempotent where possible.

## Docker Rules

- Use a deterministic lockfile and `uv sync` in builds.
- Keep build dependencies out of runtime images when possible.
- Run as non-root where feasible.
- Settings are environment-driven and validated at startup with `pydantic-settings`.
- Logs go to stdout/stderr as structured JSON in production.
- Health/readiness endpoints should prove the service can do useful work, not merely that the process exists.

## Testing

- Unit-test domain/application logic without containers.
- Contract-test HTTP and queue payloads against schemas.
- Integration-test adapters with real or controlled dependencies.
- Use realistic seed data, not production dumps.
- Include slow-network, timeout, retry, and duplicate-message/idempotency tests for worker services.

## Review Checklist

- [ ] Pydantic schemas protect every external boundary.
- [ ] Error codes and retryability are documented.
- [ ] Idempotency is defined for side-effecting operations.
- [ ] Docker build uses a lockfile and excludes secrets.
- [ ] Service logs include tenant/request/job identifiers.
- [ ] Tests cover unit, contract, and adapter integration risks.
