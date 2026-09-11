# Pointer-Rich Resumable Handoffs

A handoff is a compact index to authoritative state. It does not duplicate specifications, logs,
source bodies, or hidden reasoning.

## Required fields

| Field | Content |
| --- | --- |
| Objective/current phase | Outcome and exact workflow position |
| Decisions | Confirmed choices with owners; unresolved choices remain open |
| Artefact pointers | Stable paths/IDs, versions, and relevant sections |
| Changed state | Files, commits, migrations, external mutations, and current status |
| Evidence | Commands/checks, results, timestamps, and `NOT ASSESSED` items |
| Risks/blockers | Consequence, owner, next event, and release effect |
| Authority | Permitted actions and boundaries that still require approval |
| Recovery | Last safe state, rollback, cleanup, and retry condition |
| Next action | One concrete frontier task and acceptance oracle |

Redact secrets, personal data, and unnecessary client content. A temporary location is acceptable
only when the receiving session can access it for the required lifetime; otherwise store the record
with project evidence. Verify by giving the handoff to a fresh context and measuring whether it can
identify the next action, required inputs, constraints, and checks without prior conversation.

This reference adapts the compact handoff mechanism studied in Matt Pocock's `mattpocock/skills`
repository at commit `3cca18b` and retains Chwezi ownership, permission, and recovery controls.
