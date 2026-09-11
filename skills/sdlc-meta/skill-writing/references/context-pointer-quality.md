# Context Pointer Quality

Use a pointer when a branch needs knowledge that does not belong in every execution. A pointer is an
instruction, not a bibliography entry: it names the decision that triggers the load, the exact
resource, and what the reader should extract.

## Contract

| Field | Required question |
| --- | --- |
| Trigger | What observable task condition makes this resource necessary? |
| Target | Is the path direct, stable, and validated? |
| Purpose | Which decision, check, or output does the resource govern? |
| Return | What evidence or decision comes back to the parent workflow? |
| Fallback | What happens when the resource or capability is unavailable? |

Prefer `Load references/restore.md when recovery evidence is required; return the tested restore
command, RPO/RTO result, and unresolved gap` over `See references for more information`.

## Checks

- Positive branch loads the resource and uses its named output.
- Neighbour branch does not load it.
- Missing target fails validation.
- Unavailable external target produces a bounded degraded result, not invented content.
- The parent remains understandable without loading unrelated references.

Derived from the pointer and progressive-disclosure mechanics studied in Matt Pocock's
`mattpocock/skills` repository at commit `3cca18b`; adapted under the Chwezi portable contract.
