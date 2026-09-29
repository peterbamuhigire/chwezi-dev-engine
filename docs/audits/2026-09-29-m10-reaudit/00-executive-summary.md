# Executive summary

## Verdict

**Published 52.5 / 100** (raw 52.7; measured-constrained 52.5; Engine Eval Readiness 59.7).
The engine is a well-instrumented catalogue whose machinery outruns its content. Validators, routing
fixtures, contract gates and safety hooks all pass. What the engine tells an agent to build is less
reliable: several sampled skills give platform instructions that primary sources now contradict, the
evidence of applied output is thin outside a single fictional SaaS example, and no behavioural run
has ever been graded.

## Headline findings

1. **Stale platform guidance that would cause real defects (standards currency 48).**
   `skills/android/android-development/SKILL.md` fixes Target SDK at 35 and calls it "currently" the
   latest; Google Play has required API level 36 for new apps and updates since 31 August 2026.
   `skills/frontend-ux/nextjs-app-router/SKILL.md` uses `request.ip` and `request.geo` (removed in
   Next.js 15) and a `middleware.ts` convention that Next.js 16 deprecates in favour of `proxy.ts`; the
   skill pins no Next.js version. `postgresql-engineering` references stop at PostgreSQL 16 while 18.6 is
   current, and two of its references disagree on whether `gen_random_uuid()` needs `pgcrypto`.
   Sources in [06](06-standards-benchmark.md).
2. **Contract normalisation left duplicated structure in 59 of 167 skills.** Those skills head
   Inputs, Outputs or Decision rules twice (for example `multi-tenant-saas-architecture`,
   `api-design-first`), and 19 of the 26 AI skills carry a word-for-word identical generic "Operating contract".
   The contract gate reports 0 errors because it checks presence, not duplication or specificity.
3. **Applied proof is sparse (worked examples 42).** 39 of 167 active skills mention a worked example in SKILL.md or a first-level reference; game
   development has 1 across 25 skills; the only engine-level exemplar is FieldOps Ledger, last verified
   2026-07-08. Benchmarks F01-F16 have passing good/bad checker self-tests, which is real harness
   progress, but zero Tier-3 runs mean no model output has been graded.
4. **Routing is measured and sound in precision, weak in coverage (Readiness 59.7).** Precision@1 is
   173/191 (90.6 %), owned negatives 78/78, collisions clean; but only 11 of 167 skills have three
   positives and two owned negatives (6.6 %), and 43 skills have no positive fixture. Lexical figures
   are a drift guard, not proof of live routing.
5. **Game development is broad but under-contracted.** 22 of its 25 active skills fail at least one
   contract check in `engine_compliance.py` (input contract, degraded mode, capability contract,
   decision rules); `online-multiplayer-and-game-backend` is 54 lines with one reference.
6. **The engine breaks its own doctrine in one place.** `professional-word-output` registers Inter as
   a brand font in a code example and recommends Arial for watermarks; both are on the hard-ban list
   in the engine's own AGENTS.md design trigger block.

## What is strong

- All validators exit 0; 207 tests pass (3 skipped); control plane valid across 12 engines.
- Top router now carries explicit game, GIS and desktop intent rows (a 6 September deficiency closed),
  and the `ux-for-ai` / `ux-principles-101` alias conflict was resolved in commits `9fd98a9` and `67ae982`.
- iOS guidance carries a dated WWDC26 baseline (Xcode 27, Swift 6.4, iOS 27) with availability policy.
- ASVS guidance is version-qualified (v5.0.0, checked 2026-09-26) in the two skills that cite it, and
  v5.0.0 is confirmed as the current stable release.
- Doctrine is explicit: evidence packs, `NOT_ASSESSED` semantics, source-ingestion guardrail, Git
  safety hooks that fail closed.

## Path to the bar

P0 fixes the defects that would ship bugs (Android target SDK and edge-to-edge claim, Next.js request
APIs and proxy convention, PostgreSQL version and `pgcrypto` contradiction, the banned-font example)
and deduplicates contract sections: target about 56 published. P1 raises fixture coverage above 50 %
of skills and adds worked examples to game, mobile and database skills: target about 60. P2 executes
a funded Tier-3 run set and earns craft-standard acceptance evidence, the only route past 65: target
about 64 under the cap. Detail in [10](10-roadmap-to-world-class.md).
