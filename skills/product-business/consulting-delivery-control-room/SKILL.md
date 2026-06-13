---
name: consulting-delivery-control-room
description: Use when coordinating multi-workstream consulting bids or delivery programmes with deadlines, owners, RACI, RAID, deliverables registers, decision logs, quality gates, and client/donor reporting cadence.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Consulting Delivery Control Room
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Coordinating a multi-workstream bid, donor programme, consulting engagement, expert pool, or delivery sprint.
- Work must be tracked through owners, due dates, risks, issues, decisions, dependencies, deliverables, versions, and quality gates.

## Do Not Use When

- The task is a single small deliverable with one owner and no material coordination risk.
- A project-management system already exists and only needs routine status updates.

## Required Inputs

- Scope, workstreams, deadlines, team, roles, deliverables, dependencies, review gates, reporting cadence, and client/donor obligations.

## Workflow

- Stand up the control registers before production work accelerates.
- Apply the RACI, RAID, deliverables, decisions, evidence, and quality-gate workflow below.
- Update the registers at every control meeting and before every client-facing release.

## Quality Standards

- Every workstream and deliverable has exactly one accountable owner.
- Risks, issues, assumptions, and dependencies are live, not decorative.
- No deliverable ships without the required tooling and QC gates.

## Anti-Patterns

- Tracking deliverables only in chat, email, or memory.
- Allowing two accountable owners for the same task.
- Skipping quality gates because the deadline is close.

## Outputs

- Control dashboard, workstream tracker, RACI, RAID log, deliverables register, decision log, evidence register, and control-meeting pack.

## References

- `references/control-room-registers.md`: Required registers and fields.
- `references/raci-raid-deliverables.md`: RACI, RAID, deliverables, cadence, and gate rules.
<!-- dual-compat-end -->

## Core Workflow

1. Decompose the engagement into workstreams, deliverables, dependencies, and decision points.
2. Assign a single accountable owner for each workstream and deliverable.
3. Create a live RAID log for risks, assumptions, issues, and dependencies.
4. Create a deliverables register with acceptance criteria, reviewer, due date, evidence, and release status.
5. Create a decision log so scope, pricing, submission, legal, and delivery choices remain auditable.
6. Link every external-facing output to a tooling-readiness gate and a red-team/QC gate.
7. Run a regular control meeting: status, blockers, decisions, risks, next actions, upcoming gates.
8. Archive release evidence after each submission or client/donor delivery.
