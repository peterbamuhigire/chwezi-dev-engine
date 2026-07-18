# FieldOps Ledger Architecture Exemplar

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 architecture exemplar
Benchmark: Thoughtworks evolutionary architecture and Sam Newman microservice boundary discipline.

## Scope

This architecture covers the first production release of FieldOps Ledger: tenant onboarding, work-order dispatch, technician visit capture, invoicing handoff, client approval, and audit evidence export. It does not implement statutory accounting rules; those route to `chwezi-accounting-doctrine`.

## Boundary Decision

| Capability | Boundary | Data owner | Why it is separate |
|---|---|---|---|
| Tenant control plane | `tenant-service` | Tenant, plan, region, data-retention policy | It gates every other service and changes under enterprise onboarding pressure |
| Work execution | `work-order-service` | Work order, visit, evidence object | It owns the core operational transaction and offline conflict rules |
| Billing handoff | `billing-adapter` | Invoice draft, posting event, export status | It isolates finance integration from field operations |
| Identity and access | `identity-policy-service` | Role assignment, SSO config, service account policy | It centralizes authorization decisions and auditability |
| Evidence export | `export-service` | Export job, package manifest, signed URL | Long-running export behavior should not block work-order writes |

The first release keeps these as independently deployable modules in one repository until traffic and team ownership justify independent repositories. This avoids premature decomposition while preserving clean contracts.

## Data Model

| Entity | Key fields | Consistency rule |
|---|---|---|
| `Tenant` | `tenant_id`, `plan_id`, `region`, `retention_policy` | Strong consistency on creation and suspension |
| `WorkOrder` | `work_order_id`, `tenant_id`, `client_id`, `status`, `version` | Optimistic concurrency on status transitions |
| `Visit` | `visit_id`, `work_order_id`, `technician_id`, `started_at`, `completed_at` | Offline clients may create drafts; server resolves by version |
| `EvidenceObject` | `evidence_id`, `visit_id`, `type`, `hash`, `storage_uri` | Immutable after upload; corrections create new evidence |
| `PostingEvent` | `event_id`, `source_id`, `event_type`, `idempotency_key` | Outbox guarantees at-least-once delivery; receiver deduplicates |

## Integration Contracts

- Public API: resource-oriented JSON over HTTPS with OpenAPI contract.
- Internal events: outbox table with idempotent consumers.
- Export: asynchronous job resource with progress, cancellation, expiry, and manifest hash.
- Finance: `PostingEvent` only. The finance engine decides ledger treatment.
- Mobile sync: client sends versioned mutations; server returns accepted, rejected, and conflict records.

## Failure Modes

| Failure | Expected behavior | Evidence required |
|---|---|---|
| Mobile duplicate visit submission | Server deduplicates by idempotency key and evidence hash | Contract test and log trace |
| Replication lag on analytics replica | Operational reads never use the lagged replica | Query routing test |
| Export job interrupted | Job becomes retryable or failed with partial artifacts discarded | Background job test |
| Tenant suspended during active visit | New writes denied; existing offline drafts enter review queue | Authorization integration test |
| Finance adapter unavailable | Work completion remains accepted; posting event remains pending | Outbox replay test |

## What Not To Do

- Do not create one service per database table.
- Do not share the transactional database with analytics consumers.
- Do not let mobile clients decide final status transitions without server validation.
- Do not call the finance engine synchronously inside work-order completion.
- Do not treat "microservices" as the goal; the goal is controlled change, clear ownership, and operability.

## QA Checklist

- [ ] Every boundary maps to a business capability.
- [ ] Every cross-boundary call has a contract artifact.
- [ ] Data ownership is singular for every mutable entity.
- [ ] Offline conflicts have a deterministic server rule.
- [ ] Long-running operations expose status, cancellation, and retry behavior.
- [ ] Finance-sensitive logic routes to the finance doctrine engine.

See also: `api-contract.md`, `security-threat-model.md`, `reliability-and-release.md`.
