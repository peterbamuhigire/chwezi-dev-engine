---
name: unreal-game-development
description: Use when building or restructuring an Unreal Engine game with C++, Blueprints, Gameplay Framework classes, replication, assets, packaging, automation, or Unreal-specific profiling and release evidence.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Unreal Game Development

Build version-pinned Unreal projects with deliberate C++/Blueprint boundaries, explicit gameplay ownership, automated tests, and release-like packaged evidence.

## Use When
- The project uses Unreal Engine, Gameplay Framework, C++, Blueprints, replication, Unreal assets, or Unreal packaging.

## Do Not Use When
- Multiplayer architecture is the primary decision; load `online-multiplayer-and-game-backend` first.
- The exact engine/plugin versions are unknown.

## Required Inputs
Engine/source distribution and version, plugins, target platforms/hardware, network topology, module/asset map, performance budgets, build farm, acceptance criteria, and tests.

## Workflow
1. Inspect `.uproject`, modules, targets, plugins, config, maps, assets, source, automation, and packaging settings.
2. Record boundaries among engine framework classes, C++ domain/components, Blueprints, data assets, subsystems, and online services.
3. Define server/client authority, replicated properties, RPC contracts, relevance/update budgets, and late-join state when networked.
4. Enforce asset naming/dependency and map/cook rules; validate redirectors and unintended hard references.
5. Add automation for pure logic, gameplay integration, multiplayer network profiles, cook/package, and target-hardware smoke tests.
6. Profile and retain packaged-build CPU/GPU/network/memory evidence; preserve symbols and manifests.

## Quality Standards
- Blueprint accessibility is not a reason to hide ownership, authority, or failure handling.
- Exact APIs follow pinned official Unreal documentation, not copied book snippets.
- Editor/PIE success does not replace packaged target or network-condition testing.

## Anti-Patterns

- Gameplay logic split arbitrarily between Blueprint and C++. Fix: define ownership and test seams.
- Hard asset references everywhere. Fix: use managed loading and validate dependency/cook graphs.
- PIE-only acceptance. Fix: test packaged builds on target hardware and network conditions.
- Replication added after single-player design. Fix: establish authority and state ownership first.
- Engine upgrade without a recovery point. Fix: branch, inventory plugins/assets, convert, test, and retain rollback.

## Outputs
Unreal architecture and version manifest; module/Blueprint contract; authority/replication spec; asset validation report; automation results; packaged build evidence.

## References
- [Unreal multiplayer and production gates](references/unreal-production-gates.md)

<!-- dual-compat-start -->
## Evidence Produced

| Category | Artifact | Format | Example |
| --- | --- | --- | --- |
| Correctness | Unreal gameplay and packaging evidence | Project/build output plus Markdown | Gameplay Framework flow, asset validation, automation, package, profile, and recovery |
<!-- dual-compat-end -->

