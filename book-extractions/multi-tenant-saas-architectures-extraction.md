# Building Multi-Tenant SaaS Architectures — Tod Golding — Extraction
**Source:** Tod Golding, *Building Multi-Tenant SaaS Architectures* (O'Reilly, Early Release). Tier: **Foundational.**
**Coverage:** Ch.1 SaaS Mindset, Ch.2 Multi-tenant Architecture Fundamentals, Ch.3 Multi-Tenant Deployment Models (silo / pool / hybrid / mixed-mode / pod). Subsequent chapters referenced: Ch.4 Identity & Onboarding, Ch.5 Tenant Management, Ch.8 SaaS Microservices, Ch.9 Data Partitioning, Ch.10 Tenant Isolation, Ch.12 Serverless SaaS, Ch.14 Cost per Tenant, Ch.16 Billing.

This is the canonical reference for **how a SaaS is built underneath**: the vocabulary, the planes, the deployment patterns, and the cross-cutting constructs that every multi-tenant product must implement. Synthesised for an engineering build engine.

---

## 1. The Five Foundational Reframings

Golding spends the entire opening of the book demolishing common mental models. These reframings shape every downstream architectural choice.

### 1.1 SaaS is a business model, not an architecture
- SaaS is "a business and software delivery model that enables organizations to offer their solutions in a low-friction, service-centric model that maximizes value for customers and providers. It relies on agility and operational efficiency as pillars of a business strategy that promotes growth, reach, and innovation."
- Do **not** lead with architecture. Lead with the business outcomes you are designing for (agility, operational efficiency, innovation, frictionless onboarding, growth). The architecture exists to serve these.

### 1.2 Multi-tenant ≠ shared infrastructure
- A dedicated single-tenant-per-stack environment **is still multi-tenant SaaS** if all tenants run the same version and are operated through a single pane of glass.
- The vocabulary: from now on, single-tenant simply doesn't exist as a category. We use **silo** (resource dedicated to one tenant) and **pool** (resource shared across tenants).

### 1.3 SaaS ≠ MSP (Managed Service Provider)
- MSP keeps per-customer variations (different versions, custom config, dedicated teams). SaaS unifies them onto one version with one control plane.
- Customer pain (one-offs, dedicated environments) is the leading indicator that you've drifted from SaaS back to MSP.

### 1.4 Build a service, not a product
- The restaurant analogy: food = product, speed-to-table + greeting + recovery = service. SaaS tenants judge **service**: onboarding speed, time-to-value, frequency of releases, response to feedback, downtime.
- Engineers who think only in features starve the service dimensions. Operational attributes (onboarding, TTV, release cadence) belong **on the product owner's backlog**.

### 1.5 The Third Wall — what tenants can and cannot see
- Tenants see the **surface** of your service. They do not see patches, schema migrations, infrastructure config. Anything you expose breaks the third wall and locks you back into per-tenant customisation.
- Rule of thumb: if an external dependency is hidden and centrally managed, it's still SaaS. If a tenant can see/touch it (e.g., a tenant-hosted DB), that's MSP territory.

---

## 2. The Two Halves of Every SaaS Architecture

**Every SaaS environment splits into a Control Plane and an Application Plane.** Internalise this — it's the most useful mental model in the book.

### 2.1 Control Plane
> "The single pane of glass that is used to orchestrate and operate all the moving parts of your SaaS solution."

The control plane is **not multi-tenant in its capabilities** — its services span all tenants. Components:

| Component | Role |
|---|---|
| **Onboarding** | Provisions new tenants, creates identity, allocates resources, fires the activation flow |
| **Identity** | Authenticates users AND binds every user to a tenant |
| **Tenant management** | Single source of truth for tenant state, status, plan, config |
| **Metrics** | Centralized hub for tenant activity (cross-cutting, never per-tenant) |
| **Billing** | Plan/customer mirror, metering ingestion, invoice generation |
| **System admin console** | The internal admin app that the SaaS provider uses |

The control plane is **versioned and deployed by the SaaS provider's needs** — independent of tenant feature releases. Build it first; it's the forcing function that makes the rest of the system tenancy-aware.

### 2.2 Application Plane
The features and functionality of the SaaS service — where multi-tenancy actually manifests at runtime. There is **no single blueprint** for the application plane; it is shaped by domain, tech stack, compliance, and tiering needs. Core constructs every application plane must address:

| Construct | What it does |
|---|---|
| **Tenant context** | Token (typically JWT) carrying tenant + user identity, passed end-to-end through every service/log/metric/query |
| **Tenant isolation** | Mechanism that guarantees one tenant cannot read or affect another's resources, even in pooled infrastructure |
| **Data partitioning** | How tenant data is stored (silo, pool, or hybrid per-table) |
| **Tenant routing** | Maps incoming requests to the right siloed/pooled service instance |
| **Multi-tenant deployment** | DevOps automation that deploys updates across all tenant footprints uniformly |

---

## 3. The Silo / Pool Vocabulary

Replace "dedicated / shared" with **silo / pool**:

- **Silo** = a resource dedicated to one tenant (compute, DB, queue, storage, namespace).
- **Pool** = a resource shared by multiple tenants.

These terms are applied at **fine grain**: one microservice can have pooled compute and siloed storage; another can be fully siloed. Don't think in stacks; think per resource.

---

## 4. The Five Multi-Tenant Deployment Models

The single most-cited decision in the book. Pick or compose:

### 4.1 Full Stack Silo
Each tenant gets a complete dedicated copy of the application stack (compute, storage, queues, network).

**When it fits:** strict compliance regimes (HIPAA, PCI per-tenant), legacy migrations to SaaS without re-architecting, premium-tier offering, small tenant count.

**Considerations:**
- Control plane complexity explodes — every tenant has its own footprint to provision, monitor, deploy.
- Scaling impact — typically caps out at low hundreds of tenants.
- Cost — expensive baseline per tenant, no economy of scale.
- Cost attribution — trivially easy (cloud provider already tags each silo).
- Blast radius — naturally bounded; release waves possible.

**Implementation flavors:**
- **Account-per-tenant** (e.g., AWS account per tenant): hardest boundary, easiest cost attribution, but bumps into cloud account limits and onboarding automation friction (some account-creation steps aren't automatable).
- **VPC-per-tenant**: network-level isolation inside one account; better scaling than account-per-tenant; still has VPC limits.
- **Subnet-per-tenant** (rare): unwieldy at scale.

**Critical mindset:** even in full stack silo, treat every silo as "an instance of a pooled environment that happens to have one tenant." Never use silos as a license for per-tenant customization — that's how teams regress to MSP.

### 4.2 Full Stack Pool
All tenants share all infrastructure. Tenant context is resolved at runtime for every request.

**When it fits:** scale-out B2C SaaS, cost-margin sensitive businesses, simple operations, no per-tenant compliance.

**Considerations:**
- Scale — best efficiency, hardest scaling policy design (mixed tenant loads, new tenants arriving daily).
- Isolation — must be engineered into every layer (RLS, tenant_id discipline, per-tenant rate limits).
- Blast radius — global. An outage hits every tenant; reputational risk. Demands top-tier CI/CD, fault tolerance, bulkheads, async patterns.
- Noisy neighbor — biggest risk; need throttling, quotas, autoscaling, defensive sizing.
- Cost attribution — hard; cloud bills don't naturally break down per-tenant on shared compute.
- Operational simplicity — best. One deploy, one dashboard, one set of logs to aggregate.

### 4.3 Mixed Mode (the most common in practice)
Fine-grained silo/pool decisions per microservice or per resource. Service A: pooled compute, pooled storage. Service B: siloed compute, siloed storage. Service C: pooled compute, siloed storage.

Combined with tier policy: e.g., basic tier all pooled; premium tier gets dedicated Service 5/6 silos.

**This is the model most successful SaaS use in real life.** The full-stack patterns are mostly migration starting points or premium-tier offerings.

### 4.4 Hybrid Full Stack
Some tenants live in full stack pool (the basic tier majority), and a small number of premium/strategic tenants get a full stack silo. Constrained-count silos. Avoids drifting back to MSP — silos are still operated by the same control plane, same version.

### 4.5 Pod
Group of tenants together becomes a deployable unit. Driven by:
- Cloud limit constraints (when pool exceeds account/region quotas)
- Geography (data residency, latency)
- Isolation strategy (smaller blast radius than full pool)
- Profile clustering (similar-sized tenants pooled together)

Pods can be moved between (with substantial effort). All pods run the same version, all are managed by the same control plane. Don't use pods as MSP-by-stealth.

### 4.6 Decision rules
```
Compliance forces dedicated tenant infra (HIPAA, regulated single-tenant data)?
    -> Full Stack Silo or Mixed Mode with siloed sensitive services

Bootstrapping from a legacy single-customer codebase?
    -> Full Stack Silo (migration accelerator), plan to refactor toward Mixed Mode

Cost margins are tight, B2C-scale tenants, no per-tenant compliance?
    -> Full Stack Pool

Two-tier business model (basic + premium)?
    -> Hybrid Full Stack (premium gets silo) or Mixed Mode (premium gets siloed sub-services)

Hitting cloud account/region limits, multi-geography, or noisy-neighbor management?
    -> Pod model

Default starting point for a new B2B SaaS:
    -> Mixed Mode — start mostly pooled, silo compliance-sensitive or noisy services
```

---

## 5. Tenant Context Is the Spine

Tenant context is the runtime carrier of *which tenant am I serving right now*.

- **Format:** typically a JWT containing `user_id`, `tenant_id`, `roles`, `plan`, `entitlements`, expiration.
- **Source:** issued at authentication; **never** read from request body, headers, or query params at any boundary that decides access.
- **Propagation:** rides every internal service-to-service call (via auth header, context propagation, mTLS claims). Logs/metrics/traces all carry `tenant_id`.
- **Silo vs Pool consequence:** in silo, context is fixed at provisioning (env var). In pool, it must be resolved per request — and propagated everywhere.

**Practical guidance for the build engine:** make `tenant_id` (and `franchise_id` where applicable) a first-class field in:
- Every database table (NOT NULL, FK, leading composite index column)
- Every log line
- Every metric label
- Every trace span attribute
- Every cache key
- Every queue message envelope
- Every webhook payload signed by your platform
- Every CLI/admin command audit log

---

## 6. Tenant Isolation (Ch.10 referenced)

Three layers must be isolated:
1. **Data isolation** — RLS (Row-Level Security), per-tenant DB schemas, or per-tenant DB instances. Every query MUST be filtered by `tenant_id`; the strongest enforcement is RLS in Postgres or a tenant-aware ORM middleware that auto-injects the predicate.
2. **Compute isolation** — quotas, per-tenant rate limits, queue partitioning, namespace boundaries (K8s), service mesh policies. Prevent CPU/memory/IO from one tenant degrading another.
3. **Network isolation** — VPC/subnet/SG boundaries for siloed tenants; egress controls and per-tenant private endpoints for sensitive integrations.

Cross-tenant access **must return 404 not 403** — 403 confirms existence, enabling enumeration attacks.

---

## 7. Onboarding (Ch.4 referenced)

Onboarding is the **front door**. It must be fully automated, end-to-end, in seconds-to-minutes — anything else compromises agility and growth.

Onboarding orchestration responsibilities:
1. Create tenant record in the control plane (`tenants` table).
2. Provision identity (auth realm, default admin user, password setup or magic link).
3. Allocate infrastructure (silo: provision dedicated stack; pool: register `tenant_id` in shared services).
4. Configure billing customer (Stripe Customer create, attach Subscription/Trial).
5. Seed default data (catalogue, sample records, roles, permissions).
6. Send welcome email + magic-link.
7. Fire activation telemetry (`tenant.created`, `tenant.first_login`, `tenant.activated`).

The **onboarding state machine** itself is a control plane artifact. States: `pending → provisioning → ready → suspended → archived → deleted`. Failed onboarding must be observable and retriable.

Common failure modes:
- Partial provisioning leaves tenant in a half-state. **Fix:** orchestrate with saga + compensations.
- Cloud account/quota limits surface as onboarding errors. **Fix:** pre-provision capacity pools.
- Identity provisioning lags behind tenant creation. **Fix:** ensure auth realm + admin user are part of the atomic onboarding transaction.

---

## 8. Data Partitioning (Ch.9 referenced)

Selected per data type, not per system:

| Pattern | Use when |
|---|---|
| **Shared DB, shared schema, `tenant_id` column** | Default for B2B SaaS up to mid-thousands of tenants; RLS enforces isolation |
| **Shared DB, schema-per-tenant** | Mid-scale, heavier isolation needs, per-tenant migrations tractable |
| **DB-per-tenant** | Strict compliance, very large tenants, full-stack-silo deployment |
| **Hybrid** | Hot table per-tenant DB; cold/reference data shared |

Pick per access pattern. Don't fall in love with one model.

---

## 9. Tenant Routing

Pool: routing typically goes through one ingress and resolves tenant from JWT/subdomain.
Silo: per-tenant ingress configuration; updated at onboarding by the control plane.

Subdomain strategies:
- `tenant.example.com` — wildcard DNS + cert per-tenant or wildcard cert; admin must own DNS automation.
- `app.example.com` with tenant in path or JWT — simpler; loses some isolation feel.
- Custom domains per tenant — requires automated cert provisioning (cert-manager, ACM, etc.) and a domain claim/verification flow.

---

## 10. Multi-Tenant Deployment Automation

In a silo or pod world, deployments are **rolling waves** across tenants. Critical capabilities:
- Per-tenant deployment registry — what version each tenant is on.
- Tenant tier metadata controls deployment order (free tier first, premium last; or canary-tenant-first).
- Schema migrations: forward-compatible, deployed before code; rolled out one tenant/pod at a time in silo; one shot in pool.
- Rollback path: per-tenant or per-pod, automated.

Pool: one deploy moves everyone. Demands more rigorous testing, canary, progressive delivery (Argo Rollouts / Flagger), and feature flags.

---

## 11. Cost Per Tenant (Ch.14 referenced)

Critical operational metric — without it you cannot price, you cannot identify whales/drains, you cannot decide who gets silo'd.

- Silo: cloud-billed per silo. Aggregate to `cost_per_tenant`.
- Pool: hard. Must instrument per-tenant usage of pooled resources (compute time, request count, queries, storage bytes, egress bytes) and apportion shared infra cost by those signals.
- Output: `cost_per_tenant_monthly` per tenant + plan margin dashboard.

---

## 12. Engineering-Actionable Decisions This Book Forces

For each new SaaS the build engine designs, it must answer:

1. **Deployment model:** Full stack silo / pool / mixed mode / hybrid / pod — and why.
2. **Tenant context propagation:** JWT shape, headers, log/metric/trace fields.
3. **Isolation model per layer:** data (RLS/schema/DB), compute (quotas/namespaces), network.
4. **Onboarding state machine:** states, durations, retries, compensations, observability.
5. **Tenant lifecycle states:** pending/active/suspended/archived/deleted + transitions + retention.
6. **Routing strategy:** subdomain / path / custom domain + automation.
7. **Per-tenant cost attribution plan:** which resources are silo-billed vs metered for apportionment.
8. **Per-tenant deployment plan:** rolling waves, canary tenant, rollback granularity.
9. **Tier-aware infrastructure:** which services upgrade resource shape per tier.
10. **Blast-radius posture:** what gets bulkheaded, what's the maximum blackout, runbook.

These ten outputs are the **multi-tenant readiness pack** that should accompany every greenfield SaaS the engine ships.

---

## 13. Anti-Patterns Lifted From the Book

- **Designing the application plane first.** Build the control plane first — it forces tenancy-awareness into everything downstream.
- **Trusting client-supplied `tenant_id`.** Always derive from authenticated context.
- **Reading `tenant_id` from query string or body for authorization decisions.** Use the JWT claim.
- **Returning 403 on cross-tenant access.** Returns 404. Don't confirm existence.
- **Treating full stack silo as a license to customize per tenant.** It is not. Silo = same code, just dedicated infra.
- **Designing onboarding as a manual checklist on day one and "automating it later."** Almost no one ever does. Automate from day one — even a basic seed + email flow.
- **No per-tenant cost attribution.** You can't manage what you can't measure. Bake it in early.
- **Premature pool obsession.** Some workloads should be siloed forever (compliance, noisy). Don't force pool everywhere.
- **Premature silo obsession.** Especially common in teams coming from on-prem. Silo everything = no economy of scale, no SaaS margins.
- **No tenant-tier metadata in the routing/auth layer.** Without it, you can't gate, throttle, or route per plan.

---

## 14. Synthesis for the Build Engine

The most valuable thing this book gives a build engine is **the operational checklist of constructs every SaaS must implement**, and the **mental separation between control plane (one) and application plane (many tenants)**.

Every greenfield SaaS project should produce:

1. **Multi-tenant readiness pack** (10 outputs above).
2. **Control plane skeleton** before any application feature — tenants, users, identity, billing customer, audit log, admin console.
3. **Tenant context middleware** that injects `tenant_id` and `user_id` into every log/metric/trace/query/cache key/queue message.
4. **Tenant isolation guardrails** — automated tests that try cross-tenant reads/writes/deletions and assert they 404.
5. **Onboarding state machine** that is observable, retriable, idempotent.
6. **Cost-per-tenant telemetry** wired from day one.

These five artifacts collectively turn a single-app codebase into a SaaS the day it ships.
