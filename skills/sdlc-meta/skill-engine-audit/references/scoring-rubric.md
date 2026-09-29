# Reference: The Strict Scoring Rubric

All scores out of 100, graded against the **top 0.1% of the relevant domain** (for a design
engine: Pentagram/Apple/Awwwards-winner level; for a finance engine: Big-4 / IFRS-authoritative
level; for a research engine: top intelligence-shop / peer-reviewed level — pick the apex of the
engine's field).

## Bands

| Band | Meaning |
|---|---|
| **90–100** | Rivals the field's best; essentially nothing missing. |
| **75–89** | Excellent professional; minor gaps only. |
| **60–74** | Solid but **visibly short** of world-class; notable gaps. |
| **40–59** | Competent / amateur-to-pro; major gaps. |
| **< 40** | Skeletal / inadequate. |

## The strictness directive (enforce it)

- **Default to 45–65.** Most aspects of most engines land here.
- **A 70+ requires extraordinary, specific justification.** If you feel like scoring 70+, you
  have NOT been strict enough — go find what is missing.
- **Justify every score** with concrete, named deficiencies: missing techniques, absent reference
  files, missing worked examples, stale standards, thin workflows, coverage holes. Never "feels
  good."
- **Reward applied proof over prose.** Doctrine and workflows are necessary but not sufficient;
  worked examples, reference depth, and production/handoff readiness are what separate competent
  from world-class.

## Computing the overall engine score

Weight execution and coverage above philosophy — an engine ships work, it doesn't admire its own
doctrine. Suggested weighting (tune per engine):

- Output-type readiness & coverage — 30%
- Skill depth & worked examples — 25%
- Standards currency — 15%
- Taxonomy & structure — 10%
- Doctrine & philosophy — 10%
- Hygiene (redundancy, discovery/routing, safety) — 10%

State the weighting used. A strong doctrine on a thin skill layer should still land the overall
well below 70.

## Engine Eval Readiness (measured)

Adapted from addyosmani/agent-skills (MIT, https://github.com/addyosmani/agent-skills, commit
`2686b62`), paraphrased; adopted for the portfolio in my-10-kaizen M10-14 (AO-14).

Routing and evaluation are scored from harness output, not from judgement. Run the harness
before any dimension is scored (SKILL.md workflow step 0).

**Formula (/100).**

`Readiness = 30 × T1 + 40 × mean(T2_p1, T2_neg, T2_cov, T2_clean) + 30 × T3`

| Input | Definition | Source (run location) |
|---|---|---|
| T1 | Passing validators ÷ declared validators (a list chosen by the auditor is a stand-in and must be labelled so) | the engine's `validators` list in `chwezi-engine-agents/catalog/engines.yaml`, each run in the engine root |
| T2_p1 | Routing precision@1 as a fraction; executed known-defect cases stay in the denominator | the engine's routing smoke test (`scripts/routing_smoke_test.py` or its equivalent) |
| T2_neg | Passing owned negatives ÷ all owned negatives | the same smoke test; the portfolio route oracles (`evals/runners/run-contract-evals.py --route-oracles`) for cross-engine owners |
| T2_cov | Active skills with at least 3 positive fixtures and 2 owned negatives ÷ active skills | the engine's routing fixture files |
| T2_clean | 1 − (undeclared cross-engine pairs ≥ 0.75 involving the engine ÷ all cross-engine pairs ≥ 0.75 involving it); 1.0 when the engine is in the scan and has none; `NOT_ASSESSED` (0) when the engine is not in the scan | `scripts/validate-runtime-skill-budget.py --collisions --ownership evals/routing/ownership.yaml` in engine-agents |
| T3 | Passing behavioural runs ÷ all planned runs for the engine's Tier-3 cases | `grading.json` files under engine-agents `evals/behavioural/results/**` and dev `benchmarks/solution-selection/`; a pass needs a validated grading file bound to a pinned model and CLI version |

**Rules.**

1. `NOT_ASSESSED` = 0. A validator, fixture, run or tier that was declared or planned but not
   executed scores 0 in its slot and stays in the denominator. It is never excluded, rescaled away
   or estimated. A validator that cannot run on the audit host (for example a Linux-native suite on
   Windows) is `NOT_ASSESSED`, not passed.
2. Without harness output, routing cannot score above 50. If the audit has no T2 run for the
   engine, the discovery-and-routing dimension is `min(judged score, 50)`.
3. With harness output, the discovery-and-routing dimension **is** the Readiness score. The
   hygiene bucket (10 %) keeps its three thirds: redundancy, discovery/routing and safety; the
   routing third (about 3.3 points) is Readiness × 0.10 ÷ 3.
4. While T3 is unexecuted the Readiness ceiling is 70, and no overall score of 97 can be claimed.
5. Lexical T2 figures are a drift guard, not proof of live routing; say so wherever they appear.
6. Mixed-model Tier-3 sets are not pooled; report executed and `NOT_ASSESSED` counts separately.

**Three published numbers per engine.**

- **Raw**: the weighted overall from the dimension scores as judged.
- **Measured-constrained**: raw with the AO-14 rules applied (the routing dimension replaced by
  Readiness, or capped at 50 without harness output).
- **Published**: the measured-constrained score, capped at 65 where the portfolio craft standard's
  acceptance evidence is missing (`min(score, 65)`).

Worked example with T3 unexecuted: `eval-readiness-worked-example.md`.
