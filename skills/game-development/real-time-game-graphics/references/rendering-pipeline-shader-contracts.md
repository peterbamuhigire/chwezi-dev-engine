# Rendering Pipeline and Shader Contracts

Parent: [Real-Time Game Graphics](../SKILL.md)

This self-contained reference distils the supplied OpenGL, Vulkan and Unity 2022 material into current-engine-neutral practice. OpenGL fixed-function examples and the supplied Vulkan cookbook's version-specific recipes are historical orientation, not production API authority.

## Frame contract

Document one ordered frame for each quality tier:

1. Acquire a simulation snapshot and camera state.
2. Determine visible renderers, lights and shadow casters.
3. Prepare geometry and material data.
4. Execute depth/opaque work.
5. Execute lighting and shadows according to the active pipeline.
6. Execute transparent, particle and special-effect work in a defined order.
7. Apply only the approved full-screen passes.
8. Composite world-space/screen-space UI with protected readability.
9. Resolve and present with the platform's pacing contract.

For every pass, record inputs, outputs, attachment format, load/store behaviour, resolution, clear policy, producer/consumer, lifetime, debug label and optional-tier rule. Delete a pass whose output is unused.

## Spaces and colour

Name the coordinate space for every shader input and output. A normal in object space cannot be combined with a light direction in world space. Define the normal transform under non-uniform scale.

Name the colour space for textures, lighting calculations, frame buffers, UI and final output. Mark data textures as data rather than colour. Define HDR range, tone mapping and UI composition so authoring tools and runtime agree.

## Shader contract

Each shader or graph records:

| Field | Required content |
|---|---|
| Purpose | Player-visible role and affected materials |
| Stages | Vertex/fragment/compute or engine graph stage |
| Inputs | Attributes, textures, buffers, constants and spaces |
| Outputs | Targets, channels, ranges and alpha convention |
| Variants | Owned keywords and valid combinations |
| Precision | Per-stage precision choice and artefact risk |
| State | Blend, depth, stencil, cull, queue and double-sided policy |
| Cost evidence | Representative capture and tier disposition |
| Fallback | Missing feature/unsupported API behaviour |

Keep vertex transformation, normal transformation and fragment material response separately testable. Compile and validate shaders before runtime where the toolchain allows it. Treat runtime compilation hitches as a release defect unless a bounded warm-up policy covers them.

## Lighting and shadows

Start from the art direction's value hierarchy: focal character, route/interaction cues, threats and background. Choose baked, mixed or dynamic lighting per object mobility, time-of-day needs, memory, authoring cost and target-device captures.

For each light/shadow class, define maximum simultaneous count, influence range, caster policy, update cadence, resolution/tier, bias test scenes and behaviour at quality downgrade. Test thin geometry, grazing angles, moving foliage/characters and camera transitions.

## Materials and transparency

Own a small material taxonomy. State which surfaces share shaders, textures and sampler states. Use property overrides only when they do not break batching/instancing on the selected pipeline.

Transparency requires an order and overlap budget. Test particles, foliage, hair, water, UI and atmospheric layers at their worst screen coverage. Prefer masked/cutout or designed opaque alternatives when blending cost and sorting defects outweigh the visual value.

## Visibility and representation

Use frustum culling, distance/LOD selection and occlusion only after confirming the camera and scene structure make them useful. Protect silhouette and interaction readability across LODs. Verify collider, navigation and shadow representations do not change incorrectly when the render representation changes.

## Native graphics API boundary

OpenGL provides the conceptual programmable pipeline and state-machine model; Vulkan makes pipelines, resources, command recording and synchronisation more explicit. Within a general-purpose engine, these concepts guide diagnosis but do not automatically justify native rendering code.

A native plugin or custom renderer requires an ADR covering feature gap, supported devices/APIs, resource ownership, threading, synchronisation, validation, crash isolation, fallback, maintenance skill, capture tooling and removal plan.
