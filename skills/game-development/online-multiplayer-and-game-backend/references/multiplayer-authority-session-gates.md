# Multiplayer authority and session gates

The supplied *Multiplayer Game Development with Unreal Engine 5* is a secondary technical source covering networking basics, Unreal actor/property replication, RPCs, multiplayer AI, debugging, sessions, session data, deployment, and Epic Online Services. It is admitted for conceptual orientation; exact Unreal and service APIs must be checked against the pinned engine/plugin version and official documentation.

## Minimum contract

| Decision | Evidence |
|---|---|
| Authority | one owner for spawn, movement, combat, inventory, score, economy, and match result |
| Replication | field/event, audience, frequency, ordering/reliability need, bandwidth budget |
| RPC | caller, callee, validation, rate limit, idempotency, failure response |
| Session | state diagram with timeout, cancellation, reconnect, late join, and cleanup |
| Persistence | write owner, transaction/idempotency key, conflict rule, recovery path |
| Evolution | compatible-version window, migration path, explicit rejection behaviour |

Release tests must include measured loss, latency, jitter, reorder, duplication, disconnect, process crash, and version mismatch. A successful localhost PIE session is not release evidence.

