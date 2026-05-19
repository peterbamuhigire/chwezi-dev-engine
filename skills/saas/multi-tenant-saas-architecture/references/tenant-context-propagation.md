# Tenant Context Propagation — Reference

Tenant context is the spine of a multi-tenant SaaS — it travels with every request, every log line, every metric, every queue message, every cache key. Get this right and tenant isolation falls out naturally. Get it wrong and isolation bugs are inevitable.

## What "Tenant Context" Is

The runtime carrier of *which tenant is being served right now*. At minimum:
- `tenant_id` — unique tenant identifier.
- `user_id` — the user acting on behalf of the tenant.
- `role` / `permissions` — what the user can do in this tenant.
- `plan` / `tier` / `entitlements` — what the tenant is allowed.
- `correlation_id` — request-scoped tracing identifier.
- `region` / `pod` (if multi-region/pod) — physical placement of the data.

## Token Format (JWT)

```
Header
  alg: RS256 | EdDSA
  kid: rotation-key-id
Payload
  sub: user_id
  aud: api.example.com
  iss: auth.example.com
  iat, exp (15 min)
  tenant_id: ten_456
  user_id: usr_789
  role: admin
  plan: pro
  entitlements: { features: [...], limits: { ... } }
  pod: us-west-2 (if applicable)
  correlation_id: req_abc123 (optional; usually a separate header)
Signature
```

Issued at login or tenant switch; verified by every service on every request.

**Critical rule:** `tenant_id` comes from the verified JWT claim. **Never** from request body, query string, or unverified header. The most common SaaS isolation bug is reading `tenant_id` from POST body — any user can then forge it.

## Propagation Map

| Surface | How tenant_id propagates |
|---|---|
| Inbound HTTP | JWT in `Authorization: Bearer <token>` |
| Internal service → service | mTLS + JWT forwarded OR signed internal token with same claims |
| Database query | application middleware injects `tenant_id` predicate (or RLS `SET LOCAL tenant_id = ?`) |
| Cache key | prefix every key with `t:{tenant_id}:` |
| Queue / event payload | every message envelope carries `tenant_id`, `correlation_id`, `idempotency_key` |
| Log line | structured field `tenant_id` (and `user_id`, `correlation_id`) on every record |
| Metric label | `tenant_id` (budget cardinality! use sample/tier for high-volume metrics) |
| Trace span | `tenant_id` and `correlation_id` as span attributes |
| Webhook (outbound) | sign with tenant-scoped HMAC; include `tenant_id` in payload |
| Email send | include `tenant_id` in custom metadata; suppression list checks per-tenant |
| Storage path | prefix with `tenants/{tenant_id}/...` for S3-like stores |

## Middleware Patterns

### HTTP middleware (extracts tenant context, stores per-request)
```python
def tenant_context_middleware(request, call_next):
    token = extract_bearer(request)
    claims = verify_jwt(token)            # raises on invalid
    ctx = TenantContext(
        tenant_id=claims['tenant_id'],
        user_id=claims['user_id'],
        role=claims['role'],
        plan=claims['plan'],
        entitlements=claims['entitlements'],
        correlation_id=request.headers.get('X-Correlation-Id') or generate(),
    )
    TenantContext.set(ctx)              # contextvar / threadlocal
    try:
        response = call_next(request)
    finally:
        TenantContext.clear()
    return response
```

### Database middleware (auto-inject tenant_id filter)
```python
# ORM / query layer
def add_tenant_predicate(query):
    ctx = TenantContext.current()
    if not ctx.is_super_admin:
        query = query.filter(tenant_id=ctx.tenant_id)
    return query
```

Or use Postgres Row-Level Security:
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::int);

-- On each request:
SET LOCAL app.tenant_id = '456';
```

### Logging
```python
def log_format(record):
    ctx = TenantContext.current()
    record['tenant_id'] = ctx.tenant_id if ctx else None
    record['user_id'] = ctx.user_id if ctx else None
    record['correlation_id'] = ctx.correlation_id if ctx else None
```

### Queue envelope
```json
{
  "tenant_id": "ten_456",
  "user_id": "usr_789",
  "correlation_id": "req_abc",
  "idempotency_key": "evt_xyz",
  "occurred_at": "2026-05-11T10:23:00Z",
  "event_type": "invoice.created",
  "payload": { ... }
}
```

## Super-Admin Caveat

Super-admin actions touch cross-tenant data. They have a different propagation rule:
- JWT has `super_admin: true` and **no** `tenant_id` (or has a working tenant_id chosen explicitly).
- DB middleware skips the tenant predicate (or RLS uses a bypass policy).
- Every access writes an audit log entry with `actor_user_id`, `target_tenant_id`, `action`, `justification`.

## Anti-Patterns

- **Reading `tenant_id` from POST body** — forgeable.
- **Storing `tenant_id` in app-level globals (not request-scoped)** — leaks across requests in async runtimes.
- **Forgetting to propagate `tenant_id` into async work** — worker logs and metrics are tenantless.
- **Omitting `tenant_id` from cache keys** — cross-tenant cache hits.
- **No `correlation_id`** — debugging one request across services becomes archaeology.
- **`tenant_id` as a string in some places, int in others** — silent type-coercion bugs.
- **Logging full JWT** — secret leakage. Log claims minus `sub`/`exp` or hash.
