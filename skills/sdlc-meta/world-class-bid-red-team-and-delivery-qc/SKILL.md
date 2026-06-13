---
name: world-class-bid-red-team-and-delivery-qc
description: Use as the final quality gate for high-stakes bids, donor submissions, consulting deliverables, score predictions, compliance knockout scans, evidence audits, spreadsheet reviews, and delivery-feasibility checks.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# World-Class Bid Red Team and Delivery QC
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Before submitting a high-stakes bid or donor proposal.
- Before releasing needs assessments, TA packages, reports, dashboards, workbooks, price schedules, or executive documents.
- When evaluator scoring, compliance knockouts, evidence quality, feasibility, or spreadsheet integrity can decide success.

## Do Not Use When

- The work is low-stakes, internal, and has no material compliance or client-facing risk.
- Required source documents, scoring criteria, or deliverables are unavailable.

## Required Inputs

- Draft pack, compliance matrix, scoring grid, source evidence, workplan, budget/workbook, assumptions, and tooling validation notes.

## Workflow

- Simulate the evaluator.
- Run compliance knockout checks.
- Audit evidence and claims.
- Review spreadsheets and file outputs.
- Test delivery feasibility.
- Require four-eyes sign-off before release.

## Quality Standards

- The bid/deliverable does not ship while a knockout issue remains open.
- Every material claim traces to evidence or is labelled as an assumption.
- Workbooks reconcile and file outputs are validated.
- Feasibility is judged against people, days, budget, approvals, and data reality.

## Anti-Patterns

- Treating QC as proofreading.
- Scoring the proposal generously instead of like the evaluator.
- Ignoring spreadsheet formula risk.
- Letting deadline pressure bypass the gate.

## Outputs

- Evaluator simulation, score prediction, knockout scan, evidence audit, spreadsheet review, feasibility review, and final sign-off record.

## References

- `references/red-team-scorecard.md`: Evaluator simulation and scoring prediction.
- `references/qc-gates-and-evidence-audit.md`: Knockout, evidence, spreadsheet, feasibility, and sign-off gates.
<!-- dual-compat-end -->

## Core Workflow

1. Read the actual scoring grid and mandatory requirements.
2. Score the draft as the evaluator would, using the buyer's weights and language.
3. Predict whether the technical threshold is cleared and identify the weak scoring blocks.
4. Run a compliance knockout scan against all pass/fail requirements.
5. Audit claims, figures, laws, organisation names, dates, and benchmarks against the evidence register.
6. Review spreadsheet controls: formulae, totals, assumptions, locked cells, price/technical consistency, and VAT/tax treatment where relevant.
7. Test delivery feasibility against team capacity, fee-days, calendar, approvals, data access, travel, and reporting cadence.
8. Record required fixes and block release until critical findings are resolved.
9. Obtain independent four-eyes sign-off for release.
