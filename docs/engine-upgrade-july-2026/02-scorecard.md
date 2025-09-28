# Scorecard

Raw weighted total: 78/100. Capped audit total: 63/100. The cap is applied because this audit intentionally exposes the path from current state to 95+ rather than awarding production-certification scores.

| Dimension | Raw score | Points |
| --- | --- | --- |
| Richness | 16/20 | 16 |
| Robustness | 17/20 | 17 |
| World-Class Output Capability | 15/20 | 15 |
| Architecture & Discoverability | 12/15 | 12 |
| Composability & Reuse | 10/15 | 10 |
| Currency & Compliance | 8/10 | 8 |

## Richness

Raw score: 16/20.

The engine has 244 SKILL.md files, 2690 reference-file hits, 1420 template-file hits, and 292 example-file hits. This gives it substantial domain coverage, but the richness score is held back where references are not converted into reusable examples, current-source registers, or complete model outputs.

Top deficiencies:

- The catalogue is broad enough to risk shallow coverage in some domains unless each high-risk skill has executable examples.
- Many empty legacy directories remain after migrations and can confuse discovery or imply unimplemented capability.
- Currency depends on periodic manual updates; fast-moving platform guidance needs dated source registers and validation fixtures.

## Robustness

Raw score: 17/20.

Robustness is supported by routers/governance files (826 read), scripts/tests where present (23 script or script-like files), and explicit anti-slop or quality gates in the repository. It is limited by missing live validation, missing negative fixtures, weak automated checks, or incomplete failure-mode coverage depending on the engine.

Top deficiencies:

- The catalogue is broad enough to risk shallow coverage in some domains unless each high-risk skill has executable examples.
- Many empty legacy directories remain after migrations and can confuse discovery or imply unimplemented capability.
- Currency depends on periodic manual updates; fast-moving platform guidance needs dated source registers and validation fixtures.

## World-Class Output Capability

Raw score: 15/20.

The engine can produce credible specialist output in its domain, but the audit asks whether the output is indistinguishable from a top-tier firm. The current blocker is usually the same pattern: not enough finished exemplars, proof packs, rendered outputs, evaluator simulations, or audited workbooks to demonstrate repeatable excellence.

Top deficiencies:

- The catalogue is broad enough to risk shallow coverage in some domains unless each high-risk skill has executable examples.
- Many empty legacy directories remain after migrations and can confuse discovery or imply unimplemented capability.
- Currency depends on periodic manual updates; fast-moving platform guidance needs dated source registers and validation fixtures.

## Architecture & Discoverability

Raw score: 12/15.

The structure is discoverable enough to route by filesystem and frontmatter, but there are 76 skills missing name frontmatter and 76 missing description frontmatter. Empty directories (49) and large local project/example surfaces can also reduce routing clarity.

Top deficiencies:

- The catalogue is broad enough to risk shallow coverage in some domains unless each high-risk skill has executable examples.
- Many empty legacy directories remain after migrations and can confuse discovery or imply unimplemented capability.
- Currency depends on periodic manual updates; fast-moving platform guidance needs dated source registers and validation fixtures.

## Composability & Reuse

Raw score: 10/15.

Reuse is visible through references, templates, scripts, examples, cross-engine trigger blocks, and local governance. The gap is less about having reusable pieces and more about proving they compose into complete delivery workflows with stable contracts and acceptance criteria.

Top deficiencies:

- The catalogue is broad enough to risk shallow coverage in some domains unless each high-risk skill has executable examples.
- Many empty legacy directories remain after migrations and can confuse discovery or imply unimplemented capability.
- Currency depends on periodic manual updates; fast-moving platform guidance needs dated source registers and validation fixtures.

## Currency & Compliance

Raw score: 8/10.

Currency and compliance depend on dated source registers, official standards, live-rate or platform refresh protocols, and release gates. The score is constrained when standards are named but not tied to dated verification, reviewer sign-off, or automated freshness checks.

Top deficiencies:

- The catalogue is broad enough to risk shallow coverage in some domains unless each high-risk skill has executable examples.
- Many empty legacy directories remain after migrations and can confuse discovery or imply unimplemented capability.
- Currency depends on periodic manual updates; fast-moving platform guidance needs dated source registers and validation fixtures.
