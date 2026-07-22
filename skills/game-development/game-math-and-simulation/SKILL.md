---
name: game-math-and-simulation
description: Use when a game system needs explicit vector, matrix, quaternion, geometry, interpolation, collision, camera, steering, probability, or numerical-simulation rules; use gameplay-systems-architecture for ownership and the engine skill for API integration.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---

# Game Math and Simulation

Turn mathematical intent into named coordinate spaces, explicit units, stable numerical methods, deterministic oracles, and player-visible behaviour that survives variable frame time.

## Prerequisites

Load the approved mechanic or rendering requirement, `gameplay-systems-architecture`, and the selected engine skill before choosing engine-specific types or APIs.

<!-- dual-compat-start -->
## Use When

- Specifying movement, aiming, cameras, animation blending, steering, trajectories, collision, procedural placement, spatial queries, simulation, or shader mathematics.
- Debugging jitter, drift, tunnelling, gimbal-like rotation defects, unstable springs, frame-rate dependence, or incorrect coordinate conversions.
- Writing deterministic mathematical test oracles for gameplay, tools, or rendering.

## Do Not Use When

- The task is system ownership, persistence, or event architecture without a mathematical defect; use `gameplay-systems-architecture`.
- The task is render-pipeline, material, or GPU design; use `real-time-game-graphics` and return here for the mathematical contract.
- A built-in engine primitive already satisfies the requirement and profiling/tests show no gap; do not replace it with bespoke mathematics.

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---:|---|
| Mechanic or visual behaviour specification | game design/system owner | yes | Defines player-visible intent and limits |
| Coordinate, unit, time and precision context | engine/physics/rendering owner | yes | Prevents space, scale and timestep ambiguity |
| Failure cases and acceptance criteria | testing owner | yes | Makes the result testable |
| Target-device performance evidence | `mobile-game-performance` | conditional | Bounds numerical and query cost |

## Workflow

1. State the player-visible behaviour before selecting a formula.
2. Name every coordinate space, handedness, axis convention, unit, time source, angle unit, range and precision assumption.
3. Choose the smallest mathematical model that represents the behaviour; prefer engine-tested primitives when their contract fits.
4. Separate simulation state from presentation smoothing. Use fixed-step simulation where rule consistency requires it and render interpolation where visual continuity requires it.
5. Define boundary conditions, tolerances, degenerate inputs, clamping, normalisation, random seeds and recovery from non-finite values.
6. Work representative examples by hand, then encode property, boundary, invariant and frame-rate-independence tests.
7. Instrument the result with debug vectors, paths, bounds, state graphs or numeric traces; profile worst-case queries on target devices.

## Quality Standards

- Treat local, world, view, clip, screen, UV and tangent spaces as different types even if the engine represents them with the same structure.
- Keep units explicit. Convert at boundaries; do not scatter scale factors through gameplay code.
- Use dot products for alignment/projection questions, cross products for perpendicular/orientation questions, and quaternions for composed 3D orientation without exposing raw components to designers.
- Compare floating-point results with requirement-derived tolerances, never blanket exact equality or an unexplained epsilon.
- Preserve determinism only where the product needs replay, save reconstruction, lockstep, seeded tests, or auditability; record platform limits.

## Decision Rules

| Need | Preferred model | Gate |
|---|---|---|
| Constant-rate rule simulation | Fixed timestep plus bounded catch-up | Same input sequence gives equivalent state across tested render rates |
| Visual smoothing only | Interpolation or critically damped response | No rule state is authored from smoothed presentation |
| 3D orientation composition | Normalised quaternion through engine API | No Euler accumulation; shortest-path behaviour tested |
| Fast moving collision | Sweep/continuous query or smaller bounded step | Tunnelling case passes at maximum specified speed |
| Random but reproducible content | Explicit seeded stream per owning system | Save/replay and test sequence remain stable |

## Capability Contract

Read and search access to the requirement and implementation are required. Execute tests and visual/debug captures when available. Editing follows the parent implementation scope; without execution, return the model and unverified test vectors rather than claiming correctness.

## Degraded Mode

If the engine version, scale, timestep, or coordinate convention is unknown, stop formula-level implementation. Return the missing contract fields, provisional equations, and the exact experiments required to resolve them.

## Anti-Patterns

- Mixing local and world vectors. Fix: name conversion boundaries and assert the expected space.
- Multiplying movement by both fixed and render delta time. Fix: assign one time domain to each state update.
- Euler-angle accumulation for arbitrary 3D orientation. Fix: compose rotations with engine quaternion operations and test wrap boundaries.
- Normalising a zero-length vector. Fix: define the zero-input behaviour before the operation.
- Magic epsilon everywhere. Fix: derive tolerances from game scale, solver precision and the observable acceptance condition.
- Random calls from shared global state. Fix: give each deterministic system an owned, serialisable random stream.
- Complex custom collision before profiling built-in queries. Fix: prove the engine primitive is insufficient first.

## Outputs

| Artefact | Consumed by | Acceptance condition |
|---|---|---|
| Mathematical behaviour contract | gameplay/rendering implementation | Spaces, units, time, equations, limits and degeneracies are explicit |
| Worked test vectors and invariant suite | `game-testing-polish` | Normal, boundary, degenerate and frame-rate cases have deterministic oracles |
| Debug and profiling plan | engine/performance owners | The result can be inspected and its worst-case cost measured |

## References

- [Spatial mathematics and coordinate contracts](references/spatial-mathematics-contracts.md)
- [Numerical simulation and deterministic tests](references/numerical-simulation-tests.md)
<!-- dual-compat-end -->

## Read Next

Use `real-time-game-graphics` for shader/rendering integration, the selected engine skill for implementation, and `game-testing-polish` for balance and player-facing verification.
