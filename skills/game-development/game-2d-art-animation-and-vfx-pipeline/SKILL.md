---
name: game-2d-art-animation-and-vfx-pipeline
description: Use when producing, importing, validating, or optimising 2D game concepts, sprites, atlases, tile sets, skeletal or frame animation, UI art, particles, VFX, resolution variants, or licensed source assets.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game 2D Art, Animation, and VFX Pipeline

Move traceable 2D source art through deterministic transforms into readable, budgeted engine assets.

## Use When
- Work involves sprites, texture atlases, tiles, 2D rigs/animation, particles, effects, UI art, or pixel-density variants.

## Do Not Use When
- The task is 3D asset production or runtime graphics architecture.

## Required Inputs
Art direction, source/provenance/licence, target devices/resolutions, colour/alpha contract, camera/units, atlas/import settings, animation/VFX budgets, accessibility/readability needs, naming/version rules, and acceptance scenes.

## Workflow
1. Preserve licensed source and provenance; define deterministic export naming, scale, pivots, trim, colour, alpha, and compression rules.
2. Specify atlas/tile grouping from runtime locality and update needs, not convenience alone.
3. Define animation states/events/root/pivot behaviour and VFX lifecycle, pooling, overdraw, photosensitivity, and gameplay-readability limits.
4. Validate dimensions, formats, duplicates, missing frames, pivots, atlas boundaries, import drift, memory, draw calls, and target-device readability.
5. Retain source-to-export-to-import manifest and device captures for normal, low-quality, accessibility, and failure variants.

## Quality Standards

- Preserve source, licence, cultural restriction, export profile, and runtime owner for every asset.
- Validate scale, pivot, alpha, colour, animation timing, atlas bleed, fallback, and memory on target devices.
- Provide non-motion and non-colour-only communication for gameplay-critical VFX.
- Accept assets from engine captures and budgets, not DCC previews alone.

## Anti-Patterns

- Shipping only a source preview. Fix: capture the imported runtime asset.
- One atlas for unrelated lifecycles. Fix: group by load/unload and update behaviour.
- Particle count set by taste. Fix: profile overdraw, fill rate, CPU, memory, and readability.
- Colour alone communicates danger. Fix: add shape, motion, text, sound, or haptic alternatives.
- Missing provenance. Fix: quarantine the asset until rights and source are recorded.

## Outputs
Art direction contract; provenance manifest; export/import profiles; atlas/animation/VFX specifications; validator results; engine/device acceptance evidence.

## References
- [2D content acceptance matrix](references/2d-content-acceptance-matrix.md)

<!-- dual-compat-start -->
## Evidence Produced

| Category | Artifact | Format | Example |
| --- | --- | --- | --- |
| UX quality | 2D asset runtime acceptance sheet | Markdown plus rendered captures | source, atlas, animation, scaling, performance, accessibility, provenance, and import result |
<!-- dual-compat-end -->

