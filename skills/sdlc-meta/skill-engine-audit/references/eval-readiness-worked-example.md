# Reference: Engine Eval Readiness — Worked Example

Applies the "Engine Eval Readiness (measured)" section of `scoring-rubric.md`. Method adapted from
addyosmani/agent-skills (MIT, https://github.com/addyosmani/agent-skills, commit `2686b62`),
paraphrased. Inputs are the chwezi-dev-engine harness numbers measured on 29 September 2026
(my-10-kaizen M10-14); the dimension scores in Part C are illustrative, not an audit result.

## A. Readiness from harness output (Tier 3 not executed)

| Slot | Measured input | Fraction |
|---|---|---|
| T1 | 3 of 3 catalogue validators pass (`validate_engine_control_plane.py`, `routing_smoke_test.py`, `skill_catalog_guardrails.py`) | 1.0000 |
| T2_p1 | Routing smoke test precision@1: 173 / 191 | 0.9058 |
| T2_neg | Owned negatives: 74 pass locally + 4 cross-engine mirrors pass in the union oracles = 78 / 78 | 1.0000 |
| T2_cov | Skills with ≥ 3 positives and ≥ 2 owned negatives: 11 / 167 | 0.0659 |
| T2_clean | Undeclared cross-engine pairs ≥ 0.75 involving dev: 0 | 1.0000 |
| T3 | Behavioural runs: 0 executed; every planned run `NOT_ASSESSED (zero-spend rule)` | 0 (not estimated) |

Arithmetic:

- T1 points = 30 × 1.0000 = **30.00**
- T2 mean = (0.9058 + 1.0000 + 0.0659 + 1.0000) ÷ 4 = 2.9717 ÷ 4 = 0.7429; T2 points = 40 × 0.7429 = **29.72**
- T3 points = 30 × 0 = **0.00** (`NOT_ASSESSED` = 0; the slot stays in the formula)
- **Readiness = 30.00 + 29.72 + 0.00 = 59.7 / 100**

Reading the result: coverage is the weakest measured input (most skills lack three positives and two
owned negatives), and the empty Tier 3 caps Readiness at 70 whatever else improves.

## B. The routing cap of 50 (no harness output)

An auditor who did not run the harness may not score discovery and routing above 50. If the same
engine were judged at 72 for routing without a harness run, the dimension becomes
`min(72, 50)` = **50**. With the harness run, the dimension is the Readiness score, **59.7**.

## C. Raw, measured-constrained and published scores

Weighting from `scoring-rubric.md`: output readiness 30 %, skill depth 25 %, standards currency 15 %,
taxonomy 10 %, doctrine 10 %, hygiene 10 % (hygiene = mean of redundancy, discovery/routing, safety).

**Case 1: a strict audit.** Judged dimensions: output 55, depth 52, standards 50, taxonomy 55,
doctrine 62, redundancy 58, safety 60; routing judged 72.

| Number | Hygiene | Overall |
|---|---|---|
| Raw (routing 72, judged) | (58 + 72 + 60) ÷ 3 = 63.33 | 16.50 + 13.00 + 7.50 + 5.50 + 6.20 + 6.33 = **55.0** |
| Measured-constrained (routing = Readiness 59.7) | (58 + 59.7 + 60) ÷ 3 = 59.23 | 16.50 + 13.00 + 7.50 + 5.50 + 6.20 + 5.92 = **54.6** |
| Published (`min(54.6, 65)`) | — | **54.6** |
| Without harness output (routing = 50) | (58 + 50 + 60) ÷ 3 = 56.00 | 16.50 + 13.00 + 7.50 + 5.50 + 6.20 + 5.60 = **54.3** |

**Case 2: the published cap of 65 binds.** Judged dimensions: output 70, depth 66, standards 64,
taxonomy 68, doctrine 72, redundancy 66, safety 70; routing judged 80. (Every 70+ here would need
the strictness directive's extraordinary justification in a real audit.)

| Number | Hygiene | Overall |
|---|---|---|
| Raw | (66 + 80 + 70) ÷ 3 = 72.00 | 21.00 + 16.50 + 9.60 + 6.80 + 7.20 + 7.20 = **68.3** |
| Measured-constrained (routing = 59.7) | (66 + 59.7 + 70) ÷ 3 = 65.23 | 21.00 + 16.50 + 9.60 + 6.80 + 7.20 + 6.52 = **67.6** |
| Published: craft-standard acceptance evidence missing, `min(67.6, 65)` | — | **65.0** |

## D. What the example shows

1. Routing is only about 3.3 points of an engine score, so Readiness is reported beside the overall
   score, never folded away: 59.7 / 100 is itself the evaluation headline.
2. An unexecuted tier costs its full weight (30 points here). It is never averaged out.
3. Three numbers are always published together, with the `NOT_ASSESSED` list that produced them.
4. Recompute from the stored inputs before quoting a figure; the portfolio's stored inputs and
   script live in `chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-14/readiness/`.
