---
name: ios-platform-capabilities
description: iOS platform capability orchestration for App Intents, Siri, Spotlight semantic indexing, widgets, biometrics, Bluetooth printing, push notifications, native PDF export, networking, media, and Apple framework entitlements.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# iOS Platform Capabilities
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Implementing or reviewing iOS capabilities that require Apple frameworks, entitlements, permissions, device hardware, background delivery, native export, Siri exposure, or Spotlight indexing.
- The task references App Intents, App Entities, App Schemas, View Annotations, Core Spotlight, WidgetKit, LocalAuthentication, CoreBluetooth, APNs, notification extensions, URLSession, offline queues, certificate pinning, NowPlaying, Music Understanding, or `UIGraphicsPDFRenderer`.
- A retired capability skill is referenced by name.

## Do Not Use When

- The work is general iOS architecture or UI without a platform framework capability.
- The work is StoreKit monetization; use `ios-monetization`.
- The work is security/RBAC governance rather than capability implementation; use `ios-security-and-rbac`.

## Required Inputs

- Capability scope, target iOS versions, entitlements, permission copy, backend/API contract, offline requirements, privacy disclosures, and relevant device constraints.

## Workflow

1. Load `ios-development` for baseline Swift and app-structure rules.
2. Load `ios-security-and-rbac` when the capability touches secrets, identity, device trust, authorization, or tenant data.
3. Load `references/app-intents-siri-spotlight-wwdc26.md` when the feature exposes content/actions to Siri, Spotlight, widgets, or App Intents Testing.
4. Pick the reference for the requested capability and follow its implementation workflow.
5. Verify simulator/device limitations, entitlement setup, fallback behaviour, App Review evidence, and user-facing permission states.

## Quality Standards

- Capabilities must handle permission denied, unavailable hardware, offline operation where relevant, and background lifecycle constraints.
- Native framework use must be testable, privacy-compliant, and documented in release notes or app-review evidence when required.
- Siri/App Intents integrations must have entity/action inventory, semantic-index privacy review, App Intents tests, and unavailable-state handling.

## Anti-Patterns

- Implementing hardware or notification features without real-device verification.
- Hiding entitlement, permission, or App Review requirements inside code comments only.
- Building PDF/report/networking features without retry, failure, and export-state handling.

## Outputs

- Capability implementation guidance, framework integration checklist, entitlement/privacy notes, test plan, or review findings.

## References

- `references/ios-biometric-login.md` for Face ID/Touch ID launch gates and LocalAuthentication.
- `references/ios-bluetooth-printing.md` for CoreBluetooth ESC/POS thermal printing.
- `references/ios-push-notifications.md` for APNs, rich notifications, service extensions, and silent push.
- `references/ios-pdf-export.md` for native multipage PDF export with `UIGraphicsPDFRenderer`.
- `references/ios-networking-advanced.md` for production URLSession, typed errors, refresh, pinning, multipart, and offline queues.
- `references/app-intents-siri-spotlight-wwdc26.md` for App Intents, App Entities, App Schemas, View Annotations, Spotlight semantic indexing, App Intents Testing, and widget customization.
- `references/apple-framework-watch-items-wwdc26.md` for NowPlaying, Music Understanding, RAW, camera/media, Background Assets, Game Porting Toolkit, Unity plugins, and specialty follow-up routing.
<!-- dual-compat-end -->
