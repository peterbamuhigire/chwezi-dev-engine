# Unattended plan template

Copy this template to a project-owned `docs/plans/<name>.md` and commit it
before running the driver. Keep the Markdown plan as the readable authority.
For machine-checkable task IDs and evidence metadata, an optional companion
`docs/plans/<name>.contract.json` may use `plan_contract.py`. Existing plans
remain valid without a JSON sidecar; the driver does not parse either format
into task-level proof.

The executor proceeds through every authorised, unblocked phase in dependency
order. A checkpoint is progress, not completion, and does not require the owner
to say “continue” again. Stop dependent work only for a missing decision,
required approval, genuine blocker, or governing instruction; continue
independent authorised work.

## Outcome and authority

- Desired user outcome and why it matters:
- Accountable acceptance owner:
- In-scope user journeys and affected areas:
- Exclusions and write ownership (files, directories, or bounded discovery):
- Constraints, authorised external effects, data boundaries, and project rules:
- Existing specifications and decisions to consult, with revision or path:

## Acceptance and verification

For each material outcome, give a stable criterion ID and an observable result.
Declare one exact validation command per criterion; split independently
verifiable commands into separate criteria.
Cover the applicable normal, empty, error/invalid, denied, boundary, and
interrupted/recovery states. Omit inapplicable states with a reason; do not
pad criteria to reach a count.

| Criterion ID | Observable acceptance result | Exact command and working directory, or evidence oracle | State/result |
|---|---|---|---|
| AC-001 | | | pending |

- Environment, fixtures, and required data state:
- Commands copied from project evidence, with expected exit/result:
- Checks that cannot yet run, missing prerequisites, and release consequence:

Record each result against the code revision actually tested. Keep evidence in
a durable path and record its SHA-256 digest, criterion ID, exact command or
oracle, and result (`PASS`, `FAIL`, or `NOT_ASSESSED`). `NOT_ASSESSED` never
means pass. When inputs change, mark dependent evidence stale and rerun only
affected checks. An attempted command, edit, commit, or phase is activity; it
does not prove its acceptance outcome.

## Ordered work

Use stable task IDs that survive reordering. Name prerequisite IDs and owned
paths for each task. Keep one writer per path at a time; use bounded discovery
with a stop condition when exact paths are not yet known. Include dependencies
only where they constrain order.

| Task ID | Outcome and owned scope | Depends on | Acceptance IDs | State |
|---|---|---|---|---|
| TASK-001 | | — | AC-001 | pending |

Valid states are `pending`, `running`, `blocked`, and `complete`. A complete
task must have a passing evidence reference for every acceptance criterion.
Task state is a reported assertion; validation of this metadata does not
independently verify the code, the meaning of the evidence, or the commit.

## Replay and recovery

For every operation with an external effect, state whether it is safe to
repeat, idempotent under a named key, reconciled by reading the destination, or
requires manual recovery. After a power cut, session end, quota/usage-window
reset, or timeout, inspect durable evidence and reconcile destination effects
before retrying. A timeout does not prove that an effect failed. If its result
cannot be reconciled, stop that operation, preserve evidence, and name its
owner and next action. Never blindly replay a non-idempotent effect.

## Durable handoff

Keep this section current so a fresh runner can resume without conversation
history. Keep it concise and link to the detailed evidence.

- Current phase and task IDs:
- Completed outcomes and evidence paths (include tested revision):
- Next ready task IDs in dependency order:
- Blockers/decisions: owner, impact, exact next action; or `none`:
- Failed or `NOT_ASSESSED` checks and recovery steps:
- External effects and reconciled state/replay rule; or `none`:
- Relevant assumptions and risks; or `none`:

Mark `STATUS: DONE` on the first line only after all required outcomes have
supporting acceptance evidence and the implementation is ready for independent
completion verification. Commit that candidate. The driver then runs its
configured independent gates against the candidate revision; the marker alone
never records an accepted run. Use `STATUS: BLOCKED - reason` only when no
independent authorised work remains. The driver marker and task states are
not substitutes for verification evidence. Do not ask the owner to repeat
authorisation or continue instructions already given.

Optional contract sidecar shape (use exact verified commands or an evidence
oracle; start new work as `pending`):

```json
{
  "schema_version": 1,
  "tasks": [
    {
      "id": "TASK-001",
      "title": "Verify export denial",
      "depends_on": [],
      "scope": ["tests/export/denied_export_test.py"],
      "acceptance": [
        {
          "id": "AC-001",
          "description": "Denied export creates no download or export record",
          "evidence_oracle": "Observed denial response, no download, and no export record"
        }
      ],
      "state": "pending",
      "evidence": []
    }
  ]
}
```

The example oracle is illustrative; replace it with the project's verified
oracle or command and environment. Evidence objects use `criterion_id`, `path`,
`tested_revision`, `sha256`, `command`, and `result`. The digest binds the
referenced evidence file; `tested_revision` names the source revision checked.
These are structural metadata, not proof that the criterion is true.

Do not put secrets, raw credentials, or private data in plans or logs. A
passing command proves only the checks it ran, not complete product correctness.
