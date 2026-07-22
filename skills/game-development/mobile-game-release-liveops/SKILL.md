---
name: mobile-game-release-liveops
description: Use when preparing or operating Android/iOS game signing, packaging, store submission, privacy, ratings, analytics, crash reporting, IAP, staged rollout, rollback, support, patches, downloadable content, events, or ethical live operations.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Mobile Game Release and Live Operations
Promote the exact tested artefact through current platform gates, retain rollback and diagnosis evidence, and operate updates without compromising player trust or offline access.

## Prerequisites

Load `game-testing-polish`, existing Android/iOS mobile operations skills, security/privacy skills and current official platform requirements.
<!-- dual-compat-start -->
## Use When
- Building release pipelines, signing, store metadata, privacy declarations, ratings, analytics/crash consent, IAP, rollout, hotfix, support, DLC or live-event plans.
## Do Not Use When
- Store, SDK, tax, privacy, age-rating or platform requirements have not been checked against current primary sources.
## Required Inputs
Tested artefact and manifest, package identifiers, signing ownership, target territories/ages, data inventory, SDK/permission register, monetisation, store assets, support owners, rollout/rollback plan and legal approvals.
## Workflow
1. Verify current Unity/Godot, Android, Apple, store, privacy, rating, payment and tax requirements; date every check.
2. Produce reproducibly signed Android/iOS artefacts from tagged source and preserve symbols, dependency lock, SBOM/licence and provenance manifests.
3. Audit permissions, SDK data flows, consent, child-user posture, offline failure, account deletion and purchase restoration.
4. Validate store copy, screenshots/video, localisation, accessibility, content disclosures, ratings and cultural claims against the tested build.
5. Run internal/closed testing, staged rollout, crash/performance/player-support monitoring and explicit go/no-go thresholds.
6. Promote the tested artefact; do not rebuild between approval and release.
7. Operate patches/events through change control, save compatibility, economy simulation, content download fallback and rollback drills.
8. Conduct post-launch review and convert evidence into a prioritised roadmap rather than a raw request list.
## Quality Standards
- Keep signing keys, credentials and environment secrets outside source and with named custodians/recovery.
- Collect the minimum telemetry needed for a named decision; disclose, consent and retain it appropriately.
- Preserve offline core play unless the approved product model genuinely requires connectivity.
- Reject dark patterns, pay-to-win, undisclosed odds and manipulative child-directed monetisation.
## Anti-Patterns
- Store checklist copied from an old book. Fix: dated official-source verification.
- New release build after QA approval. Fix: promote identical artefact.
- Analytics SDK admitted for convenience. Fix: data-flow, size, performance, security and exit audit.
- Hotfix without save migration. Fix: compatibility and rollback gate.
- Reviews treated as backlog votes. Fix: triangulate with crashes, support, telemetry and research.
## Outputs
Release manifest; signing/custody plan; store compliance evidence; privacy/SDK/data map; rollout/rollback plan; support/runbook; live-ops calendar and economy controls; post-launch report.
## References
- [Store, signing and privacy gates](references/store-signing-privacy-gates.md)
- [Rollout, support and ethical live operations](references/rollout-support-liveops.md)
<!-- dual-compat-end -->
## Decision Rules
| Condition | Decision |
|---|---|
| Official requirement cannot be verified | Block submission and record the gap |
| Crash/performance threshold breaches during rollout | Halt or roll back |
| Event changes durable economy or save state | Simulate, migrate, test and version it |
| Core experience works offline | Keep account/cloud/telemetry optional where feasible |
## Read Next
Pair with existing `mobile-platform-operations`, Android/iOS release skills, security/privacy skills, and `game-testing-polish`.
