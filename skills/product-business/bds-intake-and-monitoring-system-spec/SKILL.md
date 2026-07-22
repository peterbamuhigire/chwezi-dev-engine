---
name: bds-intake-and-monitoring-system-spec
description: Use when specifying application intake, eligibility screening, selection scoring, beneficiary registers, diagnostics tracking, expert deployment, monitoring dashboards, RBAC, audit trails, and donor reporting for BDS programmes.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# BDS Intake and Monitoring System Spec
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.


## Required Inputs

| Input | Required | Use |
|---|---|---|
| Decision, audience, and deliverable | yes | Bound the business outcome |
| Source evidence, constraints, and owner | yes | Ground recommendations and accountability |
| Approved budget, customer data, or production artefacts | conditional | Support high-impact execution |

## Capability and permission contract

Default to read-only analysis and drafting. Do not publish, send, price, promise, alter customer records, commit budget, or modify production artefacts without explicit authority and a named approver. Minimise confidential data, preserve provenance, and keep reversible copies.

## Degraded mode

If evidence, stakeholder decisions, specialist tooling, or authoritative commercial data are unavailable, deliver a labelled draft, checklist, or decision memo. State what was not verified and do not claim approval, publication, financial accuracy, or customer acceptance.

## Decision rules

| Condition | Action | Stop condition |
|---|---|---|
| Output creates a commercial, customer, or delivery commitment | Obtain named approval before release | Authority or terms are unclear |
| Evidence supports a reversible draft | Produce it with assumptions and owner | Required evidence conflicts |
| Tooling or data is incomplete | Specify validation | A final executable artefact is expected |

## Domain Anti-Patterns

- Inventing customer evidence, prices, benchmarks, or approvals. Fix: cite the source or mark the gap.
- Publishing or sending a draft without authority. Fix: retain draft status and name the approver.
- Hiding assumptions inside polished prose. Fix: expose them beside each affected decision.
- Polishing presentation while the decision remains unclear. Fix: resolve audience, owner, and acceptance criteria.
- Treating unavailable tooling as passed validation. Fix: record the unassessed check.


<!-- dual-compat-start -->
## Overview

Use this skill to write requirements for the operational system behind a BDS or accelerator programme. The system may be a spreadsheet, Airtable-style base, KoboToolbox/ODK workflow, database, or lightweight app, but the requirements must define data, access, audit, scoring, monitoring, privacy, and reporting before tools are chosen.

## Use When

- Designing an application register, eligibility screen, scoring matrix, diagnostics tracker, action-plan tracker, expert deployment tracker, or M&E dashboard.
- A donor programme needs auditable selection, beneficiary tracking, and quarterly reporting.
- Sensitive company, personal, financial, or diagnostic data will be collected.

## Do Not Use When

- The task is only public campaign copy.
- There is no selection, monitoring, or reporting workflow.
- You are building software without first defining the data and control model.

## Required Inputs

- Application form fields and eligibility/award criteria.
- Monitoring indicators and reporting cadence.
- User roles, reviewers, experts, donor/client viewers, and administrators.
- Data-protection and consent constraints for the relevant countries.
- Expected tool route: spreadsheet, form tool, Airtable-like base, or app.

## Workflow

1. Define the data dictionary for applications, eligibility, scoring, diagnostics, TA packages, attendance, action plans, evidence, and outcomes.
2. Separate eligibility pass/fail checks from award scoring and ensure scoring is computed, explained, and reviewable.
3. Specify RBAC: applicant, administrator, screener, evaluator, expert, team leader, donor viewer, auditor.
4. Require audit trail and versioning. If the chosen tool cannot provide immutable logs, specify compensating controls.
5. Define consent, minimisation, retention, confidentiality, export, and anonymisation requirements.
6. Define indicator metadata: definition, source, disaggregation, owner, frequency, validation, and reporting output.
7. Specify dashboard views for pipeline, geography, selection, diagnostics, TA delivery, risks, and outcomes.
8. Produce acceptance criteria and test cases for the register and dashboard.

## Quality Standards

- Every field is typed, validated, and owned.
- Eligibility and award scoring are separate.
- RBAC matches the real capability of the chosen tool.
- Audit and version controls are explicit.
- Monitoring indicators are defined before dashboard design.
- Privacy-by-design defaults to the strictest applicable programme standard.

## Anti-Patterns

- A shared spreadsheet with personal/company data and no access control.
- Manual scoring with no formula, reviewer notes, or audit log.
- Indicators with no source or disaggregation.
- Collecting more data than the programme uses.
- Dashboards that cannot be reconciled to source records.

## Outputs

- Intake and monitoring system requirements.
- Application-register data dictionary.
- Eligibility and award-scoring rules.
- RBAC and audit-trail requirements.
- M&E indicator dictionary and dashboard requirements.
- Acceptance criteria and export requirements.

## References

- `references/data-dictionary-and-rbac.md`: Core tables, fields, scoring, roles, and controls.
- `references/monitoring-dashboard-requirements.md`: Indicator dictionary and dashboard view requirements.
<!-- dual-compat-end -->
