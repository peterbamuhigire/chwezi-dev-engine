---
name: blender-game-asset-production
description: Use when producing, automating, or reviewing Blender source assets, characters, rigs, animations, props, vehicles, collisions, LODs, FBX/glTF exports, or Blender-to-engine validation; use game-3d-asset-pipeline for DCC-neutral art direction and budgets.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Blender Game Asset Production

Turn an approved game-asset brief into version-pinned Blender source, reproducible exports, and target-engine evidence without confusing a viewport result with a runtime-ready asset.

## Prerequisites

Load `world-class-engineering`, `game-3d-asset-pipeline`, the selected engine skill, `mobile-game-performance` when mobile is in scope, and the project's research, cultural, rights, and art-direction controls.

<!-- dual-compat-start -->
## Use When

- Building or repairing `.blend` characters, props, vehicles, environments, rigs, shape keys, clips, collisions, sockets, LODs, or export presets.
- Defining Blender file organisation, linked-library boundaries, naming, transforms, axes, units, pivots, or source-control rules.
- Automating Blender validation or export and checking the imported runtime asset.
- Reviewing a Blender production line for repeatability, deformation quality, engine compatibility, or target-device cost.

## Do Not Use When

- The decision is DCC-neutral art direction, portfolio budgeting, or simultaneous on-screen cost; use `game-3d-asset-pipeline` first.
- The primary task is engine-side shaders, lighting, rendering, or profiling; use `real-time-game-graphics` and the selected engine skill.
- The source is a cinematic render with no real-time export requirement; use the appropriate animation or visual-production route.

## Required Inputs

| Artefact | Produced by | Required? | Missing-input response |
|---|---|---:|---|
| Asset brief, reference/rights ledger, camera and gameplay purpose | Art, design, research and rights owners | yes | Stop modelling and return the missing decision list. |
| Pinned Blender version, enabled extensions, export format and target-engine import contract | Technical art and engine owners | yes | Produce only a provisional spike; do not claim compatibility. |
| Runtime budgets, simultaneous counts, skeleton/animation needs and target hardware | Performance, gameplay and production owners | yes | Mark numeric acceptance provisional and block scale-up. |
| Existing `.blend`, export, import preset, build and profiler evidence | Repository and release owners | conditional | Record the absent lineage and restrict the review to design intent. |

## Workflow

1. Record Blender version, extensions, colour management, unit/axis convention, naming, folder layout, ownership, licences and target-engine version.
2. Validate the brief in a representative engine greybox before detailed modelling; settle scale, silhouette, pivots, modular seams, deformation zones and camera readability.
3. Separate editable source, linked libraries, animation scenes, generated exports and engine imports. Keep generated files reproducible from named source revisions.
4. Model, retopologise, unwrap, bake and texture against measured runtime needs; preserve transforms, normals, material slots, texel policy and provenance.
5. For characters, define export skeleton, control/mechanics layers, weights, influence limits, correctives, facial method, sockets and animation clip contract before polishing controls.
6. Build simplified collision and measured LODs/HLODs; validate switching, bounds, shadows, physics and repeated-instance cost in engine.
7. Export through a pinned preset or automation path. Re-import into a clean scene or target project and compare scale, hierarchy, normals, materials, skeleton, curves and clip identities.
8. Run structural validators, deformation/animation tests, engine stress scenes and target-hardware profiling. Retain failed cases and the exact source/export/import/build lineage.
9. Stop when the exporter, engine importer, asset rights, skeleton contract, measured budget or clean re-import fails. Recover by narrowing to a reproducible asset spike.

## Outputs

| Artefact | Consumed by | Acceptance condition |
|---|---|---|
| Blender production contract and source layout | Artists, technical artists and build engineering | Version, ownership, naming, dependencies and generated boundaries are explicit. |
| Validated source assets and export presets | Engine/content implementers | A clean-machine export and target-engine import reproduce the approved result. |
| Rig/animation contract where applicable | Animators and gameplay engineers | Skeleton, controls, deformation, clips, events, root motion and sockets are testable. |
| Asset acceptance and lineage report | QA, performance and release | Source revision, export, import, build, scene, hardware, result and limitations are recorded. |

## Evidence Produced

| Category | Artifact | Format | Example |
|---|---|---|---|
| Correctness | Structural, deformation and clean re-import report | Matrix in `references/blender-production-contract.md` | `docs/art/blender-asset-acceptance.md` |
| Performance | Engine stress-scene and target-hardware capture | Risk-based test evidence | `docs/performance/asset-stress-scene.md` |
| Release evidence | Source/export/import/build lineage manifest | Manifest schema in the production contract | `docs/release/asset-lineage.yaml` |
| UX quality | Camera-distance readability and animation review | Named build, scene and review record | `docs/art/readability-review.md` |
<!-- dual-compat-end -->

## Capability and permission boundaries

Require read and search for review. Editing `.blend` sources, running exporters, installing extensions, or changing engine imports requires task authority and reversible copies. Publishing assets, accepting licences, purchasing add-ons, or mutating a release branch requires accountable approval.

## Degraded mode

Without Blender execution or target-engine import, return a qualified production contract and inspection checklist. Mark export, deformation, material parity and runtime cost `not assessed`; never infer them from screenshots.

## Decision Rules

| Condition | Action | Failure avoided |
|---|---|---|
| Blender or exporter version is not pinned | Freeze the candidate toolchain before production. | Version drift and irreproducible export. |
| Detail does not affect silhouette, deformation or gameplay distance | Bake, texture, instance or remove it. | Source complexity with no player value. |
| Control rig feature cannot survive export | Bake to the export skeleton or reproduce it in engine. | DCC-only motion. |
| LOD or collision cost is unmeasured | Test representative simultaneous counts in engine. | Tutorial budgets treated as product evidence. |
| Current official behaviour conflicts with a supplied book | Follow the pinned official documentation and record the divergence. | Legacy Blender or engine instructions entering production. |

## Quality Standards

- Keep every book-derived rule self-contained in the linked references; never require the original book path at execution time.
- Treat Blender 2.x, 3.5 and host-specific exporter instructions as historical until verified for the pinned toolchain.
- Require deterministic names, transforms, dependencies, export selection and clip identities.
- Inspect the runtime asset in the target renderer and a release-like build.
- Apply cultural provenance and rights review before modelling or publishing historical content.

## Anti-Patterns

- Detailing before an engine blockout. Fix: prove scale, silhouette and camera distance first.
- Applying transforms or modifiers blindly at export. Fix: define their source and exported-state policy per asset class.
- One armature mixing animator controls and exported bones without separation. Fix: isolate a stable deformation/export skeleton.
- Automatic weights accepted without extreme-pose tests. Fix: inspect joints, twist, facial and prop-contact poses.
- One beauty render accepted as evidence. Fix: retain clean re-import, stress-scene and target-build captures.
- Manual export folklore. Fix: store a pinned preset or automated, reviewable export path.
- Copying numeric budgets from a tutorial. Fix: derive them from project scenes and target hardware.

## Read Next

- `game-3d-asset-pipeline` for art direction, inventory and DCC-neutral runtime budgets.
- `real-time-game-graphics` for target-renderer material and lighting integration.
- `game-ai-behaviour-and-navigation` when collision, navigation or interaction affordances depend on AI.
- `game-testing-polish` and `game-build-release-engineering` for asset regression and promoted-build evidence.

## References

- [Blender production contract](references/blender-production-contract.md)
- [Rig, animation, and export gates](references/rig-animation-and-export-gates.md)
- [Game-development source register](../../../docs/game-dev-analysis/source-register.md)
