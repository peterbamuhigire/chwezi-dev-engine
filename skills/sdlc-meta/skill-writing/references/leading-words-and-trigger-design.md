# Leading Words and Trigger Design

Routing attention is strongest at the beginning of a short description. Start with `Use when`, then
place the distinctive user outcome and trigger before qualifiers. End with the closest neighbour
boundary only when confusion is plausible.

## Pattern

`Use when <distinct outcome> for <observable conditions>; use <neighbour> when <boundary>.`

Use the user's language, not internal taxonomy. Prefer nouns and verbs that distinguish the route.
Avoid `comprehensive`, `world-class`, lists of every feature, implementation steps, and claims that
the skill always or automatically loads.

## Evaluation set

1. Clear positive prompt.
2. Near-neighbour negative prompt.
3. Ambiguous prompt that needs context.
4. Alias or former-name prompt.
5. Prompt containing shared vocabulary but seeking a different output.

Accept a description only when the intended route stays in the required rank without stealing the
neighbour cases. Record collision score and description-character cost.

Derived from leading-word and routing mechanics studied in Matt Pocock's `mattpocock/skills`
repository at commit `3cca18b`.
