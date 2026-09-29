# Roadmap to world class

Baseline: published 52.5 (raw 52.7), Readiness 59.7. Targets are believable estimates for the
published number, not commitments. Every currency edit must pass the Digital Research currentness
gate and record source, access date and review date.

## P0: stop shipping defects (target published about 56)

| Move | Files | Acceptance |
|---|---|---|
| Correct Android target SDK to the Play requirement in force (API 36 since 31 Aug 2026), date the claim, and replace the "crashes immediately" statement with the insets obligation | `skills/android/android-development/SKILL.md` | Claim carries source URL and review date; routing fixture unchanged |
| Rewrite Next.js guidance against the current major: remove `request.ip`/`request.geo`, adopt the `proxy` convention, pin the version, move authorisation into a server-side data-access check rather than middleware alone | `skills/frontend-ux/nextjs-app-router/SKILL.md` (add `references/`) | Version stated; auth example checks authorisation at the data layer |
| Add PostgreSQL 17/18 coverage, state the supported range, fix the `pgcrypto` contradiction, and move operations references out of the `postgresql-operations` alias into the active skill | `skills/backend-databases/postgresql-engineering/**`, `skills/backend-databases/postgresql-operations/` | No active link targets an `ALIAS.md`; one statement on `gen_random_uuid()` |
| Remove banned fonts from examples and watermark guidance; route typeface choice to the design engine | `skills/product-business/professional-word-output/references/python-document-generation/references/performance.md`, `references/word-features.md` | No hard-banned face in any active file (add a guardrail check) |
| Deduplicate contract sections in the 59 affected skills; replace the 19 identical AI operating-contract blocks with skill-specific decision rules | `skills/ai/*`, `skills/saas/multi-tenant-saas-architecture`, `skills/architecture/api-design-first`, and the rest of the 59 | Extend `contract_gate.py` to fail on duplicate contract headings and on blocks shared verbatim by more than three skills |
| Refresh the two overdue register rows | `docs/source-registers/ai-platforms.md` | No row past its next-review date |

## P1: prove and cover (target published about 60; Readiness about 64)

| Move | Files | Acceptance |
|---|---|---|
| Raise fixture coverage from 11 to at least 84 skills (50 %) with three positives and two owned negatives, starting with the 43 skills that have none | `scripts/routing_fixtures.yml`, `tests/routing/edge-fixtures.yml` | T2_cov at least 0.50 (Readiness rises about 4.3 points) |
| Complete input, degraded-mode, capability and decision-rule contracts in the 22 non-compliant game skills; add engine/netcode version notes | `skills/game-development/*` | `engine_compliance.py` game group 25/25 |
| Add worked examples where there are none: one per security, iOS, GIS, database and game skill family | `examples/` or `skills/<group>/<skill>/references/*-worked-example.md` | At least 70 active skills with a worked example |
| Decide cross-platform scope: add React Native and Flutter routing (or declare them out of scope in the router); add OWASP MASVS mobile verification | `SKILL.md`, `skills/mobile-cross/*`, `skills/security/*` | Router row states the decision |
| Name one ADR/runbook owner and ship a worked ADR and runbook | `skills/architecture/system-architecture-design` or `skills/sdlc-meta/sdlc-documentation` | Router lists the owner |
| Restructure: fold `android` aliases back into active depth or merge the group into mobile; move agent-workflow utilities out of `sdlc-meta` | `skills/android/*`, `skills/sdlc-meta/*`, `docs/skill-aliases.yml` | No 1-skill group except by recorded decision |

## P2: behavioural evidence and the cap (target published about 64, under the 65 cap)

| Move | Files | Acceptance |
|---|---|---|
| Execute a funded, pinned-model Tier-3 run set for the F01-F16 benchmarks and representative skill cases | `benchmarks/solution-selection/`, engine-agents `evals/behavioural/results/**` | Validated `grading.json` bound to model and CLI version; T3 above 0.5 lifts Readiness above 74 |
| Retain one build, render or deployment artefact per output family | `examples/` | Evidence pack per family with environment and owner |
| Produce the portfolio craft-standard acceptance evidence | per `portfolio-craft-standard-2026-09-04.md` | Only this removes the 65 cap |

Above 65 is not reachable without P2's acceptance evidence, whatever the dimension scores.
