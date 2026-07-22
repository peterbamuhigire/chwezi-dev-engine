# Spatial Mathematics and Coordinate Contracts

Parent: [Game Math and Simulation](../SKILL.md)

This self-contained reference distils durable computer-graphics and Unity game-mathematics practice from the supplied OpenGL and Unity material. It does not depend on the source files remaining available and does not preserve obsolete API syntax.

## Contract before calculation

Record these fields before implementing spatial behaviour:

| Field | Required statement |
|---|---|
| Spaces | Source and destination: local, parent, world, view, clip, normalised device, screen, UV, tangent |
| Axes | Up, forward, right and handedness |
| Units | Distance, mass, time, speed, acceleration and angles |
| Scale | Authoring-to-runtime conversion and valid magnitude range |
| Orientation | Representation, composition order and designer-facing form |
| Precision | Numeric type, tolerance policy and non-finite handling |

The same three numbers can describe a point, direction, velocity, normal or scale. Treat those meanings as separate contracts. Translation applies to points but not directions; inverse-transpose handling may be required for transformed normals; screen and world distances are not interchangeable.

## Vector decision table

| Question | Operation | Guard |
|---|---|---|
| How far and in which direction? | subtract points; inspect magnitude | zero-distance case |
| How aligned are two directions? | dot of normalised vectors | clamp before inverse cosine |
| What is the signed side of an axis/plane? | cross plus reference-axis dot | document handedness |
| What is the component along a direction? | projection | non-zero basis vector |
| What remains after removing the normal component? | rejection/tangent projection | normal must be normalised |
| What is the surface orientation? | cross of non-collinear edges or supplied normal | degenerate triangle |

Prefer squared distance when only ordering or range comparison matters. Normalise only when the magnitude is irrelevant; normalising velocity can silently destroy speed.

## Transform and hierarchy rules

Use homogeneous transform composition conceptually as `translation * rotation * scale` only after confirming the engine convention and multiplication order. Do not copy matrix order across engines or shader languages without a test fixture.

For each hierarchy-sensitive mechanic, test:

- identity parent;
- translated and rotated parent;
- non-uniformly scaled parent;
- mirrored/negative scale if supported;
- reparenting while preserving or intentionally changing world pose.

Avoid gameplay decisions derived from lossy matrix decomposition when stable domain state can own position, orientation and scale directly.

## Rotation rules

- Use Euler angles for authoring displays and constrained single-axis controls, not arbitrary accumulated orientation.
- Use quaternions through engine APIs for composition, shortest-path interpolation and orientation differences.
- Normalise after operations only where the API does not guarantee it.
- Define wrap behaviour at 0/360 degrees and the opposite-direction case at 180 degrees.
- Keep camera yaw/pitch limits in an explicit control model; do not infer them from arbitrary quaternion components.

## Rays, planes and intersections

Every query states origin, direction normalisation, maximum distance, layer/filter mask, trigger policy and expected ordering. For a ray-plane or ray-triangle calculation, define parallel, coplanar, behind-origin and edge-hit behaviour.

Collision tests must distinguish overlap at one instant from a swept path through time. A fast object can miss a thin collider between samples even when both end states are valid.

## Curves and interpolation

Use linear interpolation for straight parameter-space blends, spherical interpolation for orientation, and authored curves/splines where velocity or direction continuity matters. State whether parameter `t` represents elapsed time, normalised progress, arc length or an ease curve; these are not equivalent.

For camera rails, routes and animation paths, test position continuity, tangent continuity, endpoint velocity, overshoot and behaviour after a large frame delay. Constant parameter speed is not constant world speed on a general curve; use arc-length approximation when the player can perceive the discrepancy.

## Rendering handoff

The rendering contract supplies model, view and projection transforms; clip conventions and depth range belong to the active engine/API. Validate a known triangle, normal, camera and screen point end to end before authoring complex shaders. Route pipeline and GPU-state decisions to `real-time-game-graphics`.
