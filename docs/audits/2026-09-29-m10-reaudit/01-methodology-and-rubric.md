# Methodology and rubric

## Auditor independence

The auditor took no part in any my-10-kaizen phase and made no change to the engine. Git was used
read-only (`git log`, `git status`). The working tree held unstaged M10-14 edits to
`skills/sdlc-meta/skill-engine-audit` (SKILL.md, `audit-dimensions.md`, `report-structure.md`,
`scoring-rubric.md`, new `eval-readiness-worked-example.md`); they were read as the rubric and left
untouched. `git status --short` showed the same five entries before and after the validator run.
Files were written only to this folder.

## How the audit ran

1. **Harness first (SKILL.md step 0).** Ran the six commands in [11](11-measured-evidence.md) in the
   engine root with `PYTHONDONTWRITEBYTECODE=1`, recording exit codes and key lines. The compliance
   script ran read-only (no `--fix-safe`; "safe fixes applied: 0").
2. **Readiness.** Recomputed the Engine Eval Readiness from the stored M10-14 inputs
   (`chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-14/eval-readiness.json`,
   `readiness/coverage.json`, `readiness/tier1-results.json`) and cross-checked T2_p1 against this
   audit's own smoke-test run (173/191, identical).
3. **Scope.** Read the router (`SKILL.md`), `CLAUDE.md` (imports `AGENTS.md`), `AGENTS.md` doctrine,
   `docs/skill-aliases.yml`, `docs/source-registers/ai-platforms.md` and
   `skills-engine-currentness-2026-09.json`, the FieldOps Ledger example, and globbed every active
   `SKILL.md` (165 under `skills/`, 2 under `00-meta-initialization/`).
4. **Sample reading (16 SKILL.md, all 17 groups touched structurally).** Read in full or in the
   substantive sections: `ai-rag-patterns`, `ai-evaluation`, `game-development-orchestration`,
   `online-multiplayer-and-game-backend`, `postgresql-engineering` (with its references and the
   `postgresql-operations` alias), `gis-platform-engineering`, `nextjs-app-router`,
   `web-app-security-audit`, `council`, `professional-word-output` (with scripts and references),
   `android-development`, `ios-development` (with the WWDC26 reference), `multi-tenant-saas-architecture`,
   `api-design-first`, `accounting-engine`, `cicd-pipelines`. Unsampled groups were scored on structural
   evidence (compliance results, reference counts, line counts, worked-example counts) and this is stated
   per group in [03](03-existing-groups-audit.md).
5. **Catalogue-wide structural probes** (grep/find over `skills/`): worked-example mentions, duplicate
   contract headings, identical boilerplate blocks, alias stubs retaining reference depth, version
   strings for major standards, banned-font usage.
6. **Targeted external currency checks** (no paid APIs): six primary-source pages fetched on
   29 September 2026, listed with URLs in [06](06-standards-benchmark.md). Only the standards named
   there were checked externally; every other currency judgement rests on the engine's own
   currentness records.

## Fleet replaced by one auditor (documented limitation)

The skill prescribes a parallel fleet (standards benchmark, existing-skills audit, taxonomy and gaps,
per-output readiness, hardening, reading list). In this re-audit a single auditor worked through each
concern in turn. Scores therefore did not emerge independently before synthesis; the risk is
anchoring between concerns. Mitigation: each dimension cites its own named evidence, and measured
inputs (validators, Readiness) were fixed before any judged score was written.

## Rubric

Bar: top 0.1 % of software engineering practice. Bands: 90-100 rivals the best; 75-89 excellent with
minor gaps; 60-74 solid but visibly short; 40-59 competent with major gaps; below 40 skeletal.
Strictness directive applied: default 45-65; any 70+ would need an "Extraordinary justification"
paragraph. None was awarded.

Labels: **measured** (cites a command and its result), **judged** (auditor judgement from named
evidence), **NOT_ASSESSED** (not executed; scores 0 wherever it feeds a formula).

## Weighting and the three numbers

| Bucket | Weight | Input |
|---|---|---|
| Output-type readiness and coverage | 30 % | Mean of 12 output-type scores in [05](05-per-output-type-readiness.md) |
| Skill depth and worked examples | 25 % | Mean of skill depth and worked examples |
| Standards currency | 15 % | Dimension 5 |
| Taxonomy and structure | 10 % | Dimension 2 |
| Doctrine and philosophy | 10 % | Dimension 1 |
| Hygiene | 10 % | Mean of redundancy, discovery/routing, safety |

- **Raw**: routing third of hygiene uses the auditor's judged routing score (66).
- **Measured-constrained**: routing third replaced by Readiness (59.7).
- **Published**: `min(measured-constrained, 65)`; the portfolio craft standard's acceptance evidence does
  not exist for this engine, so the cap is applied (it does not bind at 52.5).

Accessibility and production/handoff are scored as dimensions but, following the rubric's six-bucket
weighting, feed the overall only through the output-type scores.

## Limitations

- Lexical routing figures are a drift guard, not proof of live routing.
- Tier 3 is `NOT_ASSESSED`: 0 `grading.json` files; zero-spend rule.
- Fan-in evidence (`skill_fanin.py`) was not run in this audit: `NOT_ASSESSED`.
- Windows host only; POSIX behaviour of scripts and hooks not exercised.
- Sampled 16 of 167 skills in depth; catalogue-wide claims rest on structural probes.
