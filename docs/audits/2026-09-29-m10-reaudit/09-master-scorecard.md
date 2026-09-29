# Master scorecard

Engine: chwezi-dev-engine at `67ae982`, 29 September 2026. Labels: **measured**, **judged**,
**NOT_ASSESSED**. No score is 70 or above, so no extraordinary-justification paragraph is required.

## A. Engine dimensions (the 11 in `audit-dimensions.md`)

| # | Dimension | Label | Score | Prior (2026-09-06) | Evidence |
|---:|---|---|---:|---|---|
| 1 | Doctrine and philosophy | judged | 62 | not scored | Explicit evidence-pack, anti-slop, Kaizen, `NOT_ASSESSED`, never-store-extractions and currentness-gate doctrine in `SKILL.md` and `AGENTS.md`. Deductions: doctrine scattered across router, AGENTS.md, `rules/`, `docs/` and templates; 19 AI skills restate it as identical boilerplate rather than applying it; `professional-word-output` uses Inter and Arial, both on the engine's own hard-ban list. |
| 2 | Taxonomy and structure | judged | 54 | 52 | Router rows for game/GIS/desktop added and alias conflict closed; still a 1-skill android group, a group-level `execution-plan-scripts`, grab-bag `sdlc-meta` and `product-business`, 37 alias stubs holding references, a circular PostgreSQL alias pointer. See [02](02-coverage-and-taxonomy.md). |
| 3 | Skill depth and rigour | judged | 55 | not scored (semantic census unavailable) | Deep: `api-design-first`, `android-development`, `cicd-pipelines`, `multi-tenant-saas-architecture`. Thin routers: `postgresql-engineering` (97 lines), `gis-platform-engineering` (85), `online-multiplayer-and-game-backend` (54, 1 reference). 59/167 skills have duplicated contract headings; 5 carry the generic "task is unrelated to this parent skill" exclusion. |
| 4 | Worked examples and applied proof | judged (measured inputs) | 42 | not scored | 39/167 active skills mention a worked example; game 1/25; security 0/6; iOS 0/4. One engine exemplar (FieldOps Ledger, verified 2026-07-08). Benchmarks F01-F16 checker self-tests pass (measured infrastructure) but Tier 3 is `NOT_ASSESSED` and adds nothing. |
| 5 | Standards currency | judged, 6 external checks | 48 | 50 | Android target SDK below Play requirement; Next.js removed/deprecated APIs; PostgreSQL stops at 16; two source-register rows overdue. Positives: WWDC26 iOS baseline, ASVS 5.0.0 version-qualified, OWASP 2025 edition pinning. See [06](06-standards-benchmark.md). |
| 6 | Coverage / output-type readiness | judged | 53.1 | individual rows only | Mean of 12 output types; see [05](05-per-output-type-readiness.md). |
| 7 | Accessibility and inclusivity | judged | 50 | not scored | WCAG 2.2 cited 12 times but 2.1 still 11 times; visual accessibility delegated to the design engine (correct); game accessibility skill exists but fails contract checks; no mobile accessibility worked example. |
| 8 | Production, handoff, render fidelity | judged | 48 | NOT ASSESSED | `templates/delivery-dod/evidence-pack.md` and evidence tables in every skill define handoff; no retained build, render, deployment or store-submission evidence for any output family. |
| 9 | Redundancy and hygiene | judged (measured inputs) | 52 | not scored | Guardrail: 0 duplicate names, 0 errors, 14 oversize warnings. 59 skills with duplicated contract sections; 19 identical boilerplate blocks; 78 alias stubs, 37 holding reference trees (including the migrated `ux-principles-101` with 9 files); personal phone number repeated in 120 SKILL.md acknowledgements. Compliance 136/165 fully compliant (82.4 %) against 153/179 (85.5 %) on 6 September. |
| 10 | Discovery and routing | **measured** | **59.7** | 144/158 top-one (proxy) | Engine Eval Readiness; see section D and [11](11-measured-evidence.md). Auditor's judged score for the raw number: 66 (p@1 90.6 %, p@3 100 %, router intent rows complete; offset by 6.6 % fixture coverage and bare-slug links to retired skills). |
| 11 | Safety and integrity | judged | 58 | not scored | Fail-closed Git safety hooks, source-ingestion guardrail, skill safety gate, `NOT_ASSESSED` discipline. Deductions: unsupported Android crash claim; Next.js route protection in middleware alone; stale APIs presented as current without dates. |

## B. Groups

| Group | Score | Group | Score |
|---|---:|---|---:|
| architecture | 60 | languages | 56 |
| devops-cloud | 58 | finance-accounting | 52 |
| ios | 58 | backend-databases | 50 |
| saas | 58 | gis | 50 |
| ai | 57 | security | 50 |
| sdlc-meta | 57 | 00-meta-initialization | 50 |
| product-business | 49 | execution-plan-scripts | 48 |
| frontend-ux | 48 | game-development | 46 |
| android | 44 | mobile-cross | 44 |

Unweighted mean 51.9. Justifications in [03](03-existing-groups-audit.md).

## C. Output types

Skill/engine meta-work 64; APIs 60; web applications and SaaS back ends 58; AI/LLM systems and agents 58;
iOS 58; testing and CI/CD 55; databases 52; security and compliance 52; engineering documentation 50;
Android 45; game development 45; cross-platform mobile 40. **Mean 53.1.**

## D. Engine Eval Readiness (measured; recomputed and agreed)

`Readiness = 30 x T1 + 40 x mean(T2_p1, T2_neg, T2_cov, T2_clean) + 30 x T3`

- T1 = 3/3 = 1.0000; 30 x 1.0000 = 30.00
- T2 mean = (0.9058 + 1.0000 + 0.0659 + 1.0000) / 4 = 2.9717 / 4 = 0.7429; 40 x 0.7429 = 29.72
- T3 = 0 (`NOT_ASSESSED`, zero-spend rule); 30 x 0 = 0.00
- **Readiness = 59.7.** The ceiling while T3 is unexecuted is 70.

## E. The three overall numbers

Buckets (weights 30/25/15/10/10/10):

| Bucket | Score | Points |
|---|---:|---:|
| Output-type readiness (30 %) | 53.083 | 15.925 |
| Skill depth and worked examples (25 %) | (55 + 42) / 2 = 48.5 | 12.125 |
| Standards currency (15 %) | 48 | 7.200 |
| Taxonomy (10 %) | 54 | 5.400 |
| Doctrine (10 %) | 62 | 6.200 |
| Hygiene (10 %), raw | (52 + 66 + 58) / 3 = 58.667 | 5.867 |
| Hygiene (10 %), measured-constrained | (52 + 59.7 + 58) / 3 = 56.567 | 5.657 |

- **Raw** = 15.925 + 12.125 + 7.200 + 5.400 + 6.200 + 5.867 = **52.7**
- **Measured-constrained** = 15.925 + 12.125 + 7.200 + 5.400 + 6.200 + 5.657 = **52.5**
- **Published** = min(52.5, 65) = **52.5** (craft-standard acceptance evidence absent; cap applied, not binding)

## F. NOT_ASSESSED

Tier 3 behavioural runs (0 grading files); per-skill fan-in (`skill_fanin.py` not run); POSIX
execution of scripts and hooks; any build, render, deployment or store submission; live (non-lexical)
routing.
