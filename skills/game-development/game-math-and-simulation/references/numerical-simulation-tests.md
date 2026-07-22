# Numerical Simulation and Deterministic Tests

Parent: [Game Math and Simulation](../SKILL.md)

This self-contained reference converts the supplied mathematics, Unity and Lean testing material into a simulation and verification playbook. Version-sensitive engine APIs must still be checked in official documentation.

## Time-domain contract

Separate three clocks:

| Clock | Owns | Must not own |
|---|---|---|
| Simulation step | rule state, physics-like integration, cooldown truth | camera smoothing or UI animation |
| Render frame | interpolation and presentation | authoritative elapsed simulation |
| Wall/real time | explicitly approved real-time features | ordinary progression or offline punishment |

Use a fixed step when repeatable rule integration matters. Bound catch-up work after stalls so one slow frame does not create an unbounded spiral. Record whether dropped time, slowed simulation or state resynchronisation is the chosen recovery.

## Integration choices

Start with the simplest integrator that passes the acceptance tests. Explicit Euler is cheap but can add energy and become unstable. Semi-implicit Euler often behaves better for game motion. More expensive methods require evidence that the visible or systemic error warrants them.

For any integrator, specify:

- state vector and derivative;
- timestep and maximum substeps;
- force/acceleration order;
- constraints and clamping;
- collision ordering;
- error tolerance and failure recovery.

Never mix transform teleportation and dynamic-body integration without an explicit authority rule.

## Stable response and smoothing

Frame-rate-independent exponential response uses a rate/time-constant model rather than a fixed per-frame fraction. Spring models name stiffness, damping, mass or the equivalent frequency/damping ratio. Test overshoot and convergence after both small and large frame intervals.

Presentation smoothing must not feed back into authoritative rule state unless the design explicitly models that lag.

## Floating-point policy

Define tolerances per quantity:

| Quantity | Tolerance basis |
|---|---|
| Position | smallest player-visible or collision-relevant distance at project scale |
| Angle | smallest aim/camera/animation deviation that changes behaviour |
| Time | scheduler and input resolution plus acceptance window |
| Normalised value | downstream branch threshold and numeric precision |

Guard division, square root, inverse trigonometry and normalisation. Clamp inputs to valid mathematical domains where rounding can push them slightly outside. Detect `NaN` and infinity at system boundaries and fail safely with diagnostic context.

## Randomness and probability

Use separate random streams for systems that must remain stable when unrelated content changes. Record seed, algorithm/version constraint, draw order and serialisation policy when replay or deterministic tests depend on it.

Test probability systems statistically only with a prespecified sample and tolerance. Test hard rules, such as pity limits or forbidden outcomes, deterministically at their exact boundaries.

## Test suite

Every mathematical behaviour should include:

1. Worked example with known input and output.
2. Identity/zero case.
3. Minimum and maximum valid magnitude.
4. Degenerate or invalid input.
5. Boundary just below, at and just above each branch threshold.
6. Equivalent runs at the supported render rates for time-sensitive rules.
7. Long-run drift or stability check.
8. Debug visual or trace that explains a failed result.

Use property tests where a relation is stronger than a single example: rotation preserves vector length, normalisation returns unit length for non-zero input, transform followed by inverse recovers the point within tolerance, and seeded replay produces the same sequence under the declared platform contract.

## Stop conditions

Stop and narrow the model when:

- the project scale or time unit is unspecified;
- the test oracle depends on what the implementation currently does;
- correctness changes with render rate outside the allowed tolerance;
- a bespoke solver cannot be debugged by the owning team;
- device cost exceeds the scenario budget.
