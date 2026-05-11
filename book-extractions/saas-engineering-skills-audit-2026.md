# SaaS Engineering Skills Audit — May 2026
**Lens:** Production SaaS build engine — multi-tenant architecture, billing, growth-eng, mobile SaaS, lifecycle infra, sales-assist features.
**Inputs:** Extractions of (1) Golding *Building Multi-Tenant SaaS Architectures*, (2) Mersch *Hacking SaaS*, (3) *How to Run a SaaS Business*, (4) Walling *The SaaS Playbook*, (5) Garbugli *The SaaS Email Marketing Playbook*, (6) WBD *The SaaS Sales Method for AEs*, (7) WBD *The SaaS Sales Method Fundamentals*.

## Current Coverage Snapshot

The engine has **~265 skills** with strong coverage of:
- Multi-tenant + modular SaaS architecture (`multi-tenant-saas-architecture`, `modular-saas-architecture`, `saas-architecture-strategy`)
- Subscription billing & Stripe (`subscription-billing`, `stripe-payments`, `saas-subscription-mastery`, `ai-saas-billing`, `ai-metering-billing`)
- K8s SaaS delivery (`kubernetes-saas-delivery`)
- Growth telemetry / PLG / experimentation (`growth-telemetry-pipeline`, `product-led-growth`, `experiment-engineering`, `saas-growth-metrics`)
- iOS monetization (`ios-monetization` — StoreKit2)
- Email **templates** (`tabler-email-templates` — 80 HTML templates)
- Auth (`dual-auth-rbac`)
- Sales business (`saas-sales-organization`)

## Critical Gaps the Books Reveal

| # | Gap | Source | Severity |
|---|---|---|---|
| 1 | Operationalized control-plane & onboarding-engine engineering | Golding Ch.2, 4, 5 | High |
| 2 | Silo / pool / pod / mixed-mode deployment patterns with IaC | Golding Ch.3 | High |
| 3 | Tenant-aware observability + cost-per-tenant attribution | Golding Ch.14 + Trio | High |
| 4 | Entitlements & plan-gating engine engineering | Walling pricing, Golding, Mersch | High |
| 5 | Transactional + lifecycle email **infrastructure** (deliverability, ESP, suppression, event-bridge) — **distinct from email templates** | Garbugli all chapters | High |
| 6 | Lifecycle email orchestration engine (six sequences, branched automation) | Garbugli Ch.41-46 | High |
| 7 | SaaS internal admin / back-office tooling (impersonation, refunds, tenant ops) | Trio Ch.4-5, Golding | High |
| 8 | Enterprise auth: SSO/SAML + SCIM + IdP-per-tenant + custom-domain | Mersch Ch.7, AE book | High |
| 9 | Android Play Billing / Google Play subscriptions (counterpart to ios-monetization) | Mersch Ch.13, B2C | Med |
| 10 | Server-side cross-platform entitlement reconciliation (web + iOS + Android) | Mersch | Med |
| 11 | GDPR/POPIA tenant data export + erasure workflow engineering | Trio, regulated SaaS | High |
| 12 | Per-tenant rate limiting & quota engineering | Golding noisy-neighbor, Trio | High |
| 13 | Sandbox / demo-tenant engineering (seeded, time-bounded, reset) | AE book, Walling | High |
| 14 | API-as-product + developer portal + sandbox keys | Trio, AE | Med |
| 15 | Trust portal + SOC2 evidence + DPA workflow engineering | Mersch Ch.7, Trio | Med |
| 16 | Free trial / freemium engineering (cohorts, branched conversion) | Walling pricing, Garbugli | Med |
| 17 | SaaS bowtie events contract + reverse-ETL to CRM | WBD Fundamentals | Med |
| 18 | Customer health score + churn risk engineering | Walling, WBD, Garbugli | Med |
| 19 | Custom contract / enterprise pricing overrides in the billing engine | AE, Mersch enterprise | Med |
| 20 | QBR data export + renewal alerting infra | WBD Fundamentals | Low |

## NEW SKILLS (10)

### 1. `saas-control-plane-engineering`
**Description:** Use when building the control plane of a multi-tenant SaaS — the cross-cutting services (tenant management, identity binding, onboarding orchestration, metrics aggregation, billing customer mirror, audit log) that operate every tenant through a single pane of glass. Distinct from `multi-tenant-saas-architecture` (which focuses on tenant isolation patterns) and `modular-saas-architecture` (pluggable modules).
**Why needed:** Golding's central architectural construct — control plane vs application plane — is not codified in any current skill. The audit shows engines that skip the control plane regress to MSP-style per-tenant variations within a year.
**Source:** Golding Ch.2 ("The Two Halves of Every SaaS Architecture") + Ch.5 (Tenant Management).

### 2. `saas-tenant-onboarding-automation`
**Description:** Use when designing and implementing the tenant onboarding state machine — the orchestrated flow from signup to ready tenant (identity provisioning, infra allocation, billing customer creation, seeding, welcome email, activation telemetry). Includes saga patterns, compensations, idempotency, retries, and observability. Companion to `saas-control-plane-engineering`.
**Why needed:** Trio book makes onboarding automation the single biggest "graduation requirement" between $1M and $10M ARR. No current skill covers the orchestration patterns.
**Source:** Golding Ch.4 + Trio operational lessons.

### 3. `saas-deployment-models`
**Description:** Use when selecting a multi-tenant deployment model — full stack silo, full stack pool, mixed mode, hybrid full stack, or pod — and translating the choice into IaC, routing, deployment automation, and operational tooling. Includes decision rules, cost/blast-radius tradeoffs, and migration paths between models.
**Why needed:** Golding Ch.3 is the most reusable engineering decision tree in the book; no current skill encodes it operationally.
**Source:** Golding Ch.3.

### 4. `saas-entitlements-and-plan-gating`
**Description:** Use when designing the entitlements engine that enforces what each plan/tier/tenant can do — feature flags vs entitlements distinction, limits enforcement (seats, API calls, storage, projects), gate placement (UI, API, worker), upgrade-discovery UX, and override mechanisms for enterprise contracts.
**Why needed:** Pricing decisions from Walling and enterprise overrides from Mersch/AE require a clean entitlements layer. Current `subscription-billing` covers Stripe Billing but not the gate runtime.
**Source:** Walling pricing chapter + Mersch enterprise + Golding tiering.

### 5. `saas-transactional-email-infrastructure`
**Description:** Use when designing the transactional and lifecycle email **infrastructure** — ESP selection (Postmark, SES, SendGrid, Customer.io, Braze), domain authentication (SPF, DKIM, DMARC, BIMI), sender reputation, subdomain separation (transactional vs marketing), suppression list management, bounce/complaint feedback loops, and event-bridge from product events to email automation. Distinct from `tabler-email-templates` (HTML templates) and `subscription-billing` (billing-event triggers).
**Why needed:** Garbugli's deliverability + data-implementation chapters are pure infra work the engine doesn't currently cover. Email is one of the highest-ROI levers in SaaS and most products mis-architect it.
**Source:** Garbugli Ch.11-12, 26-27, 33 + industry deliverability best practice.

### 6. `saas-lifecycle-email-orchestration`
**Description:** Use when designing the six core lifecycle email sequences (welcome/onboarding, behavioral/feature-discovery, upgrade/upsell, retention, reactivation, referral) — trigger contracts, branched automation, suppression rules, PQL/churn-risk triggers, and revenue attribution. Built on top of `saas-transactional-email-infrastructure`.
**Why needed:** Garbugli's deep dives Ch.41-46 are an engineering playbook; current engine has no sequence-level skill.
**Source:** Garbugli Ch.41-46.

### 7. `saas-admin-backoffice-tooling`
**Description:** Use when designing the internal admin / back-office console — tenant impersonation (audited, time-boxed), tenant lifecycle controls (suspend/restore/archive/hard-delete), billing operations (refunds, credits, plan overrides), feature-flag overrides per tenant, bulk actions, and the audit-log spine that backs all of it. Distinct from the customer-facing `/adminpanel/` in `multi-tenant-saas-architecture`.
**Why needed:** Trio book makes the back-office console a $1M-$10M graduation requirement. Currently no skill addresses it; multi-tenant skill mentions super-admin but doesn't detail back-office UX.
**Source:** Trio operations + Golding control plane + compliance baseline.

### 8. `saas-sso-scim-enterprise-auth`
**Description:** Use when implementing enterprise auth — SAML 2.0 + OIDC SSO with per-tenant IdP configuration, SCIM 2.0 user provisioning/deprovisioning, custom-domain support with automated cert provisioning, IP allowlists per tenant, and the migration from email-password tenants to IdP-enforced tenants.
**Why needed:** Mersch is emphatic that SSO/SCIM are price-of-entry for enterprise. `dual-auth-rbac` handles session+JWT but not SAML/SCIM.
**Source:** Mersch Ch.7-9 + AE book.

### 9. `saas-tenant-data-portability-and-erasure`
**Description:** Use when designing the GDPR/POPIA/CCPA-compliant data export (right to portability) and erasure (right to be forgotten) workflows — cascade through every data store including warehouse/backups, retention policy, requester verification, audit trail, and the multi-tenant nuances of erasing one tenant's data without affecting others.
**Why needed:** Trio book makes data ops a graduation requirement; current skills cover GDPR concepts but not the engineering workflow. Especially important for African market (POPIA, Uganda DPPA, Kenya DPA).
**Source:** Trio + compliance industry baseline + existing `uganda-dppa-compliance` for regional fit.

### 10. `saas-rate-limiting-and-quotas`
**Description:** Use when designing per-tenant rate limits and quotas — algorithm choice (token bucket, sliding window, leaky bucket), where to enforce (edge, gateway, service, DB connection pool), per-plan / per-tier limits, soft vs hard caps, fair-queueing for noisy neighbors, headers/responses, and how to expose quota usage to the tenant.
**Why needed:** Golding's noisy-neighbor problem + Trio scale lessons; no current skill encodes the operational patterns.
**Source:** Golding pool considerations + Trio reliability.

## ENHANCEMENTS TO EXISTING SKILLS

### `multi-tenant-saas-architecture`
- Add reference file `saas-deployment-models-decision-tree.md` summarizing silo/pool/hybrid/mixed-mode/pod with decision rules.
- Add reference file `tenant-context-propagation.md` detailing JWT shape, log/metric/trace tagging, queue envelope.
- Cross-link to new `saas-control-plane-engineering`, `saas-tenant-onboarding-automation`.

### `subscription-billing`
- Add reference file `billing-reconciliation.md` covering nightly Stripe-vs-mirror diff, drift alerting, idempotent webhook ingestion.
- Add reference file `custom-contracts-and-enterprise-overrides.md` covering per-tenant price overrides, order-form-driven plans, contract-stored-as-data.
- Add reference file `involuntary-churn-engineering.md` — pre-dunning emails, card-updater, retry strategy, end-of-dunning disposition.

### `saas-growth-metrics`
- Add reference file `saas-metrics-event-contract.md` — typed events for MRR, expansion, churn, with `is_new_customer`, `mrr_delta`, idempotency_key.
- Add reference file `cohort-analysis-engineering.md` — signup-cohort, plan-cohort, channel-cohort patterns, warehouse views.
- Add reference file `cost-per-tenant-attribution.md` — silo vs pool cost attribution; apportionment algorithm.

### `ios-monetization`
- Add reference file `cross-platform-entitlement-reconciliation.md` — single entitlement service that reconciles StoreKit2, Play Billing, and Stripe events; webhook from Apple/Google to platform.

### `product-led-growth`
- Add reference file `pql-scoring.md` — PQL definition patterns, daily-materialized score, in-app + email coordination.
- Add reference file `activation-instrumentation.md` — defining the aha event, measuring TTV, branching trial flows.

### `saas-architecture-strategy`
- Add reference file `saas-maturity-matrix.md` — capability roadmap by ARR band ($0-1M, $1-10M, $10M+).

### `kubernetes-saas-delivery`
- Add reference file `pod-deployment-pattern.md` — when to graduate from pool to pods, capacity planning, cross-pod tenant migration.

### `tabler-email-templates`
- Add reference file `email-template-event-mapping.md` — which template maps to which lifecycle event in `saas-lifecycle-email-orchestration`.

### `saas-sales-organization`
- Add reference file `sales-assist-product-capabilities.md` — sandbox tenants, demo tenants, custom-quote support, order-form integration, CRM reverse-ETL.

## CROSS-CUTTING REFERENCE FILES

In addition to per-skill references above, the following sit at engine root or in the most-used skill's `references/`:

| File | Location | Purpose |
|---|---|---|
| `saas-multi-tenancy-patterns.md` | `skills/multi-tenant-saas-architecture/references/` | Silo/pool/pod patterns canonical reference |
| `saas-billing-models.md` | `skills/subscription-billing/references/` | Per-seat, per-usage, flat, hybrid, with engineering patterns |
| `saas-observability-stack.md` | `skills/observability-monitoring/references/` | Tenant-tagged logs/metrics/traces stack |
| `saas-deliverability-and-transactional-email.md` | `skills/saas-transactional-email-infrastructure/references/` | Deliverability deep dive |
| `saas-onboarding-flows-engineering.md` | `skills/saas-tenant-onboarding-automation/references/` | State machine, sagas, observability |
| `saas-product-led-growth-eng.md` | `skills/product-led-growth/references/` | PQL + activation deep dive |
| `saas-mobile-app-revenue.md` | `skills/ios-monetization/references/` | Cross-platform entitlement |
| `saas-trust-and-compliance-eng.md` | `skills/saas-tenant-data-portability-and-erasure/references/` | Trust portal, SOC2 evidence automation, DPA flow |
| `saas-feature-flagging-and-experimentation.md` | `skills/saas-entitlements-and-plan-gating/references/` | Feature flags vs entitlements; experimentation hooks |
| `saas-pricing-page-engineering.md` | `skills/subscription-billing/references/` | Single-source-of-truth pricing page generated from billing catalogue |

## OUT OF SCOPE FOR THIS PASS (Recommended Follow-Up Sessions)

- **Detailed Android Play Billing skill** — partial coverage in `mobile-saas-planning`; deserves a dedicated `android-monetization` skill mirroring `ios-monetization`.
- **Trust portal / SOC2 evidence automation skill** — touched in `saas-tenant-data-portability-and-erasure`, but a standalone `saas-trust-and-compliance-portal` skill would help when targeting enterprise.
- **Developer portal / API-as-product skill** — `api-design-first` covers API design; a separate `saas-developer-portal` covering sandbox keys, rate-limit headers, OpenAPI hosting, docs versioning, and Stripe-style developer experience would close the gap.
- **Customer health & churn-risk scoring skill** — currently a reference in `product-led-growth`; deserves its own `saas-customer-health-scoring` skill at the next pass.
- **QBR & renewal automation skill** — currently subsumed in `saas-subscription-mastery`; standalone skill would help.
- **Per-tenant data residency / sovereignty skill** — important for enterprise and African market (data must stay in-region); deserves dedicated skill.
- **API key & service-token engineering skill** — touched in `vibe-security-skill` and `api-design-first`; deserves dedicated `saas-api-keys-and-service-tokens` for managing customer-facing API keys, scopes, rotation, leak detection.
- **In-app messaging & guides skill** — Pendo / Appcues / Intercom Messenger patterns for onboarding tours, NPS, surveys.
