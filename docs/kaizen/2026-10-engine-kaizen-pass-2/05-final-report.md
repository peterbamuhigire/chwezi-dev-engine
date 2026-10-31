# Final assessment (pass 2)

Date: 2026-10-31. Branch: `kaizen/2026-10-pass2`, created from `main` at `27a602b`; the
repository was returned to `main` when the work finished. The ratings are a conservative
practitioner judgement on the same ten dimensions as the frozen
[baseline](01-baseline-scorecard.md), not an external audit or benchmark. No rating above
70 is given: that needs proof this cycle did not produce.

## Scorecard

| Dimension | 29 Oct final | Pass-2 baseline | Pass-2 final | Evidence and remaining limit |
|---|---:|---:|---:|---|
| Doctrine | 75 | 72 | 74 | Review route and posting-service name now agree across router, gate, exercise and owning skill; router text is device-neutral. The full Task 1 request still misroutes at rank 1 under the lexical proxy, and no live-model run was allowed. |
| Taxonomy and routing | 65 | 62 | 68 | p@1 177/196 (90.3%) to 219/239 (91.6%), p@3 100%; skills with no positive fixture 43 to 1; repository-owned coverage report with a CI ceiling and a raised rank-1 floor. Only 13 skills reach three positives and two owned negatives; four cross-engine negatives `NOT_ASSESSED`. |
| Skill depth | 50 | 50 | 57 | Files with an exact duplicate H2 65 to 24 by lossless merges, with a ratchet. The generic contract blocks themselves are untouched; 20 skills keep a duplicate `Anti-Patterns` pair. |
| Applied proof | 55 | 52 | 55 | 53 new tests, each with a failing case observed; the resolver was proven on this host's real layout. No new applied example; Next.js, Compose and MySQL layers still cannot be re-run here; worked-example count unchanged at 40 of 167. |
| Standards currency | 55 | 50 | 68 | Overdue records 27 to 0 by re-reading each primary page; Step 5 items verified and dated; repository-owned check in CI. Claim support is not assessed by any validator; Apple row, the hospitality register and the 2026-11-03 Next.js notice remain open. |
| Output readiness | 65 | 55 | 57 | The invoice slice now states its gaps; the gaps themselves (pagination, money display, error format) are not fixed. |
| Accessibility and inclusion | 60 | 58 | 58 | Unchanged; the slice's accessibility gaps are now listed. |
| Production and handoff | 50 | 45 | 60 | Both cross-engine validators now run on this host (exit 0 with real parents); CI gains three steps; the whole suite runs here through a labelled stand-in and matches pass 1's real-pytest count. No real pytest, deployment, recovery or MySQL evidence. |
| Hygiene | 50 | 40 | 60 | Host paths in active content 30 to 0 with a guard; eight leaked tool-markup tails removed; 33 links repaired and a ratchet over 84 remaining; pass-1 evidence paths replaced. Tracked user-local settings file (escalated), 84 broken links and 24 duplicate-heading files remain. |
| Safety and integrity | 70 | 66 | 68 | Review route requires the accounting owner for ledger writes; no critical defect found. Personal data in a tracked file remains escalated. |

Pass-2 baseline raw mean: `(72 + 62 + 50 + 52 + 50 + 55 + 58 + 45 + 40 + 66) / 10 = 55.0`.
Pass-2 final raw mean: `(74 + 68 + 57 + 55 + 68 + 57 + 58 + 60 + 60 + 68) / 10 = 62.5`.
Portfolio Standard cap: `min(62.5, 65) = 62.5/100`. The 29 October final (59.5) is shown for
reference only: that pass scored the tree after its own fixes without the items found here,
so the two figures are not a trend. The 95/100 target was not reached and remains a target.

## Measures, before and after

| Measure | Before | After |
|---|---:|---:|
| Overdue source records | 27 | 0 |
| Control-plane validator on this host | exit 1 | exit 0 (11 public engines) |
| Approval-adapter validator on this host | exit 1 | exit 0 |
| Routing p@1 / p@3 | 177/196, 196/196 | 219/239, 239/239 |
| Skills with no positive fixture | 43 | 1 |
| Files with a duplicate H2 | 65 | 24 |
| Machine-path lines in active content | 30 | 0 |
| Broken relative links, active skill roots (unique targets) | 111 | 84 |
| Suite, stand-in runner | 220 passed, 3 skipped | 273 passed, 3 skipped |

## Kept changes

All eight selected items were kept; commits and evidence are in the
[experiment log](03-experiment-log.md). Reverted experiments: widening the accounting-engine
description (no measurable routing gain), merging `Anti-Patterns` pairs in 19 skills (text
would have landed outside its section), the `skill-writing` merge (crossed the byte
threshold) and an over-broad link repair. No skill directory was added, removed, moved or
renamed, so no relink is needed.

## Critical defects

None found. D-13 (a tracked user-local settings file naming two Windows user profiles in a
public repository) is a privacy hygiene issue judged major and escalated for Peter's
decision, because untracking it is a change to user-authored content and cannot remove it
from history.

## Residual risk

- Currency rests on page text read through a fetch tool; claim support is not independently
  assessed, and several pages were read in part (stated per record).
- The lexical routing proxy is not live routing; fixtures show the descriptions do not drift,
  not that a model chooses correctly.
- The ratchet baselines (24 headings, 84 links) are debt made visible, not debt paid.
- The example slice's contract gaps (D-01, D-04, D-05) can still be copied by a reader who
  skips the README.
- Real `pytest`, Next.js, Compose and MySQL runs were not repeated here.

## Branches

Starting branch `main`; work branch `kaizen/2026-10-pass2`, ahead of `main` by the commits
in the experiment log plus the closing documentation commit. Nothing was pushed, tagged or
opened as a pull request.
