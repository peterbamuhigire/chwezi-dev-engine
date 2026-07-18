---
name: godot-mobile-game-development
description: Use when building, migrating, profiling, testing, or exporting a Godot mobile game for Android or iOS; covers scenes, nodes, resources, signals, GDScript/C#, saves, plugins, rendering, and export pipelines.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Godot Mobile Game Development
Build a composable Godot project around explicit scene ownership, typed interfaces, resources, signals, testable logic and reproducible exports. Verify every engine-specific instruction against the pinned Godot release.

## Prerequisites

Load `world-class-engineering`, the approved game/system specification, and current official documentation for the pinned Godot version.
<!-- dual-compat-start -->
## Use When
- Implementing or reviewing Godot scenes, nodes, resources, signals, GDScript/C#, plugins or mobile exports.
- Migrating Godot 3-era `Spatial`, `KinematicBody`, old networking, file or export APIs to Godot 4.
## Do Not Use When
- The repository uses Unity or the question is engine-neutral.
- A server, raw SQL or credential is proposed inside an untrusted mobile client.
## Required Inputs
Godot version, language choice, renderer, project tree, target devices/platforms, export templates, plugins, budgets, acceptance criteria and test evidence.
## Workflow
1. Inspect `project.godot`, import settings, autoloads, scenes, resources, scripts, addons and export presets.
2. Define scene composition, node ownership, resource/data boundaries, signal direction and minimal autoload services.
3. Keep reusable rules outside presentation nodes; use typed scripts, explicit dependencies and stable save identifiers.
4. Implement input actions, pause/suspend, save recovery, localisation and mobile lifecycle behaviour.
5. Test gameplay logic, scene integration and export smoke paths; profile the release export on physical devices.
6. Verify Android/iOS toolchain and store requirements against current official Godot and platform documentation.
## Quality Standards
- Prefer signals for decoupled notification, not invisible global control flow.
- Limit autoloads to true process-lifetime services and document reset/testing behaviour.
- Quarantine obsolete Godot 3 syntax and unsafe book examples; never reproduce raw client-to-database patterns.
- Audit third-party addons for licence, maintenance, platform support, permissions, size and failure modes.
## Anti-Patterns
- Deep brittle node paths. Fix: owned references, groups or injected dependencies.
- Every system as an autoload. Fix: scene-local ownership by default.
- Frame logic tied to frame rate. Fix: use the correct process callback and delta/fixed-step rules.
- Assuming desktop export proves mobile readiness. Fix: physical-device release export.
- Client calling database endpoints without a secure service boundary. Fix: authenticated API and server-side validation.
## Outputs
Godot architecture map; version/export manifest; scene/resource contracts; implementation and tests; plugin audit; device profile; signed-export procedure and release evidence.
## References
- [Godot architecture and migration](references/godot-architecture-migration.md)
- [Godot mobile export gates](references/godot-mobile-export-gates.md)
<!-- dual-compat-end -->
## Decision Rules
| Condition | Choice |
|---|---|
| Shared immutable configuration | Resource |
| Reusable visual/behaviour composition | Scene |
| Cross-scene lifetime truly required | Minimal autoload with reset contract |
| Book uses Godot 3 names or APIs | Translate through current migration docs; never paste directly |
## Read Next
Use `mobile-game-performance`, `game-testing-polish`, and `mobile-game-release-liveops` before release.
