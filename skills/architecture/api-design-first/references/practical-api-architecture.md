# Practical API Architecture

This file is self-contained. It was prepared from local EPUB study notes and
must remain useful even if the EPUBs are deleted.

Source inputs: local EPUBs under `C:\Users\Peter\Downloads\Documents\`:
`Mastering API Architecture.epub`, `Learning Domain-Driven Design.epub`, and
`Foundations of Scalable Systems.epub`.

Use this reference when an API needs to be treated as a long-lived product
contract rather than a thin controller layer.

## API Boundary Rules

- Start from consumers and business capabilities, then define resources and
  operations. Do not expose persistence tables as the API model.
- Keep public contract models stable even when internal domain or persistence
  models change.
- Prefer explicit workflow operations over tortured CRUD when the domain action
  has business meaning: approve, cancel, settle, archive, reconcile.
- Make idempotency mandatory for commands that create money, inventory,
  provisioning, notifications, or third-party side effects.
- Version for breaking changes. Additive changes can remain in the same version
  only when old clients can safely ignore them.
- Treat pagination, filtering, sorting, partial response, and error semantics as
  first-class design, not endpoint-level afterthoughts.

## API Style Selection

| Style | Use when | Watch for |
|-------|----------|-----------|
| REST | resource lifecycle, public APIs, cacheable reads, broad tooling | CRUD bias for workflow actions |
| RPC/gRPC | internal service calls, low-latency binary exchange, strong schema | browser and partner accessibility |
| GraphQL | clients need different shapes over shared graph | query complexity, authorization, caching |
| Async events | consumers react to facts, decoupled workflows, integrations | schema evolution and replay safety |
| Webhooks | external systems need notifications | retries, signatures, idempotency, delivery logs |

Choose a style per exchange, not by fashion. A platform can use REST for public
contracts, gRPC for internal low-latency calls, and events for decoupled facts.

## Contract Design Checklist

| Area | Required decision |
|------|-------------------|
| Consumer shape | browser, mobile, internal service, partner, batch job |
| Trust boundary | user auth, service auth, tenant scoping, admin override |
| Resource model | canonical nouns, subresources, workflow commands |
| Consistency | synchronous confirmation, eventual completion, compensating action |
| Failure | retryable errors, permanent errors, conflict handling, timeout semantics |
| Evolution | versioning, deprecation notice, sunset timeline, compatibility tests |
| Observability | request ID, tenant/user IDs, audit event, SLO class, rate-limit metrics |

## REST Design Rules

- Use plural nouns for collections and stable resource identifiers.
- Use standard methods consistently: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- Do not tunnel every action through generic `/execute` endpoints.
- For domain actions, use clear command resources or action endpoints when CRUD
  would hide the business meaning.
- List endpoints must define pagination, maximum page size, sort stability, and
  filter semantics.
- Partial updates need merge/patch semantics documented precisely.
- Bulk endpoints need partial-success semantics, per-item errors, and idempotency.
- Sensitive reads should use `Cache-Control: no-store`; public stable reads can
  use cache validators.

## Versioning and Lifecycle

| Change | Compatibility | Required action |
|--------|---------------|-----------------|
| add optional response field | usually non-breaking | update contract tests and docs |
| add endpoint | non-breaking | publish capability and auth requirements |
| add enum value | potentially breaking for strict clients | document and communicate |
| rename/remove field | breaking | new major version or explicit migration |
| change required input | breaking | new major version |
| change error semantics | breaking for automation | deprecation and migration note |

Lifecycle requirements:

- publish deprecation date and sunset date
- provide migration guide for breaking changes
- keep old and new versions observable separately
- contract-test old versions until sunset
- avoid hidden changes generated from implementation code after the fact

## Error and State Semantics

- Use `409 Conflict` for state/version conflicts that the client can resolve.
- Use `422 Unprocessable Entity` for syntactically valid requests that violate
  domain validation.
- Return `404` for wrong-tenant access where revealing existence would leak data.
- Use `202 Accepted` plus an operation resource for long-running work.
- Include machine-readable error codes that remain stable across wording changes.
- Document retryability per error class; clients should not guess.

Error registry columns:

| Column | Purpose |
|--------|---------|
| code | stable machine-readable identifier |
| HTTP status | protocol-level classification |
| message | default human-readable text |
| retryable | whether automated retry is allowed |
| client action | fix input, re-authenticate, wait, contact support |
| audit event | whether security/compliance logging is required |

## Traffic Management

- Put rate limits at the correct identity: IP, user, tenant, API key, or route.
- Return limit headers and a retry time for `429`.
- Use API gateways for cross-cutting traffic controls: auth enforcement,
  routing, throttling, request size limits, WAF integration, logging, and
  gradual migration.
- Do not hide business authorization inside the gateway; keep domain decisions
  in the service or a policy engine with domain context.
- For high-traffic endpoints, define payload limits, compression policy,
  cacheability, and timeout budget.

## API Testing Pyramid

| Test type | What it proves |
|-----------|----------------|
| unit | handlers and mappers enforce local rules |
| schema/contract | implementation matches OpenAPI or schema |
| component | service works with real adapters or controlled dependencies |
| integration | service exchanges work across real boundaries |
| end-to-end | one or two critical user journeys work through the full stack |
| consumer-driven contract | provider changes do not break known consumers |

Do not rely on end-to-end tests for contract completeness. Contract tests should
run close to the API and fail quickly.

## API Architecture Risks

- Hidden chatty workflows: many small endpoints may create high-latency mobile
  or partner integrations.
- Leaky domain boundaries: one API starts returning another context's internal
  state because database joins were convenient.
- Version drift: implementation changes without contract tests tied to the
  OpenAPI document.
- Idempotency holes: network retries duplicate externally visible side effects.
- Incomplete tenant scoping: tenant IDs accepted from request bodies or query
  parameters instead of being derived from authenticated context.

## Security and Governance

- Authentication proves caller identity; authorization proves allowed action on
  this resource in this tenant and state.
- API keys must be hashed at rest and rotatable.
- JWTs need short lifetime, issuer/audience checks, key rotation, and revocation
  strategy for high-risk domains.
- CORS is a browser policy, not an authorization system.
- Webhooks require signatures, timestamps, replay windows, and delivery logs.
- PII and regulated fields should be classified in schemas and logs.
- OpenAPI documents should mark auth requirements, error responses, rate limits,
  request IDs, and examples consistently.

## Output Upgrade

When producing an API design, add these sections if absent:

- consumer contract matrix
- idempotency map
- error-code registry with retryability
- lifecycle/versioning policy
- contract-test obligations

Also include:

- rate-limit policy by consumer class
- webhook delivery/retry policy when callbacks exist
- gateway responsibilities and what stays inside the service
- schema evolution rules for events and public DTOs
