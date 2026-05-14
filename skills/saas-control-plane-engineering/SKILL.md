---
name: saas-control-plane-engineering
description: Use when building the control plane of a multi-tenant SaaS — the cross-cutting services (tenant management, identity binding, onboarding orchestration, metrics aggregation, billing customer mirror, audit log, system admin console) that operate every tenant through a single pane of glass. Distinct from `multi-tenant-saas-architecture` (tenant isolation patterns) and `modular-saas-architecture` (pluggable modules per tenant).
metadata:
  portable: true
  compatible_with:
  - Codex
  - codex
---

# SaaS Control Plane Engineering
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Designing the cross-cutting services of a multi-tenant SaaS — the **control plane** that orchestrates tenants, identity, billing customer, metrics aggregation, audit log, and the internal admin console.
- Auditing an existing SaaS where tenant lifecycle, onboarding, suspension, and admin operations are scattered through the app and unowned.
- Splitting a SaaS into application-plane services (features) versus control-plane services (operations) so that releases, scaling, and ownership are clean.
- Replacing manual ops (SSH, ad-hoc SQL, founder triage) with a deliberate set of platform services as the SaaS crosses the $1M ARR threshold.

## Do Not Use When

- The task is per-tenant isolation enforcement at the data/query layer — use `multi-tenant-saas-architecture`.
- The task is composing pluggable business modules per tenant — use `modular-saas-architecture`.
- The task is the Stripe Billing lifecycle itself — use `subscription-billing` and `stripe-payments`.
- The task is the customer-facing admin panel inside one tenant — use `multi-tenant-saas-architecture` three-panel section.

## Required Inputs

- Tenancy model and deployment model from `multi-tenant-saas-architecture` and `saas-deployment-models`.
- Plan / tier catalogue + lifecycle policy from `subscription-billing`.
- Identity provider choice (Cognito, Auth0, Keycloak, Clerk, custom) and per-tenant IdP plans from `saas-sso-scim-enterprise-auth`.
- The SaaS Maturity Matrix target ARR band — determines which control-plane services ship in v1 vs v2.

## Workflow

1. Read this `SKILL.md` end-to-end before writing code or designing schemas.
2. Map your SaaS to the seven control-plane services (§2) — for each, mark `v1 / v2 / v3 / not-needed`.
3. Design the tenant lifecycle state machine (§3) and persist it as data (`tenants.status` + `tenants.status_history`).
4. Define the canonical tenant model + identity binding (§4) — `tenants`, `users`, `user_tenant_memberships`, `tenant_billing`.
5. Build the onboarding orchestrator (§5) — see `saas-tenant-onboarding-automation` for the saga and compensations.
6. Wire the metrics aggregator + audit log (§6) so every control-plane action is observable and reversible-or-justified.
7. Stand up the system admin console (§7) — see `saas-admin-backoffice-tooling`.
8. Apply the anti-pattern checklist (§9).

## Quality Standards

- Control plane is a **separate deployment** from the application plane (different release cadence, different on-call, different SLA).
- Every control-plane mutation writes an audit log entry with actor, target tenant, action, justification, before/after.
- The control plane is **fully API-driven** — the admin console is just a UI on top of those APIs. Never embed business logic only in the UI layer.
- Tenant state changes are **events** published to the bus, not just row updates. Downstream services (email, analytics, CRM sync) consume them.
- Idempotency on every control-plane mutation (request-id header → idempotency key persisted).

## Anti-Patterns

- Building a tenant admin feature in the application plane that touches another tenant's data (it now belongs in the control plane).
- Onboarding implemented as a 300-line controller method instead of an orchestrated state machine.
- Tenant lifecycle states stored as boolean flags (`is_active`, `is_archived`, `is_suspended`) instead of a single `status` enum + `status_history`.
- No audit log on super-admin actions, so every cross-tenant operation is unaccountable.
- Control-plane services deployed in the same process/release as application-plane services, so a feature release blocks an ops fix.

## Outputs

- Control-plane service inventory mapped to v1/v2/v3.
- Canonical tenant + user + membership + billing-customer schema.
- Tenant lifecycle state machine and status_history.
- Onboarding orchestrator design (handed off to `saas-tenant-onboarding-automation`).
- Audit log schema and retention policy.
- System admin console API + UI plan (handed off to `saas-admin-backoffice-tooling`).

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Architecture | Control-plane service inventory | Markdown doc with v1/v2/v3 columns | `docs/saas/control-plane-services.md` |
| Data safety | Tenant lifecycle state machine | Markdown doc with states, transitions, persistence schema | `docs/saas/tenant-lifecycle.md` |
| Security | Audit-log spec | Markdown doc with event taxonomy, schema, retention | `docs/saas/audit-log-spec.md` |

## References

- `references/control-plane-services.md` — seven services in detail.
- `references/tenant-lifecycle-state-machine.md` — states, transitions, persistence.
- `references/audit-log-design.md` — taxonomy, schema, retention.
- Companion: `saas-tenant-onboarding-automation`, `saas-admin-backoffice-tooling`, `multi-tenant-saas-architecture`, `subscription-billing`, `saas-sso-scim-enterprise-auth`.

<!-- dual-compat-end -->

## §1 Why the Control Plane Exists

Golding's defining frame: every SaaS is two halves.

- **Application plane** — features customers use; multi-tenant at runtime; per-team release cadence.
- **Control plane** — services the SaaS provider uses to operate every tenant; not multi-tenant in capability; release cadence driven by ops needs.

If you skip the control plane, you regress to MSP — every new tenant becomes a one-off and the founder is in every ticket. **Build the control plane first, even minimally.** It is the forcing function that makes the rest of the system tenancy-aware.

## §2 The Seven Control-Plane Services

| # | Service | Owns | Minimum v1 surface |
|---|---|---|---|
| 1 | **Tenant Management** | `tenants` table, lifecycle state, plan, metadata | CRUD API + admin UI |
| 2 | **Identity Binding** | user ↔ tenant memberships, roles, auth realm bootstrap | Signup → user + tenant + first admin user |
| 3 | **Onboarding Orchestrator** | the saga from signup to ready tenant | State machine; see companion skill |
| 4 | **Billing Customer Mirror** | mirror of Stripe Customer/Subscription/Price | Webhook ingest + reconciliation |
| 5 | **Metrics Aggregator** | tenant-tagged usage, MRR/ARR/NRR/churn rollups | Event bus consumer → warehouse views |
| 6 | **Audit Log** | every control-plane mutation, every cross-tenant access | Append-only ledger + retention policy |
| 7 | **System Admin Console** | the UI provider staff use to operate the SaaS | Admin app + APIs + RBAC + audit |

`v1` for an early-stage SaaS: services 1, 2, 3, 4, 6, 7 in minimal form. Service 5 (metrics aggregator) often starts as Stripe + ad-hoc SQL and graduates to a warehouse in v2.

## §3 Tenant Lifecycle State Machine

```
                signup
                  │
                  ▼
       ┌──────► PENDING (provisioning in progress)
       │          │
       │          ├── failure ──► FAILED  (retriable, observable)
       │          ▼
       │        READY (default) ──► ACTIVE on first login
       │          │
       │          ├── admin suspend ──► SUSPENDED (data preserved, no access)
       │          ▼
       │        ACTIVE
       │          │
       │          ├── trial expire   ──► EXPIRED (read-only or upgrade-only)
       │          ├── subscription cancel ──► CANCELLED (grace period)
       │          ├── admin archive  ──► ARCHIVED (cold, recoverable for N days)
       │          ▼
       │        DELETED (hard delete, irreversible)
       └──── (admin restore from SUSPENDED/ARCHIVED)
```

**Persistence pattern:**
```sql
CREATE TABLE tenants (
    id              BIGINT UNSIGNED PRIMARY KEY,
    slug            VARCHAR(64) NOT NULL UNIQUE,
    name            VARCHAR(255) NOT NULL,
    status          ENUM('pending','failed','ready','active','suspended','expired','cancelled','archived','deleted') NOT NULL,
    plan            VARCHAR(64),
    tier            VARCHAR(64),
    created_at      DATETIME NOT NULL,
    activated_at    DATETIME,
    suspended_at    DATETIME,
    deleted_at      DATETIME,
    deletion_eligible_at DATETIME,  -- earliest date at which hard-delete can run
    region          VARCHAR(32),    -- data residency
    metadata        JSON,
    INDEX idx_status (status),
    INDEX idx_plan (plan)
);

CREATE TABLE tenant_status_history (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tenant_id       BIGINT UNSIGNED NOT NULL,
    from_status     VARCHAR(32),
    to_status       VARCHAR(32) NOT NULL,
    actor_user_id   BIGINT UNSIGNED,
    actor_type      ENUM('system','super_admin','tenant_admin','customer'),
    reason_code     VARCHAR(64),
    justification   TEXT,
    occurred_at     DATETIME NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    INDEX idx_tenant_time (tenant_id, occurred_at)
);
```

## §4 Canonical Schema

```sql
CREATE TABLE users (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    name            VARCHAR(255),
    auth_provider   VARCHAR(64),  -- 'password', 'google', 'saml', 'oidc'
    auth_subject    VARCHAR(255), -- IdP subject identifier
    super_admin     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      DATETIME NOT NULL,
    INDEX idx_provider_subject (auth_provider, auth_subject)
);

CREATE TABLE user_tenant_memberships (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         BIGINT UNSIGNED NOT NULL,
    tenant_id       BIGINT UNSIGNED NOT NULL,
    role            VARCHAR(64) NOT NULL,    -- owner, admin, member, billing
    invited_at      DATETIME,
    joined_at       DATETIME,
    revoked_at      DATETIME,
    UNIQUE KEY uq_user_tenant (user_id, tenant_id),
    INDEX idx_tenant (tenant_id)
);

CREATE TABLE tenant_billing (
    tenant_id              BIGINT UNSIGNED PRIMARY KEY,
    stripe_customer_id     VARCHAR(64) UNIQUE,
    stripe_subscription_id VARCHAR(64),
    plan                   VARCHAR(64),
    status                 VARCHAR(32),
    current_period_end     DATETIME,
    trial_end              DATETIME,
    mrr_usd                DECIMAL(10,2),
    currency               CHAR(3),
    metadata               JSON,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);
```

## §5 Onboarding Orchestrator (hand-off)

The onboarding service is the most failure-prone path in any SaaS. It owns the saga that takes a signup form submission to a usable tenant in seconds. Details, including the saga + compensation pattern, idempotency, retries, and observability, are in `saas-tenant-onboarding-automation`.

Minimum responsibilities of the orchestrator inside the control plane:
- Accept signup request, return `pending` tenant immediately.
- Run the saga: create tenant → create identity realm/admin user → provision infra (silo) or register (pool) → create Stripe customer + trial subscription → seed defaults → send welcome email → emit `tenant.activated` event.
- On any step failure: persist `failed` state, fire alert, expose retry endpoint.
- All steps idempotent; rerunning the saga is safe.

## §6 Metrics Aggregator + Audit Log

Two telemetry surfaces every control plane owns:

### Business metrics aggregator
Consumes the event bus (billing events, usage events, lifecycle events) and produces:
- Daily MRR / ARR / Net New MRR / Expansion / Contraction / Churn rollups.
- Per-tenant usage rollups (sessions, API calls, active users, storage bytes).
- Cohort views (signup-month × plan × channel).
- Per-tenant cost attribution (silo: cloud bill; pool: apportioned).

### Audit log
**Every control-plane mutation** writes an entry. Schema:
```sql
CREATE TABLE audit_log (
    id               BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    occurred_at      DATETIME(6) NOT NULL,
    actor_user_id    BIGINT UNSIGNED,
    actor_type       ENUM('super_admin','tenant_admin','system','customer','api_key'),
    actor_ip         VARCHAR(45),
    target_tenant_id BIGINT UNSIGNED,
    target_resource  VARCHAR(128),
    target_id        VARCHAR(64),
    action           VARCHAR(128) NOT NULL,
    reason_code      VARCHAR(64),
    justification    TEXT,
    before_state     JSON,
    after_state      JSON,
    request_id       VARCHAR(64),
    INDEX idx_target_tenant_time (target_tenant_id, occurred_at),
    INDEX idx_actor_time (actor_user_id, occurred_at),
    INDEX idx_action_time (action, occurred_at)
);
```

Retention: 7 years for super-admin actions, 2 years for system actions. Export to cold storage after 12 months hot.

## §7 System Admin Console (hand-off)

The internal app the SaaS provider's staff use. See `saas-admin-backoffice-tooling`. Minimum capabilities:
- Search tenants by name / slug / email of any member.
- View tenant detail (status, plan, MRR, key metrics, recent activity).
- Mutate tenant lifecycle (suspend, restore, archive, hard-delete) with justification.
- Impersonate tenant user (audited, time-boxed).
- Issue billing adjustments (refund, credit, plan override) with justification.
- Toggle feature flags per tenant.
- Bulk operations (mass invite, plan migration, region migration).

## §8 Deployment & Ownership

- Control plane is a **separate service / deployment / repo subdir** from the application plane.
- Different on-call rotation — control plane is ops-team, application plane is feature-team.
- Different SLA — control plane is 99.95% (any outage stops onboarding, billing, support); application plane SLA can be lower.
- Control plane changes pass through a stricter review (every change touches every tenant indirectly).

## §9 Anti-Patterns

- **No control plane at all.** Every cross-tenant operation lives in the application code as a `if user.is_super_admin` branch. Fix: extract into a dedicated service with its own auth domain.
- **Tenant status as booleans.** `is_active`, `is_suspended`, `is_archived` allows nonsense combinations. Fix: single `status` enum + `status_history` table.
- **No audit log.** Cannot answer "who suspended this tenant and why" 60 days later. Fix: every mutation writes an entry; retention ≥ 2 years.
- **Onboarding inline in the signup controller.** No retry, no observability, partial failures leave half-tenants. Fix: dedicated orchestrator service + saga.
- **No reconciliation of billing mirror.** Stripe state drifts from the local mirror within weeks. Fix: nightly diff job with alerting.
- **Super-admin actions execute without justification.** No ability to defend ops actions in a SOC2 audit. Fix: mandatory `justification` field on every privileged mutation.

## §10 Read Next

- `saas-tenant-onboarding-automation` — the onboarding orchestrator.
- `saas-admin-backoffice-tooling` — the system admin console.
- `multi-tenant-saas-architecture` — tenant isolation at the application plane.
- `subscription-billing` — the billing lifecycle the control plane mirrors.
- `saas-deployment-models` — choosing silo/pool/mixed/pod.

## AI Control-Plane Services Addendum

The seven core control-plane services in this skill (tenant management, identity binding, onboarding orchestrator, billing customer mirror, entitlements, signup intake, support back-office) are joined by **five AI control-plane services** when the SaaS ships AI features:

| # | Service | Purpose | Skill |
|---|---|---|---|
| 8 | LLM Gateway | provider abstraction, model selection per tier, fallback, per-tenant rate limit + caps, audit, cost capture | `ai-model-gateway` |
| 9 | Prompt Registry | versioned prompts, per-tenant pinning, A/B variants, rollback | `ai-on-saas-architecture` §3 |
| 10 | Knowledge-Base Service | per-tenant ingestion, chunking, embedding, vector storage, retrieval | `ai-rag-multi-tenant` |
| 11 | Eval Harness | golden datasets, prompt regression, judge runs, CI gate, drift detection | `ai-eval-harness` |
| 12 | AI Audit Log | append-only ledger of every prompt, model, retrieval, output, cost, decision | `ai-observability-and-debugging` |

Treat these like the other control-plane services: separate deployment, separate on-call, stricter SLA. See `ai-on-saas-architecture` for the unifying view.

Cross-references:
- `ai-on-saas-architecture`
- `ai-model-gateway`
- `ai-rag-multi-tenant`
- `ai-eval-harness`
- `ai-cost-per-tenant-attribution`
- `ai-prompt-injection-and-tenant-safety`
- `ai-observability-and-debugging`
