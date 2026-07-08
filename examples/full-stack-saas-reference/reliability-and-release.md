# FieldOps Ledger Reliability and Release Exemplar

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 reliability exemplar
Benchmark: Google SRE SLO/error-budget discipline and production release evidence expected by mature SaaS teams.

## Critical User Journeys

| Journey | SLO | Measurement |
|---|---:|---|
| Dispatcher creates work order | 99.9% monthly successful requests under 700 ms p95 | API success rate and latency by tenant |
| Technician completes visit | 99.9% monthly accepted submissions under 1.5 s p95 when online | Mobile sync endpoint success and latency |
| Accountant exports posting evidence | 99.5% monthly export jobs complete within 10 minutes | Export job state transitions |

## Error Budget Policy

If a journey consumes more than 50% of its monthly error budget before mid-month, freeze non-critical releases for that journey and spend engineering time on reliability work. If it consumes 100%, block new feature releases until the owning team completes mitigation and a reviewer accepts the release-risk note.

## Observability

| Signal | Required dimension |
|---|---|
| Request rate | tenant, route, status, version |
| Error rate | tenant, route, error code, retryable |
| Latency | route, region, p50/p95/p99 |
| Outbox lag | event type, oldest pending age |
| Export duration | job type, tenant plan, artifact size |
| Auth failures | role, reason, identity provider |

## Release Plan

1. Run schema migration in expand-only mode.
2. Deploy API with old and new response fields.
3. Enable feature flag for internal tenant.
4. Canary 5% of tenants with rollback threshold of 1% absolute error-rate increase or p95 latency above SLO for 15 minutes.
5. Promote to all tenants only if dashboards, logs, traces, and support queue are clean.
6. Remove old fields only after compatibility window and client inventory sign-off.

## Rollback Plan

| Change type | Rollback |
|---|---|
| API behavior | Disable feature flag and route to previous handler |
| Schema expand | Leave additive column in place; do not contract during incident |
| Background job | Pause queue, drain safe retries, replay from outbox |
| Export format | Revert export template version and retain manifest compatibility |

## Incident Evidence

Every production incident records:

- start and detection time;
- affected tenants and journeys;
- user-visible impact;
- error-budget burn;
- mitigation action;
- rollback or forward-fix decision;
- follow-up owner and due date.

## QA Checklist

- [ ] Every critical journey has SLO, query, dashboard, and alert.
- [ ] Every release has rollback threshold and rollback owner.
- [ ] Every database change is expand/contract or explicitly irreversible with sign-off.
- [ ] Every outbox event can be replayed without duplicate side effects.
- [ ] Every alert names action, severity, and runbook.
- [ ] Every incident review produces a prevention action or explains why none is justified.

See also: `architecture.md`, `api-contract.md`, `security-threat-model.md`.
