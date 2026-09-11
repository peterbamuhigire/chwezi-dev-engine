# Tight-Loop Construction

The loop must be fast enough to run repeatedly, deterministic enough to compare, and red-capable for
the exact symptom. Record setup, one command or action, expected observation, actual observation,
duration, isolation boundary, and cleanup.

## Selection order

1. Existing focused test that fails for the reported behaviour.
2. New black-box regression test at the nearest stable seam.
3. Minimal executable reproducer with fixed inputs and independent expected output.
4. Recorded replay or read-only query for environment-only behaviour.
5. Scoped production observation when no safe reproduction exists.

Prove red capability by a known-bad revision, fixture, mutation, or observed failing case. Never
damage production to prove a loop. A loop that can only turn green cannot validate a fix.

Minimise by removing setup, inputs, services, and timing assumptions one at a time. If the failure
disappears, restore the last dependency and record it as evidence rather than immediately calling it
the cause.
