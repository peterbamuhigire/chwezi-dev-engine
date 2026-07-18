---
name: mobile-platform-operations
description: Use when coordinating cross-platform mobile store assets, signing, RBAC operations, release planning, and Android/iOS evidence; use native release skills for platform-specific gates.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Mobile Platform Operations
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Planning or reviewing mobile delivery assets that span Android/iOS operations, app packaging, custom icons, RBAC, SaaS companion planning, Google Play readiness, App Store/TestFlight readiness, or Xcode Cloud evidence.
- The task references `mobile-custom-icons`, `mobile-rbac`, `mobile-saas-planning`, or `google-play-store-review`.
- A mobile project needs operational documentation, app-store evidence, or cross-platform implementation coordination.

## Do Not Use When

- The task is platform implementation only; use `android-development`, `ios-development`, or `kmp-development`.
- The task is only report UI; use `mobile-reports`.
- The task is iOS-only App Store release; use `ios-quality-and-release`.

## Required Inputs

- Target platforms, app distribution channels, icon/asset constraints, auth/RBAC model, SaaS backend assumptions, release timeline, and store policy obligations.

## Workflow

1. Load platform implementation skills first: `android-development`, `ios-development`, or `kmp-development`.
2. Choose the operations concern: icon assets, mobile RBAC, SaaS planning, Play Store review, App Store/TestFlight evidence, or cross-platform release coordination.
3. Load only the relevant reference below.
4. Produce the operational artifact, checklist, implementation guidance, or review evidence required for launch.

## Quality Standards

- Operational mobile work must be traceable: asset names, permissions, store evidence, release notes, and backend/API assumptions should be explicit.
- RBAC and SaaS plans must keep backend authority, offline behaviour, and platform UX states clear.
- Store review guidance must include privacy, permissions, policy risk, testing, and rollback notes.

## Anti-Patterns

- Treating store review, icons, and RBAC as last-minute polish.
- Shipping mobile apps without documented backend contracts and offline/error-state expectations.
- Using icon libraries where a project explicitly requires custom PNG assets.

## Outputs

- Mobile operations checklist, app asset manifest, RBAC matrix, SaaS companion app plan, Play Store review checklist, or release evidence.

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---|---|
| Signed release candidates | Android and iOS teams | required | Establishes shippable binaries |
| Store metadata and visual assets | Product/design owners | required | Supports review and listing consistency |
| Role, privacy, and support policies | Security/operations owners | required | Defines operational controls |

## Decision Rules

| Condition | Action |
|---|---|
| Platform evidence differs | Track separate Android and iOS exceptions; do not average readiness |
| Signing credential custody is unclear | Stop release and assign an accountable owner |
| Store claim lacks matching in-app behaviour | Correct the claim or implementation before submission |
| Critical operational path has no support runbook | Block launch |

## Degraded Mode

Without store-console, signing, CI, or device access, produce a missing-evidence register with owners. A document-only check cannot approve a mobile release.
If a required operational capability is unavailable, keep the corresponding release gate open.

## Domain Anti-Patterns

- Reusing one platform's screenshots for the other. Fix: capture each supported device family.
- Sharing signing secrets through project files. Fix: use controlled credential custody and rotation.
- Treating store approval as production readiness. Fix: verify monitoring, support, rollback, and RBAC.
- Publishing inconsistent privacy claims. Fix: reconcile manifests, disclosures, and runtime collection.
- Combining platform failures into one status. Fix: report readiness and blockers per platform.

- `references/mobile-custom-icons.md` for custom PNG icon naming, asset directories, and tracking.
- `references/mobile-rbac.md` for Android/cross-platform permission gates and offline authorization caches.
- `references/mobile-saas-planning.md` for native mobile SaaS planning documents and implementation sequencing.
- `references/google-play-store-review.md` for Android Play Store policy, testing, listing, and submission readiness.
- `references/apple-platform-operations-wwdc26.md` for Apple Silicon, Xcode 27, Device Hub, TestFlight, Xcode Cloud, and App Store evidence readiness.
<!-- dual-compat-end -->
## Read next
- Platform-specific Android and iOS release skills for signing, store, and device evidence.
