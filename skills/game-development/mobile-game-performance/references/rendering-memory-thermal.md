# Rendering, memory and thermal checklist

Back to [Mobile Game Performance](../SKILL.md).

GPU: overdraw, resolution, shader variants, materials, batches, transparencies, post effects, lights/shadows and bandwidth. CPU: per-frame scripts, physics, AI, animation, culling and submission. Memory: texture/audio/mesh duplication, residency, pools, scene unload and fragmentation. Loading: dependency graph, shader warm-up, decompression and storage.

Android and Apple guidance requires frame pacing and sustained thermal-aware measurement. Define performance and battery-friendly quality modes, but verify current APIs and thresholds from official documentation.
