# WWDC26 Apple Platform Skill Modernization Plan

Status: proposed
Date: 2026-06-21
Scope: `skills-web-dev` Apple/iOS/macOS/mobile skills, plus required companion updates in `C:\wamp64\www\design-system-skills`

## Evidence Base

Primary local research input:

- `C:\Users\Peter\Documents\Claude Projects\digital-research-engine\projects\apple-wwdc-2026-developer-impact-report\export\wwdc26-developer-impact-report.md`
- `C:\Users\Peter\Documents\Claude Projects\digital-research-engine\projects\apple-wwdc-2026-developer-impact-report\export\sources.md`

Primary Apple sources verified for planning:

- Apple Newsroom, "Apple accelerates app development with new intelligence frameworks and advanced tools", 2026-06-08.
- Apple Developer, "WWDC26 iOS guide".
- Apple Developer, "What's New - Xcode".
- Apple Developer, "What's new in Swift", WWDC26 session 262.

Planning caveat: the report states that full Apple release-note pages were not fully retrievable. This plan therefore targets confirmed public WWDC26 guidance and requires a release-note pass before code examples are changed to new beta-only APIs.

## Target Compatibility Definition

The engine should become compatible with Apple platform development as of WWDC26 by meeting these standards:

- Build and review guidance assumes Xcode 27 as the current Apple toolchain, with Apple Silicon as the required Xcode host.
- Swift guidance covers Swift 6.4 language, library, Swift Testing, concurrency, and cross-platform updates while preserving strict concurrency discipline.
- iOS and iPadOS guidance targets the iOS 27 SDK surface while preserving explicit minimum-deployment and `#available` rules for apps that still support older devices.
- macOS guidance covers macOS 27 development, AppKit modernization, SwiftUI/AppKit interop, sandboxing, notarization, Apple Silicon tooling, Safari/WebKit 27, and spatial preview paths where relevant.
- AI guidance covers Foundation Models, the Language Model protocol, Dynamic Profiles, Core AI, on-device privacy, Private Cloud Compute availability constraints, third-party model providers, and Evaluations.
- System integration guidance treats App Intents, App Entities, App Schemas, View Annotations, Spotlight semantic indexing, widgets, and App Intents Testing as first-class app surfaces.
- Quality guidance covers Xcode agents, Device Hub, Xcode Cloud, Instruments concurrency profiling, Swift Testing migration, MetricKit, TestFlight evidence, and release gates.
- Security guidance covers App Attest, Trust Insights watch items, agentic-feature threat modeling, prompt/tool injection risk, action authorization, privacy manifests, secrets, and entitlement review.
- Design guidance covers Liquid Glass-era Apple UI, iPhone resizability, iPhone Mirroring, Dynamic Type, accessibility settings, SwiftUI/UIKit/AppKit modernization, SF Symbols, haptics, and platform-native parity.

## Non-Goals

- Do not claim macOS 27 drops Intel runtime support unless Apple release notes confirm it. The confirmed claim is Xcode 27 being Apple Silicon only.
- Do not convert every Apple TODO folder into an active skill by default. The active catalog is already above the soft target; prefer updating retained skills and references unless a separate entrypoint materially improves routing.
- Do not remove support for iOS 17 projects without a migration policy. The target is latest-SDK compatibility, not forced latest-OS-only deployment.
- Do not rely on Reddit, media roundups, or search snippets for factual skill rules.

## Affected Skills

### Main Engine: Active Apple Skills

| Skill | Modernization Role | Priority |
| --- | --- | --- |
| `skills/ios/ios-development/SKILL.md` | Update baseline stack, load order, availability policy, Xcode 27, Swift 6.4, Device Hub, agent rules, and latest-SDK compatibility. | Critical |
| `skills/ios/ios-development/references/skill-deep-dive.md` | Replace Swift 6.0/Xcode 16 framing; add Swift 6.4, availability, Xcode 27, agent validation, Device Hub, and updated release gate. | Critical |
| `skills/ios/ios-ai-ml/SKILL.md` and references | Add Foundation Models, Language Model provider abstraction, Dynamic Profiles, Core AI, Evaluations, PCC constraints, and AI security gates. | Critical |
| `skills/ios/ios-platform-capabilities/SKILL.md` and references | Add App Intents, App Entities, App Schemas, View Annotations, Spotlight semantic index, App Intents Testing, widgets via App Intents, NowPlaying, Music Understanding, and service-specific routing. | Critical |
| `skills/ios/ios-quality-and-release/SKILL.md` and `references/ios-tdd.md` | Add Swift Testing 6.4 updates, Device Hub test matrix, Xcode Cloud updates, Instruments Swift Concurrency profiling, AI evaluations, and release evidence. | Critical |
| `skills/ios/ios-security-and-rbac/SKILL.md` and references | Add agentic-feature threat model, App Attest refresh, Trust Insights watch item, model/tool authorization, privacy manifests, and local AI data handling. | High |
| `skills/ios/ios-architecture/SKILL.md` and references | Add app-intelligence architecture: provider boundary, intent/entity layer, model evaluation layer, agent-safe module boundaries, and multi-platform availability rules. | High |
| `skills/ios/ios-data-persistence/SKILL.md` and references | Add semantic-index readiness, privacy-aware local indexing, SwiftData migration checks, Spotlight/Core Spotlight data exposure rules, and offline AI/cache boundaries. | High |
| `skills/ios/ios-monetization/SKILL.md` | Add WWDC26 App Store/IAP watch items, Unity StoreKit plugin note, subscription organization/group session follow-up, and StoreKit testing refresh. | Medium |

### Main Engine: Cross-Platform Mobile Skills

| Skill | Modernization Role | Priority |
| --- | --- | --- |
| `skills/mobile-cross/mobile-platform-operations/SKILL.md` | Add Apple Silicon/Xcode 27 readiness, TestFlight/Xcode Cloud release operations, Store review evidence, and cross-platform AI availability planning. | High |
| `skills/mobile-cross/kmp-development/SKILL.md` and references | Update iOS target guidance for Xcode 27, Swift interop, Swift 6.4, iOS 27 SDK, and SwiftUI-native UI boundaries. | Medium |
| `skills/mobile-cross/pwa-offline-first/SKILL.md` and references | Add Safari 27/WebKit 27 test pass for PWAs, Customizable Select, `img sizes=auto`, layout changes, and iOS/iPadOS browser constraints. | Medium |

### Main Engine: Apple TODO Promotion Candidates

Promote only when the plan owner accepts the catalog cost, or fold the content into existing retained references.

| TODO Path | Recommended Action | Reason |
| --- | --- | --- |
| `skills/ios/xcode-project-engineering/TODO.md` | Promote to active skill or fold into `ios-development/references/ios-project-setup.md`. | Xcode 27, Apple Silicon, Device Hub, MCP/ACP plugins, schemes, and signing now need stronger guidance. |
| `skills/ios/xcode-instruments-performance/TODO.md` | Promote to active skill if Apple performance work is common; otherwise fold into `ios-quality-and-release`. | Instruments gained specific Swift Concurrency and responsiveness workflows. |
| `skills/ios/xcode-cloud-testflight/TODO.md` | Promote or fold into `ios-quality-and-release`. | Xcode Cloud is now faster and covers Metal/visionOS builds; release evidence needs a clear runbook. |
| `skills/ios/swift-concurrency-macos/TODO.md` | Promote if macOS app work is active; otherwise fold into architecture references. | Swift 6.4 plus Apple agent workflows make actor boundaries and cancellation rules important. |
| `skills/ios/macos-appkit-interop/TODO.md` | Promote. | WWDC26 AppKit modernization and Mac app work need a distinct reference beyond iOS. |
| `skills/ios/macos-app-sandbox-security/TODO.md` | Promote or fold into `ios-security-and-rbac` as a macOS reference. | Sandboxing, notarization, entitlements, and local-file access are distinct from iOS RBAC. |
| `skills/ios/macos-system-integrations/TODO.md` | Promote if GlassHub/macOS work proceeds. | Spotlight, Quick Look, Share/Handoff, File Provider, and spatial preview need macOS-specific decisions. |
| `skills/ios/macos-git-libgit2/TODO.md` | Keep TODO unless GlassHub Git-client work is active. | It is domain-specific and not required for general Apple standards compatibility. |

### Design-System Engine Updates

| File | Action | Reason |
| --- | --- | --- |
| `skills/07-mobile-ios-android-cross-platform/ios-ui-ux-design/SKILL.md` | Refresh iOS 26 wording to iOS 27 SDK era; keep the Liquid Glass constraints; add transparency personalization, resizability, iPhone Mirroring, App Intents widgets, and SwiftUI/UIkit modernization notes. | Existing skill is close but should match WWDC26 terminology. |
| `skills/07-mobile-ios-android-cross-platform/cross-platform-design-parity/SKILL.md` | Add iOS 27 SDK and Android parity watch items; keep "unify meaning, diverge mechanism". | Cross-platform plans must not flatten Liquid Glass or iOS resizability into generic mobile UI. |
| `skills/03-layout-grid-and-composition/responsive-and-adaptive-layout/SKILL.md` | Add iPhone full-resizability and iPhone Mirroring QA notes for Apple-platform apps. | WWDC26 raises adaptive layout priority. |
| `skills/00-cross-cutting-ops-qa-a11y/accessibility-wcag-2-2-compliance/SKILL.md` | Add Apple-specific checks for Liquid Glass transparency, Reduce Transparency, Increase Contrast, Reduce Motion, Dynamic Type AX sizes, VoiceOver, and keyboard navigation. | Liquid Glass and personalization must not degrade accessibility. |
| `skills/08-motion-and-interaction/motion-design/SKILL.md` | Add Apple haptics/motion verification for Liquid Glass and Reduce Motion. | Motion must be meaningful and optional. |
| `skills/09-design-systems-tokens-and-theming/design-tokens-and-naming/SKILL.md` | Add Apple material/token caveat: do not tokenise system materials as fixed colors; tokenise semantic roles and fallbacks. | Liquid Glass adapts to context and accessibility settings. |
| `skills/00-cross-cutting-ops-qa-a11y/design-qa-and-pre-launch-review/SKILL.md` | Add iOS 27/iPadOS 27/macOS 27 visual QA pass. | Design QA should catch platform drift before release. |

Typography note for design-system work: native iOS UI may use San Francisco/SF Pro as the Apple system face. Any branded display or marketing face must come from the approved design-system font categories and must not use banned AI-default fonts.

## Execution Phases

### Phase 0: Evidence Lock

1. Copy the WWDC26 report source register into a repository update note or link it from the plan.
2. Archive or manually snapshot primary Apple URLs before rewriting skills that cite specific API behavior.
3. Create a short `docs/updates/2026-06-21-wwdc26-apple-platform-modernization.md` change log when implementation starts.
4. Confirm whether the user wants TODO promotions as active `SKILL.md` files or folded references, because the active catalog is above the soft target.

Exit criteria:

- Primary Apple sources are listed with access date.
- Release-note gaps remain clearly marked as gaps.
- Promotion policy is decided before new active skills are added.

### Phase 1: Baseline Apple Toolchain And Swift Update

Update `ios-development` and its references:

- Change baseline from "Swift 6.0+ | Xcode 16+ | iOS 17+" to a two-tier policy:
  - Current development toolchain: Xcode 27, Swift 6.4, latest iOS/iPadOS/macOS SDKs.
  - Deployment floor: project-specific, with iOS 17+ retained only when the product needs that fleet; latest-only examples must be gated.
- Add `#available` and `@available` rules, including Swift 6.4 `anyAppleOS` guidance after release-note verification.
- Add Xcode 27 Apple Silicon-only requirement and migration checklist for CI and developer machines.
- Add Xcode agent policy: agents may draft, test, localize, and refactor within guardrails; they must run tests, show diffs, and never handle secrets.
- Add Device Hub to simulator/device testing language.
- Add Swift 6.4 Swift Testing interoperability, warning severity, dynamic test cancellation, and flaky-test repetition to test guidance.

Exit criteria:

- No active iOS skill still presents Xcode 16 or Swift 6.0 as the current recommended baseline without context.
- Compatibility guidance distinguishes SDK target, deployment target, feature availability, and hardware support.

### Phase 2: AI And Model Runtime Update

Update `ios-ai-ml`, architecture, quality, and security references:

- Add a decision matrix for Foundation Models, Core AI, Core ML, Vision, NaturalLanguage, Speech, SoundAnalysis, Create ML, MLX, and third-party providers.
- Add provider abstraction guidance around the Language Model protocol, with local/on-device, Private Cloud Compute, and third-party paths.
- Add Dynamic Profiles as a session-level adaptation concern, not a global setting.
- Add Evaluations as mandatory evidence for AI behavior that changes by prompt, model, tool, device, locale, or data state.
- Add Core AI guidance for teams that bring their own model: model loading, specialization, memory budgets, AOT compilation, zero-copy paths, privacy, and fallback.
- Add AI availability gates for device, region, language, Apple Intelligence support, and server-model access terms.

Exit criteria:

- AI guidance no longer reads as Core ML-only.
- Each AI feature path has privacy, availability, evaluation, and fallback rules.

### Phase 3: App Intents, Siri, Spotlight, And Widgets

Update `ios-platform-capabilities`, data persistence, architecture, and quality references:

- Add App Intents inventory workflow: entities, actions, search surfaces, view annotations, widgets, and privacy boundaries.
- Add App Entities and App Schemas guidance for products with user content.
- Add Spotlight semantic index and Core Spotlight guidance, including what not to index.
- Add View Annotations guidance for visible content and onscreen action references.
- Add App Intents Testing as a required test type for Siri-facing features.
- Add WidgetKit dynamic styling and App Intents customization notes.

Exit criteria:

- Skills treat App Intents as product architecture, not as shortcut garnish.
- Siri-facing work has a test and privacy checklist.

### Phase 4: Liquid Glass, Resizability, And Native UI

Update the design-system iOS skill and related references:

- Refresh `ios-ui-ux-design` to name iOS 27 SDK-era Liquid Glass and avoid stale iOS 26-only phrasing.
- Keep the rule: Liquid Glass belongs to chrome/navigation, not content; no glass-on-glass; accessibility settings must be tested.
- Add iPhone app resizability, iPhone Mirroring, updated tab/navigation bars, refreshed materials, refined typography, and SwiftUI lazy/reorderable containers as Apple UI QA points.
- Add AppKit modernization notes to design QA: gestures, control events, keyboard navigation, state restoration, corner concentricity, and Liquid Glass updates.
- Update design QA and accessibility checks for Reduce Transparency, Increase Contrast, Reduce Motion, Dynamic Type AX sizes, VoiceOver, keyboard navigation, and focus.

Exit criteria:

- The design-system engine can guide iOS 27-era Apple UI without using banned default visual language.
- Main-engine iOS skills route user-facing screens to the design-system iOS skill.

### Phase 5: Xcode 27, Agents, Device Hub, And Release Operations

Update `ios-quality-and-release`, `mobile-platform-operations`, and the Xcode TODO candidates:

- Add Xcode 27 agent workflow rules: planning, code review, simulator interaction, previews, Playgrounds, tests, and diff review.
- Add MCP/ACP plugin guidance for Xcode only as a toolchain integration, not as a permission bypass.
- Add Device Hub test-matrix guidance for physical devices, resized simulators, iPhone Mirroring, and reproduced bugs.
- Add Xcode Cloud update: Apple Silicon, speed claim watch item, Metal builds, visionOS builds, artifacts, and release evidence.
- Add localization-agent workflow with string catalogs, plural variants, review, and locale QA.

Exit criteria:

- Skills can tell an Apple developer how to use agents without weakening review, test, or secrets controls.
- Release skills produce evidence suitable for TestFlight/App Store sign-off.

### Phase 6: Security And Privacy Update

Update `ios-security-and-rbac`, platform capabilities, and AI references:

- Add threat model for agentic app features: prompt injection, tool misuse, confused-deputy actions, data exfiltration, unauthorized intents, and unsafe model output.
- Add App Attest and device integrity checks where backend trust matters.
- Add Trust Insights as a WWDC26 watch item until the full Apple documentation is reviewed.
- Add rules for sensitive content in Spotlight, Siri, local model context, logs, telemetry, crash reports, and analytics.
- Add entitlement review for App Groups, Keychain groups, file access, background modes, push, HealthKit, Bluetooth, Wallet, and local network access.

Exit criteria:

- AI, App Intents, and app action surfaces require explicit authorization and privacy review.
- Security guidance covers local, cloud, and third-party model risks.

### Phase 7: macOS And Safari/WebKit Coverage

Add or fold macOS-specific guidance:

- AppKit modernization: SwiftUI/AppKit bridge, gesture recognizers, control events, keyboard navigation, state restoration, and menu/window behavior.
- macOS sandbox/security: security-scoped bookmarks, Keychain, hardened runtime, notarization, entitlements, and direct-download/App Store split.
- macOS integrations: Spotlight, Quick Look, Handoff, Share, notifications, menu bar extras, File Provider, and spatial preview.
- Safari/WebKit 27: Customizable Select, Grid Lanes, `img sizes=auto`, `stretch`, HTML `<model>`, Immersive Environments, extension packaging, and WebView/PWA verification.

Exit criteria:

- The engine no longer treats Apple development as iOS-only.
- Safari/WebKit guidance is routed into PWA and web-surface reviews.

### Phase 8: StoreKit, App Store, Games, Media, And Specialty Frameworks

Targeted updates only:

- Add WWDC26 watch items for Apple In-App Purchase, group/organization subscriptions, and StoreKit testing.
- Add official Unity StoreKit and Background Assets plugin note to monetization or game/media references if a game skill exists later.
- Add NowPlaying, Music Understanding, Core Image RAW v9, camera/photo changes, and Background Assets to platform-capability routing.
- Add Game Porting Toolkit 4, Steam Asset Converter, Metal, Reality Composer Pro 3, and spatial workflows as specialty routing notes, not general iOS requirements.

Exit criteria:

- Specialty framework mentions route developers to follow-up source review instead of bloating every iOS skill.

### Phase 9: Documentation, Fixtures, And Guardrails

1. Update `docs/skill-routing-index.md` for changed routing language or promoted skills.
2. Update `docs/skill-aliases.yml` only if skills are renamed, merged, or deactivated.
3. Add routing fixtures for new or materially changed Apple routes in `scripts/routing_fixtures.yml`.
4. Run:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
python -X utf8 scripts\routing_smoke_test.py
python -X utf8 scripts\routing_smoke_test.py --collisions
```

5. If design-system skills are edited, run that engine's equivalent guardrails if present and perform a manual link check for changed references.

Exit criteria:

- No broken reference links.
- Routing fixtures prove Apple/iOS/macOS queries land on the intended skills.
- Active catalog count stays under the 200 hard cap and any additions are justified.

## Proposed Work Order

1. Phase 0 evidence lock and promotion decision.
2. Phase 1 baseline toolchain update.
3. Phase 2 AI/model update.
4. Phase 3 App Intents/Siri/Spotlight update.
5. Phase 4 design-system iOS UI refresh.
6. Phase 5 Xcode/quality/release update.
7. Phase 6 security/privacy update.
8. Phase 7 macOS/Safari coverage.
9. Phase 8 specialty framework notes.
10. Phase 9 routing, fixtures, guardrails, and update record.

## Acceptance Criteria

The modernization is complete when:

- Every active Apple/iOS/mobile skill either reflects WWDC26 standards or explicitly states why it is unaffected.
- Main iOS guidance supports Xcode 27, Swift 6.4, iOS 27 SDK, Apple Silicon tooling, Device Hub, Swift Testing migration, and latest-OS feature availability.
- AI guidance covers Foundation Models, Core AI, Evaluations, provider abstraction, privacy, region/device/language gates, and security.
- App Intents guidance covers entities, schemas, view annotations, Spotlight semantic index, App Intents Testing, and widgets.
- Design-system guidance reflects current Apple UI conventions without violating Chwezi anti-slop typography and visual rules.
- macOS and Safari/WebKit 27 work have a real route, either as active skills or retained references.
- New active skills, if any, have routing fixtures and do not create near-duplicate collisions.
- Guardrail and routing checks pass or have documented known failures.

## Risks

- Beta APIs can change before public release; keep examples availability-gated and source-labeled.
- Adding too many active Apple skills can worsen catalog size and routing precision.
- Apple Intelligence and Siri AI availability varies by device, language, region, and legal constraints; skills must not imply universal availability.
- Xcode 27 requiring Apple Silicon can break teams that still depend on Intel Macs for local builds.
- AI and App Intents features can create privacy and action-authorization failures if they are treated only as UX features.

