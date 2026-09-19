# Action authority and circuit-breaker contract

`tools/approval_control_plane.py` remains the canonical local approval gate.
The September 2026 extension adds `ExecutionBudget(max_steps, max_cost,
max_seconds)`, `pause()`/`resume()`, and `trip_circuit_breaker()`. The gate
checks these limits immediately before the operation callback, after approval
scope and policy checks, so a denied step cannot invoke the side effect.

Consequential actions continue to require a policy-versioned preview,
separation of duties, typed approval, expiry, nonce, audit availability,
idempotency, rollback and post-action verification. A completed idempotency key
is bound to its preview hash; reusing the key with changed payload is denied.

The helper classifies actions through the existing L0-L3 adapter. It does not
authenticate people or supply a live budget source. Host identity, durable
checkpoint storage and production kill-switch latency are `NOT_ASSESSED` until
an adapter proves them.
