# SCIM 2.0 Provisioning (Reference)

Deep-dive for `saas-sso-scim-enterprise-auth` section 5. Covers the User and Group
schema, the CRUD endpoints, PATCH semantics (the hard part), deprovisioning, and
the Okta / Azure AD / OneLogin quirks that break naive implementations.

SCIM (RFC 7643 schema, RFC 7644 protocol) is PUSH from the buyer's IdP to your
platform. The IdP is the system of record for who exists; your endpoints receive
create / update / deactivate calls on the IdP's schedule. You implement the
receiving side. "We poll the IdP nightly" is not SCIM and is fragile.

## Endpoint surface (mounted at `/scim/v2/{tenant}/`)

| Resource | Method | Purpose | Notes |
|---|---|---|---|
| `/Users` | GET | List / filter users | Must support `filter`, `startIndex`, `count` |
| `/Users` | POST | Create user | Returns 201 + Location header |
| `/Users/{id}` | GET | Read one user | `id` is YOUR id, not the IdP's |
| `/Users/{id}` | PUT | Replace user | Full resource replace |
| `/Users/{id}` | PATCH | Partial update | Most traffic; hardest to get right |
| `/Users/{id}` | DELETE | Hard-delete user | Many IdPs never call this (see below) |
| `/Groups` | GET/POST/PUT/PATCH/DELETE | Group CRUD | Membership via PATCH |
| `/ServiceProviderConfig` | GET | Advertise capabilities | IdP reads this first |
| `/Schemas` | GET | Resource schemas | |
| `/ResourceTypes` | GET | Resource types | |

### Auth

Bearer token, one per tenant, generated in your UI and pasted into the IdP's
SCIM connector. Store only a hash (`scim_bearer_token_hash`). Validate it
constant-time. Scope every query by the tenant resolved from the token, never
from the URL alone -- a token for tenant A must never touch tenant B's rows.

## User schema (the subset that matters)

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "id": "9a8b7c6d",
  "externalId": "00u1abcOktaId",
  "userName": "ada@acme.com",
  "name": { "givenName": "Ada", "familyName": "Lovelace" },
  "displayName": "Ada Lovelace",
  "emails": [{ "value": "ada@acme.com", "type": "work", "primary": true }],
  "active": true,
  "groups": [{ "value": "grp-eng", "display": "Engineering" }],
  "meta": {
    "resourceType": "User",
    "created": "2026-05-01T10:00:00Z",
    "lastModified": "2026-05-30T08:00:00Z",
    "location": "https://app.example.com/scim/v2/acme/Users/9a8b7c6d"
  }
}
```

| Field | Map to | Rule |
|---|---|---|
| `userName` | your login / email | Unique within tenant; case-insensitive match |
| `externalId` | store as-is | The IdP's id; correlate updates by this, not by email |
| `emails[primary].value` | user email | May differ from userName at some IdPs |
| `active` | enabled flag | `false` = deactivate, NOT delete (see deprovisioning) |
| `id` | your row id | Returned to IdP; IdP addresses the user by it thereafter |

Always persist `externalId`. When the IdP renames a user's email, it still sends
the same `externalId`; match on that to avoid creating a duplicate.

## List, filter, pagination

SCIM pagination is 1-based and uses `startIndex` + `count` (not cursors):

```text
GET /Users?filter=userName eq "ada@acme.com"&startIndex=1&count=100
```

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
  "totalResults": 1,
  "startIndex": 1,
  "itemsPerPage": 1,
  "Resources": [ { "id": "9a8b7c6d", "userName": "ada@acme.com", "active": true } ]
}
```

You MUST support at least `userName eq "..."` filtering -- IdPs call it before
every create to decide create-vs-update. If you ignore the filter and always
return all users, the IdP will create duplicates. Cap `count` (e.g. 200) and
clamp oversized requests rather than rejecting them.

## PATCH semantics -- the hardest part

PATCH carries `Operations` with `op` in `add` / `replace` / `remove`. Test
against real Okta, Azure AD, and OneLogin payloads; they differ in shape.

Deactivate a user (the single most common operation):

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [{ "op": "replace", "path": "active", "value": false }]
}
```

Azure AD frequently omits `path` and sends the value as an object instead:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [{ "op": "replace", "value": { "active": false } }]
}
```

Group membership add (note the filtered path):

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [
    { "op": "add", "path": "members",
      "value": [{ "value": "9a8b7c6d", "display": "ada@acme.com" }] }
  ]
}
```

Group membership remove uses a value-path filter:

```json
{ "op": "remove", "path": "members[value eq \"9a8b7c6d\"]" }
```

PATCH rules to implement:

- Handle `op` with AND without `path` (Azure omits it; merge the value object).
- `op` is case-insensitive per spec; lowercase it before matching.
- `replace` on a missing multi-valued attribute behaves like `add`.
- `remove` with a filter must target exactly the matching sub-element.
- Apply operations IN ORDER; a later op can overwrite an earlier one.
- Make the whole PATCH atomic: apply all ops in a transaction or none.
- Return the full updated resource (200) so the IdP re-syncs its view.

Failure mode of getting `path`-less Azure payloads wrong: Azure marks the app
"unhealthy", retries with backoff, and the buyer's helpdesk files a ticket that
"deprovisioning is broken" -- a security finding, not a cosmetic bug.

## Deprovisioning (the security-critical lifecycle)

Two distinct signals, and you must honour both:

| Signal | Meaning | Your action |
|---|---|---|
| `PATCH active=false` (or PUT with active=false) | User offboarded / disabled | Disable login NOW; revoke live sessions and tokens |
| `DELETE /Users/{id}` | IdP removes the mapping | Soft-delete or fully purge per your retention policy |

Critical: most IdPs DEACTIVATE (`active=false`) rather than DELETE. If you only
implement DELETE, an offboarded employee keeps access. Deactivation must:

1. Set the user inactive (login refused).
2. Revoke all active sessions and API tokens immediately (do not wait for
   session expiry).
3. Emit an audit event (`user.deprovisioned`) for the buyer's SIEM.

Do not hard-delete on deactivate -- the IdP may reactivate later, and you owe an
audit trail. Reserve hard delete for an explicit DELETE plus your retention
window.

## ServiceProviderConfig (advertise honestly)

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
  "patch":        { "supported": true },
  "bulk":         { "supported": false, "maxOperations": 0, "maxPayloadSize": 0 },
  "filter":       { "supported": true, "maxResults": 200 },
  "changePassword": { "supported": false },
  "sort":         { "supported": false },
  "etag":         { "supported": false },
  "authenticationSchemes": [
    { "name": "OAuth Bearer Token", "type": "oauthbearertoken",
      "description": "Per-tenant bearer token" }
  ]
}
```

Advertise only what you actually implement. Claiming `bulk` you do not support
makes the IdP send bulk requests that 500.

## Error contract

Use SCIM error responses, not your generic API errors:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "409",
  "scimType": "uniqueness",
  "detail": "userName already exists in this tenant"
}
```

| Situation | HTTP | scimType |
|---|---|---|
| Duplicate userName on POST | 409 | `uniqueness` |
| Unknown user on GET/PATCH | 404 | (none) |
| Malformed filter | 400 | `invalidFilter` |
| Bad/expired bearer token | 401 | (none) |

Returning 200 on a duplicate create (instead of 409 + uniqueness) causes the IdP
to create duplicates.

## IdP quirk table

| IdP | Quirk | Mitigation |
|---|---|---|
| Azure AD / Entra | PATCH omits `path`; value is an object | Merge value object into resource |
| Azure AD | Sorts/filters on `externalId` | Index and persist `externalId` |
| Okta | Deactivate = `PATCH active=false`, never DELETE | Implement deactivate as full revocation |
| Okta | Requires `userName eq` filter before create | Implement exact-match filter |
| OneLogin | May send `emails` without `primary` flag | Treat the first work email as primary |
| Generic | Group membership via `members[value eq "..."]` | Implement value-path filters |

## Anti-patterns

- Implementing DELETE but not `active=false` -> offboarded users keep access.
- Ignoring the `filter` on `/Users` -> duplicate user creation.
- Matching updates by email instead of `externalId` -> duplicates on rename.
- Scoping by URL tenant only, not the token's tenant -> cross-tenant writes.
- Returning your house JSON error shape -> IdP treats the app as broken.
- Non-atomic PATCH -> partial updates leave users in inconsistent states.
