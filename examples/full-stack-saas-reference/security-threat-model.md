# FieldOps Ledger Security Threat Model Exemplar

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 security exemplar
Benchmark: OWASP application security review plus identity-security and database-security evidence expected in enterprise SaaS procurement.

## Scope

This model covers tenant isolation, user identity, machine identity, secrets, database access, CI/CD supply chain, file evidence, and abuse of work-order APIs.

## Assets

| Asset | Protection goal |
|---|---|
| Tenant operational records | Confidentiality, integrity, tenant isolation |
| Evidence photos and signatures | Integrity, provenance, retention control |
| Posting events | Integrity, non-duplication, auditability |
| Service credentials | Least privilege, rotation, non-disclosure |
| Admin actions | Accountability and replayable audit trail |

## Roles

| Role | Allowed actions | Explicit denial |
|---|---|---|
| Tenant owner | Manage tenant users, billing settings, exports | Cross-tenant access |
| Dispatcher | Create and schedule work orders | Change finance posting policy |
| Technician | Update assigned visits and upload evidence | View all tenant financial data |
| Accountant | Review posting events and exports | Modify evidence objects |
| Chwezi support engineer | Time-bound support access with ticket reference | Standing tenant data access |

## Threats and Controls

| Threat | Control | Evidence |
|---|---|---|
| Cross-tenant IDOR | Tenant ID is derived from authenticated context; route tenant parameter is checked against policy | Authorization integration tests |
| Stolen technician token | Short-lived access token, refresh-token rotation, device revoke | Token lifecycle test |
| Service-account overreach | Workload identity per service, no shared CI secret with production write scope | IAM policy diff |
| SQL injection | Parameterized queries and ORM-safe query builder; raw SQL review gate | Static scan and code review |
| Evidence tampering | Content hash, immutable evidence metadata, signed upload URLs, audit log | Hash verification test |
| Duplicate posting event | Idempotency key and event outbox uniqueness constraint | Database constraint test |
| Secret leak in CI | Secret scanner, protected environments, no plaintext secrets in logs | CI security job result |
| Backup restore failure | Encrypted backup and quarterly restore drill | Restore drill log |

## Ambiguity Handling

If the user has not specified identity provider, compliance target, or tenant-isolation model, default to a conservative baseline: OIDC-ready authentication, RBAC with explicit denies, tenant-scoped database predicates, service-specific workload identities, and audit logs for all admin actions. Ask only if the choice affects legal compliance, pricing, or irreversible architecture.

## Common Mistakes

- Treating RBAC as UI visibility instead of server-side authorization.
- Reusing one service account across CI, background jobs, and runtime services.
- Storing evidence files without hashes or retention policy.
- Logging JWTs, refresh tokens, or signed URLs.
- Allowing support access without ticket ID, time limit, and audit trail.

## QA Checklist

- [ ] Every role has positive permissions and explicit denials.
- [ ] Every tenant-scoped query has a tenant-isolation test.
- [ ] Every machine identity has a named owner and least-privilege policy.
- [ ] Every secret has storage location, rotation owner, and exposure response.
- [ ] Every file upload has type, size, malware, hash, and retention controls.
- [ ] Every backup has restore evidence, not only backup-success logs.

See also: `architecture.md`, `api-contract.md`, `reliability-and-release.md`.
