# Per-output-type readiness

All scores judged against the question "can this engine drive the deliverable end to end at the
top 0.1 % bar?". No output type has retained build, render or behavioural evidence; Tier 3 is
`NOT_ASSESSED` for every row.

## Ranked table

| Rank | Output type | Score | Biggest gaps | Skills to add or harden |
|---:|---|---:|---|---|
| 1 | Skill and engine meta-work | 64 | Fixture coverage 11/167; T3 zero; contract gate checks presence not duplication or specificity | Harden `contract_gate.py` to flag duplicate headings and shared boilerplate; extend fixtures |
| 2 | APIs | 60 | Worked contract only in the FieldOps example; no executed contract tests retained | Add a worked OpenAPI 3.1 contract plus conformance run to `api-design-first/examples/` |
| 3 | Web applications and SaaS back ends | 58 | Next.js skill stale (removed request APIs, deprecated middleware); FieldOps Ledger is a fictional pack last verified 2026-07-08 | Rewrite `nextjs-app-router` against the current major with a pinned version and a data-access-layer auth pattern |
| 4 | AI/LLM systems and agents | 58 | Identical generic contracts in 19 skills; eval guidance without executed results; over-split agent skills | Replace boilerplate with skill-specific decision rules; add a scored eval worked example |
| 5 | iOS apps | 58 | No worked example; `ios-development` 115 lines against a 489-line monetisation skill | Add a worked feature slice with availability fallback |
| 6 | Testing and CI/CD | 55 | No executed pipeline evidence; oversize entrypoints (cicd, kubernetes, cloud) | Split `cicd-pipelines` below 20 KB; add a pipeline run artefact |
| 7 | Databases | 52 | PostgreSQL versions stop at 16 (18.6 current); `pgcrypto` contradiction; ops depth behind a circular alias | Promote PostgreSQL operations references into `postgresql-engineering`; add 17/18 features and a migration worked example |
| 8 | Security and compliance artefacts | 52 | No CVSS; PHP-centric web audit; no MASVS; DPIA Uganda-only | Add CVSS scoring (current FIRST version, verified at edit time) and a worked finding; add mobile verification (MASVS) guidance; generalise DPIA to GDPR-style regimes |
| 9 | Engineering documentation (ADRs, specs, runbooks) | 50 | ADRs mentioned in 17 skills with no owner; runbooks mentioned in 48 with no template owner | Name an ADR/runbook owner in the router and ship one worked ADR and one worked runbook |
| 10 | Android apps | 45 | Target SDK 35 below Play's API 36 requirement; unsupported edge-to-edge crash claim; one active skill | Correct target SDK and insets guidance; restore data-persistence and TDD depth from alias stubs |
| 11 | Game development | 45 | 22/25 skills fail contract checks; one worked example; no engine or netcode versions | Complete contracts; add a vertical-slice worked example; date engine versions |
| 12 | Cross-platform mobile | 40 | React Native only as a reference checklist; Flutter absent; PWA skill versionless | Decide scope explicitly: add or declare out of scope Flutter and React Native, with routing |

**Overall output readiness: 53.1** (mean of the 12 rows: 637 / 12).

Note on ordering: rows are ranked by score; ties (58, 52, 45) are ordered by breadth of the group behind them.

## Movement against 6 September

The prior audit gave individual output judgements and no aggregate. Closed since then: router rows for
game, GIS and desktop; alias target conflict for UI skills. Still open from the prior list: fictional
exemplar as the only full-stack proof; retained build/render/replay evidence for each family.
