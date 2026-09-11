# Verified Triage State Machine

Triage moves an item only when the evidence for the next state exists.

`reported -> reproduced/observed -> scoped -> accepted/rejected/duplicate/deferred -> planned ->
implemented -> verified -> released -> learned`

For every transition record claim, source, reproducer or observation, affected scope, severity and
user consequence, owner, decision, dependency, next action, and evidence. Verify the reporter's claim
against the current product or repository before classification. Preserve rejected and out-of-scope
reasoning so it is not repeatedly rediscovered.

External tracker labels, assignments, comments, or closures require explicit authority. Without it,
produce a local triage proposal and durable pointer-rich handoff. Never mark implemented from a commit
alone, verified from an unrun test, or released from a merge.

This reference adapts the triage state and durable brief mechanism studied in Matt Pocock's
`mattpocock/skills` repository at commit `3cca18b`.
