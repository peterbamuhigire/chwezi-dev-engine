---
name: saas-admin-backoffice-tooling
description: Use when designing the internal admin / back-office console of a multi-tenant SaaS — tenant impersonation (audited, time-boxed), tenant lifecycle controls (suspend/restore/archive/hard-delete), billing operations (refunds, credits, plan overrides), feature-flag overrides per tenant, bulk actions (mass invite, plan migration, region migration), and the audit-log spine that backs all of it. Distinct from the customer-facing super-admin panel in `multi-tenant-saas-architecture`.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# SaaS Admin / Back-Office Tooling
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Designing the internal app that the SaaS provider's staff use to operate the platform — tenant ops, billing ops, support ops, compliance ops.
- Replacing SSH + ad-hoc SQL + Stripe Dashboard work with an audited, scriptable, role-based console.
- Adding tenant impersonation to a SaaS (so support can see what the tenant sees, audited and time-boxed).
- Building bulk operations (plan migration of a cohort, mass invite, region migration).
- Implementing the SOC2 / GDPR controls around privileged access.

## Do Not Use When

- The task is the customer-facing super-admin or tenant-admin panel (inside one tenant) — use `multi-tenant-saas-architecture` three-panel pattern.
- The task is the control-plane services architecture — use `saas-control-plane-engineering`; this skill is the UI/UX layer on top.
- The task is the audit log schema itself — use `saas-control-plane-engineering` §6.
- The task is general RBAC — use `dual-auth-rbac` and `multi-tenant-saas-architecture`.

## Required Inputs

- Control-plane service inventory from `saas-control-plane-engineering`.
- Audit log spec from `saas-control-plane-engineering`.
- Tenant lifecycle states from `saas-control-plane-engineering`.
- Compliance posture (SOC2, ISO27001, HIPAA?) — determines required guardrails.
- Internal roles (super admin, support engineer, billing ops, finance, security, customer success).

## Workflow

1. Read this `SKILL.md`.
2. Map the operations the back-office must support (§2) — tenant ops, billing ops, support ops, compliance ops.
3. Design the role model (§3) — internal staff roles + privileged-access controls.
4. Build the audited mutation pipeline (§4) — every action passes through guarded handlers.
5. Implement impersonation correctly (§5) — time-boxed, justified, audited, visible.
6. Build bulk operations safely (§6) — dry-run + idempotency + rate limit + rollback.
7. Apply the privileged-access workflow (§7) — break-glass, MFA, approval chains for high-risk actions.
8. Apply anti-patterns (§8).

## Quality Standards

- Every back-office mutation passes through a single audit-logging middleware. Direct DB writes from staff are forbidden in production.
- Every privileged action requires MFA for the staff user.
- Impersonation is time-boxed (default 30 minutes), justified (free-text required), and visible to the tenant (banner + email notification optionally).
- Bulk operations have a dry-run mode by default; production-mode requires a second approval.
- Every action emits an event to the audit log and to the staff-Slack channel (for transparency among the team).

## Anti-Patterns

- Staff doing tenant ops via SSH + `mysql` shell — no audit trail.
- Impersonation that masquerades silently — tenant has no idea their account was accessed.
- Refunds issued directly in Stripe Dashboard — diverges from internal records, no justification captured.
- "Admin can do anything" — no role separation; finance role shouldn't be able to delete tenants; support role shouldn't be able to refund.
- Bulk operations without dry-run — one bad query suspends 500 wrong tenants.
- Privileged actions without MFA — single password compromise = platform compromise.
- Feature-flag overrides per tenant scattered through code instead of in a single override table.

## Outputs

- Back-office app design (routes, role map, mutation handlers).
- Impersonation workflow + guardrails.
- Bulk operations playbook (dry-run + approval + rollback).
- Internal roles + permissions matrix.
- Audit-log integration spec.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Architecture | Back-office app spec | Markdown doc with routes + role map | `docs/saas/backoffice-app.md` |
| Security | Privileged-access workflow | Markdown doc | `docs/saas/privileged-access.md` |
| Operability | Bulk-operations playbook | Markdown doc | `docs/saas/bulk-ops-playbook.md` |

## References

- `references/impersonation-design.md` — time-boxed, justified, visible impersonation.
- `references/bulk-operations.md` — dry-run + approval + rollback patterns.
- `references/internal-roles-and-permissions.md` — typical role matrix.
- Companion: `saas-control-plane-engineering`, `multi-tenant-saas-architecture`, `dual-auth-rbac`, `vibe-security-skill`, `saas-sso-scim-enterprise-auth`.

<!-- dual-compat-end -->

## §1 Why the Back-Office Console Matters

Trio book: between $1M and $10M ARR, the manual-SSH-and-Stripe-Dashboard model collapses. Staff make mistakes; nothing is audited; customer trust erodes. The back-office console is **how operations becomes a discipline rather than a hero activity**.

For SOC2 and similar: every privileged access must be logged, justified, time-boxed, and traceable to a human. A console enforces this; a shell does not.

## §2 The Operations Surface

| Domain | Operations |
|---|---|
| **Tenant ops** | Search; view detail; suspend; restore; archive; hard-delete; transfer ownership; change plan/tier/region; toggle feature-flag overrides; impersonate |
| **User ops** | Search; view memberships; reset password; force logout; revoke sessions; un-suspend account; delete user (GDPR) |
| **Billing ops** | Issue refund; issue credit; apply discount; override plan price; change billing email; pause subscription; reactivate cancelled subscription |
| **Support ops** | View tickets; merge accounts; export tenant data on customer request; bulk re-invite team members; reset onboarding |
| **Compliance ops** | Initiate GDPR erasure; export audit log for tenant; sign DPA; record subprocessor change |
| **Bulk ops** | Plan-migration cohort; region-migration cohort; mass-suspend (e.g., fraud cluster); mass-email broadcast (rare, regulated) |

## §3 Internal Role Model

Don't have "is_super_admin" boolean. Have roles:

| Role | Can | Cannot |
|---|---|---|
| **support_l1** | Search, view, basic password reset, view tickets | Refund, suspend, impersonate |
| **support_l2** | + impersonate (with justification), suspend with reason, issue $50 credit | Hard delete, refund > $200 |
| **billing_ops** | Refund / credit / plan override / change billing email | Suspend / impersonate / delete |
| **engineering_oncall** | Feature-flag overrides, restart workers, replay events | Refund / billing changes |
| **security** | Force logout, revoke sessions, audit-log review, GDPR erasure | Refund / plan override |
| **super_admin** | Anything, but MFA + co-sign on highest-risk (hard delete, bulk-suspend) | — |

Each role's permissions live in a permissions table; the UI hides irrelevant controls; the API double-checks on every request.

## §4 The Audited Mutation Pipeline

Every back-office mutation passes through the same pipeline:
```
HTTP request → AuthN (staff session + MFA) → AuthZ (role + permission)
              → Captures: actor_user_id, actor_ip, justification (required for high-risk)
              → Idempotency check (Idempotency-Key header)
              → Begin DB transaction
              → Pre-state capture (before_state JSON)
              → Mutation
              → Post-state capture (after_state JSON)
              → Audit log INSERT (same transaction)
              → Commit
              → Emit event (Slack notification, downstream services)
```

A direct DB write that bypasses the pipeline is a **policy violation**, not just a bug.

## §5 Impersonation

The most-sensitive feature.

**Rules:**
- Requires high-trust role (support_l2, super_admin).
- Requires `justification` (free text, audited).
- Time-boxed (default 30 min, max 4 hours).
- Subject tenant sees a banner: "Support is currently viewing your workspace" (configurable per plan — enterprise often wants this visible).
- Optional notification email to tenant primary admin (configurable per plan).
- Impersonation start + end events in audit log.
- All actions during impersonation tagged with `acting_as_user_id`.

**Implementation pattern:**
```python
def start_impersonation(staff_user_id, target_user_id, justification, duration_min=30):
    require_role(staff_user_id, 'support_l2_or_above')
    require_mfa(staff_user_id)
    require_non_empty(justification)
    assert duration_min <= 240
    session = ImpersonationSession.create(
        staff_user_id=staff_user_id,
        target_user_id=target_user_id,
        justification=justification,
        expires_at=now() + duration_min * 60,
    )
    audit_log('IMPERSONATION_START', actor=staff_user_id, target=target_user_id,
              reason=justification, target_tenant=target_user.tenant_id)
    notify_target_tenant_admin(target_user_id)  # configurable
    return session_token
```

Every action while impersonation is active is double-stamped:
```
audit_log(actor=staff_user_id, acting_as=target_user_id, action='...', target_tenant_id=...)
```

## §6 Bulk Operations

Bulk operations are blast-radius nightmares. Pattern:

```
1. Staff selects cohort (SQL query, CSV upload, saved segment).
2. Dry-run runs the operation in a transaction-marked-readonly; produces a report (what would change, on how many tenants).
3. Staff reviews report; submits production-run with a second-approver MFA confirmation.
4. Production-run executes in batched chunks (e.g., 50 tenants per batch); pauseable; with progress reporting.
5. Per-tenant audit log entries.
6. Rollback snapshot — pre-state captured so undo is possible within N hours.
7. Slack broadcast at start, midpoint, completion.
```

Examples of safe bulk ops:
- Plan migration: "Move all `legacy_pro` to `pro_v2` with same price-locked Stripe Subscription."
- Region migration: "Move tenants in EU pod from `eu-west-1` to `eu-central-1`."
- Feature-flag rollout: "Enable `new_dashboard` for 10% of `pro` tenants."

Examples of dangerous bulk ops that need extra scrutiny:
- Mass-suspend (fraud cluster) — requires security sign-off + co-sign.
- Mass-delete — requires CEO/CFO sign-off + delay window.

## §7 Privileged-Access Workflow

| Action | Approval | MFA | Co-sign | Time-window |
|---|---|---|---|---|
| Login to back-office | MFA | Yes | No | Per session |
| View tenant | role | Yes | No | — |
| Suspend tenant | role | Yes | No | — |
| Impersonate | role | Yes | No | 30 min default |
| Refund < $100 | billing_ops | Yes | No | — |
| Refund $100-$1000 | billing_ops | Yes | Co-sign by another billing_ops | — |
| Refund > $1000 | billing_ops | Yes | Co-sign by finance lead | — |
| Hard-delete tenant | super_admin | Yes | Co-sign + 24h cooldown | — |
| Mass-suspend cohort | super_admin | Yes | Co-sign by security | — |

Co-sign mechanism: second staff user approves in the back-office UI within a time window; otherwise the action expires.

## §8 Anti-Patterns

- **`admin.html` page on the same app behind a JWT claim** — same auth surface, same code path, same risk; back-office should be a separate auth domain, separate deploy, separate network segment.
- **Impersonation invisible to tenant** — discovered later; trust catastrophe.
- **No co-sign on high-risk actions** — one bad day, one compromised laptop, platform compromised.
- **Justifications optional** — left blank by everyone; audit log is useless.
- **No internal Slack mirror of audit events** — team has no informal accountability layer.
- **Bulk ops without dry-run** — one bad SELECT kills 500 tenants.
- **Refunds via Stripe Dashboard** — bypasses platform record; ledger drift; tax-reporting headaches.
- **Same role for support and billing** — supports cancellation of others' accounts; supports cross-team mistakes.

## §9 Build Stack Suggestions

Depending on the SaaS stack:
- **Retool / Internal / Tooljet / Forest Admin / Appsmith** — fast to build, audit-friendly, role-based; great for $1M-$10M ARR stage.
- **Custom React/Vue app talking to control-plane APIs** — once team scales, custom gives the best UX and integration.
- **Django admin + customization** — works for Django stacks; needs extension for audit/impersonation/co-sign.
- **Laravel Nova / Filament** — same for Laravel/PHP stacks.

Regardless of UI tool, **the API surface is the contract** — UI is just one client; CLI / Slack-bot / scripts are equally valid clients of the back-office API.

## §10 Read Next

- `saas-control-plane-engineering` — the services this console drives.
- `multi-tenant-saas-architecture` — tenant data model + cross-tenant access rules.
- `subscription-billing` — billing operations this console invokes.
- `saas-tenant-data-portability-and-erasure` — GDPR workflows this console initiates.
- `dual-auth-rbac` — internal auth + MFA underpinning.
- `vibe-security-skill` — security baseline for the back-office app.
