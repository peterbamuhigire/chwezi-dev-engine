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
