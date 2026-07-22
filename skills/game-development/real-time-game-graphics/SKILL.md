---
name: real-time-game-graphics
description: Use when designing or diagnosing a game's render pipeline, shaders, materials, lighting, shadows, visibility, post-processing, GPU resources, frame graph, graphics API, or visual-performance trade-offs; use game-3d-asset-pipeline for content and mobile-game-performance for measured budgets.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---

# Real-Time Game Graphics

Engineer a coherent image from camera to presentation while keeping visual intent, GPU work, memory traffic, synchronisation and target-device evidence visible.

## Prerequisites

Load the approved visual direction, `game-math-and-simulation`, `game-3d-asset-pipeline`, `mobile-game-performance`, and the selected engine's current rendering documentation.

<!-- dual-compat-start -->
## Use When

- Selecting or configuring a render pipeline, graphics API, colour/HDR policy, lighting model, shadow strategy or post stack.
- Writing or reviewing shaders, materials, render features, compute work, command/resource lifetimes or frame-graph passes.
- Diagnosing overdraw, draw submission, bandwidth, shader variants, GPU stalls, visual instability or renderer-specific device defects.

## Do Not Use When

- The request is only to model, texture, rig or import assets; use `game-3d-asset-pipeline`.
- The request is a general performance investigation without a GPU/rendering diagnosis; start with `mobile-game-performance`.
- Native Vulkan/OpenGL work is proposed inside a Unity/Godot title without a measured engine limitation and ADR.

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---:|---|
| Visual direction and readability hierarchy | art/game direction | yes | Defines the image the renderer must protect |
| Camera, coordinate and lighting contract | `game-math-and-simulation` | yes | Prevents transform and shading ambiguity |
| Representative scenes and device matrix | performance owner | yes | Grounds budgets and API support |
| Engine, render-pipeline and package versions | engine owner | yes | Controls valid features and diagnostics |

## Workflow

1. Write the visual promise and the gameplay information the frame must communicate.
2. Map the frame from simulation snapshot through culling, geometry, lighting, transparency, post-processing, UI and presentation; name every intermediate resource and owner.
3. Choose engine pipeline and graphics API from target-device evidence, tooling, feature needs and failure recovery, not novelty.
4. Establish material, shader keyword/variant, light, shadow, transparency, render-texture and post-effect contracts.
5. Build a representative scene and a worst-case stress scene before content scale-up.
6. Capture CPU render submission, GPU timings, render passes, bandwidth proxies, overdraw, residency and shader compilation evidence on physical devices.
7. Remove unused passes/resources, reduce the limiting cost, and re-run the same capture. Preserve before/after evidence and visual-regression images.
8. Define quality tiers and safe fallbacks that protect silhouette, UI, navigation cues and cultural/art-direction essentials.

## Quality Standards

- Treat visibility, lighting, material response, transparency and post-processing as an ordered system; a beautiful isolated shader does not prove a frame.
- Keep shader inputs, coordinate spaces, colour spaces, texture formats and precision explicit.
- Use validation layers and GPU debuggers where the active API/toolchain supports them; warnings require disposition, not suppression by habit.
- Measure stable frame pacing and sustained thermal behaviour, not only a short peak frame rate.
- Verify current Unity, Android, Vulkan, OpenGL or platform guidance in primary documentation before encoding API/version claims.

## Decision Rules

| Evidence | Choice | Failure avoided |
|---|---|---|
| Engine pipeline meets visual and device gates | Stay within engine abstractions | Native-plugin complexity without product value |
| GPU fragment/bandwidth bound | Reduce overdraw, sampled data, attachments, resolution or expensive lighting/post | Triangle-only optimisation misses the bottleneck |
| CPU submission bound | Reduce state changes, renderers, variants and draw submission cost | Lowering texture quality does not help |
| Shader variant growth is unbounded | Constrain keywords and build a used-variant policy | Build size, warm-up and runtime hitch risk |
| Essential cue disappears on low tier | Redesign the tier; do not disable the cue | Performance option makes gameplay inaccessible |

## Capability Contract

Read/search access to project settings, shaders, materials and captures is required. Execute profiling and image comparisons when available. Network access may verify current official documentation. Without physical-device/GPU evidence, issue a provisional design and block production-budget claims.

## Degraded Mode

If the renderer, API, device or representative scene is unknown, produce the frame contract and experiment plan only. Do not prescribe fixed polygon, draw-call, texture or shader budgets from books.

## Anti-Patterns

- Choosing Vulkan because it is lower level. Fix: prove a feature, stability or measured performance need.
- Adding post effects before base lighting/readability works. Fix: validate the unprocessed frame first.
- One material instance per object by default. Fix: define sharing, instancing and property-override policy.
- Transparent layers covering the screen. Fix: inspect overdraw and redesign effect coverage.
- Unlimited shader keywords. Fix: own a variant matrix and strip only with evidence.
- Hiding synchronisation or resource-lifetime defects behind extra waits. Fix: model hazards and ownership explicitly.
- Optimising away navigation, subtitle or interaction cues. Fix: make readability a non-degradable tier constraint.

## Outputs

| Artefact | Consumed by | Acceptance condition |
|---|---|---|
| Rendering architecture and frame-pass map | engine/graphics team | Passes, resources, dependencies, spaces and fallbacks are explicit |
| Shader/material/lighting contract | art and engineering | Inputs, variants, precision, colour and acceptance specimens are defined |
| Graphics profile and tier plan | `mobile-game-performance` and QA | Same-scenario device captures support every budget decision |
| Visual regression pack | `game-testing-polish` | Intended differences and protected cues are reviewable |

## References

- [Rendering pipeline and shader contracts](references/rendering-pipeline-shader-contracts.md)
- [Mobile graphics budgets and diagnostics](references/mobile-graphics-diagnostics.md)
<!-- dual-compat-end -->

## Read Next

Use the selected engine skill for implementation, `mobile-game-performance` for the full device budget, and `game-testing-polish` for visual and compatibility gates.
