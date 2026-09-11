# Intent-Led Merge-Conflict Resolution

Resolve each hunk from the intent and primary evidence of both sides, not by choosing `ours`,
`theirs`, or the version that looks newer.

1. Record operation type, branches/commits, clean recovery point, and abort command before editing.
2. Inspect the base, each side's diff/commit message/tests, and the consuming code or document.
3. State the invariant and intended outcome each side contributes.
4. Resolve one hunk at a time; preserve both intents when compatible and escalate contradictory product
   or policy decisions to the owner.
5. Search for conflict markers, duplicate imports/sections, stale generated output, and lost renames.
6. Run focused tests after each semantic cohort, then the full relevant gate.
7. Continue only after status and diff match the intended combined change. Retain abort/recovery until
   the operation and post-merge checks complete.

Never categorically forbid abort: abort is the safe recovery when the resolution basis is wrong or
scope becomes unsafe. Never force-push a protected/shared branch without explicit authority and a
coordination plan.

This reference adapts intent-based conflict handling studied in Matt Pocock's `mattpocock/skills`
repository at commit `3cca18b` while preserving merge/rebase recovery options.
