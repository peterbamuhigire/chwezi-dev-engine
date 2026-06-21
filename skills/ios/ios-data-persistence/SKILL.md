---
name: ios-data-persistence
description: iOS data persistence standards with SwiftData, Keychain, files, offline sync, Core Spotlight semantic indexing, App Entity data exposure, and AI cache/privacy boundaries.
metadata:
  portable: true
  compatible_with:
  - Codex
  - codex
---

# iOS Data Persistence
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Designing, implementing, or reviewing iOS persistence with SwiftData, Core Data migration, UserDefaults, Keychain, file storage, offline sync, Core Spotlight semantic indexing, App Entity exposure, AI local context, or privacy-sensitive caches.
- The task mentions local storage, migrations, offline-first sync, search/indexing, Siri/App Entity data exposure, or AI cache retention.

## Do Not Use When

- The task is general iOS implementation with no local data or cache concerns; use `ios-development`.
- The task is only platform capability routing; use `ios-platform-capabilities`.
- The task is security policy rather than persistence mechanics; use `ios-security-and-rbac` alongside this skill.

## Required Inputs

- Data model, sensitivity classification, deployment target, sync/backend contract, offline requirements, account/tenant model, deletion rules, and whether data is exposed to Spotlight, Siri, widgets, or AI context.

## Workflow

1. Load `ios-development` for Swift and project standards.
2. Choose storage: UserDefaults, Keychain, SwiftData/Core Data, FileManager, URLCache/NSCache, Core Spotlight, or an AI local-context cache.
3. Load `references/ios-swiftdata.md` for SwiftData details.
4. Load `references/semantic-indexing-and-ai-caches-wwdc26.md` when data is exposed to Siri, Spotlight, App Entities, widgets, or AI.
5. Produce a model spec, migration plan, cache policy, deletion policy, and test plan.

## Quality Standards

- Persistence models must separate stored data, domain entities, DTOs, and search/intent projections when privacy or API shape differs.
- Secrets belong in Keychain or stronger platform storage, not UserDefaults, SwiftData, Spotlight, or logs.
- Offline data must have conflict, sync, stale-state, and deletion behavior.
- Indexed or AI-context data must have retention, invalidation, and user/account cleanup rules.

## Anti-Patterns

- Exposing stored models directly as App Entities without reviewing fields.
- Keeping stale Spotlight entries after logout, role change, tenant switch, or deletion.
- Using local AI context as a hidden long-term memory without retention and deletion controls.
- Treating SwiftData migrations as a compile-time concern only.

## Outputs

- Persistence model spec, storage decision, SwiftData migration plan, offline sync plan, search/index projection, AI cache policy, or review findings.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Data safety | Persistence model spec | Markdown doc per `skill-composition-standards/references/entity-model-template.md` covering entities, projections, retention, and deletion | `docs/ios/persistence-model-orders.md` |
| Correctness | Persistence test plan | Markdown doc listing CRUD, migration, sync, index, and deletion test cases | `docs/ios/persistence-tests-orders.md` |

## References

- `references/ios-swiftdata.md` for SwiftData `@Model`, relationships, model actors, migrations, CloudKit, and testing.
- `references/semantic-indexing-and-ai-caches-wwdc26.md` for Core Spotlight, App Entities, Siri semantic index privacy, local AI context, and cache invalidation rules.
- `references/skill-deep-dive.md` for UserDefaults, Keychain, repository pattern, file storage, URLCache/NSCache, offline-first architecture, and cross-skill references.
<!-- dual-compat-end -->

## Storage Decision Guide

| Data Type | Storage | Example |
|---|---|---|
| User preferences | UserDefaults | Theme, language, sort order |
| Tokens / credentials | Keychain Services | JWT tokens, API keys, passwords |
| Structured app data | SwiftData or Core Data | Products, orders, customers |
| Searchable safe projections | Core Spotlight / App Entity projection | Title, display date, safe summary |
| Large files / images | FileManager | Photos, PDFs, exports |
| Temporary cache | URLCache / NSCache | API response caching |
| AI local context | App-owned encrypted cache or SwiftData projection | Prompt-safe summaries, never raw secrets |

Rule of thumb: simple flag/scalar = UserDefaults. Secret = Keychain. Relationships/querying = SwiftData. Binary blob = FileManager. Search/Siri/AI exposure = separate projection with explicit privacy review.
