# Chwezi Product Excellence Standard wiring (8 Nov 2026)

Peter Bamuhigire supplied the Chwezi Core Systems Product Excellence Design Standard on
7 November 2026 and made it the mandatory UI/UX standard for every Chwezi app and system,
effective 01 November 2026 until further communication. The standard is canonical in
`chwezi-design-engine` (`doctrine/product-excellence-standard.md` and the skill
`skills/00-cross-cutting-ops-qa-a11y/chwezi-product-excellence-standard`). This engine adds the
engineering enforcement side only. No new skill was created; the active catalogue stays at 168.

## Changed

- `AGENTS.md`: binding section "Chwezi Product Excellence Standard". Any app or system UI work
  (Android, iOS, KMP/Compose Multiplatform, web front ends, desktop) must follow the standard;
  the design engine is resolved through the engine-routing table, never a hard-coded path.
- New `skills/frontend-ux/frontend-architecture/references/product-excellence-engineering-gates.md`
  (300 lines, ASCII): gate map PX-GATE-01..13 to engineering checks; screen state model with
  orthogonal axes and a state-matrix CI test; component contract tests and `<component>.<part>`
  test tags; screenshot matrix (light/dark, 200% text, widths, RTL, longest language, system
  bars); Baseline Profiles and Macrobenchmark on a physical floor device; Android vitals targets;
  Core Web Vitals; targetSdk 36 consequences; AGP 9 `androidApp` module for Compose
  Multiplatform; offline idempotency keys and queued-versus-confirmed states; the mobile-money
  state machine; ISO 4217 minor units in formatting code; token export to CSS custom
  properties; backend authorisation. Platform facts cite the design engine currentness register
  by ID (`CR:<ID>`) instead of restating them.
- Mandatory cross-reference block ("Chwezi Product Excellence Standard (mandatory)") inside the
  portable block of 14 skills: `frontend-architecture`, `react-development`, `tailwind-css`,
  `nextjs-app-router`, `frontend-performance`, `pos-sales-operations-engineering`,
  `ux-content-strategy`, `avalonia-desktop-development`, `kmp-development`,
  `android-development`, `ios-development`, `mobile-platform-operations`, `pwa-offline-first`,
  `saas-erp-system-design`. Each adds 4 lines and one skill-specific obligation.
- `kmp-development`: its block records that Compose Multiplatform shared UI is the primary
  mobile stack for Chwezi apps and overrides the skill's "shared logic, native UI" default.
- Currency formatting: `tailwind-css/references/house-style-web.md` and
  `android-development/references/house-style-compose.md` changed the `full` formatter from a
  fixed two decimals to the currency's ISO 4217 minor unit (UGX 0), per PX-L10N-001 (owner
  default, 2026-11-07). Compact K/M/B forms are unchanged.
- `frontend-architecture` reference list, `docs/skill-routing-index.md` (row and dated section),
  `docs/quality-gates/release-blocking-gates.md` (product excellence gate row), `CHANGELOG.md`.

## Evidence

Platform facts were not re-read for this wiring; they are cited from the design engine register
(`currentness-register.md`, rows accessed 2026-11-07, review dates 2026-12-07, 2027-02-07 and
2027-05-07). Validator results for this change are recorded in `CHANGELOG.md`. Tool choices for
screenshot tests, provider-specific mobile-money callbacks, the iOS screenshot-protection
mechanism (`CR:S2`) and Compose Multiplatform Dynamic Type and Reduce Motion behaviour
(`CR:K5`) remain `NOT_ASSESSED`.

## Open items

- Closed in wave 2 (below): `kmp-development` body and `android-development` targetSdk 36
  guidance.
- The standard lists the canonical screen states in PX-STATE-001; its foundations reference
  counts eleven in one table. This file cites PX-STATE-001; the design engine should reconcile.

Recovery: revert the listed edits and delete the new reference and this note. No skill was
moved, renamed or deleted.

## Wave 2 (independent audit and repair, 8 Nov 2026)

Fixed:

- Gate count. The standard has thirteen hard gates; PX-GATE-13 (contiguous document numbering
  where a screen issues numbered documents) was missing. The gate map gains a PX-GATE-13 row with
  concurrent-issue, offline-provisional, replay and void tests; `AGENTS.md`,
  `docs/quality-gates/release-blocking-gates.md`, `CHANGELOG.md` and this note now say
  PX-GATE-01..13. The `pos-sales-operations-engineering` and `saas-erp-system-design` blocks
  cite PX-GATE-13 explicitly.
- State count. The gates reference now lists the thirteen PX-STATE-001 states by the policy
  file's IDs (`required_screen_states` in `examples/product-excellence-policy.yaml`) with their
  `na_allowed` flags; the Kotlin and TypeScript state models gain `FilteredEmpty`, and success is
  a one-shot event after server acknowledgement. The state-matrix CI test is specified (unknown
  IDs, N/A on a non-N/A state, missing reason, missing preview) with a YAML example. The design
  engine's `foundations.md` and `accessibility-privacy-localisation.md` still say "eleven"
  (design engine to reconcile; not edited here).
- `kmp-development`: body rewritten to the standard. Strategy is Compose Multiplatform shared
  UI with `core/platform/` adapters (permissions, biometrics, camera and scanning, printing,
  notifications, keyboard and IME, system navigation, secure storage, screenshot protection);
  native screens are a DDR exception; CMP Stable on Android, iOS and desktop, Beta on web
  (`CR:K1`, `CR:K3`); AGP 9 `androidApp` module and `com.android.kotlin.multiplatform.library`
  (`CR:K4`); iOS Dynamic Type and Reduce Motion `NOT_ASSESSED` (`CR:K5`). Module map, project
  tree, decision rules, anti-patterns, inputs, outputs and the description were updated; the
  conflicting passages in `references/kmp-compose-multiplatform.md` and
  `references/skill-deep-dive.md` were aligned. CMP version is not asserted (`CR:K2`).
- `android-development`: compatibility rules updated for targetSdk 36 (Play requirement since
  31 Aug 2026, `CR:M7`): no edge-to-edge opt-out (`CR:M6`), predictive back on by default with
  no `onBackPressed` (`CR:M8`), orientation and resizability locks ignored at sw600dp (`CR:M9`),
  `elegantTextHeight` ignored (`CR:M10`). The "missing `enableEdgeToEdge()` crashes" anti-pattern
  was replaced by an accurate one.
- Gates reference strengthened: `testTagsAsResourceId` for UiAutomator and Macrobenchmark;
  screenshot tool options (Paparazzi, Roborazzi, Compose Preview Screenshot Testing, XCTest,
  Playwright `toHaveScreenshot`) with web 200% zoom and reflow emulation; Baseline Profile
  generation (`BaselineProfileRule`, `includeInStartupProfile`) and Macrobenchmark sketches with
  `StartupTimingMetric` and `FrameTimingMetric` against `CompilationMode.None()`; web field
  (RUM `web-vitals`, CrUX) versus lab (Lighthouse CI, TBT as INP proxy) evidence; Playwright with
  `@axe-core/playwright`; native accessibility scans. All tool versions are `NOT_ASSESSED` apart
  from the library versions in `CR:P7`. Target-size rows cite PX-GEOM-009 (56 dp, 8 dp spacing);
  the `ios-development` block now says the KMP iOS host runs shared CMP UI.

Hygiene finding (reported, not changed): `.claude/settings.local.json` is tracked (added in
`15620f0`, 2026-04-06; last changed in `7b3f841`) and not ignored. It is a personal permission
allow-list with local Windows paths and about 30 references to downloaded book PDFs and EPUBs.
No secret pattern matched. Recommended owner action: `git rm --cached` it, add
`.claude/settings.local.json` to `.gitignore`, and consider whether history needs cleaning in
this public repository.

Validators (Windows 11, Python 3.13, 2026-11-08, after wave 2): catalogue guardrails exit 0
(168 active, 0 errors, 16 size warnings, pre-existing); guardrail unit tests OK; routing
precision@1 222/242, precision@3 242/242, 0 lint findings; coverage, collision gate (one
allow-listed pair), control plane, source register (0 findings), both hook tests (61/61, 7/7),
contract gate (162 scanned, 0 errors) and `git diff --check` exit 0. pytest: 272 passed,
3 skipped, 1 failed (`test_current_checkout_is_under_file_budget`, pre-existing, ignored local
folders in this checkout).

Still open: screenshot and accessibility tool versions, provider mobile-money callbacks,
`CR:S2` and `CR:K5` device behaviour remain `NOT_ASSESSED`.
