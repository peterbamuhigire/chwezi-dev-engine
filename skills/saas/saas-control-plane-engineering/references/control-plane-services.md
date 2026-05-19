# Control Plane Services — Detailed Reference

The seven control-plane services, in depth.

## 1. Tenant Management

**Owns:** `tenants` table and tenant lifecycle. Single source of truth for what a tenant is, what plan it is on, what region it lives in, what status.

**API surface (v1):**
- `POST /admin/tenants` — create (called by onboarding orchestrator, not by signup form).
- `GET /admin/tenants/:id`, `GET /admin/tenants?filter=...` — read.
- `PATCH /admin/tenants/:id` — update plan, tier, metadata.
- `POST /admin/tenants/:id/suspend`, `/restore`, `/archive`, `/delete` — lifecycle transitions (each requires `justification`).
- `GET /admin/tenants/:id/status-history`.

**Authorisation:**
- Super-admin only for mutations.
- Tenant-admin can read its own tenant via the application plane's `/me/tenant` endpoint (separate API surface).

**Events emitted:**
- `tenant.created`, `tenant.activated`, `tenant.plan_changed`, `tenant.suspended`, `tenant.restored`, `tenant.archived`, `tenant.deleted`.

## 2. Identity Binding

**Owns:** `users`, `user_tenant_memberships`. Binds every authenticated identity to one or more tenants.

**Critical decisions:**
- One user across many tenants vs one user per tenant. Default: one user across many (matches Slack/GitHub/Linear behavior). Same email = same user.
- Cross-tenant identity: a user invited to a second tenant uses the same auth credentials.
- IdP-per-tenant (SAML/OIDC): each tenant's IdP creates a tenant-scoped user when the user first authenticates from that IdP. Email collisions resolved by claiming flow (verify ownership of email).

**Auth flow contract:**
- User authenticates → identity service issues a session/JWT with `user_id` only.
- User picks a tenant from their memberships → tenant-scoped JWT issued with `user_id`, `tenant_id`, `role`, `plan`, `entitlements`.
- All application-plane requests carry the tenant-scoped JWT.

**See:** `saas-sso-scim-enterprise-auth` for SAML/SCIM details.

## 3. Onboarding Orchestrator

**Owns:** The saga from signup form submission to active tenant.

See dedicated skill: `saas-tenant-onboarding-automation`.

## 4. Billing Customer Mirror

**Owns:** Local mirror of Stripe Customer + Subscription + Invoice state.

**Why mirror:** Stripe is the source of truth, but every page load can't call the Stripe API. The mirror is read-optimised for the platform. Mirror is **eventually consistent** with Stripe; reconciliation closes drift.

**Webhook ingest pattern:**
```
Stripe webhook → signed → enqueue to durable queue → consumer:
  1. Validate signature
  2. Idempotency check (event.id)
  3. Apply mutation to mirror
  4. Emit internal event for downstream (email, analytics, CRM)
  5. ACK
```

**Reconciliation:**
- Nightly: list all subscriptions in Stripe, diff against mirror. Surface drift on a dashboard. Alert if drift > 0.1%.
- See `subscription-billing/references/billing-reconciliation.md` (new ref this audit adds).

**Events emitted:**
- `billing.subscription_created`, `billing.subscription_upgraded`, `billing.subscription_downgraded`, `billing.subscription_cancelled`, `billing.payment_failed`, `billing.payment_succeeded`, `billing.invoice_created`.

## 5. Metrics Aggregator

**Owns:** Tenant-tagged usage rollups, business metrics (MRR/ARR/etc.), per-tenant cost attribution.

**Pattern:**
- Event bus (Kafka / Kinesis / SQS) carries every product event with `tenant_id`.
- Consumer materialises views in the warehouse (BigQuery / Snowflake / Postgres analytic schema).
- Pre-computed aggregates in `metrics_daily`, `metrics_monthly` tables.

**Output dashboards:**
- MRR / ARR / Net New MRR / Expansion / Contraction / Churn / NRR (see `saas-growth-metrics`).
- Per-tenant usage panel.
- Per-tenant cost attribution.
- Cohort retention curves.

## 6. Audit Log

**Owns:** Every privileged action against the system.

**What goes in:**
- Every super-admin mutation (tenant suspend, refund, plan override, feature-flag toggle).
- Every cross-tenant access by super-admin (read another tenant's data).
- Every impersonation start/stop.
- Every API key creation, rotation, revocation.
- Every tenant-admin action that modifies tenant-wide settings (member added, role changed, plan changed).
- Every authentication event (login success/failure, MFA, password reset).

**What doesn't go in:**
- Routine application reads (page views).
- Routine business writes (creating an invoice the customer is creating themselves).

**Retention:**
- Super-admin and privileged actions: 7 years (SOC 2 + tax).
- Authentication: 1 year (security baseline).
- System actions: 90 days hot, 2 years cold.

**Export:**
- Audit log API endpoint for customers (enterprise feature) to pull their own tenant's audit trail into their SIEM.

## 7. System Admin Console

**Owns:** The internal app for operating the SaaS.

See dedicated skill: `saas-admin-backoffice-tooling`.

---

## Cross-Service Patterns

### Event bus is the spine
All seven services communicate via events, not by direct API calls. This keeps the control plane loosely coupled and makes downstream integrations (email, analytics, CRM) cheap to add.

### Every service is API-first
The admin console is a thin UI over APIs. No business logic in the UI. Every operation can be scripted/automated.

### Everything writes audit
Every mutation writes an audit log entry, even when it's a system action (e.g., automated tenant suspension after 60 days inactive — audit it with `actor_type='system'`).

### Idempotency everywhere
Every control-plane API accepts an `Idempotency-Key` header; replays are safe. Critical for orchestrator retries and webhook reprocessing.
