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

## Outputs
Art direction contract; provenance manifest; export/import profiles; atlas/animation/VFX specifications; validator results; engine/device acceptance evidence.

## References
- [2D content acceptance matrix](references/2d-content-acceptance-matrix.md)

