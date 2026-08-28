---
name: electronic-fiscal-taxing
description: Use when implementing or reviewing electronic fiscal taxation integrations in web, ERP, POS, or mobile-backed systems; covers jurisdiction adapters, tenant-scoped tax identities, API security, queues, offline operation, fiscal evidence, and Uganda EFRIS as the detailed reference.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Electronic Fiscal Taxing

This engineering skill builds the software boundary between a commercial system
and an electronic fiscal authority. It supports one-client deployments and
multi-tenant systems without mixing tax identities, credentials, devices,
catalogues, queues, or evidence. It is general by design; Uganda EFRIS is the
detailed reference implementation.

<!-- dual-compat-start -->
## Prerequisites

Load `system-architecture-design`, `api-design-first`,
`database-design-engineering`, `distributed-systems-patterns`,
`reliability-engineering`, `observability-monitoring`, and
`vibe-security-skill` as applicable. For accounting, tax, or statutory output,
also load the external `chwezi-accounting-doctrine` electronic fiscal taxing
skill and the finance quality gate.

## Use When

- An ERP, POS, billing, e-commerce, or mobile-backed system must fiscalise
  invoices, receipts, credit notes, debit notes, or cancellations.
- A provider requires signed/encrypted requests, device registration, rotating
  keys, acknowledgements, or authority-specific dictionaries.
- A system must support multiple tenants, each with a distinct TIN/tax ID,
  fiscal profile, branch/device mapping, and credentials.
- A remote fiscal service needs an outbox, idempotent retries, dead-letter,
  replay, reconciliation, or controlled offline mode.
- A mobile client needs fiscal status and receipt artefacts without direct
  access to authority credentials.

## Do Not Use When

Do not use for tax-law interpretation without the accounting doctrine and
current source register, for generic payment integrations, or for visual
receipt/UI styling without the design engine. Do not call a third-party fiscal
API directly from an untrusted browser or mobile client.

## Inputs

| Artifact | Required | Produced by |
|---|---:|---|
| Context map and critical flows | yes | system architecture |
| Source system schema and writers | yes | database/POS audit |
| Jurisdiction technical pack and source register | yes | authority/onboarding owner |
| Tenant and identity model | yes for SaaS | SaaS/security architecture |
| API consumers and latency/failure budget | yes | product/operations |
| Accounting/tax mapping | yes where financial | accounting doctrine/controller |

If the technical pack or credentials are absent, build contracts and test
fixtures only; block production activation and mark the gap explicitly.

## Outputs

- jurisdiction-neutral fiscal port and adapter contract;
- tenant/client fiscal-profile and isolation map;
- versioned API/OpenAPI and error/idempotency contract;
- schema and expand-contract migration plan;
- canonical fiscal-document builder and validation rules;
- outbox/queue/retry/dead-letter/replay/reconciliation design;
- security, secrets, audit, observability, runbook, rollback, and UAT pack;
- client/mobile read model that exposes status and authority artefacts safely.

Acceptance requires executable or recorded contract evidence, negative tenant
tests, duplicate/replay tests, redacted evidence, rollback instructions, and an
explicit release state.

## Non-negotiables

1. The authenticated session or service context determines tenant scope; never
   accept `tenant_id`, TIN, or fiscal profile from a request body/query as the
   authority for routing.
2. A single-client deployment may use an implicit profile, but the same profile
   interface must exist so it can be isolated later.
3. Every fiscal side effect has a stable tenant-scoped idempotency key. A
   timeout is an unknown result; reconcile before retrying.
4. Store raw authority responses only under explicit retention and redaction
   rules. Never log private keys, tokens, passwords, or symmetric keys.
5. Provider FDN/verification/QR artefacts are persisted atomically with the
   fiscal result and are never fabricated by a fake client in production.
6. Online, authority-approved offline, manual exception, rejected, and
   disabled states are distinct. Offline is bounded by current authority rules.
7. A queue is at-least-once unless the provider proves otherwise. Workers must
   be concurrency-safe, bounded, observable, replayable, and quarantine poison
   messages.
8. A mobile app consumes ERP fiscal projections; it does not contain URA
   credentials/private keys or become a second fiscalisation writer.

## Decision Rules

| Situation | Choose | Failure avoided |
|---|---|---|
| One legal entity, one deployment | One profile behind the common interface | Hard-coded identity that cannot evolve |
| Shared SaaS schema | Tenant-scoped rows, composite uniqueness/indexes, trusted context | Cross-tenant submission |
| Strong tenant boundary required | Schema/database isolation with profile resolver | Credential/data contamination |
| Immediate fiscal response required | Synchronous adapter within bounded timeout, then durable unknown state | False success or duplicate retry |
| Bursty/slow provider | Transactional outbox and worker | Lost side effects and blocked checkout |
| Offline permitted by authority | Isolated local/enabler store with deadline and upload audit | Unlimited unfiscalised backlog |
| Technical contract not current | Contract tests and blocked adapter activation | Production protocol drift |

## Core Workflow

1. **Inventory writers and ownership.** Find every invoice, receipt, payment,
   stock, correction, print, queue, and mobile sync path; select one canonical
   fiscalisation hook.
2. **Define the domain port.** Use provider-neutral commands/results for
   fiscalise, query, correct, cancel, sync catalogue, and reconcile. Preserve
   provider codes and payload hashes alongside normalized states.
3. **Prove identity isolation.** Resolve tenant/profile from trusted auth,
   validate branch/device/product ownership, and test wrong-tenant requests as
   indistinguishable not-found outcomes.
4. **Design contract first.** Specify request/response schemas, auth, version,
   time, idempotency, rate limits, errors, telemetry, and consumer projections.
5. **Build durable state.** Add additive schema changes, unique keys, immutable
   evidence, outbox claims, retry policy, dead-letter, replay authorization,
   and retention.
6. **Implement adapter.** Keep EFRIS cryptography, envelope, dictionary IDs,
   endpoint, and response parsing inside the Uganda adapter; do not leak them
   through domain or mobile APIs.
7. **Integrate commercial paths.** Route POS, manual, order, and agent sales
   through the canonical service; preserve accounting/stock transaction truth.
8. **Verify and release.** Run unit, contract, integration, failure, isolation,
   offline, load, security, migration, UAT, and rollback checks. Activate only
   after current source-register and authority onboarding gates pass.
9. **Kaizen.** Record the baseline, smallest experiment, evidence, standardised
   learning, owner, rollback, and next re-measurement in the engine.

## Anti-Patterns

- Direct URA calls from Android or browser code. Fix: ERP gateway and safe
  read-only projection.
- Client-supplied tenant/TIN routing. Fix: derive profile from verified context.
- One global AES/key cache or offline store. Fix: tenant/profile-scoped key and
  device lifecycle with explicit isolation tests.
- New idempotency key after timeout. Fix: reconcile and reuse the original key.
- `FakeEfrisClient` in production wiring. Fix: fail closed unless a configured,
  authorized adapter is selected.
- Storing only normalized status. Fix: retain redacted provider code/message,
  hashes, version, and attempt evidence.
- Retrying validation or authorization failures. Fix: classify deterministic,
  transient, unknown, and manual-review outcomes.
- Adding `tenant_id` to a table without backfill/index/rollback evidence. Fix:
  use expand-contract and prove zero unowned rows before enforcement.

## Read Next

- `chwezi-accounting-doctrine` electronic fiscal taxing for tax and ledger rules
- `api-design-first`, `database-design-engineering`,
  `distributed-systems-patterns`, and `reliability-engineering`
- `multi-tenant-saas-architecture`, `saas-erp-system-design`, and
  `pos-sales-operations-engineering`
- `android-development`, `android-data-persistence`, and `android-tdd` for
  downstream mobile projections

## References

- [Architecture and tenant isolation](references/architecture-and-tenant-isolation.md)
- [Adapter, API, and queue contract](references/adapter-api-and-queue-contract.md)
- [Uganda EFRIS source register](references/jurisdictions/uganda-efris/source-register.md)
- [Uganda EFRIS interface catalogue](references/jurisdictions/uganda-efris/interface-catalogue.md)
- [Uganda offline and device deployment](references/jurisdictions/uganda-efris/offline-device-deployment.md)
- [Testing, observability, and release](references/testing-observability-and-release.md)
- [ERP mapping example](examples/erp-efris-mapping-example.md)

<!-- dual-compat-end -->
