# Data Dictionary and RBAC

## Core Entities

- Applicant organisation.
- Contact person.
- Application.
- Eligibility screen.
- Award score.
- Reviewer note.
- Company diagnostic.
- TA package.
- Expert assignment.
- Session/attendance.
- Action-plan item.
- Evidence file.
- Indicator observation.
- Risk/issue.

## Field Rules

Every field must have:

- Name.
- Description.
- Type.
- Required/optional.
- Allowed values or validation.
- Source.
- Owner.
- Confidentiality level.
- Retention rule.

## Scoring Rules

- Eligibility fields are pass/fail and cannot be averaged into award scoring.
- Award criteria have weights, reviewer notes, and conflict-of-interest declarations.
- Score changes require reviewer identity, timestamp, and reason.
- Tie-break and geographic-balance logic must be documented.

## RBAC Baseline

| Role | Access |
|---|---|
| Applicant | Own submitted data and public guidance only. |
| Administrator | Configure forms, users, exports, and audit logs. |
| Screener | Eligibility fields and administrative notes. |
| Evaluator | Award criteria assigned to them; conflict declaration required. |
| Expert | Assigned company diagnostic/action-plan data only. |
| Team leader | All programme records and quality gates. |
| Donor viewer | Aggregated dashboard and approved reports, not raw confidential data by default. |
| Auditor | Read-only access to logs, scoring, and evidence. |
