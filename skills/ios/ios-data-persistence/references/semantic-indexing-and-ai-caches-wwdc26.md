# Semantic Indexing And AI Caches WWDC26

Use this reference when app data is exposed to Siri, Spotlight, App Entities,
View Annotations, widgets, or AI context.

## Treat Indexing As Export

Core Spotlight and semantic indexes are not just local implementation details.
They make data discoverable outside the app's main screen. Before indexing:

- classify fields as public, private, regulated, tenant-scoped, or secret;
- define account/tenant isolation;
- define delete and logout cleanup;
- define stale-index invalidation;
- document whether results can appear on lock screen, Siri, or system search.

## Safe Entity Mapping

Do not expose persistence models directly as App Entities when stored fields
include internal IDs, tenant IDs, audit fields, payment data, health data,
security labels, or raw user content. Create a separate projection:

```
SwiftData Model -> Domain Entity -> Search/Intent Projection
```

The projection owns display title, searchable terms, attribution, and allowed
actions.

## AI Local Context

Local AI context and caches must have:

- purpose and retention period;
- user-visible deletion path;
- no secrets, tokens, raw credentials, or hidden tenant data;
- encryption or file protection class appropriate to sensitivity;
- model/provider version metadata for evaluation reproduction.

## Offline And Sync Rules

- Index only records the current user is authorized to access.
- Remove or mark stale records after logout, role change, tenant switch, or sync
  conflict.
- Server-denied records win over local search results.
- If an offline cache feeds AI output, show stale/last-synced state in the UI.

## Test Matrix

- index add/update/delete;
- logout cleanup;
- tenant/account switch cleanup;
- permission downgrade;
- search result opens the correct app route;
- App Intent action re-checks authorization;
- AI feature handles missing/stale local context.
