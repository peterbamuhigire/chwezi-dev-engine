# RACI, RAID, Deliverables, and Gates

## RACI Rule

Every task has exactly one Accountable owner. Many people may be Responsible or Consulted, but accountability cannot be shared.

## RAID Log

| Type | Meaning | Required fields |
|---|---|---|
| Risk | Future uncertainty that may affect success. | Probability, impact, mitigation, owner. |
| Assumption | Unproven belief the plan depends on. | Validation method, due date, owner. |
| Issue | Current problem requiring action. | Severity, action, owner, due date. |
| Dependency | External input or sequence dependency. | Provider, needed date, fallback. |

## Deliverables Register

Every deliverable needs:

- Description.
- Accountable owner.
- Reviewer.
- Due date.
- Acceptance criteria.
- Source evidence.
- Tooling route where file output is promised.
- QC gate status.
- Release/version.

## Gate Sequence

1. Owner self-check.
2. Tooling readiness if file output is involved.
3. Evidence and claims audit.
4. Red-team/QC review.
5. Accountable owner release decision.
