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

## When test-first has been selected

This table applies only after the risk-scaled rule above has chosen test-first. It does not
override the paragraph that says when not to force it.

| Excuse | Reality |
|---|---|
| "The change is too small to test." | Small changes to money, stock and permission paths are where silent regressions live. The test is small too. |
| "I will add the test after the code works." | A test written after the code has never failed, so nobody knows whether it can. Run it red first. |
| "The existing tests already cover this." | Name the test and show it failing against the old behaviour. If you cannot, it does not cover it. |
| "Mocking the database is enough." | A mock proves the call was made, not that the query, constraint or transaction is right. Use the real engine for the seam that matters. |
| "The fixture data is too hard to build." | Hard fixtures point to a missing builder or seeder. Build it once; the next ten tests reuse it. |
| "It passed on my machine." | Evidence is the command and its output in the shared environment, per `rules/common/verification.md`. |
| "The new test passes, so the task is done." | The project's suite defines green, not the new test file alone. Run the full suite, or the agreed subset, before claiming done. |

Do not write string-presence tests for prompts, skills or scripts: a test that only asserts a file
contains a phrase passes whether or not the behaviour exists. Test the behaviour (run the script on a
fixture, check the output), or record the check as a review item. The one allowed exception is a
doctrine guard that pins an exact contract token a machine consumer depends on, such as a status
word a parser reads, and it must say so in its name.

(Excuse table adapted from obra/superpowers, MIT, https://github.com/obra/superpowers, commit
8ca22dba9a94f28898bbce59f2537ff4d87c747d.)
