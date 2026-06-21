# WWDC26 Apple Platform Compatibility

Self-contained implementation guidance distilled from the WWDC26 research export
and primary Apple Developer sources checked on 2026-06-21.

## Source Baseline

- Apple Developer WWDC26 iOS guide: iOS 27, Foundation Models, App Intents,
  Core AI, platform improvements, games/media, and availability caveats.
- Apple Developer macOS 27 guide: macOS AI stack, AppKit modernization,
  Safari/WebKit 27, spatial preview, and Mac app concerns.
- Apple Developer Xcode page: Xcode 27 agents, Device Hub, Instruments, and
  localization workflows.
- WWDC26 "What's new in Swift" session: Swift 6.3/6.4 language, library,
  Swift Testing, interoperability, and performance changes.

Do not treat this file as full beta release-note coverage. Read the current
Apple release notes before using beta-only APIs in shipped code.

## Toolchain Baseline

| Area | Standard |
| --- | --- |
| IDE | Xcode 27 for current Apple-platform work. |
| Host hardware | Apple Silicon for Xcode 27; audit CI and developer Macs before migration. |
| Swift | Swift 6.4-ready code with strict concurrency checking. |
| SDK target | Latest available iOS/iPadOS/macOS/watchOS/visionOS/tvOS SDKs for new work. |
| Deployment target | Product-specific. Keep iOS 17+ only when the product needs older devices. |
| Feature gates | Use `#available`, `@available`, capability checks, region/language checks, and server flags. |

## Availability Policy

Every feature using iOS 27, macOS 27, Apple Intelligence, Siri AI, Foundation
Models server routes, Core AI, App Intents Testing, or Safari 27 must document:

- minimum OS and SDK;
- required hardware, including Apple Intelligence-enabled devices where needed;
- supported languages and regions;
- privacy and data-flow path: on-device, Private Cloud Compute, or third-party;
- fallback UI and behavior when unavailable.

Never infer universal availability from an SDK compile. Apple's WWDC26 iOS guide
states that some capabilities and services vary by region, language, law, and
feature availability.

## Swift 6.4 Update Notes

- Prefer Swift Testing for new unit and integration tests.
- Use Swift Testing/XCTest interoperability during migration; do not rewrite a
  working legacy test suite only to change syntax.
- Use issue severity and dynamic cancellation to keep known flaky or
  environment-gated tests visible without hiding real failures.
- Use `anyAppleOS` only after verifying the project toolchain accepts it; it is
  useful for shared Apple-platform availability checks.
- Use module selectors (`ModuleName::TypeName`) when imported modules collide.
- Treat `@C` and Swift-C interop as specialized migration tools, not default app
  architecture.
- Keep performance attributes such as specialization and forced inlining behind
  measured bottlenecks.

## Xcode 27 Agent Policy

Coding agents in Xcode may draft plans, tests, prototypes, localization updates,
low-risk refactors, previews, Playgrounds, Device Hub runs, and diffs for human
review.

Coding agents must not receive secrets, signing credentials, App Store
credentials, production tokens, or private customer data. They must not change
release signing, entitlements, billing logic, authorization gates, or data
deletion logic without a human review record.

MCP and Agent Client Protocol integrations are toolchain connectors, not trust
boundaries. Treat every connected tool as least-privilege infrastructure.

## Device Hub And Simulator Matrix

Use Device Hub for:

- physical device inventory and configuration checks;
- resizable simulator testing;
- iPhone Mirroring layout checks;
- reproduced bug sessions with device state recorded;
- accessibility settings sweeps: Dynamic Type, VoiceOver, Reduce Motion,
  Reduce Transparency, Increase Contrast, and Dark Mode.

Record the tested device/OS/runtime for release evidence.

## macOS And Safari Watch Items

If an Apple-platform project includes macOS or web surfaces, verify:

- AppKit modernization: gestures, control events, keyboard navigation, state
  restoration, SwiftUI/AppKit bridge boundaries, and menu/window behavior;
- sandboxing, security-scoped bookmarks, Keychain, hardened runtime,
  notarization, and App Store/direct-download divergence;
- Safari/WebKit 27 features such as Customizable Select, Grid Lanes,
  `img sizes=auto`, `stretch`, HTML `<model>`, Immersive Environments, and web
  extension packaging;
- Spatial Preview only for apps handling USD, 3D, spatial photos, Apple
  Immersive Video, or Vision Pro workflows.
