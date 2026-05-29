# Audit Log API (Reference)

Deep-dive for `saas-sso-scim-enterprise-auth` section 8. Covers the event schema,
immutability guarantees, cursor pagination, retention, and the export contract a
buyer's SIEM (Splunk, Datadog, Elastic, Sentinel) pulls against.

The buyer's security team wants a tenant-scoped, tamper-evident, paginated feed
of who-did-what. This is a price-of-entry feature for enterprise deals and is
frequently checked in security questionnaires (SOC 2, ISO 27001).

## Event schema

One row per event. Make it append-only and self-describing.

```json
{
  "id": "evt_01HZX4Q9K3",
  "occurred_at": "2026-05-30T08:14:22.512Z",
  "tenant_id": "ten_acme",
  "actor": {
    "type": "user",
    "id": "usr_9a8b",
    "email": "ada@acme.com"
  },
  "action": "user.role.changed",
  "target": {
    "type": "user",
    "id": "usr_77c1",
    "display": "grace@acme.com"
  },
  "context": {
    "ip": "203.0.113.7",
    "user_agent": "Mozilla/5.0 ...",
    "request_id": "req_abc123",
    "session_id": "sess_def456"
  },
  "metadata": { "from_role": "member", "to_role": "admin" },
  "sequence": 184213
}
```

| Field | Required | Rule |
|---|---|---|
| `id` | yes | Globally unique, opaque, sortable (ULID/KSUID) |
| `occurred_at` | yes | UTC, RFC 3339, millisecond precision |
| `tenant_id` | yes | Every query is scoped to it; never leak cross-tenant |
| `actor` | yes | `user` / `api_key` / `system` / `support` (break-glass) |
| `action` | yes | Stable dotted verb namespace (see catalogue) |
| `target` | when applicable | The resource acted upon |
| `context.ip` | yes | Source IP; key for SIEM correlation |
| `metadata` | optional | Action-specific, JSON; no PII beyond what is necessary |
| `sequence` | yes | Monotonic per tenant; drives the cursor and gap detection |

### Action catalogue (tenant-relevant events to emit)

```text
auth.login.succeeded        auth.login.failed         auth.logout
auth.mfa.enabled            auth.mfa.disabled         auth.sso.enforced
user.invited                user.removed              user.role.changed
user.provisioned (scim)     user.deprovisioned (scim)
apikey.created              apikey.revoked
plan.changed                billing.payment_method.updated
data.exported               integration.created       integration.revoked
domain.custom.added         ip_allowlist.changed
support.break_glass.used    audit.retention.changed
```

Emit only tenant-relevant events on this API. Internal platform telemetry
(metrics, debug traces) does not belong here; it pollutes the buyer's SIEM and
risks cross-tenant leakage.

## Immutability and tamper evidence

The audit log must be append-only. No UPDATE, no DELETE except retention
expiry, no application path that mutates a row.

- Storage: write-once table with no UPDATE grant for the app role; or an
  append-only store (e.g. an immutable bucket, or DB with row-level triggers
  rejecting UPDATE/DELETE). Retention deletion runs under a separate, audited job
  role.
- Tamper evidence (hash chain): each event carries the hash of the prior event
  for the tenant, so any deletion or edit breaks the chain and is detectable.

```text
event.chain_hash = SHA256( prev_chain_hash || canonical_json(event_without_chain_hash) )
```

Store `chain_hash` and `prev_chain_hash`. Periodically (and on demand) a verifier
walks the chain per tenant and asserts continuity; a break is an alert. This lets
a buyer's auditor verify the log was not edited.

- Sequence gaps: because `sequence` is monotonic per tenant, a missing number is
  detectable. Surface a gap as an integrity warning.

## Pagination: cursor, not offset

Use a forward cursor over `(occurred_at, sequence)` so large windows page
efficiently and new writes do not shift pages.

```text
GET /api/v1/admin/audit-log?from=2026-05-01T00:00:00Z&to=2026-05-31T00:00:00Z&limit=200&cursor=<opaque>
Authorization: Bearer <tenant_admin_api_key>
```

```json
{
  "data": [ /* events, ascending by (occurred_at, sequence) */ ],
  "cursor": "eyJzZXEiOjE4NDIxM30",
  "has_more": true
}
```

- The cursor encodes the last `(occurred_at, sequence)` returned; the next page is
  `WHERE (occurred_at, sequence) > (cursor.ts, cursor.seq)`.
- Stable ordering by `(occurred_at, sequence)` makes the cursor deterministic even
  when timestamps collide.
- Do NOT use `OFFSET N` -- at large N the database scans and discards N rows per
  page (O(N) per page, O(N^2) for a full export) and rows shift under concurrent
  writes, causing skips/duplicates.
- Default `limit` 200, max 1000. Clamp, do not reject, oversized requests.
- Filters: `action` prefix (`auth.*`), `actor.email`, `target.id`. All combine
  with the time range.

### Tail / streaming for SIEM

For continuous ingestion, the SIEM polls with the last cursor it stored:

```text
GET /api/v1/admin/audit-log?cursor=<last-seen>&limit=1000
```

Because the cursor is on a monotonic key, the SIEM gets exactly-once, in-order
delivery with no missed events across polls. Optionally offer a webhook push for
enterprise tenants in addition to pull.

## Retention

```text
GET /api/v1/admin/audit-log/retention-policy
```

```json
{ "retention_days": 365, "plan": "enterprise", "min_days": 90, "configurable": true }
```

| Plan | Default retention | Configurable |
|---|---|---|
| Pro | 90 days | no |
| Enterprise | 365 days | up to 7 years (compliance) |

- Deletion at retention boundary runs as an audited job (it emits
  `audit.retention.expired` summarising counts). It is the only delete path.
- Changing the retention policy is itself an audited event
  (`audit.retention.changed`) -- shortening retention to hide activity must be
  visible.
- For long compliance windows, tier storage: hot (DB, last 90d) + cold (object
  store, older), both queryable through the same API with the cold tier slower.

## Authentication and authorisation

- Tenant-admin API key or a scoped OAuth token; the audit-read scope is distinct
  from write scopes.
- Every query is hard-scoped to the token's tenant. A bug that lets tenant A read
  tenant B's audit log is a critical cross-tenant breach -- enforce in the data
  layer, not just the controller.
- Reads are idempotent and side-effect-free, but the fact that an export was
  performed is itself logged (`data.exported`, target = audit-log).

## Rate limiting

Customers pull large historical windows on first integration. Rate-limit
generously and prefer cursor pagination over hard caps:

| Endpoint | Limit | Why |
|---|---|---|
| List/tail | e.g. 60 req/min/tenant, 1000 events/page | Allows full backfill in minutes |
| Retention policy | 30 req/min/tenant | Cheap metadata read |

Too-aggressive limits here break SIEM ingestion and generate support tickets;
this is called out as an anti-pattern in the parent skill.

## Anti-patterns

- Offset pagination -> O(N^2) exports and shifting pages.
- Any UPDATE/DELETE path on audit rows besides the audited retention job.
- Emitting internal telemetry on the tenant audit feed -> cross-tenant leakage.
- Tenant scoping enforced only in the controller, not the data layer.
- No hash chain / sequence -> deletions are undetectable; fails audit.
- Aggressive rate limits that throttle legitimate SIEM backfill.
- Silent, unaudited break-glass actions absent from the feed.
