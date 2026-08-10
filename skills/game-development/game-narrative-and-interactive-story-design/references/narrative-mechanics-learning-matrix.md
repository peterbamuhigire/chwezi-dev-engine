# Narrative mechanics learning matrix

Use this reference to test whether a game mechanic creates an intended player
meaning rather than merely adding plot or dialogue. It is an independent design
tool, not a reproduction of any source text.

| Design unit | Ask | Evidence before standardising |
|---|---|---|
| Player verb | What can the player do, refuse, combine, risk, or protect? | Playtest observation and input/state trace |
| System response | What changes immediately and later, including failure or recovery? | Deterministic state transition and failed-path test |
| Feedback | Can the player understand cause, consequence, and available next choice? | Comprehension test, accessibility review, telemetry where appropriate |
| Meaning | What value, relationship, theme, or world rule does the mechanic let the player experience? | Player explanation plus designer intent; label inference |
| Agency | Is the choice consequential without pretending to offer control the system does not honour? | Choice/consequence matrix and edge-case playtest |
| Emergence | Can combinations produce useful, harmful, or surprising outcomes within safe bounds? | Scenario matrix, balance/economy evidence, rollback plan |

## Kaizen use

At the initial analysis, publish the product score at `min(raw_score, 65)` and keep
unknown meaning, comprehension, and agency evidence unassessed. Pick one reversible
change toward 95/100, state the root cause and guardrails, test normal and adversarial
play, then update the narrative contract, implementation, tests, telemetry, and
next review only when the evidence supports the change.
