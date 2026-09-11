---
name: level-world-and-content-production
description: Use when designing and producing game levels, worlds, encounters, missions, narrative content, procedural generation, streaming partitions, content schemas, validation, pacing, or multidisciplinary content handoffs.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Level, World, and Content Production

Turn design intent into versioned, testable content that a multidisciplinary team can produce at a measured rate.

## Use When
- Building levels, encounters, missions, dialogue/narrative packages, world partitions, spawning rules, or procedural content.

## Do Not Use When
- Core game-system architecture or asset creation is the primary task.

## Required Inputs
Player verbs, design pillars, content schema, camera/input, target performance, progression dependencies, accessibility/localisation constraints, asset kit, streaming/save model, throughput estimate, owners, and playtest questions.

## Workflow
1. Define level/encounter goals, teaching/test beats, pacing, metrics, dependencies, completion/failure, and observability.
2. Establish modular kits, naming/ownership, greybox-to-final gates, content schemas, validation, and review cadence.
3. Make streaming, checkpoints, save identifiers, spawn/despawn, navigation, and procedural seeds deterministic and migration-safe.
4. Test impossible states, sequence breaks, backtracking, interruption, low-memory streaming, localisation expansion, accessibility routes, and missing content.
5. Measure throughput and rework by content type; recalibrate schedule rather than hiding variance.

## Quality Standards

- Every level exposes a player goal, readable route, meaningful choice, recoverable failure, and exit.
- Streaming, navigation, collision, encounter, save, accessibility, and device budgets are measured.
- Content schemas and validators catch missing dependencies before manual play review.
- Throughput forecasts use observed cycle time and rework rather than asset-count optimism.

## Anti-Patterns

- Greybox skipped. Fix: prove traversal, pacing, and encounter logic before finish art.
- Landmark without gameplay purpose. Fix: connect orientation, decision, payoff, or story function.
- Procedural output accepted unseen. Fix: validate seeds, bounds, solvability, repetition, and fallback.
- Streaming tuned in editor. Fix: capture release-like target-device traversal.
- Schedule hides rework. Fix: measure queue, blocked time, rejection, and revision by content type.

## Outputs
Content bible/schema; level and encounter briefs; dependency/streaming map; validators; playtest evidence; throughput forecast and variance; acceptance manifest.

## References
- [Content production gates](references/content-production-gates.md)

<!-- dual-compat-start -->
## Evidence Produced

| Category | Artifact | Format | Example |
| --- | --- | --- | --- |
| UX quality | Level traversal and content acceptance report | Markdown plus play capture | goal, route, pacing, encounter, streaming, accessibility, failure, and device budget |
<!-- dual-compat-end -->

