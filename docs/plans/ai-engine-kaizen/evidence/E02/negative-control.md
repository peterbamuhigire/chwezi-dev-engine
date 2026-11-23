# E02 negative-control record

- **Acceptance ID:** AC-E02
- **Defect introduced:** remove the meaningful negator `not` from normalized support text for the query “Does Atlas retain jobs for seven days?”
- **Expected unsafe result:** the claim “seven days” appears supported by the ablated text.
- **Observed control:** `negative-control.json` records `answer_supported: true` against ablated text and `original_source_supports_claim: false` against the unmodified P2 source.
- **Assertion that catches it:** `test_negation_ablation_is_rejected_and_source_span_is_recoverable` asserts the false positive exists only in the ablated representation, then recovers the original `not seven days` span and confirms the source-backed comparison.
- **Repair check:** `tests.txt` shows the full targeted suite passing 4/4 on the repaired evaluator.
- **Initial oracle failures:** the first run also failed the answer-support negation check and the no-answer abstention check because `for` was counted as a meaningful match. Both failures and their repair are described in `receipt.md`.
