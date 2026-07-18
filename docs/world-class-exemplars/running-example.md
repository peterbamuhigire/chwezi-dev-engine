# Running Example: FieldOps Ledger

Last verified: 2026-07-08

FieldOps Ledger is the shared running example for the July 2026 upgrade. It is a fictional but concrete Chwezi Core Systems SaaS used to connect the engine's architecture, API, data, security, reliability, deployment, and evidence-pack guidance.

## Domain

FieldOps Ledger serves maintenance contractors that dispatch field teams, buy spare parts, invoice clients, and reconcile mobile-money collections. It is deliberately chosen because it crosses the engine's major skill families:

| Concern | Example detail | Skill families exercised |
|---|---|---|
| Multi-tenancy | Each contractor is a tenant with strict data isolation | SaaS, database, security |
| API design | Work orders, visits, invoices, attachments, exports, and idempotent payment callbacks | API, architecture |
| Data systems | PostgreSQL OLTP, event outbox, audit log, analytics replica | Database, distributed systems |
| Identity | SSO for larger contractors, RBAC for dispatchers, technicians, accountants, and client approvers | Security, SaaS |
| Reliability | 99.9% monthly availability SLO for dispatch and invoicing flows | DevOps, SRE, observability |
| Mobile/offline | Technicians capture photos and job notes with intermittent connectivity | Mobile, PWA |
| Finance handoff | VAT, payroll, and statutory accounting route to `chwezi-accounting-doctrine` | Cross-engine finance |

## Vocabulary

| Term | Meaning in the example |
|---|---|
| Tenant | A contractor company using the SaaS |
| Work order | Client-authorised job request |
| Visit | Technician execution record against a work order |
| Evidence object | Photo, signature, GPS point, note, or meter reading attached to a visit |
| Posting boundary | Point where operational events become accounting events in the finance engine |
| Error budget | Allowed unreliability for the dispatch and invoicing user journeys during the SLO window |

## Thread Across Artifacts

The example appears in:

- `examples/full-stack-saas-reference/README.md`
- `examples/full-stack-saas-reference/architecture.md`
- `examples/full-stack-saas-reference/api-contract.md`
- `examples/full-stack-saas-reference/security-threat-model.md`
- `examples/full-stack-saas-reference/reliability-and-release.md`
- `templates/delivery-dod/evidence-pack.md`

## Anti-Patterns This Example Prevents

- Architecture advice without a domain transaction.
- API examples that ignore idempotency, pagination, versioning, and export operations.
- Security guidance that stops at passwords and ignores machine identities, service accounts, and CI/CD secrets.
- Reliability guidance that names SLOs but never ties them to release decisions.
- Finance-sensitive examples that hardcode statutory values inside engineering skill logic.
