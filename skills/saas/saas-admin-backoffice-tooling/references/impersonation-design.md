# Impersonation Design - Reference

Impersonation is the single most dangerous feature in the back-office. Done well it lets support see exactly what the tenant sees and resolve issues in minutes. Done badly it is an invisible, unlogged, unbounded master key over every customer's data, and the first thing a regulator or a breached-tenant lawyer asks about.

This reference specifies how to build it to an audited, time-boxed, consent-aware standard.

## section 1 The Decision: Should You Even Build It?

| Situation | Build impersonation? | Failure mode of the wrong choice |
|---|---|---|
| B2C app, low-sensitivity data | Yes, full impersonation | Without it, support cannot reproduce bugs; tickets bounce for days |
| B2B app, business data | Yes, but read-only default + write requires consent | Full write impersonation by default means a support typo edits a customer's live records with no recourse |
| Health / finance / regulated data | Read-only, scoped, consent-gated, dual-control | Unrestricted PHI/PII access is a reportable breach the moment a regulator audits the access log |
| Single high-value enterprise tenants | Per-tenant opt-in; tenant can disable entirely | Forcing impersonation on a tenant that contractually forbids it is a contract breach |

If you cannot afford the audit, consent, and time-boxing machinery below, do not ship impersonation. A "view as user" feature with no guardrails is worse than no feature.

## section 2 Read-Only vs Write Impersonation

These are two different features with two different risk profiles. Treat them separately.

| Mode | What it allows | When granted | Guardrails |
|---|---|---|---|
| **Read-only (default)** | GET requests served as the target user; all mutating verbs rejected at the gateway | support_l2 + justification | Banner, audit, 30-min box |
| **Write (elevated)** | Full session as the target; mutations allowed | support_l2 + tenant consent OR super_admin co-sign | Banner, audit, 15-min box, every write double-stamped |

Enforce the read-only boundary at the request gateway, not in business logic. A read-only impersonation session carries a claim `impersonation_mode=read_only`; the gateway rejects any non-idempotent method (POST, PUT, PATCH, DELETE) with 403 before it reaches a handler. Relying on each handler to check the mode itself guarantees one handler will forget, and that handler will be the one that deletes data.

```python
def gateway_guard(request, session):
    if session.is_impersonation and session.mode == "read_only":
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            audit_log("IMPERSONATION_WRITE_BLOCKED",
                      actor=session.staff_user_id,
                      acting_as=session.target_user_id,
                      target_tenant=session.target_tenant_id,
                      path=request.path)
            raise Forbidden("Read-only impersonation cannot perform writes.")
```

## section 3 Consent Model

Consent is a per-tenant, per-plan policy decision, resolved at session-start time. Do not bake one global rule into code.

| Consent policy | Behaviour | Typical plan |
|---|---|---|
| `implicit` | Support may impersonate without per-session approval; banner shown | Free / self-serve |
| `notify` | Support may impersonate; tenant primary admin emailed at session start | Pro |
| `explicit` | Support requests access; tenant admin must click "Grant access" (time-boxed grant) before session can start | Enterprise / regulated |
| `disabled` | Impersonation forbidden entirely; back-office shows a greyed control with the policy reason | Contractually opted-out tenants |

The wrong choice here is treating every tenant as `implicit`. An enterprise customer who signed a DPA forbidding staff access will treat a single silent impersonation as a breach notification trigger. Resolve consent from `tenant_impersonation_policy` and fail closed (deny) if the row is missing.

## section 4 Scoping

An impersonation session must be scoped to exactly one target user within one tenant. It must NOT grant cross-tenant movement.

- Scope the session token to `target_user_id` and `target_tenant_id`. Any request whose tenant context differs from the session's `target_tenant_id` is rejected.
- A staff member who needs to view two tenants opens two sessions, each separately justified and audited. Reusing one session across tenants destroys the per-tenant audit trail.
- Never let an impersonation session escalate the target user's own privileges. If the target user is a tenant-admin, the staff member sees what that admin sees - no more. Do not silently impersonate the highest-privilege user in the tenant "to be safe".

## section 5 Time-Boxing

Every session has a hard `expires_at`. There is no "renew" - when it expires, the staff member starts a fresh, freshly justified session.

| Mode | Default | Maximum | Idle timeout |
|---|---|---|---|
| Read-only | 30 min | 4 hours | 15 min idle ends session |
| Write | 15 min | 1 hour | 10 min idle ends session |

Enforce expiry at the gateway on every request (compare `now()` to `session.expires_at`), not only via a background sweep. A background-only sweep leaves a window where an expired session still works. The wrong choice - unbounded sessions - means a laptop left unlocked at lunch is an open door into a customer account for the afternoon.

## section 6 Session Banner

The banner is the tenant-visible proof that access is happening. It is not optional UI polish; it is the consent surface.

- Persistent, non-dismissible bar at the top of every page: "A support engineer (Jane Doe, ticket #4821) is currently viewing your workspace. Read-only. Ends 14:32." 
- For write mode, the banner is red and says "...and can make changes on your behalf."
- The banner text is rendered server-side from the impersonation session, never from a client flag the staff browser could suppress.
- The tenant's own admins see the banner too - so the customer organisation knows, not just the impersonated individual.

A silent impersonation (no banner) is the canonical trust catastrophe: discovered months later, it reads as covert surveillance regardless of intent.

## section 7 Audit

Every impersonation session produces a bracketed pair of audit events plus a stamp on every action taken inside it.

```json
{
  "event": "IMPERSONATION_START",
  "actor_user_id": 9001,
  "actor_ip": "10.2.3.4",
  "target_user_id": 55012,
  "target_tenant_id": 123,
  "mode": "read_only",
  "justification": "Reproducing export bug, ticket #4821",
  "ticket_id": "4821",
  "consent_policy": "notify",
  "consent_evidence": "email_sent:2026-05-30T13:01:02Z",
  "started_at": "2026-05-30T13:02:00Z",
  "expires_at": "2026-05-30T13:32:00Z"
}
```

Every mutation within a write session is double-stamped with both identities:

```json
{
  "event": "RECORD_UPDATED",
  "actor_user_id": 9001,
  "acting_as_user_id": 55012,
  "target_tenant_id": 123,
  "impersonation_session_id": "imp_7f3a",
  "before_state": {"...": "..."},
  "after_state": {"...": "..."}
}
```

`IMPERSONATION_END` records the reason for ending (manual, expiry, idle, kill-switch). Audit rows are written in the same transaction as the action; an action that cannot be logged must not commit.

## section 8 Break-Glass

Some incidents need access that exceeds normal scope or bypasses consent (for example, a live security incident where the tenant admin is unreachable and customer data is being exfiltrated). This is break-glass: deliberately friction-heavy, loud, and rare.

- Requires super_admin + a second super_admin co-sign within a 10-minute window.
- Requires an incident ticket reference.
- Posts a high-visibility alert to the security Slack channel and pages the on-call security lead.
- Time-boxed to 30 minutes, write-enabled, no renewal.
- Generates a post-incident review obligation: a break-glass session that is not reviewed within 48 hours auto-escalates to the CISO.

The failure mode of having no break-glass path is staff inventing one - sharing a super-admin credential, or running raw SQL - precisely during the incident when auditability matters most. Build the loud door so nobody climbs through the window.

## section 9 Kill-Switch

A tenant admin, or a security operator, must be able to terminate any active impersonation session against that tenant in under five seconds. Implement with a runtime-checked revocation key (for example a Redis set of revoked session IDs) consulted on every request, with the database updated asynchronously for audit. A purely database-backed revocation that the runtime caches for minutes is too slow to stop active exfiltration.

## section 10 Anti-Patterns

- **Login-as via a magic admin URL** that mints a normal target-user session with no impersonation flag - indistinguishable from the real user in logs; forensics impossible.
- **Justification field optional** - everyone leaves it blank; the audit log becomes a list of "someone accessed something".
- **One global consent rule in code** - breaks the contract with the tenant that opted out.
- **Read-only enforced per-handler** - the one handler that forgets is the one that mutates.
- **Reusing a session across tenants** - collapses per-tenant attribution.
- **Banner rendered from a client flag** - staff browser can suppress it; consent surface defeated.
- **No idle timeout** - abandoned session stays open for the full max window.
- **Break-glass with no review obligation** - the emergency door becomes the everyday door.

## See Also

- `saas-admin-backoffice-tooling` section 5 - the impersonation workflow this expands.
- `references/internal-roles-and-permissions.md` - which roles may impersonate.
- `saas-control-plane-engineering` - the audit-log spine.
- `dual-auth-rbac` - MFA and co-sign primitives.
- `saas-tenant-data-portability-and-erasure` - why access to a tenant's data is itself a processing event.
