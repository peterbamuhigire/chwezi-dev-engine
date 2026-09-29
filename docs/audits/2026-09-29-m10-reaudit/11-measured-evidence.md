# Measured evidence

Host: Windows 11, Git Bash, Python on PATH, `PYTHONDONTWRITEBYTECODE=1`. Working directory: engine
root `C:\wamp64\www\chwezi-dev-engine` at HEAD `67ae982`. Run on 29 September 2026 by the auditor.

## Validators and tests

| # | Command | Exit | Key output |
|---:|---|---:|---|
| 1 | `python scripts/validate_engine_control_plane.py --workspace-root ..` | 0 | engines: 12; findings: 0; "PASS: control-plane registry is valid" |
| 2 | `python -X utf8 scripts/routing_smoke_test.py --min-rank1 88 --lint-fixtures` | 0 | active skills indexed 167; fixtures 191; precision@1 173/191 (90.6 %); precision@3 191/191 (100.0 %); negatives 78 (owned 78; pass 74, fail 0, not assessed 4); fixture lint findings 0; failures 0 |
| 3 | `python -X utf8 scripts/skill_catalog_guardrails.py` | 0 | findings 14 (errors 0, warnings 14); all warnings are report-only `skill-bytes` over 20,480 bytes (largest `saas/subscription-billing` 28,876) |
| 4 | `python -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all` | 0 | scanned 161; 0 errors; 0 warnings; 6 exempt |
| 5 | `python -X utf8 skills/sdlc-meta/skill-engine-audit/scripts/engine_compliance.py --root .` | 0 | skills 165; fully compliant 136; safe fixes applied 0; failures: input_contract 23, degraded_mode 23, capability_contract 14, decision_rules 13, five_anti_patterns 2, trigger 1, output_contract 1, portable_sections 1, no_empty_contract_sections 1 |
| 6 | `python -X utf8 -m pytest tests -q -p no:cacheprovider` | 0 | 207 passed, 3 skipped |

Notes:

- Command 5 counts 165 because it scans `skills/` only; the two `00-meta-initialization` skills make 167.
- `engine_compliance.py --json` was also run (exit 0) to list failing skills: 22 in game-development,
  3 in sdlc-meta (`council`, `github-ops`, `santa-method`), and one each in finance-accounting,
  frontend-ux, product-business, saas.
- `git status --short` showed the same five pre-existing M10-14 entries before and after; no command
  modified the tree.

## Catalogue probes (grep/find, exit 0)

| Probe | Result |
|---|---|
| Active SKILL.md files | 165 under `skills/` + 2 under `00-meta-initialization/` = 167 |
| `ALIAS.md` stubs | 78; 37 with a `references/` tree |
| Skills with a duplicated Inputs, Outputs or Decision-rules heading | 59 |
| Skills carrying the identical AI operating-contract block | 19 (all in `ai/`) |
| Active skills mentioning a worked example (SKILL.md or first-level reference) | 39 |
| SKILL.md containing the personal phone number acknowledgement | 120 |

## Engine Eval Readiness

Inputs from `chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-14/eval-readiness.json`
(entry `chwezi-dev-engine`) and `readiness/coverage.json`:

| Slot | Input | Fraction | Cross-check |
|---|---|---:|---|
| T1 | 3 of 3 declared catalogue validators pass | 1.0000 | This audit's runs 1-3 exit 0 |
| T2_p1 | 173 / 191 | 0.9058 | This audit's run 2: 173/191 |
| T2_neg | 74 local passes + 4 cross-engine mirrors passing in the union oracles = 78 / 78 | 1.0000 | Run 2: 74 pass, 0 fail, 4 not assessed locally |
| T2_cov | 11 / 167 skills with at least 3 positives and 2 owned negatives | 0.0659 | coverage.json: 124 skills with any positive, 37 with any owned negative |
| T2_clean | 0 undeclared of 9 cross-engine pairs at or above 0.75 | 1.0000 | eval-readiness.json |
| T3 | 0 executed; all planned runs `NOT_ASSESSED` (zero-spend rule) | 0 | 0 `grading.json` files |

Arithmetic: 30 x 1.0000 = 30.00; (0.9058 + 1.0000 + 0.0659 + 1.0000) / 4 = 0.7429, x 40 = 29.72;
30 x 0 = 0.00. **Readiness = 59.7.** Auditor recomputation: 59.717, rounds to 59.7. **Agreed.**

Caveat: T2 figures are a lexical drift guard, not proof of live routing. T2_neg depends on four
cross-engine mirrors that pass only in the union oracle, not in the local run.

## NOT_ASSESSED

| Slot | Cause |
|---|---|
| Tier 3 behavioural runs | Zero-spend rule; 0 grading files |
| Per-skill fan-in | `skill_fanin.py` not run in this audit |
| Live routing | Only the lexical proxy exists |
| POSIX execution | Windows host only |
| Build, render, deployment, store submission | No retained artefacts for any output family |

## External fetches (free, no paid APIs)

Six pages, listed with URLs in [06](06-standards-benchmark.md), accessed 29 September 2026.
