---
name: mobile-game-performance
description: Use when establishing or enforcing mobile-game frame-time, memory, loading, storage, network, battery, thermal, rendering, physics, AI, audio, and asset budgets through physical-device profiling; not for speculative optimisation.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Mobile Game Performance
Measure sustained player experience on representative devices, identify the limiting subsystem, change one cause at a time, and block regressions with evidence.

## Prerequisites

Load `world-class-engineering`, the target-device definition, representative scenarios and the selected engine profiler workflow.
<!-- dual-compat-start -->
## Use When
- Setting device tiers or budgets; investigating hitching, low FPS, heat, battery drain, memory kills, long loads, large installs, overdraw, GC, physics, AI or audio cost.
## Do Not Use When
- No reproducible scenario, target device or profiler evidence exists.
## Required Inputs
Device matrix, target experience/frame rate, representative and stress scenes, release-like build, profiler captures, thermal conditions, budgets, change history and player-visible symptom.
## Workflow
1. Define minimum/target/high devices by real chipset/GPU, RAM, OS, resolution, storage and market relevance.
2. Set per-scenario CPU, GPU, frame pacing, memory, load, package, battery and thermal budgets as provisional hypotheses.
3. Reproduce on a physical device using a release-like instrumented build and controlled scenario.
4. Determine CPU, GPU, memory, I/O, network or thermal bound; inspect subsystem markers and allocation/streaming behaviour.
5. Change the highest-impact cause, rerun the same capture, compare, and retain before/after evidence.
6. Build quality tiers and sustained-load degradation paths; test pause/resume and background recovery.
7. Add CI/static budget checks and periodic device regression tests.
## Quality Standards
- Prefer stable frame pacing over unstable peaks; measure percentiles and hitches, not only average FPS.
- Profile sustained play long enough for heat and battery effects to emerge.
- Record renderer, resolution, quality tier, build, scene, device, temperature, power state and capture method.
- Verify current Android, Apple, Unity or Godot guidance from official documentation before encoding platform numbers.
## Anti-Patterns
- Optimising in editor only. Fix: release-like device capture.
- Universal polygon or texture budget copied from a book. Fix: measured asset and scene budgets.
- Pooling everything. Fix: prove churn and account for retained memory.
- Lowering resolution without UX review. Fix: controlled quality tiers and readability checks.
- One flagship phone. Fix: minimum/target/high matrix.
## Outputs
Device matrix; scenario budget; capture protocol; profiler evidence; bottleneck diagnosis; optimisation change log; quality tiers; regression gate and residual-risk report.
## References
- [Profiling and budget playbook](references/profiling-budget-playbook.md)
- [Rendering, memory and thermal checklist](references/rendering-memory-thermal.md)
<!-- dual-compat-end -->
## Decision Rules
| Evidence | Action |
|---|---|
| GPU-bound | Reduce overdraw, shader/material/light/shadow/resolution cost by measured impact |
| Main-thread CPU-bound | Reduce scripts, physics, AI, animation and submission work |
| Memory pressure | Fix residency, duplication, texture/audio/mesh footprint and unload policy |
| Thermal decline | Lower sustained workload and add adaptive quality; do not chase burst benchmark |
## Read Next
Use `real-time-game-graphics` for render-pipeline diagnosis, the relevant engine and asset/audio skills for implementation, and `game-testing-polish` for regression release gates.
