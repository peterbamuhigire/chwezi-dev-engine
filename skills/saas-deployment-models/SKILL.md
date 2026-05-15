---
name: saas-deployment-models
description: Use when selecting a multi-tenant deployment model — full stack silo, full stack pool, mixed mode, hybrid full stack, or pod — and translating the choice into IaC, routing, deployment automation, and operational tooling. Includes decision rules, cost/blast-radius tradeoffs, migration paths, and the relationship between deployment model and tiering strategy.
metadata:
  portable: true
  compatible_with:
  - Codex
  - codex
---

# SaaS Deployment Models — Silo, Pool, Mixed Mode, Hybrid, Pod
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Choosing the deployment model for a new multi-tenant SaaS (often the first architectural decision after picking the stack).
- Evaluating whether to migrate an existing pool deployment to mixed-mode or pods because of compliance, noisy neighbor, or geographic constraints.
- Designing a tier-aware deployment strategy where premium customers get silo and basic-tier customers stay pooled.
- Onboarding a regulated tenant (HIPAA, PCI, GDPR-strict, data residency) that cannot live in pool.
- Hitting cloud account/VPC/region limits and needing to pod the platform.

## Do Not Use When

- The task is the data isolation enforcement layer (RLS, tenant_id filtering) — use `multi-tenant-saas-architecture`.
- The task is the modular composition of features per tenant — use `modular-saas-architecture`.
- The task is K8s-specific tenant isolation — use `kubernetes-saas-delivery`.
- The task is single-tenant deployment — this skill is multi-tenant only.

## Required Inputs

- Tenancy goals from product (target tenant count, expected ACV range, compliance profile).
- Business constraints (margin pressure, time-to-market).
- Compliance constraints (data residency, HIPAA/PCI, audit needs).
- Cloud provider + IaC stack (Terraform, Pulumi, CDK).
- Existing deployment topology (if migrating).

## Workflow

1. Read this `SKILL.md`. Cross-reference the multi-tenant book extraction for the canonical patterns.
2. Run the decision tree (§3) to land on a starting model.
3. Map each microservice / data store to silo vs pool individually (§4) — most production SaaS are mixed mode, not full stack.
4. Design routing (§5) to support the chosen model.
5. Design deployment automation (§6) — rolling waves across silos/pods, single deploy for pool.
6. Design the per-tenant cost attribution strategy (§7) — silo is easy, pool requires apportionment.
7. Define the migration path (§8) if you'll evolve the model over time.
8. Apply anti-patterns (§9).

## Quality Standards

- The deployment model is **documented** in an ADR — future engineers must understand why.
- Per-tenant fingerprint exists in every plane: routing knows the model per tenant; deployments know which tenants to upgrade in which wave; cost telemetry reflects the model.
- Migration paths between models are designed up front; no model is a one-way door.
- All silos run the same version of the code — never use silos as a license for per-tenant customization.

## Anti-Patterns

- Choosing full stack silo because it "feels safer" without quantifying the operations cost.
- Choosing full stack pool because it has "best margins" without addressing noisy-neighbor at scale.
- Treating the deployment model as immutable; refusing to graduate from pool to pods when scale demands it.
- Mixing the deployment model with the tenancy isolation enforcement — they are separate concerns.

## Outputs

- ADR — deployment model decision + rationale.
- Per-service silo/pool table (the application-plane footprint).
- Routing diagram with tenant→stack mapping.
- Deployment automation plan (single-shot for pool; rolling waves for silo/pod).
- Cost attribution plan (silo = native cloud; pool = apportionment).
- Migration playbook (current → target).

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Architecture | Deployment model ADR | ADR markdown | `docs/adr/0007-deployment-model.md` |
| Architecture | Per-service silo/pool footprint | Markdown table | `docs/saas/silo-pool-footprint.md` |
| Operability | Deployment-waves plan | Markdown doc | `docs/saas/deployment-waves.md` |

## References

- `references/decision-tree.md` — full silo/pool decision tree with weighted criteria.
- `references/silo-implementations.md` — account-per-tenant, VPC-per-tenant, namespace-per-tenant patterns.
- `references/pod-deployment.md` — pod design, capacity planning, cross-pod migration.
- Companion: `multi-tenant-saas-architecture`, `modular-saas-architecture`, `kubernetes-saas-delivery`, `saas-control-plane-engineering`, `saas-rate-limiting-and-quotas`.

<!-- dual-compat-end -->

## §1 The Vocabulary — Silo and Pool

(From Golding's book, restated for execution.)

- **Silo** = a resource dedicated to one tenant. Examples: tenant-specific DB instance, namespace, VPC, K8s namespace, S3 bucket.
- **Pool** = a resource shared by multiple tenants. Examples: shared DB with `tenant_id` column, shared API server fleet, shared object store with per-tenant prefixes.

These are **applied per resource**, not per stack. A microservice can have pooled compute and siloed storage. A platform can be pool for tenants 1-1000 and silo for premium tenant 1001.

## §2 The Five Models

### 2.1 Full Stack Silo
Every tenant gets a complete dedicated copy.

| Pros | Cons |
|---|---|
| Strongest isolation (compliance) | Highest cost per tenant |
| Easy cost attribution | Highest operational complexity |
| Bounded blast radius | Caps out at low hundreds of tenants |
| Allows legacy code to lift-and-shift to SaaS | Onboarding is slowest (provisioning) |

**Default use:** regulated single-tenant workloads (HIPAA, PCI, banking), premium tier of mid-market SaaS, legacy migration to SaaS.

**Sub-flavors:**
- **Account-per-tenant** (AWS account, GCP project): hardest boundary, hits cloud account quotas, hardest to scale.
- **VPC-per-tenant**: network-level isolation in one account, scales to ~hundreds of VPCs before becoming unwieldy.
- **Namespace-per-tenant** (K8s): the most operationally tractable silo; see `kubernetes-saas-delivery`.

### 2.2 Full Stack Pool
All tenants share all infrastructure. Tenant context resolved at runtime.

| Pros | Cons |
|---|---|
| Best margins (economies of scale) | Global blast radius |
| Simple operations (one deploy, one dashboard) | Complex isolation engineering |
| Easy to scale tenant count | Hard cost attribution |
| | Noisy-neighbor risk |

**Default use:** B2C SaaS at scale, SMB SaaS where margin matters, MVP stage before any premium tier exists.

### 2.3 Mixed Mode (the most common)
Per-service silo/pool decisions. Service A: pool. Service B: silo. Service C: silo for premium, pool for basic.

**Default use:** **most production B2B SaaS.** Start pool, silo the services that demand it (sensitive data store, noisy report engine, regulated workflow).

### 2.4 Hybrid Full Stack
Basic tier: full stack pool. Premium tier (small count): full stack silo. Same code, same control plane.

**Default use:** when you have a clear premium tier ($50K+ ACV) that the basic tier doesn't justify.

### 2.5 Pod
Group of tenants forms a deployment unit. Multiple pods exist; control plane routes to the right pod.

**Default use:**
- Hit cloud account/VPC/region quotas at full-pool scale (10K+ tenants in one pool).
- Multi-geography (data residency); each region is a pod.
- Want bounded blast radius without the cost of per-tenant silo.
- Want to roll updates pod-by-pod for safer canary.

## §3 Decision Tree

```
Q1: Does any tenant's data face strict per-tenant regulatory boundary
    (HIPAA, PCI, EU data sovereignty for specific data)?
    YES → Full Stack Silo for those tenants
         (Hybrid if mixed with non-regulated; Mixed Mode if only certain services regulated)
    NO  → continue

Q2: Are you migrating a legacy single-customer codebase to SaaS quickly?
    YES → Full Stack Silo (lift-and-shift) as starting point;
          refactor toward Mixed Mode over 12-24 months.
    NO  → continue

Q3: Will you have > 10,000 tenants?
    YES → Full Stack Pool or Pod
         (Pool if no geography/residency constraint; Pod if you have either)
    NO  → continue

Q4: Do you have a clear premium tier ($50K+ ACV) with isolation expectations?
    YES → Hybrid Full Stack OR Mixed Mode with siloed premium services
    NO  → continue

Q5: Default choice for a new B2B SaaS:
    Mixed Mode — start pooled, silo as compliance / noisy-neighbor demands.
```

## §4 The Per-Service Silo/Pool Map

Most production SaaS map looks like:

| Service | Compute | Storage | Why |
|---|---|---|---|
| API gateway | Pool | n/a | Routes by tenant context |
| Auth service | Pool | Pool (RLS) | Cross-tenant identity is OK |
| Tenant core service | Pool | Pool | Hot path |
| Reporting engine | Pool (autoscale per tier) | Pool | Spawn isolated workers per request |
| Document storage | Pool | Pool (per-tenant prefixes) | Cheap to silo if needed |
| Search index | Pool | Pool (per-tenant indexes) | Per-tenant indexes when scale demands |
| Financial ledger | Pool compute | **Silo storage** (per-tenant DB or schema) | Strict isolation for audit/compliance |
| AI / LLM workers | Pool | Pool | Per-tenant rate limits |
| Heavy analytics | Pool (queue partition per tenant) | Pool | Noisy-neighbor controlled by partition |
| Email worker | Pool | Pool | Per-tenant suppression list |

Document this for the SaaS as an ADR or table. The build engine should generate this map for every greenfield SaaS.

## §5 Routing

- **Pool model:** one ingress; routes by tenant context (subdomain, JWT claim, path).
- **Silo model:** per-tenant ingress; control plane provisions DNS + cert + ingress rule at onboarding.
- **Mixed mode:** ingress to the right service variant (siloed service has its own per-tenant routing; pooled service routes by tenant context).
- **Pod model:** pod-aware router at the edge (subdomain or JWT claim → pod → service inside pod).

**Subdomain strategies:**
- `tenant.app.com` — wildcard DNS + wildcard cert (or per-tenant cert with cert-manager / ACM).
- `app.com/tenant/...` — single domain; tenant in path; simpler; loses isolation feel.
- `tenant.com` (custom domain) — fully white-labeled; requires automated cert provisioning + domain verification.

## §6 Deployment Automation

- **Pool:** single deploy to the shared fleet; everyone gets the new version at the same time. Demands rigorous testing + canary + feature flags + progressive delivery.
- **Silo / Hybrid silo:** rolling waves. Order: internal test tenant → free-tier sample → SMB cohort → premium cohort. Per-tenant migration runs as part of the deploy step.
- **Pod:** rolling waves across pods. Per-pod canary + rollback granularity.

**Schema migrations:**
- Pool: deploy schema before code (forward-compatible); rollout once.
- Silo: per-tenant migration with retry; concurrent migration limit (e.g., 10 in parallel) to protect shared DB infra.
- Pod: per-pod migration in wave with the code release.

## §7 Cost Attribution

- **Silo:** cloud provider already tags each silo's resources to a tenant. Use cost-tag automation (AWS Cost Allocation Tags, GCP labels) to aggregate per-tenant cost.
- **Pool:** harder. Apportion shared compute by:
  - **Request count weight** — count requests per tenant; apportion proportionally.
  - **Resource time weight** — measure compute-seconds per tenant for heavy workloads (reporting, AI).
  - **Storage bytes** — direct, often per-tenant prefixes already.
  - **Egress bytes** — per-tenant log-driven.
- **Hybrid/Mixed/Pod:** apply silo logic to siloed pieces, apportion logic to pooled pieces, sum.

Goal: `cost_per_tenant_monthly_usd` on every tenant. Then `gross_margin_per_tenant = (mrr - cost_per_tenant) / mrr` informs pricing, plan design, and whale identification.

## §8 Migration Between Models

You **will** evolve. Common paths:

- **Pool → Mixed Mode:** identify the noisy / regulated services; silo their compute and/or storage; the rest stay pool. Migrate per-tenant data into siloed stores in waves.
- **Pool → Hybrid:** create a premium tier with siloed full stacks; migrate signed premium customers into silos.
- **Mixed Mode → Pod:** when one big pool exceeds scale limits (DB connections, account quotas), split into pods grouped by tenant size / geography.
- **Silo → Pool (rarely):** if cost pressure overwhelms compliance freedom; usually after acquiring better isolation primitives (RLS, encrypted-at-rest, audit log).

Plan migrations as engineering programs: design doc, dry run in staging, per-tenant migration with rollback, monitoring during transition.

## §9 Anti-Patterns

- **Picking silo "because customers expect it" without quantifying.** Pool with strong RLS often satisfies the same customer concern at 1/10th the cost. Ask, don't assume.
- **Treating full stack silo as license for per-tenant customization.** Every silo runs the same code. Never fork.
- **Pool with no per-tenant rate limit / quota.** Noisy neighbor will eventually break the platform.
- **Pool with no per-tenant cost telemetry.** You cannot identify whales or drains; cannot price intelligently.
- **Mixed mode but no documentation of which services are silo/pool.** New engineers ship features into the wrong half.
- **Pod model with pods that drift in version.** Every pod must run the same release. Document the wave + reconcile.
- **No migration playbook between models.** When scale forces evolution, panic ensues.

## §10 Read Next

- `multi-tenant-saas-architecture` — tenant isolation enforcement.
- `kubernetes-saas-delivery` — K8s-specific silo/pool patterns (namespaces, ArgoCD, progressive delivery).
- `saas-rate-limiting-and-quotas` — per-tenant quotas critical for pool/mixed safety.
- `saas-control-plane-engineering` — control plane that orchestrates the chosen model.
- `subscription-billing` — tiering policy that may drive deployment model.
- `infrastructure-as-code` — IaC patterns for silo provisioning.
