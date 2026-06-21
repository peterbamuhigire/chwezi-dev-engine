# WWDC26 Apple Platform Skill Modernization

Date: 2026-06-21

## Summary

Implemented the WWDC26 Apple platform modernization plan without adding new active
skill entrypoints. The active catalog stays focused while the existing iOS,
mobile, security, release, AI, platform-capability, and design-system guidance
now reflects the current Apple development baseline.

## Main Engine Changes

- Updated `ios-development` for Xcode 27, Swift 6.4-ready guidance, latest SDK
  compatibility, availability gates, Device Hub, Xcode agents, and Apple Silicon
  build assumptions.
- Updated `ios-ai-ml` for Foundation Models, Language Model providers, Dynamic
  Profiles, Core AI, Core ML, privacy, provider boundaries, and evaluation gates.
- Updated `ios-platform-capabilities` for App Intents, App Entities, App Schemas,
  View Annotations, Siri, Spotlight semantic indexing, widgets, media, and
  specialty framework watch items.
- Updated architecture, persistence, quality/release, security/RBAC,
  monetization, KMP, PWA, and mobile operations guidance with Apple-specific
  compatibility, privacy, testing, and release evidence rules.
- Added routing fixtures for iOS AI, App Intents/Siri/Spotlight, and iOS
  release evidence tasks.

## Design-System Changes

- Updated the external `design-system-skills` Apple UI guidance for current
  Liquid Glass usage, SF Symbols 8, Dynamic Type, haptics, accessibility
  settings, app icon variants, iPhone/iPad/Mac-designed-for-iPhone resizability,
  Safari/WebKit behavior, and pre-launch Apple visual QA.

## Sources

- Local research export:
  `C:\Users\Peter\Documents\Claude Projects\digital-research-engine\projects\apple-wwdc-2026-developer-impact-report\export`
- Apple Developer WWDC26 iOS guide:
  `https://developer.apple.com/wwdc26/guides/ios/`
- Apple Developer WWDC26 Design guide:
  `https://developer.apple.com/wwdc26/guides/design/`
- Apple Developer What's New - Xcode:
  `https://developer.apple.com/xcode/whats-new/`
- Apple Developer "What's new in Swift", WWDC26 session 262:
  `https://developer.apple.com/videos/play/wwdc2026/262/`
