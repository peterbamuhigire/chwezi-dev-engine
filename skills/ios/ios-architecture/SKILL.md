---
name: ios-architecture
description: Use when defining iOS module boundaries, dependency direction, state ownership, App Intent integration, or AI provider seams; use ios-development for feature implementation details.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# iOS Architecture
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Designing, reviewing, or refactoring iOS app architecture, modular boundaries, dependency injection, navigation, production patterns, or large-team delivery.
- The task mentions MVVM, clean architecture, Swift patterns, UIKit/SwiftUI boundaries, modularization, App Intents, Siri/Spotlight, Foundation Models, Core AI, provider abstraction, scaling, CI impact, or maintainability.
- A narrow retired iOS architecture skill is referenced by name.

## Do Not Use When

- The request is only about general iOS implementation; use `ios-development`.
- The request is only about UI polish; use `ios-ui-ux-design`.
- The request is only about persistence, platform capabilities, quality/release, or security/RBAC; use those parent skills.

## Required Inputs

- App scope, platform targets, current module layout, UI framework mix, backend/API shape, team size, release constraints, and the concrete architectural decision or defect.
- Existing project files or diagrams when implementation or review is requested.

## Workflow

1. Load `ios-development` first for shared iOS implementation standards.
2. Identify the architecture concern: app composition, module boundaries, Swift patterns, scale practices, or production gotchas.
3. Load only the matching reference below.
4. Produce a concrete architecture decision, refactor plan, review finding, or implementation patch with tests and rollout notes when relevant.

## Quality Standards

- Architecture decisions must preserve platform-native UX, testability, dependency clarity, and predictable release behaviour.
- Module boundaries must have explicit ownership, public APIs, dependency direction, and migration steps.
- Any scale guidance must include CI, build-time, ownership, or observability impact when it changes delivery workflow.

## Anti-Patterns

- Creating abstract layers without a current complexity or testability problem.
- Mixing UIKit, SwiftUI, model state, and networking without clear ownership.
- Treating large-team practices as default for small apps.

## Outputs

- iOS architecture decision record, module map, refactor plan, review findings, or implementation guidance.

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---|---|
| Product flows and quality attributes | Product discovery | required | Establishes architectural drivers |
| API and error contract | `api-design-first` | conditional | Defines client boundaries |
| Threat model | `ios-security-and-rbac` | required for protected data | Constrains trust boundaries |

## Decision Rules

| Condition | Choice |
|---|---|
| Small feature with one owner | Feature module, not a new framework layer |
| Reused domain behaviour with stable semantics | Extract a dependency-inverted package |
| Framework or vendor API may change | Hide it behind a narrow protocol |
| Cross-feature mutable state | Assign one owner and expose immutable observations |

## Degraded Mode

Without repository access, return assumptions and an architecture sketch only. Without builds, mark dependency cycles, actor isolation, package visibility, and launch behaviour as unverified.
If execution is unavailable, keep build-dependent findings in the exception register.

## Domain Anti-Patterns

- Creating modules by screen count. Fix: split on ownership and dependency boundaries.
- Putting SwiftUI types in the domain layer. Fix: map presentation state at the feature edge.
- Using a global service locator. Fix: inject explicit protocols at composition roots.
- Sharing mutable state across actors. Fix: assign actor ownership and send values.
- Abstracting a single stable implementation prematurely. Fix: add a seam only for a named change risk.

- `references/ios-architecture-advanced.md` for dependency injection, MVVM variants, navigation, and testable architecture patterns.
- `references/ios-at-scale.md` for modularization, large-team workflows, build systems, and CI practices.
- `references/ios-production-patterns.md` for production UIKit/SwiftUI lifecycle and app-store-proven implementation rules.
- `references/ios-swift-design-patterns.md` for Swift-idiomatic patterns and reusable implementation recipes.
- `references/app-intelligence-architecture-wwdc26.md` for App Intents, semantic indexing, Foundation Models/Core AI provider boundaries, evaluation layers, and agent-safe module ownership.
<!-- dual-compat-end -->
## Read next
- `ios-development` for implementation; `ios-quality-and-release` for verification and distribution.
