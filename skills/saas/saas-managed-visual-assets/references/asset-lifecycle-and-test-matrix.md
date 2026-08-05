# Asset Lifecycle and Test Matrix

Parent skill: [`saas-managed-visual-assets`](../SKILL.md).

## Lifecycle

Use explicit states so retries, cleanup, and incident diagnosis do not depend on filesystem
guesswork:

```text
received -> quarantined -> validated -> canonicalized -> scanned -> committed -> active/inactive
                 \-> rejected
committed -> superseded -> grace-period -> deletion-queued -> deleted
```

Only committed active assets are publicly selectable. A rejection records a bounded reason code
and removes candidate bytes. `superseded` remains recoverable only for the documented rollback
window. A janitor reconciles stale quarantine objects, metadata/object mismatches, and failed
deletion jobs without guessing ownership from filenames.

## Critical flows

| Flow | Success | Failure behaviour | Evidence |
|---|---|---|---|
| Add background | Canonical object and record committed; quota/order updated once | Candidate removed; pool unchanged | Audit event, metadata, object hash |
| Replace logo/favicon | New immutable object becomes current atomically | Old slot remains current | Before/after IDs, rollback pointer |
| Reorder backgrounds | Dense order and manifest version advance once | Stale version returns conflict and fresh state | Concurrency test and audit event |
| Delete inactive background | Record becomes unavailable; cleanup queued | Logical result retained; cleanup retries | Queue/job evidence |
| Delete selected journey image | New requests omit it; existing journey falls back safely | No broken path or cross-scope lookup | Public delivery test |
| Tenant override missing/invalid | Platform default or bundle renders | Error logged without customer outage | Fallback test |

## Audit and observability

For each mutation record event ID, timestamp, actor ID/type, permission, scope type/opaque ID,
asset type/opaque ID, operation, prior/new state or version, detected MIME/dimensions/bytes,
result code, correlation ID, and source IP/device fields allowed by policy. Do not log raw bytes,
secrets, signed URLs, storage credentials, or full original names.

Track upload attempts/results by reason, processing latency, compression ratio, quota denials,
version conflicts, active-pool size, missing-object delivery failures, fallback rate, quarantine
age, orphan count, and cleanup retries. Alert on repeated decoder failures, cross-scope denials,
or sustained fallback/missing-object rates.

## Verification matrix

| Area | Required cases |
|---|---|
| Authorization | Platform admin, tenant admin, ordinary user, wrong tenant, expired session, CSRF failure |
| Quota | 0, 19, 20, attempted 21, and concurrent attempts at 19 |
| Slots | Empty, upload, replace, failed replace, restore default, retry same idempotency key |
| Backgrounds | Active/inactive selection, reorder conflict, delete selected image, empty active pool |
| Processing | Approved formats, spoof/truncate/polyglot/SVG, pixel bomb, alpha, metadata, output too large |
| Storage | Write failure, metadata failure, cleanup failure, orphan reconciliation, path/key restriction |
| Delivery | Correct MIME/nosniff/cache, opaque IDs, missing object fallback, manifest version invalidation |
| UX/accessibility | Keyboard upload/reorder/delete, status announcements, progress/cancel/retry, 20-item message |
| Performance | Representative mobile CPU/network, processing budget, likely auth-page LCP image budget |

## Release and rollback

Ship schema/storage policy before exposing upload controls. Seed bundled fallbacks before enabling
managed slots. Roll out behind a platform flag when migrating existing products, import legacy
assets through the same canonical pipeline, and compare public manifests before cutover.

Rollback disables mutation first, restores the prior manifest/slot metadata, and leaves immutable
objects intact until verification completes. Never roll back by deleting newly referenced objects
or rewriting audit history. Name the release owner, rollback owner, scanner/decoder owner, and
orphan-cleanup owner in the evidence bundle.
