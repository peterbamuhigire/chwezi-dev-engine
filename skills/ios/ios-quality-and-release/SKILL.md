---
name: ios-quality-and-release
description: Use when planning or gating iOS tests, performance, TestFlight, App Store review, CI, device coverage, or release evidence; use ios-development for implementation before the release gate.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# iOS Quality And Release
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Planning, implementing, or reviewing iOS testing, TDD, debugging, stability, crash prevention, App Store readiness, or release evidence.
- The task mentions Swift Testing, XCTest, Device Hub, Xcode agents, Xcode Cloud, AI Evaluations, App Intents Testing, LLDB, Instruments, MetricKit, crash triage, regression gates, TestFlight, App Review, privacy labels, or production readiness.
- A retired iOS quality/release skill is referenced by name.

## Do Not Use When

- The task is only general implementation; use `ios-development`.
- The task is primarily security/RBAC; use `ios-security-and-rbac`.
- The task is primarily StoreKit monetization; use `ios-monetization` plus this skill only for release evidence.

## Required Inputs

- Feature scope, risk level, test targets, crash or defect context, release channel, App Store requirements, and acceptance criteria.

## Workflow

1. Load `ios-development` for baseline implementation rules.
2. Choose the quality lane: TDD, debugging, stability hardening, AI/App Intents evaluation, Device Hub testing, or App Store release.
3. Load only the matching reference.
4. Produce executable tests, triage steps, release checklist updates, or review findings with concrete evidence.

## Quality Standards

- Risky code paths need deterministic tests before sign-off.
- Debugging guidance must identify reproduction, instrumentation, suspected layer, and validation.
- Release guidance must include App Store policy, privacy, performance, accessibility, and rollback evidence where applicable.
- AI, App Intents, and Xcode-agent-assisted work require evaluation/test evidence, not only screenshots or manual review notes.

## Anti-Patterns

- Shipping iOS features with only manual happy-path testing.
- Treating crashes as isolated stack traces without reproduction and regression tests.
- Waiting until submission day to handle privacy labels, permissions, or review notes.

## Outputs

- iOS test plan, failing/passing tests, debug notes, crash RCA, stability checklist, App Store readiness checklist, or release evidence pack.

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---|---|
| Release candidate and change set | Delivery team | required | Defines the test scope |
| Risk-based test plan | Testing owner | required | Maps checks to failure impact |
| Privacy, entitlement, and store metadata | Security and product owners | required | Prevents submission blockers |

## Decision Rules

| Finding | Gate |
|---|---|
| Crash, data loss, entitlement, privacy, or purchase defect | Block release |
| Unsupported oldest-OS or required-device path | Block release |
| Flaky critical-flow test | Treat as failure until root cause is isolated |
| Non-critical cosmetic defect with owner and date | May ship only through explicit risk acceptance |

## Degraded Mode

Without Xcode Cloud, TestFlight, devices, or App Store access, return a release exception register. Never convert missing evidence into a pass.
If execution is unavailable, retain every runtime gate as open.

## Domain Anti-Patterns

- Testing only the latest simulator. Fix: cover the declared OS and physical-device matrix.
- Retrying flaky tests until green. Fix: quarantine with an owner and diagnose the race.
- Shipping without rollback or feature disablement. Fix: document containment before approval.
- Using screenshots as purchase evidence. Fix: retain signed transaction and server-event traces.
- Submitting stale privacy metadata. Fix: reconcile manifests, SDK declarations, and store answers.

- `references/ios-tdd.md` for Swift Testing/XCTest TDD workflow and test pyramid.
- `references/ios-debugging-mastery.md` for LLDB, Instruments, watchpoints, and advanced triage.
- `references/ios-stability-solutions.md` for crash prevention and resilient production patterns.
- `references/app-store-review.md` for App Store submission, policy, metadata, privacy, and review evidence.
- `references/wwdc26-quality-release.md` for Swift Testing 6.4 migration, Device Hub, Xcode 27 agents, Xcode Cloud, Instruments concurrency profiling, AI Evaluations, and release evidence.
<!-- dual-compat-end -->
## Read next
- `ios-development` for implementation fixes; `ios-platform-capabilities` for entitlement-specific validation.
