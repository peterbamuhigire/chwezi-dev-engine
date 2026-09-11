# Completion Criteria and Handoff

A sequential skill must say what closes each phase and what happens when work stops early. Activity
is not completion.

## Phase contract

| Field | Requirement |
| --- | --- |
| Entry | Inputs, authority, and prior evidence needed to start |
| Action | Smallest bounded operation performed in the phase |
| Oracle | Observable result that distinguishes pass from plausible output |
| Failure | Stop, retry, rollback, or escalation condition |
| Exit | Artefact and evidence required before the next phase |

## Handoff contract

Store pointers to authoritative artefacts rather than copying their bodies. Record objective,
current phase, completed evidence, open decisions, blockers, changed files, commands/results,
authority boundaries, rollback, next action, and re-check date. Redact secrets and sensitive data.

A fresh agent must be able to resume without reconstructing hidden reasoning. If durability is not
available, return the handoff in the response and mark persistence `NOT ASSESSED`.

Derived from completion and handoff mechanics studied in Matt Pocock's `mattpocock/skills`
repository at commit `3cca18b`; adapted to the Chwezi evidence and control-plane contracts.
