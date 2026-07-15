# Game-development deepening — evidence synthesis, 15 July 2026

## Purpose

This note records how the second game-engineering source set was used to deepen the existing `skills/game-development/` family. It is a disposition record, not a substitute for the new skills or their operational references.

The appraisal performance report named in the original request was excluded before analysis and contributed nothing to this work.

## Source disposition

| Supplied Markdown source | Usable evidence | Applied contribution | Quarantine or gap |
|---|---:|---|---|
| Borromeo, *Hands-On Unity 2022 Game Development*, 3rd ed. (2022) | yes; 10,703 lines | scenes/components/prefabs, input and physics, AI/state machines, URP/shaders/VFX/lighting, UI, animation/camera/timeline, profiler/frame debugger/memory profiler and builds | Unity 2022 package names, APIs and build screens are not current-version authority |
| Baker et al., *Computer Graphics with OpenGL* | yes; 30,011 lines | primitives, transformations, viewing, modelling/animation, visibility, illumination, texturing, shaders and the mathematics appendix covering matrices, quaternions, curves, normals and numerical methods | legacy OpenGL calls and historical hardware assumptions are concept sources only |
| Łapiński, *Vulkan Cookbook* | yes; 18,590 lines | explicit device/resource/memory ownership, synchronisation, descriptor sets, render passes, shaders/SPIR-V, graphics/compute pipelines and command recording | recipe code and Vulkan-version details require current official verification; no recipe was copied into an engine mandate |
| Boeira, *Lean Game Development*, 2nd ed. (2023) | yes; 5,682 lines | inception, risky assumptions, hypotheses, MVP/MVG/prototype selection, automated tests, CI, measurement, analysis, iteration and consolidated learning | “minimum viable” is not permission to lower cultural, accessibility, player-safety or release quality |
| *Basic Math for Game Development with Unity 3D* supplied Markdown | no; 154 bytes, title only | none | content missing; explicitly rejected as evidence |

## Synthesis decisions

Three narrow skills were added rather than expanding the existing ten skills into monoliths:

1. `game-math-and-simulation` owns coordinate spaces, units, clocks, transforms, quaternions, interpolation, probability, deterministic streams, numerical failure handling and test vectors.
2. `real-time-game-graphics` owns image-pipeline, shader/material, lighting/shadow, visibility, resource/synchronisation, tier-fallback and GPU-diagnostic contracts.
3. `lean-game-product-development` owns inception, falsifiable hypotheses, prototype fidelity, evidence thresholds, harm/stop thresholds and go/narrow/pivot/repeat/stop decisions.

The family orchestrator and relevant Unity, gameplay, asset, performance, testing and design skills now hand off explicitly to these specialists.

## Primary-source refresh

Version-sensitive claims were checked against primary sources on 15 July 2026:

- Unity identifies Unity 6.3 as its current LTS line and lists support through December 2027: <https://unity.com/releases/unity-6/support>.
- Unity’s profiling guidance requires target-platform/device evidence because Editor results are only an approximation: <https://docs.unity3d.com/2022.2/Documentation/Manual/profiler-profiling-applications.html>.
- Android’s games optimisation guidance treats performance as a frame-pacing, CPU/GPU, memory, thermal and device problem: <https://developer.android.com/games/optimize/overview>.
- Android Frame Pacing is the official rendering-presentation integration surface checked for supported games: <https://developer.android.com/games/sdk/frame-pacing>.
- The Vulkan specification and guide remain the authority for pipeline and synchronisation semantics: <https://docs.vulkan.org/spec/latest/chapters/pipelines.html> and <https://docs.vulkan.org/guide/latest/synchronization.html>.

The skills intentionally avoid freezing a Unity patch, Android target level, device budget or Vulkan recipe. Each implementation must pin and verify its own current toolchain.

## Project application

The synthesis was specialised into:

- a cross-title Chwezi game-development excellence standard;
- The Open Ground simulation/graphics/lean blueprint for *Great Journey: Children of the River*;
- The Broken Causeway movement/camera/herd/graphics/lean blueprint for *Moon Over Kitara*.

All three retain the platform wellbeing standard: voluntary mastery, curiosity, attachment and consequence are permitted; streak loss, energy gates, paid randomness, real-time punishment, pay-to-recover and emotional rescue purchases are prohibited.

## Residual evidence gaps

No supplied book proves fun, market fit, device performance, cultural permission, award success or title-specific retention. Those remain hypotheses requiring named playtests, consultant review and physical-device traces. The missing Basic Math content should be re-supplied only if the user wants its unique claims assessed; the operational mathematics skill is self-contained without it.
