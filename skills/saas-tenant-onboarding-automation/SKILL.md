---
name: saas-tenant-onboarding-automation
description: Use when designing and implementing the tenant onboarding state machine — the orchestrated saga from signup to ready tenant (identity provisioning, infra allocation, billing customer creation, default seeding, welcome email, activation telemetry). Includes saga patterns, compensations, idempotency, retries, and observability. Companion to `saas-control-plane-engineering`.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# SaaS Tenant Onboarding Automation
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Designing the onboarding pipeline of a multi-tenant SaaS — sub-60-second self-serve provisioning from form submission to a usable tenant.
- Replacing a manual / partial / fragile onboarding flow (the founder is in every signup) with an idempotent orchestrated saga.
- Adding per-tenant infrastructure provisioning (silo / pod) to an existing onboarding pipeline without sacrificing onboarding time-to-ready.
- Designing the failed-onboarding recovery story — observability, retries, compensations, support escalation.

## Do Not Use When

- The task is general saga design — use `distributed-systems-patterns` for the underlying pattern.
- The task is the full control plane — use `saas-control-plane-engineering`; this skill is one of its services.
- The task is configuring Stripe Customer/Subscription primitives — use `subscription-billing`; this skill calls those primitives.
- The task is in-product activation / aha-event design — use `product-led-growth`; this skill ends at "tenant active", PLG starts at "drive to activation".

## Required Inputs

- Tenancy model from `multi-tenant-saas-architecture` (silo vs pool determines provisioning workload).
- Plan catalogue + trial policy from `subscription-billing`.
- Identity model from `saas-control-plane-engineering`.
- Email infra from `saas-transactional-email-infrastructure`.
- Default seed data (catalogue, roles, sample records) from product requirements.

## Workflow

1. Read this `SKILL.md`. Load `distributed-systems-patterns` if you need the saga underpinnings.
2. Map your tenant's provisioning to the 7 onboarding steps (§2) — for each, decide synchronous vs async.
3. Choose the saga style (§3) — orchestrated (Temporal / Step Functions / custom state machine) vs choreographed (event chain).
4. Define each step's idempotency key, retry policy, and compensation (§4).
5. Define observability — every step emits start/end/duration with `correlation_id` and `tenant_id` (§5).
6. Wire failure modes — partial failures → `failed` state, alert, retry endpoint (§6).
7. Instrument the activation funnel — `signup`, `pending → ready`, `first_login`, `aha_event`, `activated` (§7).
8. Apply anti-pattern checklist (§9).

## Quality Standards

- Median signup-to-ready < 30 seconds for pool model; < 5 minutes for silo with provisioning.
- p99 signup-to-ready < 2 minutes for pool model; < 15 minutes for silo.
- Failed-onboarding rate < 0.5%. Every failure is observable and retriable.
- Saga is **idempotent end-to-end** — rerunning with the same idempotency key is safe.
- Every step writes structured logs with `correlation_id`, `tenant_id`, `step_name`, `duration_ms`, `status`.

## Anti-Patterns

- Onboarding implemented as a 300-line `signupController.create()` method with no state, no retry, no observability.
- Sending the welcome email before the tenant is actually usable.
- Stripe customer created but tenant infrastructure provisioning then fails; result is a Stripe customer with no tenant, never reconciled.
- No `correlation_id` propagated through steps; debugging requires log archaeology.
- Synchronous waiting on slow steps (e.g., DNS propagation for custom subdomain) so the UI hangs; should be async with status polling.
- No compensation defined for partial failures (orphaned Stripe customers, leaked IdP users).

## Outputs

- Onboarding saga design — steps, dependencies, sync/async breakdown.
- Idempotency key strategy + retry/backoff policy per step.
- Compensation matrix (step X failed → undo Y and Z).
- Observability spec — events emitted, dashboards, alerts.
- Activation funnel events for downstream consumption (email automation, analytics).

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Architecture | Onboarding saga spec | Markdown doc with steps, retries, compensations | `docs/saas/onboarding-saga.md` |
| Operability | Onboarding observability spec | Markdown doc + dashboard link | `docs/saas/onboarding-observability.md` |
| Release evidence | Activation funnel baseline | Markdown doc with step-by-step conversion rates | `docs/saas/activation-funnel-baseline.md` |

## References

- `references/onboarding-saga-patterns.md` — orchestrated vs choreographed; engine choice (Temporal / SQS-saga / DB-state-machine).
- `references/onboarding-compensations.md` — per-step compensation actions.
- Companion: `saas-control-plane-engineering`, `subscription-billing`, `saas-transactional-email-infrastructure`, `product-led-growth`, `distributed-systems-patterns`.

<!-- dual-compat-end -->

## §1 Why Onboarding Is The Most Important Flow

Onboarding is the front door. Every other flow is downstream of it. Get it wrong and:
- Time-to-value stretches; activation suffers; trial-to-paid drops.
- Half-provisioned tenants pollute the database forever.
- Stripe customers without tenants accumulate; reconciliation becomes a nightmare.
- Failed onboarding silently fails; support gets the angry tickets days later.

The Trio book treats onboarding automation as **the single graduation requirement** between $1M and $10M ARR. The earlier you build it correctly, the cheaper your scale.

## §2 The Seven Onboarding Steps

| # | Step | Sync/Async (pool) | Sync/Async (silo) | Can fail? |
|---|---|---|---|---|
| 1 | Create tenant record (status `pending`) | Sync | Sync | Rarely (DB issue) |
| 2 | Bootstrap identity (auth realm or just create first user) | Sync | Sync | Yes (email collision, IdP outage) |
| 3 | Provision infrastructure | n/a (skip) | **Async** (mins) | Yes (cloud quota, IaC failure) |
| 4 | Create billing customer + start trial subscription | Sync | Sync | Yes (Stripe outage, declined card) |
| 5 | Seed default data (catalogue, roles, sample records) | Sync | Async | Rarely |
| 6 | Send welcome email + magic-link / verification | Async | Async | Rarely (ESP queueing) |
| 7 | Emit activation telemetry, flip tenant to `ready` | Sync | Sync | Rarely |

**Pool model:** all sync steps complete within ~2-5 seconds; user sees the workspace immediately.

**Silo model:** sync steps complete in ~2 seconds → return "Setting up your workspace, we'll email you when it's ready" → async provisioning takes minutes → completion email + redirect.

## §3 Saga Style Choice

### Orchestrated (recommended for SaaS)
A central orchestrator service drives the sequence, knows the state, handles retries and compensations.

**Engines:**
- **Temporal** / **Cadence** — purpose-built, durable, retries built-in. Best for silo (long-running provisioning).
- **AWS Step Functions** — managed; good if already on AWS.
- **n8n / Airflow** — workflow tools; lighter weight; fine for v1.
- **Custom DB-state-machine** — a `onboarding_runs` table with `current_step`, `status`, `retry_count`, polled by a worker. Simplest; fine for pool with sub-second steps.

### Choreographed (event chain)
Each step listens for the prior step's event, runs, emits the next event. No central orchestrator.

**Pros:** loose coupling, scales horizontally.
**Cons:** state is implicit (which event last fired?), retries hard, compensations require reverse-event chain. Hard to reason about.

**Default choice for SaaS:** orchestrated. Onboarding is short-lived and benefits from a single source of truth for state.

## §4 Per-Step Idempotency, Retry, Compensation

```
Step: Create Stripe Customer
  Idempotency key: stripe-customer-{onboarding_run_id}
  Retry: 3x with exponential backoff (200ms, 1s, 5s)
  Compensation: delete Stripe customer (if next steps fail)
  Stripe API native idempotency: Idempotency-Key header

Step: Provision Infrastructure (silo)
  Idempotency key: infra-{tenant_id}
  Retry: 5x with exponential backoff (5s, 30s, 2m, 10m, 30m)
  Compensation: terraform destroy / cloud delete
  Surface as 'provisioning' status to UI; poll for ready

Step: Bootstrap Identity
  Idempotency key: identity-{tenant_id}
  Retry: 3x
  Compensation: delete IdP user / realm
  Atomic with: create first user_tenant_membership row

Step: Seed Defaults
  Idempotency key: seed-{tenant_id}-{seed_version}
  Retry: 3x
  Compensation: truncate tenant tables (only if tenant is still in pending state)

Step: Send Welcome Email
  Idempotency key: welcome-{tenant_id}
  Retry: handled by ESP queue
  Compensation: (none — emails are non-critical for ready state)

Step: Flip to Ready + Emit tenant.created
  Idempotency key: flip-{tenant_id}
  Retry: 3x
  Compensation: (none — terminal step)
```

## §5 Observability

Every step emits:
```json
{
  "event": "onboarding.step.completed",
  "correlation_id": "ob_2026_05_11_abc123",
  "tenant_id": 12345,
  "step": "stripe_customer_create",
  "status": "ok",
  "duration_ms": 423,
  "retry_count": 0,
  "actor_user_id": 678,
  "ip_address": "203.0.113.1",
  "user_agent": "..."
}
```

Dashboards:
- **Onboarding funnel:** signups → step1 → step2 → … → ready. Conversion at each step.
- **Onboarding latency:** p50 / p95 / p99 per step + total.
- **Onboarding failures:** by step, by error code, count + rate.
- **Failed onboardings retry queue:** tenants in `failed` state, retry attempts, age.

Alerts:
- Onboarding failure rate > 1% in 5-min window.
- Onboarding p95 > 60s (pool) or > 10min (silo).
- Stripe step failure rate > 2% in 5-min window (indicates Stripe outage or pricing config drift).

## §6 Failure Recovery

**State during failure:** `tenants.status = 'failed'`, `onboarding_runs.status = 'failed'`, `failed_step` recorded.

**Recovery options:**
1. **Auto-retry** — orchestrator retries with backoff. If exhausted, escalate.
2. **Admin retry** — admin console exposes a "Retry onboarding" button on failed tenants. Submits the saga with the same idempotency keys (so completed steps short-circuit).
3. **Admin manual repair** — if auto-retry can't recover (e.g., misconfigured plan), admin fixes the underlying issue then retries.
4. **Hard abort** — admin marks failed run as abandoned; saga runs compensations to clean up; tenant deleted from DB.

## §7 Activation Funnel — Where Onboarding Hands Off

Onboarding ends at `tenant.ready`. PLG begins at `tenant.first_login`. The handoff is the **activation funnel**:

```
signup → pending → ready → first_login → first_action → first_value (aha) → activated → engaged → retained
   │        │       │         │             │              │                  │            │           │
   │        │       │         │             │              │                  │            │           └── d+30 still active
   │        │       │         │             │              │                  │            └── d+7 still active
   │        │       │         │             │              │                  └── product-defined activation event
   │        │       │         │             │              └── "aha moment" — first time core value experienced
   │        │       │         │             └── any meaningful action (create, invite, upload)
   │        │       │         └── magic-link clicked or password set
   │        │       └── onboarding saga complete
   │        └── saga started
   └── form submitted
```

Every transition is an event. PLG + lifecycle email engine + analytics all subscribe.

## §8 The Asynchronous-Silo Pattern

When silo provisioning takes minutes, UX must not block. Pattern:

```
1. Submit form
2. Sync: create tenant row (status pending), create Stripe customer, create first user
3. Redirect to /onboarding/status?tenant=abc
4. Async: provisioning runs in background
5. /onboarding/status polls or uses WebSocket; shows "Setting up your environment..."
6. On completion: status flips to ready, page redirects to dashboard, email sent
```

Or: skip the wait page entirely — let the user explore a "minimal" pooled environment immediately; provision the silo in the background; transparently switch when ready.

## §9 Anti-Patterns

- **No `correlation_id`.** Cannot trace one onboarding's path through services. Fix: generate at form submit; propagate everywhere.
- **Welcome email sent before tenant is `ready`.** User clicks the link → 404 or blank workspace. Fix: send email after `tenant.ready` event.
- **Stripe customer created → infra step fails → no cleanup.** Stripe accumulates orphan customers. Fix: compensation deletes Stripe customer.
- **No idempotency keys.** Retry creates duplicate Stripe customers, duplicate users. Fix: `Idempotency-Key` header on every external call; persist them.
- **Saga state in app memory.** Worker dies mid-saga, state lost. Fix: persist `onboarding_runs.current_step` and `status` in DB.
- **No retry endpoint.** Failed onboardings are dead; manual SQL surgery. Fix: admin console "Retry" button.
- **Seed data hard-coded in app code instead of versioned.** Updating defaults retroactively breaks old tenants. Fix: seed-version per tenant; idempotent re-seed only safe for the same version.
- **Onboarding latency unmonitored.** Slow onboarding silently kills conversion. Fix: dashboard + alert on p95.

## §10 Sample DB-State-Machine Implementation

```sql
CREATE TABLE onboarding_runs (
    id                   BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    correlation_id       VARCHAR(64) NOT NULL UNIQUE,
    tenant_id            BIGINT UNSIGNED,
    initiator_email      VARCHAR(255) NOT NULL,
    initiator_ip         VARCHAR(45),
    status               ENUM('running','succeeded','failed','abandoned') NOT NULL,
    current_step         VARCHAR(64),
    failed_step          VARCHAR(64),
    failed_reason        TEXT,
    retry_count          INT NOT NULL DEFAULT 0,
    started_at           DATETIME NOT NULL,
    completed_at         DATETIME,
    payload              JSON NOT NULL,    -- the signup form data
    step_state           JSON,             -- per-step idempotency keys + outputs
    INDEX idx_status     (status),
    INDEX idx_started    (started_at)
);
```

Worker loop:
```python
while True:
    run = db.fetch_pending_run()    # SELECT ... FOR UPDATE SKIP LOCKED
    if not run: time.sleep(1); continue
    try:
        execute_next_step(run)      # advances current_step; persists step_state
    except RetryableError as e:
        run.retry_count += 1
        if run.retry_count >= MAX_RETRIES:
            fail_run(run, e)
            alert(run)
        else:
            schedule_retry(run, backoff(run.retry_count))
    except FatalError as e:
        fail_run(run, e)
        run_compensations(run)
        alert(run)
```

## §11 Read Next

- `saas-control-plane-engineering` — the parent context.
- `distributed-systems-patterns` — saga theory + compensation patterns.
- `subscription-billing` — Stripe Customer/Subscription primitives this skill orchestrates.
- `saas-transactional-email-infrastructure` — welcome email infrastructure.
- `product-led-growth` — activation funnel definition + measurement.
- `saas-admin-backoffice-tooling` — admin retry / abandon UI.
