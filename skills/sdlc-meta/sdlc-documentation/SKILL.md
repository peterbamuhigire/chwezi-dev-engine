---
name: sdlc-documentation
description: Use when producing, reviewing, or consolidating SDLC documentation across planning, requirements, design, testing, deployment, user rollout, post-deployment, and maintenance phases. Load absorbed SDLC phase references as needed.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# SDLC Documentation
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

Use this parent skill as the active SDLC documentation entrypoint. Keep the phase-specific details in references and load only the phase being authored or reviewed.

<!-- dual-compat-start -->
## Use When

- Creating or reviewing SDLC document sets, delivery evidence, traceability, phase gates, and lifecycle handoffs.
- Consolidating planning, design, testing, deployment, user rollout, post-deployment, and maintenance documents.
- Aligning project documentation with implementation, validation, release, and support obligations.

## Do Not Use When

- The task is unrelated to this parent skill or is better handled by a narrower active parent named in the workflow.
- The request only needs a trivial answer and no reference module needs to be loaded.

## Required Inputs

| Artefact | Required? | Purpose |
|---|---|---|
| System, repository, environment, and constraints | yes | Ground the document in actual delivery context |
| Requested lifecycle phase and audience | yes | Select only the needed reference and output |
## Workflow

1. Load `world-class-engineering` for baseline delivery quality.
2. Load the needed phase reference:
   - `references/sdlc-planning.md` for project planning and initiation.
   - `references/sdlc-design.md` for solution and technical design documents.
   - `references/sdlc-testing.md` for test planning, evidence, and acceptance gates.
   - `references/sdlc-user-deploy.md` for user rollout and adoption documents.
   - `references/sdlc-post-deployment.md` for go-live review and stabilisation evidence.
   - `references/sdlc-maintenance.md` for support, maintenance, and continuous improvement.
3. Pair with `project-requirements`, `advanced-testing-strategy`, `deployment-release-engineering`, or `implementation-status-auditor` when the task needs those outputs.

## Quality Standards

- Every document must be tied to a decision, acceptance criterion, release gate, or operating obligation.
- Preserve traceability from requirement to design, implementation, test evidence, release, and support.
- Avoid generic SDLC text that cannot guide an implementation or audit decision.

## Anti-Patterns

- Treating absorbed reference files as active skills or separate routing entrypoints.
- Loading every migrated child reference instead of the one that matches the task.
- Producing generic advice without constraints, evidence, or next verification steps.
## Outputs

- SDLC document, review findings, traceability notes, phase gate checklist, or handoff package.

## Evidence Produced

| Category | Artifact | Format | Example |
|---|---|---|---|
| Correctness | Traceability results | Matrix | Requirement-to-test mapping |
| Security | Security review | Findings register | Unresolved authorization risk |
| Data safety | Data-control evidence | Checklist | Recovery verification |
| Performance | Performance verification | Test record | SLO result |
| Operability | Operational handoff | Runbook and checklist | Monitoring ownership |
| UX quality | User validation | Acceptance record | Accessibility result |
| Release evidence | Release decision | Approval record | Signed gate outcome |

## References

- Load only the references/<old-skill>.md files named in the workflow when their depth is required.
<!-- dual-compat-end -->

## Decision Rules

| Condition | Action |
|---|---|
| One lifecycle phase is requested | Load only its absorbed reference |
| Evidence conflicts with an older document | Flag and reconcile before update |
| Required operational fact is unknown | Mark it open; do not invent it |

## Capability Contract

Read and search are required. Editing and validation execution require authorisation.

## Degraded Mode

Fallback: without repository evidence, return a document skeleton and open-question register.

## Domain Anti-Patterns

- Copying every phase template into one document.
- Presenting planned behaviour as implemented.
- Omitting owner or acceptance evidence.
- Leaving stale cross-document contradictions.
- Inventing deployment or maintenance facts.
