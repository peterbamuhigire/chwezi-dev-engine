# Apple Platform Operations WWDC26

Use this reference when mobile release work touches iOS, iPadOS, macOS,
watchOS, visionOS, TestFlight, Xcode Cloud, App Store Connect, or multi-platform
Apple evidence.

## Toolchain Baseline

- Use Apple Silicon for primary Xcode 27 builds and agent-assisted workflows.
- Capture Xcode version, SDK version, Swift version, simulator/device runtime,
  and build number in release evidence.
- Keep fallback instructions for teams that have not yet moved all CI runners
  to Xcode 27, but do not let fallback CI define the target API surface.
- Verify signing assets in App Store Connect before a release window starts:
  certificates, provisioning profiles, bundle IDs, capabilities, associated
  domains, app groups, push notification keys, and merchant IDs.

## Device And Runtime Matrix

| Surface | Required evidence |
| --- | --- |
| iPhone | Current iOS runtime on physical device, compact and regular text sizes, portrait and landscape when supported. |
| iPad | iPadOS multitasking, Stage Manager where relevant, pointer/keyboard path, resizable layouts. |
| Mac Catalyst or macOS | Window resizing, menu commands, keyboard shortcuts, permissions, sandbox entitlements. |
| watchOS | Complications/widgets, background delivery limits, workout/media sessions if applicable. |
| visionOS | Spatial layout, immersion level, hand/eye input fallback, motion comfort. |
| Web/PWA | Safari/WebKit compatibility, installability, offline path, permission prompts. |

## Release Evidence

- Link the Xcode Cloud workflow or CI run that produced the candidate build.
- Attach TestFlight group, tester count, build number, crash-free session rate,
  and known feedback items.
- Record App Store review metadata changes: privacy nutrition labels, ATT,
  data collection, age rating, IAP products, subscriptions, and review notes.
- Store screenshots for App Store and Play Store separately; do not reuse
  Android screenshots for Apple unless the UI is genuinely identical.
- Keep a rollback note: previous live build, server feature flag, minimum
  supported API version, and entitlement migration path.

## WWDC26 Watch Items

- Device Hub can reduce manual device tracking, but release evidence still
  needs explicit device/runtime coverage.
- Xcode agents may help implementation and tests; record human review of
  generated code, security-sensitive actions, and release notes.
- Test App Intents, widgets, Live Activities, semantic indexing, and background
  assets as release surfaces, not only as local implementation details.
- For AI features, require evaluation reports plus privacy review before
  enabling a production experiment or App Store submission.
