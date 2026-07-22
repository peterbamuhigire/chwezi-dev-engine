---
name: game-3d-asset-pipeline
description: Use when directing or producing game-ready 3D environments, characters, props, materials, rigs, animations, LODs, collisions, lighting assets, or DCC-to-engine imports; mobile budgets must come from target-device measurement.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game 3D Asset Pipeline
Move verified visual research through concept, modelling, UVs, PBR texturing, rigging, animation, export, import, optimisation and acceptance without losing provenance or device fitness.

## Prerequisites

Load the approved art direction, cultural/reference ledger, `mobile-game-performance`, and the selected engine's import requirements.
<!-- dual-compat-start -->
## Use When
- Creating art direction, asset briefs, Maya/Blender models, Substance-style textures, rigs, clips, LODs, collisions or engine import presets.
## Do Not Use When
- Designing UI appearance without the design-system engine, or inventing cultural references without research and consultation.
## Required Inputs
Art pillars, reference/rights ledger, target camera and devices, engine/renderer, real-world scale, asset inventory, simultaneous counts, material/texture contract, animation needs and measured budgets.
## Workflow
1. Approve reference provenance, gameplay purpose, silhouette, scale, value hierarchy and cultural review.
2. Produce production-facing turnarounds, scale/material/animation callouts and a technical asset brief.
3. Block out in engine before detail; validate camera, traversal, touch readability and modular dimensions.
4. Model for silhouette and deformation; validate topology, normals, pivots, hierarchy and transforms.
5. Unwrap to the project seam, padding and texel-density policy; bake and texture non-destructively under neutral and final lighting.
6. Rig, skin and test extreme poses; author named clips, root-motion policy, sockets, events and transition poses.
7. Export through a versioned contract; rebuild materials in engine; create simple colliders, LODs and import presets.
8. Test stress scenes on the minimum device and feed defects back to source assets.
## Quality Standards
- Count runtime triangles, material slots, texture memory, bones, overdraw, lights, particles and animation memory in context.
- Derive numeric budgets from representative scenes and target-device profiling, not book examples.
- Keep source files, licences, contributor rights, references and derived assets traceable.
- Require visible state variants for interactable, damaged, harvested, inactive or completed objects where gameplay needs them.
## Anti-Patterns
- Detailed model before engine blockout. Fix: validate scale and silhouette first.
- Generic “African” visual borrowing. Fix: source-specific research, consultation and provenance.
- Render mesh as collider. Fix: deliberate simplified collision.
- Huge textures justified by hero status. Fix: screen-coverage and memory evidence.
- DCC viewport treated as engine parity. Fix: material and lighting acceptance in target renderer.
## Outputs
Art bible; reference/rights ledger; asset inventory and briefs; budget profile; DCC/export/import contracts; accepted source and runtime assets; QA reports; stress-scene/device evidence.
## References
- [Concept-to-engine 3D pipeline](references/concept-to-engine-pipeline.md)
- [Asset acceptance and mobile budgets](references/asset-acceptance-mobile-budgets.md)
- [Practical 3D scene evidence](references/practical-3d-scene-evidence.md)
<!-- dual-compat-end -->
## Decision Rules
| Condition | Choice |
|---|---|
| Detail does not affect silhouette or survive gameplay distance | Put it in texture or remove it |
| Asset repeats often | Prioritise instancing, shared materials and lower-cost variants |
| Deformation is visible | Topology and skin tests dominate static beauty |
| Budget is not measured on device | Mark provisional; do not scale content |
## Read Next
Use `real-time-game-graphics` for material/lighting/render integration, `mobile-game-performance` for budgets, and `game-testing-polish` for visual regression and acceptance.
