# Internal Roles and Permissions - Reference

The back-office is operated by your own staff, but "internal" does not mean "trusted with everything". The internal role model is where least privilege, separation of duties, and SOC2 access controls are made concrete. The anti-pattern this reference exists to kill is the `is_super_admin` boolean: a single flag that lets any staff member do anything, which makes the audit log meaningless and a single phished credential catastrophic.

## section 1 Principles

- **Least privilege**: each role gets the narrowest permission set that lets the holder do their job. A support agent does not need refund rights to answer tickets.
- **Separation of duties**: no single role both initiates and approves a high-risk action. The person who requests a large refund is not the person who co-signs it.
- **Deny by default**: a permission not explicitly granted is denied. New endpoints are inaccessible until a role is granted them.
- **Roles are data, not code**: permissions live in tables; granting/revoking is an audited mutation, not a deploy.
- **The API is the enforcement boundary**: the UI hides controls the role lacks, but the API re-checks every request. UI hiding is convenience, not security; an attacker calls the API directly.

## section 2 The Role Matrix

Roles are additive capability bundles. A staff member may hold more than one role; their effective permissions are the union, except where a separation-of-duties rule blocks a combination (section 4).

| Role | Can | Cannot | Why bounded |
|---|---|---|---|
| **support_l1** | Search tenants/users, view detail, view tickets, basic password reset, force logout | Impersonate, suspend, refund, any billing change, any delete | First-line; highest headcount, highest churn, so smallest blast radius |
| **support_l2** | All L1, plus impersonate (read-only, justified), suspend with reason, issue credit up to $50 | Hard-delete, refund over $200, plan price override, bulk ops | Escalation tier; can touch a live account but not move money meaningfully |
| **billing_ops** | Refund, credit, apply discount, override plan price, change billing email, pause/reactivate subscription | Suspend, impersonate, delete tenant, change feature flags | Owns money; deliberately cannot also alter account state or access content |
| **engineering_oncall** | Feature-flag overrides, restart workers, replay events, run reversible bulk ops (flag rollout, region migration with co-sign) | Refund, billing change, hard-delete, impersonate | Owns runtime; deliberately walled off from money and customer-content access |
| **security** | Force logout, revoke sessions, audit-log review, initiate GDPR erasure, kill-switch impersonation sessions, co-sign mass-suspend | Refund, plan override, normal impersonation | Owns incident response; reads everything in the audit log but does not transact |
| **finance_lead** | View billing, co-sign refunds over $1000, export financial reports | Issue refunds directly, impersonate, suspend, delete | Approver, not initiator - separation of duties on large refunds |
| **super_admin** | Everything, subject to MFA + co-sign on the highest-risk actions (hard-delete, mass-suspend, mass-delete) | Nothing technically, but every high-risk action is co-signed and audited | Break-glass tier; membership is tiny and reviewed quarterly |

The wrong choice - one `admin` role that is the union of all the above - means your support agent and your finance lead and your on-call engineer all have refund-and-delete power, and the access log can never answer "who could have done this?".

## section 3 Permission Model

Roles map to fine-grained permissions; endpoints require permissions, not roles. This decouples "what a role can do" from "what an endpoint needs", so adding an endpoint does not require editing every role.

```sql
CREATE TABLE permissions (
    code         VARCHAR(64) PRIMARY KEY,   -- 'tenant.suspend', 'billing.refund', 'tenant.impersonate'
    risk_tier    ENUM('low','medium','high','critical') NOT NULL
);

CREATE TABLE roles (
    code         VARCHAR(32) PRIMARY KEY,   -- 'support_l2', 'billing_ops'
    display_name VARCHAR(64)
);

CREATE TABLE role_permissions (
    role_code       VARCHAR(32) NOT NULL,
    permission_code VARCHAR(64) NOT NULL,
    PRIMARY KEY (role_code, permission_code)
);

CREATE TABLE staff_roles (
    staff_user_id BIGINT UNSIGNED NOT NULL,
    role_code     VARCHAR(32) NOT NULL,
    granted_by    BIGINT UNSIGNED NOT NULL,
    granted_at    DATETIME NOT NULL,
    expires_at    DATETIME,                 -- temporary elevation is time-boxed
    PRIMARY KEY (staff_user_id, role_code)
);
```

```python
def require_permission(staff_user_id, permission_code):
    perms = effective_permissions(staff_user_id)   # union of role permissions, expiry-filtered
    if permission_code not in perms:
        audit_log("AUTHZ_DENIED", actor=staff_user_id, permission=permission_code)
        raise Forbidden(permission_code)
    if permission_risk_tier(permission_code) in ("high", "critical"):
        require_mfa(staff_user_id)
```

Temporary elevation (a support_l2 granted billing_ops for an afternoon to cover an absence) uses `staff_roles.expires_at` and is itself an audited grant - never an untracked code path.

## section 4 Separation of Duties

Some permission combinations are forbidden in one person, and some actions require two different people.

| Rule | Enforcement |
|---|---|
| Initiator of a refund over $1000 cannot be its co-signer | Co-sign request rejects if `cosigner_id == initiator_id` |
| `billing_ops` and `security` not held simultaneously by default | Granting the second triggers a review flag; allowed only with documented justification |
| Hard-delete requires super_admin initiate + a *different* super_admin co-sign | Co-sign binds to a distinct staff id |
| Bulk mass-suspend requires super_admin + security co-sign | Two roles, two people |

The failure mode of ignoring separation of duties: the same person who issues a fraudulent refund also approves it; the audit log shows a clean self-approved transaction and nothing flags. Two-person control on money and destruction is the entire point.

## section 5 MFA and Session Requirements

- Every back-office login requires MFA. A back-office without MFA is one phished password away from a platform compromise.
- High and critical risk-tier permissions re-prompt for MFA at action time (step-up), not just at login.
- Back-office sessions are short (for example 8 hours) and bound to IP/device; idle timeout 30 minutes.
- The back-office is a separate auth realm and ideally a separate network segment from the customer app - not an `admin.html` page behind a JWT claim on the same surface.

## section 5a Worked Example - A Denied Action

A support_l1 agent opens a tenant and clicks a "Refund" control that should not be visible to them (a stale cached UI, or a hand-crafted API call). The flow:

```text
1. UI: the Refund control is hidden for support_l1 (convenience only).
2. Agent crafts POST /admin/tenants/123/refunds directly.
3. API: require_permission(agent_id, 'billing.refund')
   -> effective_permissions(agent_id) = {tenant.search, tenant.view, user.password_reset, user.force_logout}
   -> 'billing.refund' not in set
   -> audit_log("AUTHZ_DENIED", actor=agent_id, permission='billing.refund', target_tenant=123)
   -> 403 Forbidden
4. The AUTHZ_DENIED row is reviewed: repeated denials from one staff member are an
   insider-risk signal worth investigating, not just noise.
```

The two lessons: the API, not the UI, is the boundary; and denied attempts are themselves audit evidence. A back-office that hides the button but does not re-check at the API has no enforcement at all.

## section 5b Worked Example - A Time-Boxed Elevation

A billing_ops specialist is on leave; a support_l2 agent must cover for one afternoon.

```text
POST /admin/staff/4477/roles
  body: { "role_code": "billing_ops", "reason": "Cover for J. on leave, ticket OPS-991",
          "expires_at": "2026-05-30T18:00:00Z" }
  -> require_permission(granter_id, 'staff.grant_role')   # only managers hold this
  -> co-sign required: billing_ops is a money-touching role
  -> write staff_roles (granted_by, granted_at, expires_at)
  -> audit_log("ROLE_GRANTED", actor=granter_id, subject=4477, role='billing_ops', expires_at=...)
```

At 18:00 the row's `expires_at` lapses; `effective_permissions` filters it out on the next request. No deploy, no manual revoke, no orphaned standing privilege. The wrong choice - granting the role with no expiry "just for today" - leaves the agent with refund powers indefinitely, which the next access review must catch (and usually does not until it is a finding).

## section 6 Lifecycle and Review

- **Joiner**: role grant is a ticketed, approved, audited action; default is no roles.
- **Mover**: changing teams revokes old roles and grants new ones in one reviewed change - no accretion of stale permissions.
- **Leaver**: offboarding revokes all `staff_roles` rows immediately; sessions invalidated.
- **Quarterly access review**: super_admin and security membership reviewed every quarter; stale grants revoked. SOC2 CC6 expects evidence of this review.

## section 7 Anti-Patterns

- **`is_super_admin` boolean** - one flag, no granularity, useless audit attribution.
- **Roles checked in the UI only** - API called directly bypasses every control.
- **Permissions hard-coded into role checks in code** - every new endpoint needs a deploy to wire authorisation; drift is guaranteed.
- **No expiry on temporary elevation** - the afternoon's billing_ops grant is still active a year later.
- **Same person initiates and approves** - separation of duties defeated; fraud invisible.
- **No MFA on privileged actions** - single credential compromise equals platform compromise.
- **No leaver revocation** - departed staff retain back-office access.
- **No periodic review** - permissions only ever accumulate; least privilege erodes to "everyone can do everything".

## See Also

- `saas-admin-backoffice-tooling` section 3 and section 7 - the role model and privileged-access workflow this expands.
- `references/impersonation-design.md` - which roles may impersonate, in which mode.
- `references/bulk-operations.md` - which roles may run which bulk class, and co-sign rules.
- `dual-auth-rbac` - the underlying RBAC and MFA primitives.
- `multi-tenant-saas-architecture` - customer-side RBAC, kept distinct from staff-side.
