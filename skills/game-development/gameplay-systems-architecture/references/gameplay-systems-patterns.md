# Gameplay systems patterns

Back to [Gameplay Systems Architecture](../SKILL.md).

For each system define promise, authoritative state, invariants, commands, queries, events, states/transitions, dependencies, time/randomness, persistence, content schema, failure recovery, debug view, telemetry and tests.

Use state machines for exclusive modes, utility scoring for inspectable choice, command queues for ordered actions, events for notification, pools only for measured churn, and spatial/temporal LOD for costly AI. Separate sensing, decision, locomotion and action. Spread herd perception work and define fallback/path-recovery behaviour.
