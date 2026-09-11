# Human-Only Operation Wizards

Use a wizard when an authorised operator must complete staged setup or release actions that cannot be
safely automated end to end: account ownership, credentials, signing, DNS, provider consoles,
regulated approvals, physical devices, or production confirmation.

## Stage contract

Each stage records prerequisites, operator, exact action, expected observable state, static/read-only
verification, secret handling, retry/idempotency behaviour, rollback, and the next locked stage. Do not
advance because the operator says "done" when an API, file, status page, or test can verify the result.

Capture identifiers and status, never secret values. Write secrets only to the approved secret store
through the provider's supported path and only with explicit authority. A generated shell or
PowerShell helper defaults to status/dry-run, quotes literal paths, validates target scope, and can be
rerun without duplicating or destroying state.

## Failure behaviour

- Missing account or permission: preserve completed stages and identify the required owner.
- Partial provider setup: verify existing state before retry; do not create duplicates.
- Secret exposed: stop, revoke/rotate through the authorised process, and preserve incident evidence.
- Human-only verification unavailable: mark the stage `NOT ASSESSED`; do not unlock dependants.
- Rollback unsafe: define a bounded roll-forward or stop release.

Output a resumable stage ledger and pointer-rich handoff. External mutation, spending, messages, DNS,
production change, and credential actions remain action-specific approval boundaries.

This reference adapts the staged wizard mechanism studied in Matt Pocock's `mattpocock/skills`
repository at commit `3cca18b` and adds Chwezi idempotency, secret, recovery, and evidence controls.
