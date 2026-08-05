# Asset Domain and API Contract

Parent skill: [`saas-managed-visual-assets`](../SKILL.md).

## Domain model

Treat the platform default and each tenant override as separate scopes. A scope owns:

- zero to 20 background records, including inactive records;
- one optional light-surface logo slot;
- one optional dark-surface logo slot;
- one optional favicon slot;
- a monotonically increasing manifest version for cache invalidation and concurrency control.

Each record stores an opaque asset ID, scope ID/type, asset type, canonical storage key, detected
MIME, width, height, byte size, checksum, state, order, creator, timestamps, and version. Keep
original names out of public metadata; retain them only if policy requires it and protect them as
sensitive metadata.

## Invariants

1. Tenant scope is resolved from authenticated server context. Platform scope requires a
   platform-level permission.
2. A tenant read resolves its valid override first, then the valid platform default, then a
   bundled safe fallback. An invalid or missing override never suppresses the fallback.
3. Background order is dense and deterministic. Only `active` records enter random selection.
4. Slot replacement is one logical operation. At most one current asset exists for each
   light-logo, dark-logo, and favicon slot.
5. The 20-background quota is checked inside the same serialization boundary as insertion.
6. Public identifiers never reveal filesystem/bucket keys or permit arbitrary path selection.

## Permission model

Use separate capabilities where the product needs separation of duties:

| Capability | Permitted operations |
|---|---|
| `visual_assets.view` | List metadata and previews for the actor's authorized scope |
| `visual_assets.upload` | Stage and process a candidate |
| `visual_assets.manage` | Activate, deactivate, reorder, replace, restore default |
| `visual_assets.delete` | Delete or schedule deletion after explicit confirmation |
| `platform_visual_assets.manage` | Mutate platform defaults across tenants |

Browser-session mutations require CSRF protection in addition to authentication and permission.
Log denied attempts at the security boundary without leaking whether another tenant's asset exists.

## Operation contract

The transport may be REST, RPC, or server-rendered forms, but it must expose equivalent semantics:

| Operation | Required behaviour |
|---|---|
| List | Return authorized metadata, slot state, quota usage, order, and manifest version |
| Upload | Accept one candidate, process it, then commit metadata; support an idempotency key |
| Preview | Serve only a committed or explicitly quarantined preview authorized to the actor |
| Activate/deactivate | Validate at least one safe fallback remains available |
| Reorder | Accept opaque IDs plus expected manifest version; reject stale writes |
| Replace slot | Preserve current slot until candidate commit succeeds |
| Delete | Remove logical availability first; enqueue physical cleanup after commit |
| Public manifest | Return active opaque URLs/IDs and version, never storage paths |

Use stable machine error codes such as `ASSET_LIMIT_REACHED`, `ASSET_TYPE_UNSUPPORTED`,
`ASSET_DECODE_FAILED`, `ASSET_DIMENSIONS_INVALID`, `ASSET_OUTPUT_TOO_LARGE`,
`ASSET_VERSION_CONFLICT`, and `ASSET_NOT_FOUND`. User messages explain recovery without exposing
decoder internals or storage locations.

## Concurrency and idempotency

- Lock the scope row or use an equivalent serializable/advisory lock while enforcing the quota,
  dense order, or fixed-slot replacement.
- Bind idempotency to actor, scope, operation, and candidate checksum. A retry returns the prior
  result; it does not create a second background.
- Reorder and activation requests carry an expected manifest version. Return a conflict and fresh
  state when another administrator won the race.
- Treat storage and database as a saga: staged candidate, canonical object, metadata commit, then
  old-object cleanup. Record compensating actions for every pre-commit failure.

## Public selection

The server chooses from the active authorized background pool at journey start. Persist only the
opaque selected ID in session/journey state. On each delivery, re-check that it still resolves;
fall back safely if an administrator removed it. Never accept a path, URL, tenant ID, or storage
key from the unauthenticated client as selection authority.
