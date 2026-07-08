# Architecture Decision Record Template

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 architecture template
Benchmark: Thoughtworks ADR practice plus staff-engineer strategy memo discipline.

## Decision Identity

| Field | Value |
|---|---|
| ADR ID | `<ADR-0001>` |
| Title | `<decision title>` |
| Status | `<proposed / accepted / superseded / rejected>` |
| Date | `<yyyy-mm-dd>` |
| Owner | `<name/role>` |
| Reviewers | `<names/roles>` |
| Related skills | `<skill paths>` |

## Context

State the business capability, system boundary, data ownership issue, reliability target, or security constraint that forces a decision. Name the concrete user journey or domain transaction.

## Decision

We will `<decision>`.

## Rationale

| Reason | Evidence |
|---|---|
| `<reason>` | `<source, test, benchmark, incident, or constraint>` |

## Alternatives Considered

| Alternative | Why rejected | Reversal trigger |
|---|---|---|
| `<option>` | `<specific trade-off>` | `<condition that would make it better>` |

## Consequences

| Area | Consequence | Owner |
|---|---|---|
| API | `<impact>` | `<owner>` |
| Data | `<impact>` | `<owner>` |
| Security | `<impact>` | `<owner>` |
| Reliability | `<impact>` | `<owner>` |
| Operations | `<impact>` | `<owner>` |

## Validation

- [ ] Boundary maps to a business capability.
- [ ] Data owner is singular for every mutable entity.
- [ ] Contract artifacts exist for cross-boundary calls.
- [ ] Failure modes are named.
- [ ] Rollback or migration path is named.
- [ ] Cross-engine handoffs are routed, not duplicated.

## See Also

- `templates/delivery-dod/evidence-pack.md`
- `examples/full-stack-saas-reference/architecture.md`
