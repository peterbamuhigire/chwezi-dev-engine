# Blender production contract

Back to [Blender Game Asset Production](../SKILL.md).

This reference is self-contained. It distils durable production practices from the supplied Blender books and current official documentation checks; future agents do not need the original book files. Menu paths, add-on names and exporter behaviour remain subordinate to the project's pinned Blender and engine documentation.

## 1. Toolchain and lineage record

Record these fields before asset production:

| Field | Required content |
|---|---|
| `asset_id` | Stable project identifier, not a display filename. |
| `source_revision` | Repository commit or immutable source-package identity. |
| `blender_version` | Exact stable/LTS build used for the candidate. |
| `extensions` | Name, version, source, licence and enablement reason. |
| `unit_axis_contract` | Real-world unit, forward/up axes, handedness and scale conversion. |
| `colour_contract` | Working space, texture colour-space rules and target-renderer expectation. |
| `export_format` | FBX, glTF or approved alternative plus exact preset revision. |
| `engine_target` | Engine, renderer and importer versions. |
| `generated_path` | Export destination; generated assets do not become hand-edited sources. |
| `rights_record` | References, scans, textures, fonts, add-ons and contributor rights. |
| `acceptance_build` | Build checksum, scene, hardware and reviewer. |

Use the latest approved stable/LTS Blender release for production unless a project-specific compatibility study selects another version. Never upgrade a project during a delivery candidate without a controlled compatibility branch, re-export, re-import and regression pass.

## 2. Source layout and collaboration

Separate these concerns:

- `source/model`: editable high/low geometry, modifiers and construction history.
- `source/rig`: approved mesh, deformation/export skeleton and animator rig.
- `source/animation`: linked or overridden rig plus actions/clips; do not duplicate the character source per shot.
- `source/material`: texture source, bake cages, node source and licence trail.
- `generated/export`: machine-reproducible interchange files.
- `engine/import`: importer profile, engine-native materials, physics and runtime metadata.
- `evidence`: validation output, clean re-import images, engine capture and profiler data.

Use linked libraries or the current equivalent to allow a model or rig to improve without duplicating it into every animation scene. Test library overrides before depending on them. A linked update is valuable only when identifier stability and compatibility checks prevent silent breakage.

## 3. Asset brief before geometry

The technical asset brief must answer:

- What player action, feedback or world-reading task does this asset serve?
- At what minimum and maximum screen coverage is it read?
- What variants and gameplay states are visible?
- What moves, deforms, breaks, attaches, collides, occludes or casts shadows?
- Which parts repeat, instance or share a material/rig?
- Which historical or cultural features are source-bound and who approves adaptations?
- What is the simultaneous worst-case count?
- Which runtime measures decide acceptance?

Place reference images with known provenance. When measurements matter, distinguish photographic perspective from orthographic evidence. Model from several views and validate proportions in the engine camera.

## 4. Greybox and transform gate

Before detail:

1. Set the project unit and axis convention.
2. Block primary volumes and moving parts.
3. Choose parent/root, pivots/origins and modular seams from intended motion and assembly.
4. Apply only the transforms the contract permits; reject accidental negative or non-uniform scale where the importer cannot preserve it safely.
5. Test the blockout in the target engine for camera, traversal, attachment, collision and animation range.

Do not confuse a pivot used by artists with an engine socket or physics centre. Name each role and test it in context.

## 5. Modelling and topology gate

Use topology to serve silhouette, shading, deformation and editability:

- Build primary, secondary and tertiary form in that order.
- Use non-destructive modifiers while they preserve predictable export; define which are applied or baked.
- Retopologise sculpted characters and dense hard-surface work into a runtime mesh with deliberate edge flow.
- Put deformation loops where joints compress, stretch and twist; use extreme poses while topology is still cheap to revise.
- Inspect normals, tangents, hard edges, smoothing, non-manifold elements, zero-area faces and triangulation changes.
- Count exported vertices, not only Blender face counts; UV seams, hard normals and material splits can duplicate runtime vertices.

For repeated mechanical detail, prefer instances, arrays, decals, trim sheets or baked normals when they retain the required silhouette and interaction.

## 6. UV, bake, texture and material gate

Define per asset class:

- channel purpose and colour space;
- texel-density range and exception rule;
- seam placement, padding and mip-safety rule;
- mirrored/overlapped UV permissions;
- high/low/cage naming and bake space;
- channel packing, compression and alpha use;
- material-slot limit and shader family;
- texture size based on screen coverage and device memory.

Inspect bake skew, cage misses, ray projection, normal orientation, gradients, seams and mip behaviour. Rebuild runtime materials in the target engine; a Blender node network is not evidence of shader parity. Preserve texture source and rights, not only compressed runtime files.

## 7. Hierarchy, pivots, collision and interaction

Decompose an asset by behaviour, not convenience. A moving part needs a stable pivot, parent, limits and state owner. An interactable needs a visible affordance, collision/trigger boundary, socket or anchor where applicable, and deterministic disabled/broken states.

Use simplified collision primitives or bounded compound collision. Reject render-mesh collision unless a measured exception proves it is required. Validate:

- resting and moving contacts;
- narrow passages and navigation clearance;
- high-speed tunnelling risk;
- compound-child transforms;
- ragdoll or articulated limits where applicable;
- collision-layer and trigger intent in engine.

## 8. LOD and repeated-instance gate

LOD is a measured runtime system, not a decimation exercise. For each level record:

- switch condition or screen-size threshold;
- triangle/vertex/material/bone/texture cost;
- silhouette and deformation changes;
- shadow and collider policy;
- transition method and visible pop result;
- worst-case simultaneous count.

Hand-author critical silhouettes where automatic reduction breaks identity, historical detail, joints or openings. Test bounds and culling. For modular sets and repeated props, measure instancing, batching and merge/HLOD options in the actual engine.

## 9. Export and clean re-import gate

An export preset must control selection, transforms, axes/units, modifiers, normals/tangents, triangulation, armature, deform bones, leaf/helper bones, animation sampling, action selection, custom properties and embedded/external media.

Execute two checks:

1. Clean re-import into a new Blender file or neutral inspector to expose missing dependencies and transform drift.
2. Import into the pinned target engine and compare hierarchy, scale, pivot, normals, materials, skeleton, animation names, duration, root motion and sockets.

FBX and glTF do not preserve every Blender feature. Bake or reconstruct unsupported constraints, modifiers, procedural materials and simulations deliberately. Do not rely on an exporter option because a book mentioned it; verify the installed exporter and engine importer.

## 10. Acceptance matrix

| Gate | Minimum evidence | Reject when |
|---|---|---|
| Provenance | Brief, reference/rights record, owner | Source or adaptation rights are unknown. |
| Structure | Validator output for names, transforms, hierarchy and links | Broken dependency, accidental scale, duplicate identity or unowned object. |
| Visual | Approved camera-distance and target-renderer comparison | Silhouette, material or state cue fails in gameplay view. |
| Interaction | Engine test for pivot, socket, trigger and collision | Motion, attachment or contact differs from specification. |
| Performance | Stress scene on named target hardware | Budget or frame-time envelope fails at simultaneous count. |
| Reproducibility | Clean export/import from recorded source revision | Manual intervention or hidden local dependency is required. |
| Release | Manifest links source, export, engine import and build | Any identity is missing or mismatched. |

## Source limits

- *Blender 3D Noob to Pro* and *Introducing Character Animation with Blender* contain useful fundamentals but describe legacy Blender generations. Exclude their UI, Python, Blender Game Engine and exporter details.
- *Blender 3D Cookbook* uses Blender 2.7-era workflows. Retain the staged character-production and iterative deformation lessons; re-verify every tool instruction.
- *Blender 3D Incredible Models* is strong for reference-to-hard-surface practice, modifier workflows, UVs, baking and decals, but it is not a game-runtime budget authority.
- *Farming Simulator Modding with Blender* supplies valuable hierarchy, pivot, collision-proxy, LOD, test and publishing discipline. Its I3D, XML and ModHub specifics apply only when that host/version is the approved target.
- The supplied *Blender 3D for Jobseekers* Markdown contains only an identifier and contributed no usable practice.
