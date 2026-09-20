# Test-First Seams and Independent Oracles

Agree the observable seam before implementation: input, action, expected output/state, dependencies,
and failure boundary. Write the smallest test that can fail for the intended reason, run it red, make
the smallest behaviour change, run it green, then refactor without changing the oracle.

The expected value must be independent of the implementation. Reject tests that call the same helper,
copy the same formula, assert only that a mock was called, or pass because the failing path is never
reached. Prove red capability through the absent behaviour, a known-bad revision, or a safe mutation.

Do not force test-first when no executable oracle is appropriate, such as initial visual exploration,
disposable discovery, or unrepeatable external evidence. Predeclare another check and preserve the
reason. Risk still determines unit, integration, contract, journey, device, render, security, and
operational layers.

This reference adapts Red-Green-Refactor, pre-agreed seams, and tautological-test warnings studied in
Matt Pocock's `mattpocock/skills` repository at commit `3cca18b`.

## Risk-scaled simplification proof

Short code or fewer dependencies is not an acceptance criterion by itself. A
simplification is acceptable only when its risk-appropriate negative cases still
fail for removed validation, permission checks, transaction boundaries,
retry/idempotency, recovery, auditability, accessibility state, and observability.
Do not impose a one-test ceiling: choose the smallest sufficient set of independent
oracles and record why lower-risk checks are enough.

For a decision that introduces a dependency, crosses a trust boundary, mutates
data, handles money, or changes asynchronous recovery, include a mutation or
withheld case that would fail if the safeguard disappeared. Keep the failed result
and mutation scope in the evidence record.
