# Standards benchmark (short, targeted)

Scope: six primary sources fetched on 29 September 2026 to test specific claims found in sampled
skills. This is not a full standards sweep; every other currency judgement in this audit is judged
from the engine's own currentness records (`docs/source-registers/ai-platforms.md`,
`docs/source-registers/skills-engine-currentness-2026-09.json`), with no fresh external research.

| # | Engine claim (file) | Primary source (accessed 2026-09-29) | Finding |
|---|---|---|---|
| 1 | "Target SDK: 35 (Android 15)"; "Target the latest stable SDK (currently 35)" (`skills/android/android-development/SKILL.md` lines 50, 210) | https://developer.android.com/google/play/requirements/target-sdk | From 31 August 2026 new apps and updates must target API level 36 (extension possible to 1 November 2026). **Stale; would block Play submission.** |
| 2 | Without `enableEdgeToEdge()` "the app crashes immediately on Android 15 devices" (same file, lines 206, 384) | https://developer.android.com/develop/ui/views/layout/edge-to-edge | Edge-to-edge is enforced automatically for apps targeting SDK 35 on Android 15+; `enableEdgeToEdge()` enables it on earlier versions; the risk is obscured content and unhandled insets, not a crash. **Unsupported claim.** |
| 3 | `request.ip`, `request.geo` in middleware (`skills/frontend-ux/nextjs-app-router/SKILL.md`, Middleware section) | https://nextjs.org/docs/app/guides/upgrading/version-15 | "The `geo` and `ip` properties on `NextRequest` have been removed" in Next.js 15. **Stale code.** |
| 4 | `middleware.ts` convention (same file) | https://nextjs.org/docs/app/guides/upgrading/version-16 (docs version 16.3.6) | The `middleware` filename and export are deprecated and renamed to `proxy`. **Stale convention; no version pinned in the skill.** |
| 5 | Highest PostgreSQL version cited is 16 (`postgresql-engineering` references); `gen_random_uuid()` "requires pgcrypto" (`postgresql-fundamentals.md` line 375) versus "without requiring pgcrypto" (`postgresql-patterns.md` line 134) | https://www.postgresql.org/support/versioning/ | Supported majors 14-18, current 18.6; 19 in beta. The engine does not cover 17 or 18. The `pgcrypto` contradiction is internal (the patterns file is the correct one; built-in since 13 per the engine's own cited docs page). |
| 6 | ASVS "v5.0.0 is the latest stable release" (checked 2026-09-26) (`ecommerce-platform-audit-requirements`, `web-app-security-audit/references/network-security-audit.md`) | https://owasp.org/www-project-application-security-verification-standard/ | Latest stable is 5.0.0. **Current and correctly version-qualified.** |

## From the engine's own records (no fresh external research)

- `ai-platforms.md` rows past their next-review date on 29 September 2026: OpenAI changelog (next review
  2026-08-08) and Apple Developer Documentation (2026-09-08).
- `skills-engine-currentness-2026-09.json`: 37 sources, 26 claims, review dates from 2026-10-01
  onwards; accessed 2026-09-17.
- OWASP Top 10 2025 is cited in 7 places; the remaining 2021 identifiers are labelled historical and mapped to 2025 categories (good practice); the API Security Top 10 2023 is cited as a source.
- WCAG 2.2 cited 12 times; WCAG 2.1 still cited 11 times.
- iOS: WWDC26 baseline (Xcode 27, Swift 6.4, iOS 27) checked 2026-06-21.

**Standards currency: 48 / 100 (judged, with six targeted external checks).** Prior: 50. Movement -2:
the iOS and ASVS work is current, but three skills that drive common deliverables (Android, Next.js,
PostgreSQL) are behind primary sources in ways that break builds or submissions, and two register rows
are overdue.
