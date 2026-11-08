---
name: kmp-development
description: Use when sharing Kotlin business logic and Compose Multiplatform UI across Android and iOS with Kotlin Multiplatform behind deliberate platform adapters; use native development skills for platform entry points, platform-only integration and release work.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Kotlin Multiplatform Development Standards
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Chwezi Product Excellence Standard (mandatory)

Any Chwezi app or system UI work (effective 01 Nov 2026) MUST follow the Chwezi Product Excellence Standard in `chwezi-design-engine` (resolve via the engine-routing table; never hard-code the path): `doctrine/product-excellence-standard.md` and skill `skills/00-cross-cutting-ops-qa-a11y/chwezi-product-excellence-standard`. Engineering gates: [product-excellence-engineering-gates.md](../../frontend-ux/frontend-architecture/references/product-excellence-engineering-gates.md). For Chwezi apps, Compose Multiplatform shared UI with platform adapters is the primary mobile stack (CMP web is Beta and needs a DDR); see the strategy below. With AGP 9+ the Android entry point is a separate `androidApp` module. Where this skill and the standard differ, the standard wins.

## Use When

- Kotlin Multiplatform development standards for sharing business logic and, for Chwezi apps, Compose Multiplatform UI across Android and iOS behind platform adapters. Covers project structure (shared/androidApp/iosApp), source sets, targets, expect/actual, DI (Koin)...

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | Shared-module contract test results | CI log or recorded test report covering commonTest / actual / expect surfaces | `docs/kmp/shared-tests-2026-04-16.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
- `references/kmp-compose-multiplatform.md` for shared Compose UI across Android, iOS, Desktop, and Web targets.
- `references/kmp-tdd.md` for shared-module Red-Green-Refactor, common tests, and expect/actual test strategy.
- For iOS targets in 2026+ Apple toolchains, load `../../ios/ios-development/references/apple-platform-compatibility-wwdc26.md`; keep the Xcode 27 / Swift 6.4 host, iOS adapters and availability gates in the `iosApp/` module.
<!-- dual-compat-end -->
## Strategy: Compose Multiplatform UI With Platform Adapters

For Chwezi apps (Product Excellence Standard, effective 01 Nov 2026) the default is one shared
Kotlin codebase for domain, data, networking and UI. The UI is Compose Multiplatform (CMP),
which is Stable on Android, iOS and desktop and Beta on web (`CR:K1`, `CR:K3`; register rows in
the design engine `currentness-register.md`, accessed 2026-11-07). Pin and record the CMP version
per project and re-check `CR:K2` at implementation time; this skill does not assert a version.

- Share screens, components, theme and tokens in `commonMain` wherever the required behaviour
  is supported on every shipped target.
- Put everything the OS owns behind a narrow interface in `core/platform/` with one `actual`
  or injected implementation per target: runtime permissions, biometrics, camera and barcode
  scanning, printing (receipt and Bluetooth printers), notifications, keyboard and IME
  behaviour, system navigation (Android predictive back, iOS edge-swipe back, deep links),
  secure storage and screenshot protection.
- Embed a native view only where an adapter needs one (`AndroidView` on Android, `UIKitView`
  or `UIKitViewController` on iOS, for example a camera preview), and record why.
- CMP for production web is Beta: it needs a design decision record (DDR). Existing web
  front ends keep their stack and consume the same tokens.
- Native UI per platform (Jetpack Compose plus SwiftUI) is the exception, not the default. Use
  it only for a screen that CMP cannot deliver at the standard's bar on a shipped target, and
  record that in a DDR with the evidence.
- iOS Dynamic Type and Reduce Motion behaviour under CMP is not documented (`CR:K5`,
  `NOT_ASSESSED`): device-test both on iOS before claiming the accessibility gates. Semantics map
  to VoiceOver and test tags map to accessibility identifiers (`CR:K5`).

## Module-to-Skill Mapping

| Module | Governs | Skill |
|---|---|---|
| `shared/` (or `composeApp/` as a KMP library) | Domain, data, networking, shared CMP UI, design system, platform adapter interfaces | **This skill** (kmp-development) plus the design engine standard |
| `androidApp/` | Android entry point: Activity, manifest, insets, back handling, Baseline Profiles, Play release | android-development |
| `iosApp/` | Xcode host for the shared UI (`ComposeUIViewController`), iOS adapters, Apple availability gates, Xcode 27 release evidence | ios-development |

## Project Structure

With AGP 9 or later the Android entry point is a separate `androidApp` module
(`com.android.application`) and the shared module applies
`com.android.kotlin.multiplatform.library`; iOS needs the `iosArm64` and `iosSimulatorArm64`
targets (`CR:K4`). Older single-module `composeApp/` projects migrate when they move to AGP 9.

```text
project-root/
  shared/                          # KMP + com.android.kotlin.multiplatform.library (this skill)
    src/
      commonMain/kotlin/
        core/designsystem/         # generated tokens, typography, theme, components
        core/platform/             # adapter interfaces: permissions, biometrics, camera/scan,
                                   # print, notifications, keyboard, navigation, secure storage
        features/<feature>/{presentation,domain,data}
      commonMain/composeResources/ # strings (all declared languages), fonts, images
      androidMain/kotlin/          # Android adapter implementations
      iosMain/kotlin/              # iOS adapter implementations, MainViewController()
      commonTest/                  # shared logic and UI tests
      androidUnitTest/  iosTest/
    build.gradle.kts
  androidApp/                      # com.android.application (android-development)
  iosApp/                          # Xcode project hosting the shared UI (ios-development)
  build.gradle.kts
  gradle/libs.versions.toml        # version catalogue; pin CMP, Kotlin, AGP together
```

## Additional Guidance

## Decision Rules

| Code concern | Location |
|---|---|
| Pure domain rule, validation, or API model | `commonMain` |
| Stable platform service with distinct implementations | Narrow expect/actual or injected interface |
| Screen, component, theme or token | `commonMain` shared CMP UI |
| OS-owned capability (permission, biometrics, camera, print, notification, keyboard, system back) | Interface in `core/platform/`, implementation per platform source set |
| Screen CMP cannot deliver at the standard's bar on a shipped target | Native screen behind the same view model, with a DDR |
| Library lacks supported targets | Choose an alternative or isolate it; do not leak it into common code |

## Capability Contract And Degraded Mode

Read and search all target source sets before moving code. Edits and builds require authority. Without both Android and iOS toolchains, return the target-specific checks still outstanding and do not claim parity.
If either target toolchain is unavailable, mark cross-platform parity unverified.

## Domain Anti-Patterns

- Calling platform APIs from shared screens. Fix: route them through a `core/platform/` adapter.
- Building native screens by default for a Chwezi app. Fix: use shared CMP UI; a native screen needs a DDR.
- Spreading expect/actual across domain types. Fix: inject one narrow platform service.
- Choosing dependencies from Android support alone. Fix: verify every declared target.
- Catching platform errors as generic strings. Fix: map them into a shared typed error model.
- Declaring parity after one target builds. Fix: run shared and platform tests on both targets.

Extended guidance for `kmp-development` was moved to [references/skill-deep-dive.md](references/skill-deep-dive.md) to keep this entrypoint compact and fast to load.

Use that deep dive for:
- `Technology Stack`
- `Source Sets and Targets`
- `Architecture: Clean Architecture in Shared Module`
- `Expect/Actual Pattern`
- `Dependency Injection with Koin`
- `Networking with Ktor`
- `Database with SQLDelight`
- `Modularization`
- `Native Library Integration`
- `Tooling`
- `Mandatory Rules`
- `Anti-Patterns`
## Inputs
| Artefact | Required? | Purpose |
|---|---|---|
| Shared-domain scope, platform capabilities, API contracts, and platform-adapter boundaries | yes | Choose KMP sharing boundaries |
## Outputs
- Produce KMP architecture or code with shared CMP UI, platform adapters, tests, and per-target integration evidence.
## Degraded mode
Fallback without both platform toolchains: validate shared code and mark per-target UI and adapter behaviour unverified.
## Capability contract
Builds and tests follow task scope; signing, store release, backend mutation, and destructive device actions require explicit authority.
