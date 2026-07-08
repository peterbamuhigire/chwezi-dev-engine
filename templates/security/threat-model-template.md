# Security Threat Model Template

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 security template
Benchmark: OWASP application review, identity-security practice, and database least-privilege review.

## System Scope

| Field | Value |
|---|---|
| System | `<system>` |
| Data classes | `<PII, financial, operational, credentials, etc.>` |
| Trust boundaries | `<boundary list>` |
| Review date | `<yyyy-mm-dd>` |
| Reviewer | `<name/role>` |

## Assets

| Asset | Confidentiality | Integrity | Availability | Notes |
|---|---|---|---|---|
| `<asset>` | `<low/med/high>` | `<low/med/high>` | `<low/med/high>` | `<notes>` |

## Identities and Access

| Principal | Authentication | Authorization | Session/token rule | Audit rule |
|---|---|---|---|---|
| `<user/service>` | `<method>` | `<scope/role>` | `<expiry/rotation>` | `<logged event>` |

## Threats and Controls

| Threat | Attack path | Control | Test/evidence | Residual risk |
|---|---|---|---|---|
| `<threat>` | `<how it happens>` | `<prevention/detection>` | `<test path or artifact>` | `<risk>` |

## Required Checks

- Tenant isolation or authorization negative tests.
- Parameterized query or ORM-safe query evidence.
- Secret scanning and secret-storage location.
- Dependency and container scan.
- Backup restore evidence.
- File upload validation if uploads exist.
- CI/CD permission review.
- Support/admin access audit trail.

## Ambiguity Handling

If identity provider, compliance regime, or data classification is unknown, use the conservative baseline and mark the decision dependency. Do not invent compliance status.

## See Also

- `examples/full-stack-saas-reference/security-threat-model.md`
- `docs/source-registers/ai-platforms.md`
