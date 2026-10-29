# Frozen baseline scorecard

**Snapshot:** `22b8e7d0` (pre-change)  
**Date:** 2026-10-29  
**Scoring:** each applicable dimension /100; overall is the arithmetic mean. Scores are practitioner judgement anchored in the evidence below, not test-pass percentages. Baseline is frozen before any implementation change.

| Dimension | Raw | Evidence | Deficiency |
|---|---:|---|---|
| Doctrine | 65 | `skills/sdlc-meta/world-class-engineering/SKILL.md`; pre-change Next.js and Android examples in `skills/frontend-ux/nextjs-app-router/SKILL.md` and `skills/android/android-development/SKILL.md` | Current operational examples contradict the security and currency principles they are meant to apply. |
| Taxonomy and routing | 65 | Prepared routing run: 167 skills, 191 fixtures, precision@1 173/191 and precision@3 191/191; 78 owned negatives, 74 passed and 4 `NOT_ASSESSED` ([prepared routing output](/tmp/chwezi-portfolio-kaizen/dev-prep/validator-2.log)) | Routing is measurable but rank-1 precision and negative ownership are incomplete. |
| Skill depth | 50 | 64 active entrypoints have an exact duplicate H2 ([pre-change structural scan](/tmp/chwezi-portfolio-kaizen/dev-prep/structural.json)) | Repeated headings and generic sections make task-specific instructions harder to distinguish. |
| Applied proof | 35 | Pytest 207 passed, 3 skipped ([prepared test output](/tmp/chwezi-portfolio-kaizen/dev-prep/pytest.log)); prepared PHP SQLite proof ([fixture evidence](/tmp/chwezi-portfolio-kaizen/dev-prep/invoice-proof)); task observations in `00-scope-and-evidence.md` | No linked end-to-end invoice fixture covered the route; no Next build or Android emulator proof. |
| Standards currency | 35 | `/tmp/chwezi-portfolio-kaizen/dev-prep/currentness.json`; Android API 35 guidance and stale/unsupported examples remain | Several examples lagged verified platform behavior; source expiry remains across unrelated entries. |
| Output readiness | 40 | Practitioner tasks and file/line observations in `/tmp/chwezi-portfolio-kaizen/dev-prep/observations.md` | Unsafe Next.js authentication, cache, mutation and API examples can be copied into an output. |
| Accessibility and inclusion | 55 | Android/Next guidance and absence of a rendered invoice implementation in the preparation record | No matched, rendered cross-platform invoice flow or accessibility evidence exists. |
| Production and handoff | 35 | Catalog/release gates and available PHP runtime; no MySQL, Android emulator, or production proof | Delivery handoff does not establish tested deployment, recovery, or target-runtime compatibility for the observed slice. |
| Hygiene | 50 | 64 exact-H2 duplicates ([structural scan](/tmp/chwezi-portfolio-kaizen/dev-prep/structural.json)); source/link and historical path findings in prepared structural and coverage reports | Duplicate sections and stale records remain in the active catalogue. |
| Safety and integrity | 35 | Next.js role-cookie trust, unscoped users cache/read, unchecked mutation and PHP flawed specimen review | Affected examples fail tenant isolation and authorization expectations; the Next route is a release blocker. |

**Raw mean:** (65 + 65 + 50 + 35 + 35 + 40 + 55 + 35 + 50 + 35) / 10 = **46.5**.  
**Portfolio Standard cap:** min(46.5, 65) = **46.5/100**.  
**User’s initial 45-point reporting cap:** min(46.5, 45) = **45/100**. The standard cap and requested cap are both shown; the stricter requested cap is used for the user-facing cycle headline unless directed otherwise.

## Blockers and unassessed evidence

The unsafe tenant/cache/auth examples are a release blocker regardless of the score. Native offline loading confirms installation and the specific tested prompt-input behavior only. MySQL deployment, Android emulator/build, production operations, public marketplace acceptance, account-specific plugin availability, independent human review, and comparative model quality/cost/latency remain `NOT_ASSESSED`.
