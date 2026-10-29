# Scope and evidence

**Cycle:** 2026-10 Dev Engine Kaizen  
**Snapshot:** `22b8e7d0` (full commit: see cycle branch ancestry)  
**Owner:** Chwezi Dev Engine  
**Access date:** 2026-10-29  
**Status:** pre-change baseline frozen before implementation

## Scope

This cycle covers the active engineering catalogue and its practitioner path for a tenant-scoped invoice listing across PHP, Next.js and Android Compose. It also covers Claude/Codex native discovery evidence and the package/checkout file-count requirement. It does not change canonical accounting doctrine or another engine, make a production deployment, submit to a public marketplace, call a paid model, or mutate user-level Codex configuration.

Repository state at the start was clean on `main`, with `22b8e7d0` at HEAD. The cycle proceeds on `kaizen/2026-10`. No pre-existing local edits needed exclusion from commits.

## Practitioner tasks and observations

The synthetic tenant/invoice task, flawed review specimen, routing decisions, defects, and limitations are recorded in the preparation observation file, which is retained outside the repository at `/tmp/chwezi-portfolio-kaizen/dev-prep/observations.md`. The essential findings are:

- PHP task routes through `world-class-engineering`, `php-modern-standards`, `mysql-engineering`, and `multi-tenant-saas-architecture`; `saas-accounting-system` supplies the posting boundary. The target is a read-only invoice listing. The existing source guidance supports the design, but a complete linked tenant-invoice fixture was missing. PHP 8.5.12 with PDO SQLite was exercised; MySQL deployment is not established.
- The deliberately flawed review specimen contains SQL injection, a missing verified tenant predicate, an N+1 customer query, ledger mutation outside `JournalPostingService`, and unescaped output. This was a manual practitioner review, not a benchmark of live model detection.
- Android routing selects `android-development`; its guidance still describes target API 35 as current. Google Play target requirements and Android platform currency were checked in official sources on 2026-10-29; no emulator/build proof is claimed. The unsupported statement that omitting `enableEdgeToEdge` necessarily crashes on Android 15 is treated as an open unsupported claim.
- Next.js routing selects `nextjs-app-router`. The audited examples include synchronous request parameters, removed `request.ip`/`request.geo`, a role cookie trusted as authority, an unscoped shared users cache/database query, and an unchecked mutation. Official Next.js 16 documentation was checked on 2026-10-29. Copy/paste safety of the examples is a release blocker until corrected and regression checked.

## Baseline measures

The prepared evidence is in `/tmp/chwezi-portfolio-kaizen/dev-prep/`: `validators.json`, `validator-1.log` through `validator-3.log`, `coverage.json`, `compliance.json`, `structural.json`, `currentness.json`, and `public-control-plane.log`. It records exact commands and outputs. Key observed measures:

- Routing: 167 active skills, 191 fixtures, precision@1 173/191, precision@3 191/191. There are 78 owned negatives: 74 pass, 4 external cases are `NOT_ASSESSED`.
- Catalog guardrail: exit 0 with 14 warnings; no errors. Pytest: 207 passed, 3 skipped.
- Default-parent control-plane invocation exits 1 because checkout aliases do not share that parent layout. The device-mapped public catalogue run passes 11 installed public engine contracts. A private extra registry entry is outside the public catalogue measurement and remains `NOT_ASSESSED`; it is not counted as a pass.
- The checkout has 2,552 filesystem entries including `.git`, and 2,468 package-oriented entries under the documented exclusion method in `/tmp/chwezi-portfolio-kaizen/packaging-research.md`; both counts are below the documented 5,000-file submission bound. This is a checkout count, not a built-archive count.
- Native Claude and Codex offline install/load proof succeeded in isolated Podman environments per root-provided logs. Default Codex prompt-input loads 130/165 manifest paths, with 35 missing and an approximately 22,000-character skills-section truncation. An explicitly pinned Luna/high invocation with `skills.max_context_tokens=10000` loads 165/165 paths with no missing paths. This is evidence for those offline invocations, not a claim about every account or runtime. No raw prompt output is included here.
- Exact duplicate-H2 scan found 64 affected entrypoints, a different measure from the earlier 59-heading audit. Worked-example counts vary by definition; no direct trend is claimed.
- The source inventory found 27 expired source IDs. Exact IDs and scanner output are in the external preparation record; this cycle only updates records tied to selected fixes.

## Currentness and models

Official source snapshots for Android/Google Play, Kotlin/Compose, Next.js, PHP, MySQL, PostgreSQL, OWASP ASVS/Top 10, PCI DSS, and SLSA were checked on 2026-10-29. Claim-level records and limitations are in `/tmp/chwezi-portfolio-kaizen/dev-prep/currentness.json`. Model catalogue/release evidence is in `/tmp/chwezi-portfolio-kaizen/packaging-research.md`: the local Codex policy check passed and Luna/high remains the selected default. Comparative quality, latency, cost, and account entitlement remain `NOT_ASSESSED`; no paid model calls were made.

Selected official advisory and release sources for Next.js, PHP, PostgreSQL, MySQL, Android, Kotlin and Compose were recorded in the cycle source register. Exact applicability remains conditional on the deployed version, package/build, enabled features and configuration. The Next.js 2026-11-03 notice did not yet include affected-version details at the access date; its applicability remains `NOT_ASSESSED`.

## Command and review evidence

Prepared command outputs are frozen before edits. Final validator and runtime results are in [the validation record](04-validation-record.md). Tests and runtime checks are separated from structural/catalogue checks. Missing MySQL, Android emulator, production deployment, account-specific marketplace acceptance, independent stakeholder review, and public directory acceptance remain `NOT_ASSESSED` unless later evidence closes them.
