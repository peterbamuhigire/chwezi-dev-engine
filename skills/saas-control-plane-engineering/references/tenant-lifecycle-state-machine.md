# Tenant Lifecycle State Machine — Reference

## States and meanings

| State | Meaning | Can users log in? | Data visible? | Recoverable? |
|---|---|---|---|---|
| `pending` | Onboarding saga in progress | No | No | Yes (auto-retry) |
| `failed` | Saga aborted | No | No | Yes (admin retry) |
| `ready` | Provisioned, awaiting first login | Yes (first time) | Yes | Yes |
| `active` | Normal operating state | Yes | Yes | — |
| `suspended` | Admin-paused (non-payment, abuse, support hold) | No | No (read-only optional) | Yes |
| `expired` | Trial ended without conversion | No (or limited) | Yes (read-only) | Yes (convert to paid) |
| `cancelled` | Customer-cancelled, in grace period | Yes (read-only) | Yes | Yes (un-cancel) |
| `archived` | Cold storage, customer departed | No | No | Yes (within retention) |
| `deleted` | Hard-deleted | No | No | No |

## Transition Matrix

```
                  ┌─ pending  ─► failed ─┐
                  │     │                │
   signup ────────┤     ▼                │
                  │   ready ─► active    │
                  │     │       │  ▲     │
                  │     │       │  └──── admin restore
                  │     │       ▼        │
                  │     │   suspended ◄──┘
                  │     │       │
                  │     │       ▼
                  │     ├──► expired (from active on trial end without conversion)
                  │     │
                  │     ├──► cancelled (from active on subscription.cancel)
                  │     │       │
                  │     │       ▼
                  │     └──► archived (from any non-pending state, admin or auto)
                  │             │
                  │             ▼
                  └────────► deleted (from archived after retention)
```

## Auto-Transition Triggers

| From → To | Trigger |
|---|---|
| `pending → ready` | Onboarding saga complete |
| `pending → failed` | Saga aborted after retries |
| `ready → active` | First user login |
| `active → expired` | Trial ended + no subscription created |
| `active → cancelled` | `customer.subscription.deleted` Stripe event |
| `cancelled → archived` | 30 days after cancellation (grace period elapsed) |
| `archived → deleted` | 90 days after archive (retention policy + GDPR sweep) |

Configurable per region/plan/customer — large enterprise customers might have a 365-day archive retention.

## Manual Transitions (Admin-Driven)

All require `justification` + write to audit log.

| From → To | Reason codes |
|---|---|
| `* → suspended` | `non_payment`, `abuse`, `legal_hold`, `support_investigation` |
| `suspended → active` | `payment_recovered`, `investigation_closed`, `legal_hold_lifted` |
| `cancelled → active` | `customer_un_cancel`, `csm_save` |
| `* → archived` | `customer_departed`, `policy_inactive_180d` |
| `archived → active` | `customer_return` |
| `archived → deleted` | `gdpr_erasure_request`, `retention_policy` |

## State-Aware UX

The application plane reads `tenants.status` to render:
- `pending`: spinner + "We're setting up your workspace…" page.
- `failed`: failure page + support link + retry button.
- `suspended`: blocked-tenant page with reason category (not full justification) + contact-support CTA.
- `expired`: paywall page + upgrade CTA.
- `cancelled`: read-only banner with "your subscription ends YYYY-MM-DD" + reactivate CTA.

## Data Handling Per State

| State | Reads allowed (app) | Writes allowed (app) | Backups continue? | Cost-attribution continues? |
|---|---|---|---|---|
| `active` | Yes | Yes | Yes | Yes |
| `suspended` | Optional read-only | No | Yes | Yes (reduced) |
| `expired` | Read-only | No | Yes | No |
| `cancelled` | Read-only | No | Yes | No |
| `archived` | No | No | No (move to cold) | No |
| `deleted` | No | No | Erased on next backup rotation | No |

## Persistence Pattern

`tenants.status` is the current state. `tenant_status_history` is the audit log of transitions. Status updates always run inside a transaction that writes both rows.

```sql
START TRANSACTION;

UPDATE tenants
   SET status = 'suspended', suspended_at = NOW()
 WHERE id = ?;

INSERT INTO tenant_status_history
       (tenant_id, from_status, to_status, actor_user_id, actor_type, reason_code, justification, occurred_at)
VALUES (?, 'active', 'suspended', ?, 'super_admin', ?, ?, NOW());

INSERT INTO audit_log
       (occurred_at, actor_user_id, actor_type, target_tenant_id, action, reason_code, justification)
VALUES (NOW(), ?, 'super_admin', ?, 'TENANT_SUSPEND', ?, ?);

COMMIT;
```

After commit, publish `tenant.suspended` event to the bus. Email service consumes → notifies tenant admins. Analytics → updates cohort. CS tool → opens task.

## Hard-Delete Pipeline

`archived → deleted` is the most dangerous transition. Must be carefully orchestrated:

1. Confirm tenant is in `archived` and `deletion_eligible_at <= NOW()`.
2. Generate final data-portability export, store in cold bucket, notify admin contact one last time (regulatory requirement in EU).
3. Begin **cascading erasure**:
   - Application-plane databases — per-tenant tables purged (or RLS-scoped DELETE).
   - File storage — per-tenant objects deleted.
   - Search index — per-tenant docs removed.
   - Cache — per-tenant keys flushed.
   - Email suppression list — entries marked GDPR-deleted.
   - Audit log — **kept** (legal/SOC2 requires retention), but PII redacted (replace email with `<deleted-tenant-{id}>`).
   - Backups — flagged for redaction on next rotation; document the retention policy publicly.
   - Warehouse — tenant data anonymised (replace identifiers with hashes).
4. Update `tenants.status = 'deleted'`, `tenants.deleted_at = NOW()`.
5. Emit `tenant.deleted` event for any remaining downstream cleanup (CRM, analytics, billing).

See `saas-tenant-data-portability-and-erasure` for the cascade details.
