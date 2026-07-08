# API Contract Template

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 API contract template
Benchmark: Google resource-oriented API patterns and Stripe idempotency discipline.

## API Identity

| Field | Value |
|---|---|
| API name | `<name>` |
| Version | `<v1>` |
| Owner | `<team/person>` |
| Consumers | `<consumer list>` |
| Compatibility policy | `<policy link>` |

## Resource Model

| Resource | Canonical name pattern | Owner | Notes |
|---|---|---|---|
| `<resource>` | `<parents/{parent}/resources/{resource}>` | `<service>` | `<notes>` |

## Methods

| Method | Route | Idempotency | Auth scope | Retry behavior |
|---|---|---|---|---|
| Create | `POST <route>` | Required | `<scope>` | `<safe/unsafe + condition>` |
| Get | `GET <route>` | N/A | `<scope>` | Safe |
| List | `GET <route>` | N/A | `<scope>` | Safe; paginated |
| Patch | `PATCH <route>` | Conditional | `<scope>` | Retry only with version/idempotency guard |
| Delete/Archive | `<route>` | Required if side effects | `<scope>` | `<policy>` |
| Custom | `POST <resource>:<verb>` | Required if mutating | `<scope>` | `<policy>` |

## Pagination

List methods use `max_page_size` and opaque `page_token`. Clients must continue until `next_page_token` is absent. Returning fewer than requested items does not mean the list ended.

## Error Model

```json
{
  "error": {
    "code": "<machine_code>",
    "message": "<human-readable message>",
    "target": "<field or resource>",
    "request_id": "<request id>",
    "retryable": false,
    "details": {}
  }
}
```

## Compatibility Rules

- Additive optional response fields are compatible.
- New required request fields, changed units, removed fields, and changed default sort are breaking.
- Versioned migrations must include client inventory, warning period, and rollback policy.
- Field names include units where applicable.

## QA Checklist

- [ ] Every mutating method declares idempotency behavior.
- [ ] Every list method is paginated from first release.
- [ ] Every error has machine code, target, retryability, and request ID.
- [ ] Every resource has a data owner.
- [ ] Every breaking change has migration path and compatibility note.

## See Also

- `examples/full-stack-saas-reference/api-contract.md`
- `templates/delivery-dod/evidence-pack.md`
