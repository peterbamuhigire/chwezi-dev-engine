---
name: unity-mobile-game-development
description: Use when building, restructuring, profiling, testing, or packaging a Unity mobile game in C# for Android or iOS; covers project architecture, scenes, prefabs, data, input, assets, saves, builds, and Unity-specific release evidence.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Unity Mobile Game Development
Build a Unity game as modular, testable C# systems with reproducible mobile builds and measured target-device behaviour. Verify APIs and package guidance against the project's exact Unity version.

## Prerequisites

Load `world-class-engineering`, the approved game/system specification, and current official documentation for the pinned Unity version.
<!-- dual-compat-start -->
## Use When
- Creating or changing a Unity game, C# component, scene, prefab, ScriptableObject, mobile build, or Unity test.
- Migrating legacy UnityScript, old scene loading, input, UI, render-pipeline, networking, or platform code.
## Do Not Use When
- The project uses Godot; use `godot-mobile-game-development`.
- The task is engine-neutral design, art, audio, performance strategy, or release operations.
## Required Inputs
Repository and Unity version, render pipeline, target platforms/devices, package manifest, architecture, acceptance criteria, performance budgets, build/signing posture, and existing tests.
## Workflow
1. Inspect project settings, packages, assemblies, scenes, prefabs, assets, build scripts and tests before editing.
2. Record an ADR for costly choices: render pipeline, input, asset delivery, save model, scene flow, third-party SDKs and backend boundary.
3. Keep pure domain/gameplay logic separate from `MonoBehaviour`; use composition, explicit interfaces and event ownership.
4. Define a bootstrap/composition root, additive scene policy, prefab boundaries, data assets, lifetime rules and deterministic save identifiers.
5. Use the current supported input, UI, async loading, addressable-content and build paths verified for the pinned editor version.
6. Add edit-mode tests for pure logic, play-mode tests for integration, and physical-device smoke tests.
7. Profile development and release-like IL2CPP builds on the device panel; close with reproducible build and rollback evidence.
## Quality Standards
- Pin editor and package versions; commit text-serialised project assets and review dependency changes.
- Avoid hidden global state, stringly typed scene/object lookup, per-frame allocation, synchronous heavy I/O, and unbounded `Update` work.
- Keep secrets out of client builds and treat every analytics, ads, IAP or social SDK as a privacy, size, performance and failure dependency.
- Do not copy obsolete book APIs into production; translate the durable pattern into current official APIs.
## Anti-Patterns
- `Find` calls and singleton sprawl. Fix: explicit composition and scoped services.
- Business rules inside scene components. Fix: testable C# domain classes.
- One giant persistent scene. Fix: bounded additive scenes and ownership rules.
- Optimising only in Editor. Fix: device profiler and release-like build evidence.
- Upgrading packages casually. Fix: ADR, compatibility check, backup, tests and measured diff.
## Outputs
Unity architecture map; project/version manifest; system and scene specifications; implementation and tests; device profile; build pipeline; Unity-specific release evidence and residual-risk record.
## References
- [Unity project architecture](references/unity-project-architecture.md)
- [Legacy Unity migration and mobile build gates](references/unity-mobile-build-gates.md)
<!-- dual-compat-end -->
## Decision Rules
| Condition | Choice |
|---|---|
| Exact API/package behaviour is version-sensitive | Check official docs and package changelog before coding |
| Logic can run without Unity objects | Keep it in a plain C# assembly and unit-test it |
| Asset is large, optional or patchable | Evaluate addressable/remote delivery with offline failure handling |
| Plugin lacks maintenance, privacy or rollback evidence | Do not admit it |
## Read Next
Use `gameplay-systems-architecture`, `game-math-and-simulation`, `real-time-game-graphics`, `mobile-game-performance`, and `game-testing-polish` for their respective gates.
