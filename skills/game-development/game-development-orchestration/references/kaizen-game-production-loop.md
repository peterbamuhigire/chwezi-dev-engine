# Kaizen Game Production Loop

Use with the game orchestration lifecycle and `sdlc-meta/kaizen-improvement-system`.

## Loop

1. State the player/product hypothesis and the smallest testable slice.
2. Observe the real playtest or runtime: player behaviour, comprehension, fun/friction, narrative clarity, accessibility, AI behaviour, performance, and failure paths.
3. Record evidence and compare it with the expected outcome; do not convert a single anecdote into a conclusion.
4. Choose one reversible countermeasure and define a success threshold, guardrail, owner, and stop rule.
5. Re-test with the same scenario plus an adversarial or accessibility case.
6. Standardise only the change that improves the target without violating safety, performance, narrative, or platform constraints.
7. Update the game brief, requirements, system contract, test evidence, telemetry, and next experiment.

## Book-informed applications

- Treat steering, finite-state machines, pathfinding, flocking, and scripting as foundations, not current engine APIs; add modern engine and performance verification before implementation.
- Treat story, character, gesture, silhouette, framing, and composition as cross-disciplinary system inputs. Narrative and visual decisions must be testable in gameplay, not isolated in a writer or art document.
- Preserve player agency, accessibility, localisation, privacy, economy integrity, and rollback as product-quality constraints.

## Two-level 65-to-95 contract

Run this loop at both levels:

| Level | Initial analysis | Improvement target |
|---|---|---|
| Engine | Audit routes, skills, references, fixtures, validators, handoffs, and game-family coverage; publish `min(raw_score, 65)`. | Improve one capability or routing gap toward 95/100, then re-run catalogue and representative fixtures. |
| Product | Audit the player promise, mechanics, narrative meaning, performance, accessibility, safety, economy, telemetry, and release evidence; publish `min(raw_score, 65)`. | Run one reversible product experiment toward 95/100 with owner, measure, guardrail, stop/rollback, and acceptance evidence. |

Never raise the published initial score because a plan was written. Standardise a
winning change only after the relevant evidence passes and update the owning skill,
reference, contract, test, telemetry, and next review.
