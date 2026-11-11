# Unattended plan template

Copy this template into your project-owned plan, then commit it before running the driver. The driver does not parse the sections below. Use `STATUS: DONE` or `STATUS: BLOCKED - reason` as the first line only when appropriate.

## Outcome and boundaries

- Desired user outcome and why it matters:
- In-scope flows and affected areas:
- Constraints, authorised external effects, data boundaries and project-specific rules:
- Existing specifications and decisions to consult:

## Acceptance and verification

- Observable examples for the behaviour, including normal and failure cases:
- Relevant commands configured in `auto-agents/config.json` and why they test this work:
- Checks that cannot yet run and the conditions needed to run them:

## Ordered slices

For each slice record its outcome, dependencies, expected files or interfaces, checks and recovery note. Work sequentially where a dependency requires it. Keep slices small enough to finish, verify and commit within the session limit.

- [ ] Slice 1:
- [ ] Slice 2:

## Durable handoff

- Last completed slice and commit:
- Next slice and current decision context:
- Failed checks, known gaps and precise recovery steps:
- Assumptions made and unresolved decisions that actually block work:

Do not put secrets, raw credentials or private data in the plan or logs. Preserve project-owned plans and settings when upgrading the driver. A passing command is evidence of its own checks, not proof of complete product correctness.
