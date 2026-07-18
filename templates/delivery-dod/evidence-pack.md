# Delivery Evidence Pack Template

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 Delivery Definition of Done
Benchmark: Stripe-style API changelog discipline, Google SRE release evidence, Thoughtworks evolutionary architecture records.

Use this template for any implementation, architecture, security, AI, SaaS, mobile, data, or DevOps deliverable. A deliverable without this pack is not release-ready.

## 1. Artifact Identity

| Field | Value |
|---|---|
| Project | `<project-name>` |
| Deliverable | `<artifact-name>` |
| Owner | `<owner>` |
| Reviewer | `<reviewer>` |
| Date | `<yyyy-mm-dd>` |
| Related skills | `<skill paths>` |
| Running example variant | `<if applicable>` |

## 2. Decision Record

| Decision | Rationale | Alternatives rejected | Reversal trigger |
|---|---|---|---|
| `<decision>` | `<why this is the right trade-off>` | `<credible options not chosen>` | `<condition that reopens it>` |

Pass criteria: every material architecture, API, database, security, or release choice has a named rationale and a reversal trigger.

## 3. Contract Evidence

| Contract | Evidence | Location | Pass/fail |
|---|---|---|---|
| API/OpenAPI/schema | `<contract artifact>` | `<path>` | `<pass/fail>` |
| Database migration | `<migration + rollback>` | `<path>` | `<pass/fail>` |
| Event/interface contract | `<producer/consumer evidence>` | `<path>` | `<pass/fail>` |
| Auth/RBAC contract | `<roles, policies, test>` | `<path>` | `<pass/fail>` |

Pass criteria: no integration boundary relies on prose alone.

## 4. Test Evidence

| Layer | Required evidence | Result |
|---|---|---|
| Unit | Meaningful tests for business rules and edge cases | `<result>` |
| Contract | Consumer/provider or schema compatibility checks | `<result>` |
| Integration | Database, queue, cache, auth, and external dependency behavior | `<result>` |
| Security | OWASP-relevant checks, dependency scan, secret scan, permission test | `<result>` |
| Reliability | Load, timeout, retry, rollback, and observability checks | `<result>` |
| Accessibility/frontend | WCAG and state coverage where UI exists | `<result>` |

Pass criteria: no `assert true`, no unrun tests, no untriaged failures.

## 5. Operational Evidence

| Area | Evidence required | Release blocker |
|---|---|---|
| Observability | Dashboards, alerts, logs, traces, SLO query | Missing signal for critical user journey |
| Rollback | Reversible migration or compensating action | Irreversible change without sign-off |
| Runbook | Detection, diagnosis, mitigation, escalation | On-call cannot operate it |
| Capacity | Expected load, headroom, scaling limits | Unknown limit on critical flow |
| Incident learning | Known failure modes and postmortem template | Repeated failure has no prevention owner |

## 6. Source and Currency Evidence

| Claim type | Required source |
|---|---|
| Current AI/platform behavior | `docs/source-registers/ai-platforms.md` or official vendor docs |
| Finance/accounting/statutory rule | External `chwezi-accounting-doctrine` |
| Visual/typographic rule | External `design-system-skills` |
| Security standard | OWASP, NIST, CIS, vendor primary documentation, or project security policy |

Pass criteria: no volatile fact appears without last-verified date and source.

## 7. Anti-Slop Gate

- The artifact states decisions, not only information.
- Every section has a concrete project-specific detail.
- Known edge cases and failure modes are named.
- Generic claims such as "secure", "scalable", or "production-ready" are backed by evidence.
- The reviewer can trace every claim to code, test, source, or decision record.

## 8. Release Verdict

| Gate | Verdict | Reviewer note |
|---|---|---|
| Architecture | `<pass/fail>` | `<note>` |
| Security | `<pass/fail>` | `<note>` |
| Reliability | `<pass/fail>` | `<note>` |
| Data | `<pass/fail>` | `<note>` |
| Docs/runbook | `<pass/fail>` | `<note>` |
| Anti-slop | `<pass/fail>` | `<note>` |

Final release decision: `<ship / hold / rollback / research further>`
