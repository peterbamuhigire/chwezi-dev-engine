# React Native Production Checklist

Use when a React Native or Expo app is heading to TestFlight, the App Store,
or Google Play, or when auditing an existing RN codebase for release
readiness. It covers the RN-specific layer: toolchain currency, architecture,
accessibility, performance, OTA updates, and store gates. Platform store
detail stays in `google-play-store-review.md` and
`apple-platform-operations-wwdc26.md`; shared TypeScript structure comes
from `skills/languages/typescript-full-stack/references/large-scale-react-ts.md`.

## Inputs

| Input | If absent |
|---|---|
| `package.json`, lockfile, `app.json`/`app.config.ts`, native folders or CNG config | Stop: toolchain cannot be assessed |
| Target platforms, minimum OS versions, device classes (phone, tablet) | Assume phones on both platforms and record the assumption |
| Store accounts, bundle IDs/application IDs, signing custody | Release gate stays open |
| Backend contract, auth model, offline expectations | Mark data and failure states `NOT_ASSESSED` |
| Access to physical devices (at least one low-end Android) | Performance and accessibility proof is `NOT_ASSESSED` |

## 1. Toolchain and architecture currency

Decision rules (verified 2026-09-24, re-check each release):

| Situation | Action |
|---|---|
| New app | Start with Expo (`npx create-expo-app@latest`) on the current SDK unless a documented native constraint rules it out. Use Continuous Native Generation; keep `ios/`/`android/` out of source control unless you own custom native code. |
| RN version below 0.82 | Plan the upgrade first. 0.82+ runs only on the New Architecture; the legacy opt-out flags are blocked. |
| A dependency has no New Architecture support | Replace it or wrap the capability in an Expo Module / Turbo Module you own. Do not pin the whole app to an old RN for one library. |
| Legacy "Debug JS Remotely" / Chrome debugger instructions in docs or onboarding | Delete them. Use React Native DevTools. |
| Class components with `componentWillMount`-era lifecycles | Migrate to function components; required for React 19 behaviour and the compiler. |

Checklist:

- [ ] RN and Expo SDK are within the versions their docs list as supported.
- [ ] Hermes is the JS engine (default; Hermes V1 is default from RN 0.84).
- [ ] Node, Xcode, Android Gradle Plugin, and Kotlin meet the release notes'
      minimums (RN 0.87: Node 22, AGP 9, Kotlin 2.0+).
- [ ] TypeScript strict mode; RN 0.87 makes the Strict TypeScript API the
      default, so fix type errors rather than disabling it.
- [ ] React Compiler: on by default in new Expo SDK 54+ apps; keep it on and
      fix Rules of React violations it reports.
- [ ] `npx expo-doctor` (Expo) or the RN Upgrade Helper diff reviewed and clean.

## 2. App structure

- Same layering as the large-scale React reference: `models`, `http-client`,
  `api/<domain>`, `config`, `localization`, `primitives`, `components`,
  `screens`. Screens replace views.
- Navigation: Expo Router (file-based) or React Navigation; deep links and
  universal/app links declared and tested for every entry screen.
- Server state in TanStack Query with persistence for offline reading;
  mutations queued with idempotency keys when offline writes are allowed
  (see `pwa-offline-first` for queue and conflict rules).
- Secrets and tokens in `expo-secure-store` / Keychain / Keystore, never
  `AsyncStorage`. Nothing secret in `EXPO_PUBLIC_*` or JS bundles.
- Config per build profile (development, preview, production) with the API
  base URL and feature flags validated at start-up.

## 3. Accessibility gate (both platforms)

Use `role` and `aria-*` props (current RN docs recommend them over the older
`accessibilityRole` etc., and `role` wins when both are set).

- [ ] Every interactive element has an accessible name (`aria-label` or
      visible text) and a `role`; icon-only buttons are never unnamed.
- [ ] State is exposed: `aria-checked`, `aria-selected`, `aria-expanded`,
      `aria-disabled`, `aria-busy` as relevant.
- [ ] Touch targets at least 44x44 pt (Apple HIG) and 48x48 dp (Material);
      use `hitSlop` when the visual is smaller.
- [ ] Text scales: no fixed-height text containers; tested at the largest
      accessibility text size on iOS and 200% font scale on Android.
      `maxFontSizeMultiplier` only where layout would truly break, never
      `allowFontScaling={false}` on body text.
- [ ] Reduced motion honoured via `AccessibilityInfo.isReduceMotionEnabled()`
      or Reanimated's reduced-motion hook.
- [ ] Focus order is logical; modals set `aria-modal` (iOS) and trap focus;
      status changes announced with `aria-live` (Android) or
      `AccessibilityInfo.announceForAccessibility`.
- [ ] Colour contrast meets WCAG 2.2 AA (4.5:1 text, 3:1 UI components) in
      light and dark themes.
- [ ] Manual pass with VoiceOver and TalkBack on physical devices, recorded
      per screen. Automated lint alone is not proof.

## 4. Performance gate

Budgets must be measured on a release build on a low-end Android device
(for East African markets, a 2-3 GB RAM Android Go-class phone is a
realistic floor) and a supported older iPhone.

| Metric | Senior default budget | How to measure |
|---|---|---|
| Cold start to interactive | < 2 s mid-range, < 4 s low-end | Release build, stopwatch or platform startup tracing |
| Scroll/animation | Sustained 60 fps, no JS-thread stalls > 100 ms on core lists | Perf Monitor, React Native DevTools profiler, Android Studio / Instruments |
| JS bundle | Tracked per release; flag growth > 10% | Metro/Expo bundle output |
| Crash-free sessions | >= 99.5% before widening a staged rollout | Crash reporting (Sentry, Crashlytics) |

These budgets are engineering targets set here, not platform-published
thresholds.

Practices:

- Long lists use `FlatList`/`SectionList` with stable `keyExtractor`, or
  FlashList; never `ScrollView` + `map` over unbounded data.
- Images sized to the display, cached (`expo-image`), and served in modern
  formats from the backend.
- Animations on the UI thread (Reanimated worklets or the new animation
  backend from RN 0.85), not `setState` per frame.
- Remove `console.*` in production builds; they cost time on the JS thread.
- Defer non-critical work until after first interaction; lazy-load heavy
  screens.
- Test on slow 3G and offline: every screen has loading, empty, error, and
  offline states.

## 5. Security and privacy

- TLS only; certificate pinning only with a rotation plan and kill switch.
- Validate every API response (Zod) before it reaches state.
- Obfuscation is not a control; server authorises every action.
- Remove debug menus, test endpoints, and verbose logging from release
  builds; confirm with a release-build smoke test.
- iOS privacy manifest (`PrivacyInfo.xcprivacy`) includes required-reason
  API declarations for your code and third-party SDKs (Expo can generate
  entries from config); Play Data safety form matches actual collection.
- If the app creates accounts: in-app account deletion (App Store guideline
  5.1.1(v)); check the current Google Play User Data policy for its
  equivalent web and in-app deletion requirement.
- If the primary login is a third-party/social login, offer an equivalent
  privacy-preserving option such as Sign in with Apple (guideline 4.8).

## 6. Over-the-air (OTA) updates

- Use EAS Update (or an equivalent) with `runtimeVersion` tied to native
  fingerprint so a JS bundle never lands on an incompatible binary.
- OTA may fix bugs and adjust content; it must not add or change features or
  the app's purpose (App Store guideline 2.5.2). New features go through
  review.
- Roll out OTA updates by percentage with a tested rollback (republish the
  previous update) and monitor crash-free rate between steps.

## 7. Store readiness gates

Apple (App Store / TestFlight):

- [ ] Built with Xcode 26+ and the iOS/iPadOS 26 SDK (required for uploads
      since 2026-04-28); minimum deployment target iOS 13 or later.
- [ ] Updated age-rating questionnaire answered.
- [ ] Demo account (or approved demo mode) and a live backend for review
      (guideline 2.1(a)).
- [ ] Not a thin web wrapper: native navigation, offline states, and device
      capabilities justify the app (guideline 4.2).
- [ ] TestFlight internal round, then external group with written test notes.

Google Play:

- [ ] `targetSdkVersion` 36 (Android 16) for new apps and updates from
      2026-08-31 (extension possible to 2026-11-01).
- [ ] 16 KB memory page size supported for apps targeting Android 15+
      (required for new apps and updates since 2025-11-01); check native
      libraries in the Play Console app bundle explorer.
- [ ] Edge-to-edge layout correct on Android 15+ (RN 0.86 adds full
      support); no content under system bars.
- [ ] Android App Bundle signed with Play App Signing; upload key custody
      recorded.
- [ ] Closed testing track completed before production; staged rollout
      percentages and halt criteria defined.

Both:

- [ ] Store screenshots captured per device family from the release build,
      not mock-ups; listing claims match in-app behaviour.
- [ ] Crash reporting, analytics consent, and support contact live.
- [ ] Rollback plan: previous binary retained, OTA rollback tested, server
      feature flags can disable the new path.

## What Apple-grade looks like vs. generic output

| Generic | Apple-grade |
|---|---|
| "Add accessibilityLabel to buttons" | Every screen verified with VoiceOver and TalkBack, largest text size, reduced motion, recorded per screen |
| Tested in the simulator on a flagship | Release build on a low-end Android and an older iPhone, on a slow network |
| One `App.tsx` with fetch calls | Layered app with validated API clients, secure token storage, offline states |
| OTA used to ship features after approval | OTA limited to fixes; runtime-version gated; staged with rollback |
| Store checklist from memory | Requirements re-verified against Apple and Google pages on the release date |

## Worked example (original)

A Kampala savings-group (VSLA) app built with Expo for members on shared
low-end Android phones and treasurers on iPhones. Release gate findings:
contribution amounts in UGX rendered with `Intl.NumberFormat`; the
contributions list moved from `ScrollView` to FlashList after a 4-second
stall on a 2 GB device; Luganda strings overflowed at 200% font scale until
fixed-height rows were removed; treasurer approvals announced via
`announceForAccessibility`; OTA updates restricted to copy and bug fixes,
with a runtime-version check. Play `targetSdkVersion` raised to 36 before the
August 2026 deadline; iOS build moved to Xcode 26.

## Evidence/currentness

Accessed 2026-09-24: reactnative.dev/versions (0.87 latest; 0.77-0.87 listed),
reactnative.dev blog (0.82 New Architecture only; 0.84 Hermes V1 default,
precompiled iOS binaries, Node 22; 0.85 animation backend; 0.86 edge-to-edge;
0.87 strict TS API, AGP 9, Kotlin 2.0+), reactnative.dev/docs/accessibility
(`role`/`aria-*` preferred), GitHub releases facebook/react-native (v0.87.1,
2026-08-26), docs.expo.dev/versions/latest (SDK 57 -> RN 0.86, React
19.2.3), react.dev React Compiler v1.0 post (Expo SDK 54+ default),
developer.apple.com/news/upcoming-requirements and App Review Guidelines
(2.1(a), 2.5.2, 4.2, 4.8, 5.1.1(v)), developer.android.com target-SDK page,
Android Developers Blog on 16 KB page sizes (May 2025).

`NOT_ASSESSED`: current Google Play account-deletion policy wording; any
16 KB enforcement date after 2025-11-01; EAS Update pricing and limits;
Expo SDK support for RN 0.87 (SDK 57 targets 0.86); the performance budget
figures (engineering targets, not published thresholds).

Sources: Bin Uzayr (ed.) (2023) *Mastering React Native: A Beginner's
Guide* (concept input for component, platform API, debugging, and store
deployment topics; its debugging and architecture guidance is superseded);
reactnative.dev; docs.expo.dev; developer.apple.com; developer.android.com.
