# App Intelligence Architecture WWDC26

Use this reference when an iOS/macOS app exposes content/actions to Siri or adds
Foundation Models, Core AI, or agentic features.

## Boundary Model

```
Presentation
  SwiftUI/UIKit/AppKit views, View Annotations, permission states
Intent Surface
  AppIntents, AppEntity/AppSchema, widgets, Shortcuts, Siri actions
AI Surface
  Prompt builders, provider protocol, tools, Dynamic Profiles, Evaluations
Domain
  Use cases, authorization checks, business invariants, audit decisions
Data
  SwiftData/Core Data, Core Spotlight, API clients, local caches, Keychain
Infrastructure
  Foundation Models, Core AI/Core ML, PCC, third-party model providers
```

Presentation may call domain use cases through view models. App Intents and AI
tools also call domain use cases, not repositories directly. This keeps UI,
Siri, widgets, and models under the same authorization and validation rules.

## Provider Protocol

Create an app-owned protocol for model work:

- `generate`, `classify`, `summarize`, or domain-specific methods;
- provider metadata: provider kind, model/profile id, local/cloud path;
- cancellation and timeout;
- structured error states: unavailable, denied, unsafe, quota, invalid output.

Do not let SwiftUI views, App Intents, or repositories depend directly on a
third-party model SDK.

## App Intents Ownership

- Keep App Intent types near the feature they expose, but route actual work to
  domain use cases.
- Keep AppEntity mapping separate from persistence models when privacy or
  indexing fields differ from the stored record.
- Treat Core Spotlight indexing as a data export: schema, retention, deletion,
  tenant/account isolation, and opt-out rules matter.

## Evaluation Layer

AI evaluations belong beside the feature, not inside unit-test helpers only.
Store evaluation cases for prompt/template versions, provider variants,
locale/region variants, allowed/denied tools, defect regression prompts, and
unavailable-state fallbacks.

## Agent-Safe Modules

Mark modules that agents may edit without elevated review: UI prototypes,
localization strings, tests, docs, and low-risk adapters. Require human review
for authorization, billing, deletion, entitlements, signing, privacy, and data
migration modules.
