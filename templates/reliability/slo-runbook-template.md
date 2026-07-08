# SLO and Runbook Template

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 reliability template
Benchmark: Google SRE SLO, error-budget, and incident-response practice.

## Service Identity

| Field | Value |
|---|---|
| Service | `<service>` |
| Critical journey | `<journey>` |
| Owner | `<team/person>` |
| On-call route | `<route>` |
| Review date | `<yyyy-mm-dd>` |

## SLO

| Indicator | Objective | Measurement window | Query/dashboard |
|---|---:|---|---|
| Availability | `<99.x%>` | `<window>` | `<link/path>` |
| Latency | `<p95 target>` | `<window>` | `<link/path>` |
| Correctness | `<target>` | `<window>` | `<link/path>` |

## Error Budget Policy

| Burn condition | Action |
|---|---|
| `<threshold>` | `<release freeze, rollback, mitigation, escalation>` |

## Alerts

| Alert | Trigger | Severity | First action |
|---|---|---|---|
| `<alert>` | `<condition>` | `<sev>` | `<action>` |

## Diagnosis

1. Check `<dashboard/log/query>`.
2. Confirm whether impact is tenant-specific, regional, or global.
3. Identify recent deploys, migrations, feature flags, queue lag, and dependency health.
4. Decide rollback, mitigation, or forward fix.

## Rollback

| Change | Rollback action | Data safety note |
|---|---|---|
| `<change>` | `<action>` | `<note>` |

## Incident Review

- Impact:
- Timeline:
- Detection gap:
- Mitigation:
- Error-budget burn:
- Prevention action:
- Owner and due date:

## QA Checklist

- [ ] Every critical journey has an SLO.
- [ ] Every SLO has a query or dashboard.
- [ ] Every alert names a human action.
- [ ] Rollback is rehearsed or explicitly constrained.
- [ ] Incident review produces a prevention action or a justified no-action decision.

## See Also

- `examples/full-stack-saas-reference/reliability-and-release.md`
- `templates/delivery-dod/evidence-pack.md`
