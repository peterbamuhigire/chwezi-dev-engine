---
name: kmp-development
description: Use when sharing Kotlin business logic across Android and iOS with Kotlin Multiplatform while retaining deliberate platform boundaries; use native development skills for platform UI and release work.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Kotlin Multiplatform Development Standards
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Kotlin Multiplatform shared module development standards for sharing business logic across Android and iOS while keeping native UI. Covers project structure (shared/composeApp/iosApp), source sets, targets, expect/actual, DI (Koin)...

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | Shared-module contract test results | CI log or recorded test report covering commonTest / actual / expect surfaces | `docs/kmp/shared-tests-2026-04-16.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
- `references/kmp-compose-multiplatform.md` for shared Compose UI across Android, iOS, Desktop, and Web targets.
- `references/kmp-tdd.md` for shared-module Red-Green-Refactor, common tests, and expect/actual test strategy.
- For iOS targets in 2026+ Apple toolchains, load `../../ios/ios-development/references/apple-platform-compatibility-wwdc26.md` and keep SwiftUI-native UI, Xcode 27, Swift 6.4, and availability gates in the `iosApp/` module.
<!-- dual-compat-end -->
## Strategy: Shared Logic, Native UI

KMP shares business logic (domain, data, networking) across platforms. Each
platform keeps its native UI framework: Jetpack Compose for Android, SwiftUI
for iOS. This preserves the best user experience on each platform while
eliminating business logic duplication.

## Module-to-Skill Mapping

| Module | Governs | Skill |
|---|---|---|
| `shared/` | Business logic, data, networking | **This skill** (kmp-development) |
| `composeApp/` | Android UI, platform integration | android-development |
| `iosApp/` | iOS UI, platform integration, Apple availability gates, Xcode 27 release evidence | ios-development |

## Project Structure

Every KMP project has three modules:

```text
project-root/
  shared/                    # Shared Kotlin module (this skill governs)
    src/
      commonMain/            # Shared code (domain, data, use cases)
        kotlin/
        resources/
      androidMain/           # Android-specific implementations
        kotlin/
        AndroidManifest.xml
      iosMain/               # iOS-specific implementations
        kotlin/
      commonTest/            # Shared tests
      androidUnitTest/       # Android-specific tests
      iosTest/               # iOS-specific tests
    build.gradle.kts         # KMP Gradle config
  composeApp/                # Android app (follow android-development skill)
    src/main/
    build.gradle.kts
  iosApp/                    # iOS Xcode project (follow ios-development skill)
    iosApp/
    iosApp.xcodeproj
  build.gradle.kts           # Root build file
  gradle/libs.versions.toml  # Version catalog
```

## Additional Guidance

## Decision Rules

| Code concern | Location |
|---|---|
| Pure domain rule, validation, or API model | `commonMain` |
| Stable platform service with distinct implementations | Narrow expect/actual or injected interface |
| Native navigation, accessibility, or platform interaction | Platform source set and native UI |
| Library lacks supported targets | Choose an alternative or isolate it; do not leak it into common code |

## Capability Contract And Degraded Mode

Read and search all target source sets before moving code. Edits and builds require authority. Without both Android and iOS toolchains, return the target-specific checks still outstanding and do not claim parity.
If either target toolchain is unavailable, mark cross-platform parity unverified.

## Domain Anti-Patterns

- Moving UI wholesale into shared code by default. Fix: share stable logic and keep native experiences intentional.
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
| Shared-domain scope, platform capabilities, API contracts, and native UX boundaries | yes | Choose KMP sharing boundaries |
## Outputs
- Produce KMP architecture or code with shared/native separation, tests, and platform integration evidence.
## Degraded mode
Fallback without both platform toolchains: validate shared code and mark native integration unverified.
## Capability contract
Builds and tests follow task scope; signing, store release, backend mutation, and destructive device actions require explicit authority.
