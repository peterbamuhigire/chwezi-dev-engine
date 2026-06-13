# Remediation Backlog Template

| Field | Description |
|---|---|
| ID | Stable finding ID. |
| Area | Security, payment, privacy, AI, integration, data, UX trust, operations. |
| Finding | Clear observed issue. |
| Evidence | Screenshot, config, interview note, log, policy, or test result. |
| Standard/control | OWASP, PCI, CVSS, privacy table, policy, or requirement. |
| Severity | Critical, high, medium, low, advisory. |
| Business impact | What happens if unresolved. |
| Owner | Company role responsible. |
| Effort | Small, medium, large. |
| Dependency | Vendor, developer, policy, legal, finance, logistics. |
| Recommendation | Specific fix. |
| Acceptance criteria | How to know it is fixed. |
| Due date | Target date. |
| Status | Open, in progress, blocked, accepted risk, done. |

## Prioritisation

Fix first:

1. Customer/payment data exposure.
2. Authentication and admin-access weaknesses.
3. Broken payment or reconciliation controls.
4. Missing consent/privacy controls for active jurisdictions.
5. High-impact integration failures.
6. Trust blockers that directly suppress conversion.
