# Order creation boundary contract

Applies to every untrusted entry point (HTTP `handle_create` and queue `consume`).

| Condition | HTTP status | Machine code | Queue result |
|---|---|---|---|
| Body larger than `MAX_BODY_BYTES` (checked before parsing) | 413 | `body_too_large` | n/a (queue receives dicts) |
| Body is not valid UTF-8 JSON, or an object repeats a key | 400 | `malformed_json` | n/a |
| Value violates `ORDER_SCHEMA` (types, ranges, unknown fields, nulls, nested items) | 422 | `validation_failed` | `{"status": "rejected", "error": {"code": "validation_failed"}}` |
| Valid | 201 | - | `{"status": "accepted"}` |

Error payloads have the shape `{"error": {"code": <machine code>, "details": [...]}}`.
Nothing is written to the store unless the whole order is valid.
Booleans are never integers; `null` is only accepted where the schema says `nullable`.
Order identifiers become file names in the store, so they must match the schema pattern.
