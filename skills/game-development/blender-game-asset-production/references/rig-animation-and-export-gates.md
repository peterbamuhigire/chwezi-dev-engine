# Rig, animation, and export gates

Back to [Blender Game Asset Production](../SKILL.md).

This reference is self-contained. It synthesises the usable rigging and animation practice from the supplied character books into a game-production contract. Exact Blender and engine operations must be checked against the pinned versions.

## 1. Character feasibility before rigging

Review character design with modelling, rigging, animation, gameplay and performance owners. Test early blockouts for shoulder/hip clearance, layered clothing, hair, props, facial range, silhouette and camera distance. Record compromises while geometry and costume design are still cheap to change.

Define the runtime envelope before rig construction:

- skeleton and skinned-mesh count;
- bones per skeleton and per-draw limits;
- influences per vertex;
- animation-memory and sampling policy;
- facial method and active target count;
- cloth/hair method;
- retargeting and body-variant plan;
- sockets, weapon/prop families and root-motion policy.

These values are project measurements, not numbers copied from a book.

## 2. Mesh and scene preparation

Before adding bones:

- verify proportions, default pose, symmetry assumptions, manifold state, normals and deformation topology;
- remove or explicitly retain modifiers, old vertex groups, hidden objects and unused shape keys;
- establish units, axes, root transform and file naming;
- separate rig/mesh collection from control-shape widgets and generated exports;
- confirm the mesh can be revised without breaking stable identifiers.

Default-pose changes after rig construction are costly. Stop and resolve them first unless the change-control plan explicitly covers skeleton and animation migration.

## 3. Skeleton and rig layers

Use a stable export/deformation skeleton plus non-exported mechanics and animator controls. Typical responsibilities are:

| Layer | Purpose | Export rule |
|---|---|---|
| Root/export hierarchy | Stable engine skeleton, props and sockets | Export. |
| Deformation bones | Drive skinned vertices and required correctives | Export when supported and budgeted. |
| Mechanics bones | IK/FK, twist distribution, readers and constraints | Bake or exclude. |
| Animator controls | Clear manipulation, space switching and selection | Exclude. |

Do not assume every engine or format treats non-deforming bones, leaf bones, bone axes or constraints identically. Test the actual exporter/importer pair. Keep exported bones under one explicit root unless the target contract states otherwise.

## 4. Naming and orientation

Names must state role, body part, side and sequence where needed. Use one convention for skeleton, controls, actions, shape keys, sockets and props. Automatic names such as `Bone.046` are release defects.

Fix orientations early. Mirror and retarget workflows depend on coherent left/right axes and roll. Validate local axes visually and through a clean engine import; a rig that deforms in Blender can still import with confusing or incompatible axes.

## 5. Weighting and deformation

Automatic weights are a starting hypothesis. Validate:

- shoulder elevation and twist;
- elbow/knee full flexion;
- wrist/forearm and ankle twist;
- hip flexion, crouch and extreme stride;
- neck/head range;
- hand grip and prop contact;
- facial extremes and asymmetry;
- clothing, hair and accessories;
- LOD skeleton/mesh compatibility.

Use topology, bone placement and weights before adding correctives. Add corrective bones or shape keys only when the measured visual need justifies their runtime and authoring cost. If a corrective depends on DCC drivers or constraints, either bake it into clips or implement an approved engine-side pose/angle reader.

## 6. Facial, cloth, hair and props

Choose facial technique from art style, capture/retarget needs, engine optimisation and simultaneous count:

- a standardised action-unit/blend-shape set supports tracking and predictable retargeting;
- a freeform bone or shape approach supports stylised exaggeration;
- a hybrid can combine stable shapes with limited bone control.

Record missing expressions, conflicts, active-target limits and LOD degradation. Test speech readability, expression asymmetry, lip closure, eye direction and interruption transitions in engine.

For cloth and hair, decide whether motion is keyed, bone-simulated, mesh-simulated, baked or hybrid. Provide a deterministic fallback when simulation is disabled or unstable.

Use sockets or exportable prop bones for reusable attachments. Animation should target the attachment contract rather than one duplicated prop instance. Test grip changes, hand-off, drop, unequip and interruption.

## 7. Animator-facing quality

The last production pass must make the rig safe and legible:

- expose only intended controls;
- use consistent control shapes, colours and selection sets;
- set meaningful rotation modes and limits;
- provide IK/FK and space-switch behaviour where justified;
- keep custom properties named and documented;
- include a rig test scene and known limitations.

Animator convenience never overrides engine compatibility. It should sit above a stable export skeleton.

## 8. Animation contract

For every clip, record:

| Field | Required content |
|---|---|
| `clip_id` | Stable name used by engine/content data. |
| `skeleton_version` | Compatible export skeleton identity. |
| `frame_rate` | Authored and exported sampling rule. |
| `range` | Inclusive start/end and expected duration. |
| `loop` | Looping intent and seam tolerance. |
| `root_motion` | In-place, extracted or authored root behaviour. |
| `events` | Footfalls, impacts, gameplay windows and ownership. |
| `contacts` | Foot, hand, prop or world locks and tolerance. |
| `transitions` | Required entry/exit poses and interruption cases. |
| `additive` | Reference pose and layer restrictions. |
| `rights` | Mocap, performer, audio and derived-work record. |

Keep rig source and animation scenes separate through tested links/overrides. Reuse and retarget actions only when bone identities, rest poses, proportions and curve ownership are compatible.

## 9. Export and engine acceptance

Export mesh/skeleton and clips through explicit presets. Test at least:

1. reference pose and scale;
2. skeleton hierarchy and bone count;
3. weights and maximum influences;
4. shape keys/blend shapes;
5. named clips, ranges and sample rate;
6. root motion and locomotion distance;
7. sockets/prop bones;
8. curve/event transfer or deliberate engine-side recreation;
9. retargeting result;
10. runtime compression, memory and CPU cost.

Use clean re-import to catch missing actions and hidden dependencies. Constraints, drivers, modifiers and simulations are not assumed portable. Verify baked output or recreate the behaviour in engine.

## 10. Rig and animation test matrix

| Test | Oracle |
|---|---|
| Extreme-pose deformation | No unapproved collapse, inversion, penetration or volume loss at named poses. |
| Loop seam | Root, contacts and visible pose stay within the project's transition tolerance. |
| Root motion | Engine displacement and rotation match authored values within tolerance. |
| Interruption | State transition completes or recovers without stuck control, pose or gameplay state. |
| Prop interaction | Socket, grip, release and hand-off align in the target engine. |
| Retarget | Required characters meet contact and silhouette tolerances; exceptions are listed. |
| Compression | Error stays below the declared visual/contact threshold at runtime settings. |
| LOD | Skeleton and mesh switches preserve required motion and do not reference removed bones. |
| Re-export | Same source revision and preset reproduce matching structural identities. |

Retain the `.blend` revision, export file checksum, engine import settings, animation asset identity, build checksum, scene, device and capture for each release claim.
