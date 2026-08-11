# Release-Blocking Gates

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 release gate
Benchmark: Google SRE launch discipline, OWASP security review, Stripe API compatibility practice, Thoughtworks architecture fitness functions.

This gate applies to every deliverable produced by `skills-web-dev`. It is stricter than a checklist: any blocker below holds release until evidence is added or the scope is explicitly reduced.

## Gate Matrix

| Gate | Blocks release when | Evidence that clears it |
|---|---|---|
| Architecture | Boundary, dependency, or data-ownership decision lacks rationale | ADR, architecture note, or evidence-pack decision record |
| API contract | Endpoint behavior is described only in prose | OpenAPI/schema, examples, error model, idempotency and compatibility notes |
| Data safety | Migration, backup, restore, tenancy, or consistency behavior is untested | Migration test, restore drill, tenant-isolation test, consistency note |
| Security | Auth, RBAC, secrets, injection, dependency, or tenant-isolation risk is unreviewed | Threat model, scan output, policy test, dependency report |
| Reliability | Critical journey lacks SLO, alert, rollback, or runbook | SLO query, dashboard, alert rule, rollback plan, runbook |
| Current facts | Vendor, platform, standard, or statutory claim lacks dated source | Source register entry or Digital Research Skills Engine verification note |
| Output quality | Section is generic, unsupported, or viewpoint-free | Specific decision, evidence, edge case, and reviewer-facing implication |
| Cross-engine handoff | Finance, visual design, statutory, or research ownership is copied instead of routed | Link to `chwezi-accounting-doctrine`, `design-system-skills`, or `digital-research-skills` |

## Reviewer Procedure

1. Open the artifact and its evidence pack together.
2. Mark every claim as code-backed, test-backed, source-backed, decision-backed, or unsupported.
3. Quarantine unsupported claims instead of polishing them.
4. Confirm that every external standard or platform fact has a last-verified date.
5. Run applicable repository gates:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
python -X utf8 scripts\routing_smoke_test.py --report-only
```

## Common Release Mistakes

- Calling a system production-ready because it has a deployment script.
- Treating a smoke test as proof of correctness.
- Describing authorization rules without negative tests.
- Naming SLOs without a query, alert, and release consequence.
- Presenting vendor features as current without a dated source register entry.
- Copying statutory or design rules into this engine instead of routing to the canonical engine.

## Verdict Format

| Gate | Verdict | Blocking evidence gap |
|---|---|---|
| Architecture | `<pass/fail>` | `<gap>` |
| API | `<pass/fail>` | `<gap>` |
| Data | `<pass/fail>` | `<gap>` |
| Security | `<pass/fail>` | `<gap>` |
| Reliability | `<pass/fail>` | `<gap>` |
| Currency | `<pass/fail>` | `<gap>` |
| Anti-slop | `<pass/fail>` | `<gap>` |

Final verdict must be one of: `ship`, `hold`, `rollback`, or `research further`.
