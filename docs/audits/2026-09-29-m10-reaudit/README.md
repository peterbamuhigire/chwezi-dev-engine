# chwezi-dev-engine: M10-14 measured re-audit (29 September 2026)

Engine: `C:\wamp64\www\chwezi-dev-engine`, committed HEAD `67ae982`, 167 active skills (cap 200).
Auditor: independent (took no part in any my-10-kaizen phase). Method: the engine's own
`skills/sdlc-meta/skill-engine-audit` skill with the AO-14 "Engine Eval Readiness (measured)" extension.

## Headline numbers

| Number | Score /100 | Basis |
|---|---|---|
| Raw | **52.7** | Weighted overall from judged dimensions, discovery and routing judged at 66 |
| Measured-constrained | **52.5** | Routing replaced by the measured Engine Eval Readiness (59.7) |
| Published | **52.5** | `min(52.5, 65)`; the 65 cap applies (no portfolio craft-standard acceptance evidence) but does not bind |
| Engine Eval Readiness (measured) | **59.7** | T1 30.00 + T2 29.72 + T3 0.00 (Tier 3 NOT_ASSESSED, zero spend); recomputed and agreed |

Weighting: output readiness 30, skill depth and worked examples 25, standards currency 15,
taxonomy 10, doctrine 10, hygiene 10 (hygiene = mean of redundancy, discovery/routing, safety).
No dimension, group or output type scored 70 or above.

## Verdict

The engine's control plane is in good order: all five validators and the test suite exit 0, routing
precision@1 is 90.6 % on the lexical proxy, and the router now exposes game, GIS and desktop work that
the 6 September audit found missing. The skill layer beneath it is uneven. Three sampled skills
carry platform guidance that is out of date against primary sources checked today (Android target SDK,
Next.js request APIs and middleware, PostgreSQL versions); 59 of 167 skills repeat their contract
sections after normalisation; game development (25 skills) has one worked example and 22
contract-compliance failures; and Tier 3 behavioural evidence does not exist, so Readiness cannot exceed 70.
A published score of 52.5 places the engine in the "competent, major gaps" band. The prior audit
withheld an overall score, so this is the first comparable whole-engine figure; per-dimension movement
is shown in the scorecard.

## Files

- [00 Executive summary](00-executive-summary.md)
- [01 Methodology and rubric](01-methodology-and-rubric.md)
- [02 Coverage and taxonomy](02-coverage-and-taxonomy.md)
- [03 Existing groups audit](03-existing-groups-audit.md)
- [05 Per-output-type readiness](05-per-output-type-readiness.md)
- [06 Standards benchmark (short, cited)](06-standards-benchmark.md)
- [09 Master scorecard](09-master-scorecard.md)
- [10 Roadmap to world class](10-roadmap-to-world-class.md)
- [11 Measured evidence](11-measured-evidence.md)

Not re-run in the M10-14 measured re-audit:

- 04 gap analysis (new skills): not re-run in the M10-14 measured re-audit; gaps are named inside 02 and 05.
- 07 hardening of existing skills: not re-run in the M10-14 measured re-audit; named hardening moves are in 10.
- 08 reading list: not re-run in the M10-14 measured re-audit.

Prior audit for comparison: [2026-09-06 Kaizen](../2026-09-06-kaizen/README.md) (overall withheld;
taxonomy 52; standards currency 50; local 65 cap).
