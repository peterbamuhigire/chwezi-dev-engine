# Invocation Ownership

Invocation is part of behaviour. Declare whether a skill may be selected by the model, must be
requested explicitly by the user, or supports both. If no declaration exists, this engine treats the
skill as model-invoked when its trigger matches; a host may still impose a stricter policy.

## States

| State | Meaning | Required protection |
| --- | --- | --- |
| `implicit` | Model may select the skill from task context | Positive and neighbour routing fixtures |
| `explicit` | Only a direct user request may start it | No automatic or transitive invocation; clear refusal/fallback |
| `both` | Either route is intended | Fixtures for direct and automatic entry |

Use `metadata.invocation` only when a non-default state matters. Canonical skill content owns the
semantic state; vendor adapters may map it to host fields but may not broaden it. If the host cannot
enforce the state, report enforcement `NOT ASSESSED` and retain the safest documented behaviour.

Never use explicit invocation as a substitute for permission checks. Mutation, publication,
spending, production access, secrets, and destructive work still require action-specific authority.

Derived from invocation adapters studied in Matt Pocock's `mattpocock/skills` repository at commit
`3cca18b`; adapted without assuming Claude or Codex metadata equivalence.
