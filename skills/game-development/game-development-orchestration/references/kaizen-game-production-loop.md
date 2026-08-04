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
