# Mobile Graphics Budgets and Diagnostics

Parent: [Real-Time Game Graphics](../SKILL.md)

This self-contained reference combines durable principles from the supplied graphics books with current official-tool expectations. Numeric budgets are always project measurements; the book examples are not device targets.

## Representative capture protocol

Record:

- build identifier, engine/render-pipeline/API and scripting backend;
- device model, SoC/GPU, RAM, OS, display resolution/refresh and power state;
- quality tier, render scale and target frame rate;
- scene, route, camera path, duration and input script;
- cold/warm state, ambient conditions and capture tool;
- CPU main/render time, GPU time, frame-time percentiles/hitches, memory, temperature/thermal state and battery trend.

Use the same route before and after each change. A screenshot without a timing capture proves image parity only; a timing capture without a screenshot can hide a visual regression.

## Bottleneck ladder

| Evidence | Inspect next | Typical experiment |
|---|---|---|
| GPU fragment or bandwidth bound | overdraw, resolution, texture sampling, attachments, post, blending, shadows | disable one pass or reduce coverage at a time |
| GPU geometry/vertex bound | visible vertices, skinning, LOD, shadow casters | fixed camera with controlled LOD/caster change |
| CPU render/submission bound | renderer count, material/state changes, culling and command generation | consolidate proven repeated work |
| Shader/pipeline hitch | compilation, variant warm-up, pipeline cache and asset arrival | trace first-use and repeat-use frames |
| Memory pressure | texture/render-target/mesh residency, duplication and unload | capture snapshots before/after scene transitions |
| Thermal decline | sustained CPU/GPU clocks and workload | lower target/tier, then repeat long-session path |

Do not optimise by checklist order. Start with the measured limiter.

## Mobile/tile-GPU questions

Ask whether a pass forces extra full-screen bandwidth, render-target resolves, framebuffer reads or attachment stores. Count render targets and their formats at each resolution. A visually small effect can still be expensive when it touches every pixel.

Avoid unnecessary clears, attachments and render passes. Prefer compact texture formats and precision only after checking visible artefacts on the minimum device. Validate ASTC/ETC variants on actual supported GPUs; do not assume one compression result represents every device.

## Quality tier contract

Define tier changes in an ordered table:

| Protected | May degrade | Must never happen |
|---|---|---|
| UI/subtitles, interaction highlights, route cues, critical silhouettes, readable threats | shadow distance/resolution, secondary lights, particle density, ambient detail, post intensity, render scale within tested limits | hidden objective, unreadable enemy, missing cultural signifier, unstable pacing |

Each automatic tier transition needs hysteresis so the game does not oscillate between states. Provide a user choice where platform conventions and product intent require it; explain battery/performance consequences in plain language.

## Graphics validation

Capture golden images for representative cameras and tiers. Compare geometry, material, lighting, shadows, transparency, effects, UI and colour/tone behaviour. Allow only prespecified tolerances for temporal effects and platform precision.

Test:

- first scene entry and shader first use;
- repeated entry after caches are warm;
- background/resume and surface recreation;
- resolution/orientation change where supported;
- low memory and asset unload/reload;
- missing/corrupt optional content;
- API/driver fallback;
- long session after thermal equilibrium.

Block release for unexplained validation errors, device-specific corruption, protected-cue loss, unbounded shader variants, or a target-tier capture that lacks its build/device metadata.
