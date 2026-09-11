# Two-Axis Code Review

Review two independent questions before synthesising severity.

## Axis A: specification fidelity

Check the implemented behaviour against approved requirements, acceptance criteria, user states,
non-goals, contracts, and migration promises. Report missing, extra, contradictory, or untraceable
behaviour with the exact source and code/test evidence.

## Axis B: engineering standards

Check correctness, security, privacy, data safety, accessibility, performance, maintainability,
operability, tests, observability, dependency use, and rollback. A requirement-conformant change may
still fail this axis; elegant code may still implement the wrong product.

## Review contract

1. Freeze the diff and source requirements being reviewed.
2. Run each axis independently; do not let a pass on one suppress findings on the other.
3. For every finding record axis, severity, evidence, consequence, smallest remedy, and verification.
4. Add security/evidence overlays after the two axes, then let the integrator resolve duplicates and
   cross-axis trade-offs.
5. Re-review changed scope. Missing requirement, execution, runtime, or reviewer evidence is
   `NOT ASSESSED`, never a pass.

Fixture the method with one standards-pass/spec-fail change and one spec-pass/standards-fail change.

This reference adapts the independent Standards and Spec review mechanism studied in Matt Pocock's
`mattpocock/skills` repository at commit `3cca18b`.
