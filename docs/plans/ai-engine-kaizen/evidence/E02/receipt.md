# E02 evidence receipt

- **Acceptance ID:** AC-E02
- **Input:** K2 in `docs/plans/ai-engine-kaizen/casebook.md`, implemented with original synthetic rows P1-P4 and four held-out query cases in the public RAG example.
- **Source revision:** `78c8b94` (clean starting revision before this slice).
- **Receipt digest:** SHA-256 is stored in `build.contract.json` after this receipt is final.
- **Scope:** the existing curated corpus reference, an offline lexical retrieval fixture, deterministic answer-support oracle, regression tests, and this evidence record. No hosted model, external corpus, private data, or production service was used.

## Reproduction

From the repository root:

```sh
python -B skills/ai/ai-rag-patterns/examples/curated-retrieval/evaluate.py
python -B -m unittest discover -s skills/ai/ai-rag-patterns/examples/curated-retrieval -p "test_*.py" -v
python -B skills/ai/ai-rag-patterns/examples/curated-retrieval/evaluate.py --drop-negation
```

The normal result is preserved in `result.json`; the targeted suite is in `tests.txt`; the controlled negation ablation is in `negative-control.json`. Four tests pass. In the held-out Atlas query, P2 revision 2 ranks first with reciprocal rank 1. The fixture response claim “five days” is graded `UNSUPPORTED` even though retrieval is correct. A separate expected claim “not seven days” is supported and its selected source span is recoverable at the original-text offsets. Queries without eligible supporting rows abstain. P1 (withdrawn) and P3 (another tenant) never appear in eligible or ranked IDs.

## Negative control and repair

The first test run exposed two oracle defects. The substring grader accepted “seven days” inside “not seven days”, and a query with no supporting record matched a shared function word. The tests failed at `test_negation_ablation_is_rejected_and_source_span_is_recoverable` and `test_no_eligible_document_abstains_without_leaking_ids`. The grader now checks local negation, and common function words are excluded from lexical overlap. The repaired suite passed 4/4.

The explicit ablation removes `not` from the normalized support text. Its report shows `answer_supported: true` for the claim “seven days” while `original_source_supports_claim: false`. The evaluator preserves the unmodified P2 text, recovers the exact `not seven days` span, then reruns retrieval against the original corpus. This demonstrates why normalized text is not a substitute for the source.

## K2 outcome and limits

The result stores the corpus fixture revision, tenant eligibility set, ranked IDs, reciprocal rank, selected original-source span, response claim, and deterministic reviewer grade. P2's active revision 2 is answerable for tenant-a. A query for Cygnus has no matching row and abstains. A tenant-c query returns no IDs or text. The raw identifier `P2` is preserved and matched case-sensitively; lower-case `p2` does not select it. Withdrawn P1 is filtered before ranking.

Retrieval and answer support remain separate fields. This fixture's scorer is a small token-overlap demonstration, not BM25 and not a quality benchmark. The support checker handles literal claims and local negation only; it is not a natural-language entailment model or reviewer. The held-out relevance cases are synthetic and fixed before implementation. No production access-control claim is made.

## Source record

| Source | Scope and locator | Publication/version | Access date | Freshness and review | Support and uncertainty |
|---|---|---|---|---|---|
| [CheckList paper, arXiv:2005.04118](https://arxiv.org/abs/2005.04118), R05 | Abstract and method: behavioral test matrices can expose failures missed by aggregate held-out accuracy. | Submitted 2020-05-08; ACL 2020. | 2026-11-23 | Durable research method; review by 2027-02-23 or if the cited work is superseded for this use. | Primary paper page rechecked. It motivates edge-case fixtures; it does not validate this synthetic oracle. |
| [RAG paper, arXiv:2005.11401](https://arxiv.org/abs/2005.11401), R06 | Abstract and v4: RAG combines parametric and non-parametric memory for generation. | v4 revised 2021-04-12; NeurIPS 2020. | 2026-11-23 | Durable architecture description; review by 2027-02-23 or if the cited work is superseded for this use. | Primary paper page rechecked. Retrieval provenance alone does not prove that a response claim is supported. |

The operator rechecked the source evaluations and replayed both evaluator outputs on 23 November 2026. The published [CheckList abstract](https://aclanthology.org/2020.acl-main.442/) supports behavioral test design. The [RAG abstract, v4](https://arxiv.org/abs/2005.11401v4) describes combining learned parameters with external retrieval. Both are primary methodological sources. The four local tests and the frozen output records establish the observed fixture behavior. Production access control and model performance remain unassessed.
