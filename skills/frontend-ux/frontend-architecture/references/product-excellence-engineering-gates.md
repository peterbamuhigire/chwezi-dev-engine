# Product excellence engineering gates

Parent skill: [`frontend-architecture`](../SKILL.md). Siblings that implement the visual layer:
[`house-style-web.md`](../../tailwind-css/references/house-style-web.md) and
[`house-style-compose.md`](../../../android/android-development/references/house-style-compose.md).

The Chwezi Product Excellence Standard is the mandatory UI/UX standard for every Chwezi app and
system (Android, iOS, tablet, desktop, web; KMP/Compose Multiplatform as the primary mobile
stack), adopted by Lead Developer Peter Bamuhigire and the Chwezi Core Systems design team,
effective 01 November 2026 until further communication. It is owned by the design engine, not
by this file:

- `chwezi-design-engine` -> `doctrine/product-excellence-standard.md` (mandate, precedence,
  hard gates PX-GATE-01..13, release decision).
- `chwezi-design-engine` -> `skills/00-cross-cutting-ops-qa-a11y/chwezi-product-excellence-standard/`
  (`SKILL.md`, `references/rules-catalogue.md` for every `PX-<AREA>-NNN` rule,
  `references/currentness-register.md` for every platform fact, `examples/product-excellence-policy.yaml`).

Resolve `chwezi-design-engine` from the engine-routing table; never hard-code its path. This
file turns the standard into checkable engineering gates; where they disagree, the standard wins.

**Currentness.** Platform facts cite the design engine register as `CR:<ID>` (read 2026-11-07).
If a cited row lapses or turns `NOT_ASSESSED`, the dependent gate reports `NOT_ASSESSED`, not pass.

## Release decision in one paragraph

Only `MEASURED` evidence closes a hard gate. PASS: score at least 85/100 and zero open gates.
CONDITIONAL: 70-84, zero open gates, owned and dated remediation, pilot only. BLOCKED: any open
or `NOT_ASSESSED` gate at release, or a score under 70. The implementer never verifies their own
work (PX-QA-006).

## Gate map

| Hard gate | Engineering check | Evidence artefact |
|---|---|---|
| PX-GATE-01 Duplicates | Double-tap, timeout-then-retry and offline-replay tests on every create and payment | Test report: one record per scenario |
| PX-GATE-02 False confirmation | Label-to-backend-condition table; state-machine tests for sync and payments | Audit table + test report |
| PX-GATE-03 Numbers reconcile | Formatter tests per currency and locale; screen totals vs ledger query | Formatter suite + reconciliation log |
| PX-GATE-04 Interface-only authorisation | Low-role API calls for every restricted action | Role x endpoint denial matrix |
| PX-GATE-05 Sensitive data | Visibility matrix per role; screenshot protection test; analytics payload scan | Matrix + capture log |
| PX-GATE-06 Accessibility | Automated scan (below) plus logged TalkBack, VoiceOver and keyboard runs of every core journey; a scan alone never closes the gate | Scanner output + assistive-technology log |
| PX-GATE-07 Large-text loss | Screenshot matrix at 200% text / largest accessibility size | Screenshot set |
| PX-GATE-08 Work lost | Process-death, rotation, back and connectivity-loss tests; non-core endpoints blocked | Test report |
| PX-GATE-09 Invented content | Fixture-data scan of the production build; requirement trace per field | Build scan + trace |
| PX-GATE-10 Missing state | State-matrix test per screen (below) | State matrix + screenshots |
| PX-GATE-11 Device budget | Macrobenchmark on the physical floor device; vitals dashboard | Traces + budget diff |
| PX-GATE-12 Unverified release | Independent verifier record; human domain reviewer for money or clinical change | Signed review record |
| PX-GATE-13 Document numbering (where a screen issues numbered documents) | Concurrent-issue test (N parallel issues give N contiguous numbers, no gap or duplicate); offline issue shows a provisional tag and is numbered at server issue; replay with the same idempotency key returns the same number; void keeps the number and delete is refused | Test report against the tenant counter |

## Reporting surfaces: RPT gates

When a screen or output reports figures (dashboard, KPI tile, register with totals, statement,
daily close, scheduled report, PDF or print, CSV or XLSX export, written or AI narrative), the
Chwezi Reporting and Dashboards Standard 1.0.0 (adopted 8 Nov 2026) adds eight hard gates to the
PX gates above. They block release the same way: an applicable gate open or `NOT_ASSESSED` at
release blocks PASS. This engine carries the standard locally in
[`reporting-and-export-engineering`](../../../saas/reporting-and-export-engineering/SKILL.md)
(doctrine and full rule catalogue in its `references/`).

| Gate | Applies when | Engineering check | Also trips |
|---|---|---|---|
| RPT-GATE-01 Report does not reconcile | Any figure with a detail list, ledger or export | Reconciliation harness: headline = detail = ledger = PDF = XLSX for positive, zero, negative, reversed and missing-data fixtures | PX-GATE-03 |
| RPT-GATE-02 Undefined metric | Any headline, exported or scheduled metric | Approved, versioned metric contract; no measure logic in presentation code | PX-GATE-09 |
| RPT-GATE-03 Ambiguous scope | Every reporting surface and exported page | Context row (period, timezone, tenant or branch, currency, filters); comparable comparison windows | None (reporting-specific) |
| RPT-GATE-04 Export leak | Download, print, schedule, share link | Lower-role session calls export APIs directly; row and field filters in query and export service | PX-GATE-04, PX-GATE-05 |
| RPT-GATE-05 Unsafe spreadsheet | Any CSV or XLSX | Injection fixture (`=`, `+`, `-`, `@`, tab, carriage return) and leading-zero identifiers | None (reporting-specific) |
| RPT-GATE-06 Print failure | Any A4 PDF or print | Dedicated template; repeated headings; totals with labels; page x of y; legibility floor | None (reporting-specific) |
| RPT-GATE-07 Ungrounded narrative | Any written or AI insight from product figures | Claim-to-evidence table; human approval for consequential text | PX-GATE-09 |
| RPT-GATE-08 Unknown shown as known | Any surface that can lack data | No data, restricted, stale and failed reconciliation never shown as zero, complete or live; integrity warning not dismissable | PX-GATE-02, PX-GATE-10 |

Reporting states extend the screen state model below with partial data, stale snapshot,
reconciliation failure, source disconnected, access restricted and export pending (RPT-STATE-001).

## Screen state model

Every data screen implements the thirteen canonical states of PX-STATE-001. Use the IDs from the
design engine's `examples/product-excellence-policy.yaml` (`required_screen_states`) so matrices
and policy agree:

| State ID | N/A allowed | State ID | N/A allowed |
|---|---|---|---|
| `initial_loading` | no | `offline_cached` | yes |
| `content` | no | `queued_change` | yes |
| `refreshing` | yes | `syncing` | yes |
| `empty` | yes | `conflict` | yes |
| `filtered_empty` | yes | `permission_restricted` | yes |
| `error` | no | `session_expired` | yes |
| `success` | no | | |

A state that cannot occur is declared `N/A` with a reason, never omitted (PX-GATE-10). If the
policy file and this table ever differ, the policy file wins and this table is corrected.

Model the orthogonal axes separately so a screen can be "content + offline cached + 3 queued"
at once; one flat enum cannot express that:

```kotlin
@Immutable
data class ScreenUiState<T>(
    val load: LoadState<T>,        // Loading, Content(data), Refreshing(data), Empty(cause), FilteredEmpty(total), Error(reason)
    val connectivity: SyncState,   // Online, OfflineCached(lastSyncAt), Syncing(done, total)
    val pending: PendingState,     // None, Queued(count), Conflict(items)
    val access: AccessState,       // Full, Restricted(reason, grantor), SessionExpired(draftKept)
)
// success is a one-shot event (Channel or SharedFlow -> snackbar or result screen), emitted only
// after server acknowledgement; it is not a persistent load state.
```

On the web, use the same axes as TypeScript discriminated unions (`kind: "loading" | "content" |
"refreshing" | "empty" | "filteredEmpty" | "error"`, with `cause` on empty). No networking or
business calculation in render functions (PX-ARCH-005); empty states name
their cause and one next action (PX-STATE-004); errors say what happened, what is safe and what
next (PX-STATE-005); success only after server acknowledgement (PX-STATE-002).

**State-matrix test.** Keep one machine-readable matrix per screen (for example
`docs/quality/screens/<screen-id>.states.yaml`) listing each of the thirteen state IDs as
`covered` with a preview or story name, or `N/A` with a reason. A CI test fails when a state ID
is missing or unknown; a state whose policy entry says `na_allowed: false` is marked `N/A`; an
`N/A` has no reason; or a `covered` state has no preview, story and screenshot of that name.

```yaml
screen: pos.checkout
states:
  initial_loading: {covered: CheckoutLoadingPreview}
  filtered_empty:  {na: "Checkout has no filter"}
  queued_change:   {covered: CheckoutQueuedPreview}
  # ... all thirteen IDs
```

## Component contract tests

Each shared component carries a contract (PX-ARCH-006): purpose, parameters (immutable state and
semantic callbacks only, never repositories or network clients), sizes, variants, states,
semantics, keyboard, test tags, RTL, previews and performance limits. A new component or variant
needs a design decision record (DDR) (PX-ARCH-007). Contract tests assert:

| Check | Assertion |
|---|---|
| Loading | Geometry reserved; a second activation while loading is ignored (one callback) |
| Disabled | Carries a reason exposed to assistive technology |
| Semantics | Role, accessible name and state present; status changes use a polite live region |
| Target size | Android 48x48 dp (`CR:M1`), iOS 44x44 pt (`CR:I1`), web at least 24x24 CSS px (`CR:A5`); at least 56 dp with 8 dp spacing for glove, field, workshop and POS keypad screens (PX-GEOM-009, Chwezi rule) |
| Long text | Wraps at 200% text; nothing essential clipped without an accessible full value |
| Tokens only | No colour, radius or spacing literal outside the theme package (house-style guardrails) |

**Test tags.** Name tags `<component>.<part>` (for example `kpi.value`, `cart.total`,
`pay.submit`). Use the same names for Compose `Modifier.testTag`, web `data-testid` and
desktop automation IDs so cross-platform journey tests share selectors. On Android, set
`Modifier.semantics { testTagsAsResourceId = true }` once on the root composable so UiAutomator
and Macrobenchmark journeys can find tags as resource IDs (`By.res("pay.submit")`). On iOS,
Compose Multiplatform maps test tags to accessibility identifiers (`CR:K5`). Never use
translated text as a selector; a test that must assert copy reads it from the string resource.

## Screenshot matrix

Screenshot tests cover every required state of every core screen across:

| Axis | Values |
|---|---|
| Theme | light, dark |
| Text size | 100%, 200% (Android font scale, `CR:M13`); iOS accessibility sizes AX1-AX5 where tested (`CR:I3`, `CR:I4`); web 200% zoom |
| Width | compact and expanded at minimum; every window class the product ships (`CR:M3`, `CR:M4`) |
| Direction and language | LTR in English; RTL in Arabic (`CR:R1`, `CR:R5`); the product's longest supported language |
| System bars (Android) | gesture navigation, 3-button navigation, cut-out, keyboard open (`CR:M6`) |

Screenshots must come from running code; static mockups are never release evidence (PX-QA-004).

**Tool options.** Versions and current capabilities of every tool below are `NOT_ASSESSED`
here; pin them in the project and record name and version in the evidence pack.

| Platform | Options | Notes |
|---|---|---|
| Android (Compose) | Paparazzi (JVM, layoutlib); Roborazzi (Robolectric); the Android Gradle plugin's Compose Preview Screenshot Testing | Drive the axes from one parameterised preview set: font scale, night mode, layout direction, locale and width. Compose `ui-test` `DeviceConfigurationOverride` can force font scale and layout direction inside a test |
| Compose Multiplatform shared UI | Android screenshots of the shared composables, plus device or simulator screenshots on iOS | JVM screenshot tools render with Android or desktop text stacks, not iOS; iOS Dynamic Type stays a device test (`CR:K5`) |
| iOS (native screens) | XCTest UI tests with attached screenshots, or a snapshot-testing library | Run at Large, AX1 and AX5 and in Arabic |
| Web | Playwright `toHaveScreenshot` | Set `colorScheme`, `locale`, viewport and `dir`; emulate 200% zoom by halving the CSS viewport width (1280 -> 640) and also test 320 CSS px reflow (WCAG 1.4.10); test text-only enlargement by raising the root font size where the CSS uses `rem` |

Screenshot diffs need a fixed font set, disabled animations and a fixed clock; a flaky baseline
is fixed, not re-recorded blindly. A human reviews every changed baseline.

## Android device budget

1. **Baseline device profile** (PX-PERF-001): commit `docs/quality/baseline-device.md` with
   model, SoC, RAM, OS/API, screen, network profiles, dataset size, distribution channel and the
   evidence source. Pick a floor device (all MUST budgets) and a typical device.
2. **Baseline Profiles** with a Startup Profile are required for every Android product (`CR:P7`).
   Generate them with the Baseline Profile Gradle plugin from a `com.android.test` module that
   targets the app module (with Compose Multiplatform on AGP 9, the `androidApp` module) using
   `BaselineProfileRule.collect(packageName, includeInStartupProfile = true) { ... }` over the
   core journeys (start, sale, scan, pay, search). Commit the generated profile and regenerate it
   when those journeys change. Keep the binary profile under the size `CR:P7` records.
   Sideloaded or third-party-store installs may not apply profiles at install time (`CR:P7`), so
   measure startup on the channel users actually use.
3. **Macrobenchmark** on the physical floor device; emulator-only evidence fails PX-GATE-11
   (PX-PERF-002). Benchmark a release-like build (non-debuggable, minified, `profileable`):

   ```kotlin
   @Test fun coldStart() = rule.measureRepeated(
       packageName = PKG,
       metrics = listOf(StartupTimingMetric()),   // timeToInitialDisplayMs, timeToFullDisplayMs
       compilationMode = CompilationMode.Partial(BaselineProfileMode.Require),
       startupMode = StartupMode.COLD,
       iterations = 10,
   ) { pressHome(); startActivityAndWait() }

   @Test fun cartScroll() = rule.measureRepeated(
       packageName = PKG,
       metrics = listOf(FrameTimingMetric()),     // frameDurationCpuMs, frameOverrunMs percentiles
       compilationMode = CompilationMode.Partial(BaselineProfileMode.Require),
       iterations = 10,
       setupBlock = { startActivityAndWait(); openCartWithItems(200) },
   ) { device.findObject(By.res("cart.list")).fling(Direction.DOWN) }
   ```

   Run the same tests with `CompilationMode.None()` to show the profile's gain, and record warm
   and hot start too. Report median and P90 with device, build and dataset size. Library
   versions beyond those recorded in `CR:P7` are `NOT_ASSESSED` here.
4. **Time to full display**: call `ReportDrawn`, `ReportDrawnWhen` or `ReportDrawnAfter` in
   Compose, or `reportFullyDrawn` (`CR:P6`), so `timeToFullDisplayMs` measures real usability.
5. **Field jank** with JankStats, tagged with UI state (`CR:P8`).
6. **Budgets**: the first measured release sets start and frame budgets; CI or the device-lab
   run fails on a regression beyond them (PX-PERF-003). No recorded budget means PX-GATE-11 is
   open.

## Android vitals targets

| Metric | Gate | Source |
|---|---|---|
| User-perceived crash rate | Below the core-vital threshold overall and per phone model, over 28 days | `CR:P1` |
| User-perceived ANR rate | Below the core-vital threshold overall and per phone model | `CR:P1` |
| Excessive partial wake locks | Below the core-vital threshold | `CR:P1` |
| Memory and bitmap memory | Below the RAM-tier threshold for the floor device; no bitmap growth over a 30-minute session | `CR:P1`, `CR:P2` |
| Slow and frozen frames | Core-task trace shows no frozen frames; slow-frame share recorded per release (diagnostic, not a core vital) | `CR:P3`, `CR:P4` |
| Startup | Excessive-start thresholds are diagnostic; Chwezi SHOULD: hot start at most 1 s TTID | `CR:P5` |
| Crash-free sessions | Chwezi SHOULD: at least 99.9% per platform, rolling 28 days (PX-PERF-009) | Chwezi rule |

Read thresholds from the register rows at release time. Slow frames, frozen frames and startup
are not core vitals; never call them that.

## Web: Core Web Vitals

Web front ends meet the "good" thresholds at p75, segmented by mobile and desktop (`CR:W1`,
`CR:W3`), on a low-end mobile profile (PX-PERF-014); a "poor" value (`CR:W2`) is a regression
alarm. Do not date INP's replacement of FID (`CR:W4` is `NOT_ASSESSED`).

| Evidence | Tool | What it can prove |
|---|---|---|
| Field (closes the gate) | Real-user monitoring with the `web-vitals` library, or CrUX where the origin has enough traffic | p75 LCP, INP and CLS per segment. INP is a field metric; internal tenant apps rarely appear in CrUX, so plan RUM |
| Lab (regression alarm) | Lighthouse CI with throttled mobile emulation and per-route budget assertions | LCP, CLS and Total Blocking Time as a lab proxy for INP; always labelled "lab" |
| Accessibility scan | Playwright with `@axe-core/playwright` (`AxeBuilder` with tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`) on every core route and state | A subset of WCAG failures; zero violations is necessary, not sufficient, for PX-GATE-06 |

Tool versions are `NOT_ASSESSED` here. Page-weight budgets live in the design engine
(`doctrine/references/web-performance-budgets-2026.md`); measurement method is in
[`frontend-performance`](../../frontend-performance/SKILL.md).

## Native accessibility scans

Android: enable Accessibility Test Framework checks in instrumented tests (Espresso
`AccessibilityChecks.enable()`, or the Compose `ui-test` accessibility-check hook where the
pinned version offers it) and assert semantics directly: role, `contentDescription` or text,
`stateDescription`, and a 48 dp touch bound (`CR:M1`). iOS: run Xcode's accessibility audit in
UI tests where the toolchain offers it, and Accessibility Inspector on each core screen. Tool
availability per version is `NOT_ASSESSED`. Every scan is followed by a logged TalkBack or
VoiceOver run and a hardware-keyboard run of each core journey (PX-GATE-06).

## Android targetSdk 36 consequences

Google Play requires new apps and updates to target API 36 (`CR:M7`). For every Play-distributed
app these are MUST checks:

| Platform change | Engineering rule | Test |
|---|---|---|
| Edge-to-edge has no opt-out at targetSdk 36 on Android 16+ (`CR:M6`) | Handle status bar, navigation bar, cut-out and IME insets on every screen; bottom bars and the floating cart bar sit above the gesture area; pad scrolling content by the inset, never by a fixed number (PX-GEOM-002) | Screenshot matrix system-bar axis |
| Predictive back on by default; `onBackPressed` not called, `KEYCODE_BACK` not dispatched (`CR:M8`) | No business logic in `onBackPressed`; use `BackHandler` or `PredictiveBackHandler`; intercept back only to protect unsaved data and then offer save, discard or stay (PX-NAV-003) | Back-behaviour matrix per screen, including mid-payment and mid-form |
| Orientation, resizability and aspect-ratio locks ignored where smallest width is at least 600 dp (`CR:M9`) | Every screen that can run on a tablet or foldable has landscape and resizable layouts; state and drafts survive rotation and resize | Rotate and resize on a sw600dp device |
| `elegantTextHeight` ignored (`CR:M10`) | Re-test tall scripts | Arabic screenshots at 100% and 200% |

## Compose Multiplatform module layout

Compose Multiplatform is the primary mobile UI stack for Chwezi apps. It is Stable on Android,
iOS and desktop and Beta on web (`CR:K1`, `CR:K3`), so a production Compose-for-Web front end
needs a DDR; existing web front ends keep their stack and consume the same tokens. Pin and
record the CMP version per project (`CR:K2`).

With AGP 9 or later the Android entry point lives in a separate `androidApp` module
(`com.android.application`) and the shared module uses `com.android.kotlin.multiplatform.library`
(`CR:K4`):

```text
androidApp/                      Activity, manifest, insets, back handling
iosApp/                          Xcode project hosting the shared UI
shared/ (or composeApp/)         KMP + com.android.kotlin.multiplatform.library
  core/designsystem/             generated tokens, typography, theme, components
  core/platform/                 adapters: permissions, camera/scan, print, secure storage, screenshot protection
  features/<feature>/{presentation,domain,data}
```

Enforce feature boundaries with a dependency lint. CMP Dynamic Type and Reduce Motion on iOS are
undocumented (`CR:K5`): device-test them and record `MEASURED` evidence.

## Offline: idempotency keys and queued versus confirmed

Record states: draft, queued, syncing, confirmed, conflict, failed. The label always matches
backend truth (PX-STATE-002): "Saved" without qualification means the server has it; queued work
says "Saved on this device, waiting to send" (PX-OFFLINE-003).

1. Generate the idempotency key once, when the user commits; persist it with the queued item in
   the same local transaction; send it on every retry (for example an `Idempotency-Key` header).
2. The server stores the key with the result and returns the original result for a repeated key.
   The key is durable on the document row, so a replay returns the same document number.
3. Offline documents show a clearly provisional tag; the contiguous number is allocated by the
   server at issue (PX-DATA-013; see [`tenant-document-numbering`](../../../saas/tenant-document-numbering/SKILL.md)).
4. The queue survives process death and reboot and replays FIFO per record.
5. Every screen with cached data shows the last successful sync time, the pending count and any
   conflict (PX-OFFLINE-001). Failures and conflicts reach their owner with a deep link.
6. Tenant rules decide what may queue; a blocked action says why and what to do.

Tests: kill and reboot mid-queue (one server record each); 20 offline actions (20 synced in
order); forced conflict (resolution UI, nothing lost).

## Mobile-money payment state machine

```text
initiated -> pending -> confirmed -> reversed
                    \-> failed
                    \-> timed-out --(status query, same key)--> confirmed | failed | pending
```

Implement the states as a sealed type with an explicit transition table; reject and log any
illegal transition. Only provider confirmation (callback or verified status query) makes a
payment "paid" (PX-DATA-010). Rules: Pay is disabled from initiated onward; pending uses `info`
styling with a "Check status" action and lets the cashier park the sale; timed-out never
auto-retries a charge and offers only "Check status" (same key) and, after a failed status
result, another method; a late callback updates the record and notifies, never creating a second
sale; split tender completes only when every part is confirmed; due, received and reconciled are
separate states (PX-DATA-005). Tests: simulated, late and duplicate callbacks; timeout; kill
during pending; ten double taps on Pay give one request. Provider-specific callback behaviour is
`NOT_ASSESSED` until verified per integration.

## Currency formatting: ISO 4217 minor units

Store money as integer minor units per currency, or as decimal strings from the API; never float
arithmetic. The number of decimals in a full amount comes from the currency's ISO 4217 minor unit
(`CR:C1`, `CR:C2`): UGX and RWF 0, KES, TZS and USD 2 (PX-L10N-001). This overrides the house-style
`full` formatter's fixed two decimals (owner default, 2026-11-07). Compact K/M/B forms keep their
two decimals, because those scale the unit; never use compact forms for closing balances,
invoice totals or payment inputs.

```kotlin
fun full(minor: Long, currency: String, locale: Locale): String {
    val digits = MinorUnits.of(currency)          // project table from ISO 4217, unit-tested
    val amount = BigDecimal.valueOf(minor).movePointLeft(digits)
    val f = NumberFormat.getNumberInstance(locale)
    f.minimumFractionDigits = digits; f.maximumFractionDigits = digits
    return f.format(amount)
}
```

```js
const full = (minor, currency, locale) => {
  const digits = MINOR_UNITS[currency]; // same table, generated from one source
  return new Intl.NumberFormat(locale, { minimumFractionDigits: digits, maximumFractionDigits: digits })
    .format(minor / 10 ** digits); // integer division safe only within Number range; use BigInt/decimal for large ledgers
};
```

Keep the minor-unit table in the project, generated from one source and asserted in tests
(`UGX 1250000 -> "1,250,000"`), not each runtime's built-in currency data. TZS cash rounding
follows CLDR cash digits (`CR:C2`). Format machine strings with a fixed locale such as
`Locale.US`; locale formatting may emit non-ASCII digits (`CR:C4`).

## Tokens to CSS custom properties

One token source feeds every platform (PX-TOKEN-008). A build step emits the Kotlin theme objects
and a CSS file of custom properties and, where the web stack uses Tailwind, its theme mapping. No
hand-maintained copies. Emit light values on `:root`, dark values under
`@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])` and again under
`:root[data-theme="dark"]`, and zero motion durations under `prefers-reduced-motion: reduce`
(`CR:X1`). When an interchange format is wanted, use the one the design engine's standards
register names. CI regenerates the files and fails if the diff against the committed output is
not empty. Semantic roles include `danger` (never "critical"), `warning`, `info` and `neutral`;
a product theme changes only `brand.*` tokens. Mapping detail: [`house-style-web.md`](../../tailwind-css/references/house-style-web.md).

## Backend authorisation and sensitive data

- Enforce every permission in the domain and backend; hiding a control is convenience only
  (PX-PRIV-001, PX-GATE-04). Scope every query by tenant and branch on the server.
- Test a role x endpoint matrix with a low-role session token for every restricted action and
  record: one denial per row. See [`vibe-security-skill`](../../../security/vibe-security-skill/SKILL.md).
- Masked fields read "Restricted", not blank (PX-PRIV-006). Patient, payroll and credential
  screens set Android `FLAG_SECURE` (`CR:S1`; not fully reliable on API 30 and lower). The iOS
  equivalent is `NOT_ASSESSED` (`CR:S2`) and must be device-tested.
- Analytics payloads carry no sensitive fields; CI scans them (PX-PRIV-010).

## Evidence pack and CI wiring

Keep an evidence folder per release in the product repository (PX-QA-011); its contents are listed
in the design skill's `references/scorecard-and-release-gate.md`. Suggested CI jobs: token
regeneration diff; state-matrix completeness; component contract tests; screenshot matrix;
formatter suite; idempotency and offline replay; payment state machine; role-denial matrix;
Macrobenchmark on a device lab where available. Anything the pipeline cannot run is recorded
`NOT_ASSESSED`, which blocks PASS for a hard gate.

## Currentness

Cited register rows (accessed 2026-11-07; review by 2026-12-07 for library facts, 2027-02-07 for
platform and store, 2027-05-07 for standards): A5, C1, C2, C4, I1, I3, I4, K1-K5, M1, M3, M4,
M6-M10, M13, P1-P8, R1, R5, S1, S2, W1-W4, X1. Re-read them there, not here.
