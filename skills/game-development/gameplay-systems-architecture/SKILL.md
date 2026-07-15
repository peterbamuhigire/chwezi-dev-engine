---
name: gameplay-systems-architecture
description: Use when specifying or implementing engine-neutral gameplay systems such as movement, combat, AI, quests, dialogue, inventory, progression, save/load, world state, spawning, cameras, or narrative state; engine skills own framework integration.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Gameplay Systems Architecture
Turn game rules into deterministic, inspectable systems with clear state, ownership, events, persistence and test seams.

## Prerequisites

Load the approved player verbs and system requirements, `world-class-engineering`, and the selected engine skill for integration constraints.
<!-- dual-compat-start -->
## Use When
- Designing or coding combat, AI, interaction, quests, dialogue, inventory, abilities, progression, cattle/herd, companions, world state, camera or saves.
## Do Not Use When
- Selecting the overall game concept or implementing engine packaging.
## Required Inputs
Approved player verbs, rules and invariants; system dependencies; content schema; save compatibility; target scale; failure cases; determinism and networking needs.
## Workflow
1. Write the system promise, authoritative state, invariants, inputs, outputs, events and failure modes.
2. Model explicit states and transitions; separate simulation, presentation, authoring data and persistence.
3. Choose event, command, query and ownership boundaries; prevent circular dependencies.
4. Design data schemas and stable IDs before authoring large content sets.
5. Add deterministic tests for rules, integration tests for boundaries, save migrations, debug views and telemetry.
6. Integrate through the chosen engine's composition root and profile worst-case content.
## Quality Standards
- Make time, randomness, identity and persistence injectable or reproducible where tests require it.
- Version save data and content schemas; recover safely from corruption and interrupted writes.
- Treat AI as readable state/utility/behaviour logic with perception and action budgets, not uncontrolled per-frame search.
- Keep narrative branches, quests and dialogue data-validatable and localisation-safe.
## Anti-Patterns
- God object player controller. Fix: capability components and orchestrated state.
- Events with no owner or lifecycle. Fix: explicit subscription and cleanup contract.
- Save by serialising scene objects blindly. Fix: versioned domain snapshot and migration.
- AI state hidden across coroutines. Fix: explicit state and debug trace.
- Content authored before schema validation. Fix: validators and stable identifiers first.
## Outputs
System specification; state/sequence diagrams; data schema; interfaces/events; implementation plan; automated tests; debug tooling; save migration and performance evidence.
## References
- [Gameplay systems patterns](references/gameplay-systems-patterns.md)
- [Save, quest and narrative state](references/persistence-narrative-state.md)
<!-- dual-compat-end -->
## Decision Rules
| Need | Pattern |
|---|---|
| Mutually exclusive behaviour modes | Explicit state machine |
| Many scored alternatives | Utility selection with inspectable scores |
| Authored sequential objective flow | Validated quest graph |
| Cross-system notification without command authority | Typed event |
| Durable player/world state | Versioned snapshot plus migrations |
## Read Next
Use `game-math-and-simulation` for spatial, time, probability and numerical contracts; use the selected engine skill for integration and `game-testing-polish` for systemic and playtest validation.
