# Deployment Model Decision Tree — Detailed Reference

The expanded decision tree for picking the multi-tenant deployment model. See parent skill `saas-deployment-models` for the summary version.

## The Tree

```
Q1: Is any tenant's data subject to strict per-tenant regulatory boundary?
    (HIPAA per-tenant, PCI per-tenant, sovereign EU data per-tenant, banking regs)
    │
    ├── YES → A: Affected services live in Silo for affected tenants
    │          B: Non-affected services can be Pool for everyone
    │          → Mixed Mode (default), or Full Stack Silo if everything is regulated
    │
    └── NO → continue

Q2: Are you migrating a legacy single-customer codebase to SaaS within months?
    │
    ├── YES → Full Stack Silo as lift-and-shift accelerator
    │         Plan refactor toward Mixed Mode over 12-24 months
    │
    └── NO → continue

Q3: Will the platform support > 10,000 tenants within 24 months?
    │
    ├── YES → Q3a: Data residency or geographic latency constraints?
    │              │
    │              ├── YES → Pod model (one pod per region)
    │              └── NO  → Full Stack Pool (with serious noisy-neighbor mitigation)
    │
    └── NO → continue

Q4: Is there a clear premium tier ($50K+ ACV) with isolation expectations?
    │
    ├── YES → Q4a: Will premium tier be > 5% of tenants?
    │              │
    │              ├── YES → Mixed Mode with siloed premium services
    │              └── NO  → Hybrid Full Stack (pool basic, silo premium)
    │
    └── NO → continue

Q5: Default for new B2B SaaS → Mixed Mode
    Start mostly pooled, silo individual services that demand it as you learn.
```

## Per-Service Silo/Pool Worksheet

For each service, ask:

```
1. Does this service's data face a per-tenant regulatory boundary?
   YES → Silo storage (at minimum); consider Silo compute.

2. Is this service's compute prone to noisy-neighbor problems?
   (Long-running, CPU-intensive, memory-intensive, IO-intensive — e.g., heavy reports, analytics, AI)
   YES → Silo compute OR per-tenant queue partition + rate limit.

3. Is this service in the hot path for every tenant request?
   YES → Pool (for cost) with strict isolation primitives.
   NO → either; preference Pool for simplicity.

4. Is this service tier-differentiated?
   YES → Silo for premium, Pool for basic — Hybrid pattern within the service.

5. What is the per-tenant cost of this service?
   High → consider Silo for billing transparency.
   Low → Pool for cost.

6. What is the blast radius if this service fails?
   Catastrophic (e.g., auth) → Pool with extreme reliability investment.
   Tenant-bounded (e.g., a tenant's reports) → Silo bounds blast.
```

## Examples Across Industries

| SaaS type | Recommended model | Why |
|---|---|---|
| Generic B2B SaaS (CRM, project mgmt) | Mixed Mode (default) | Most services pool, sensitive optional silo |
| Healthcare SaaS (EHR-adjacent) | Mixed Mode with siloed PHI storage | HIPAA per-tenant on PHI |
| Banking / fintech SaaS | Full Stack Silo (often) | Strict compliance + per-tenant audit |
| B2C consumer app (millions of users) | Full Stack Pool | Scale + cost margin demands it |
| Global B2B SaaS | Pod (region-based) | Data residency + latency |
| Vertical SaaS for SMB | Mixed Mode | Single-region, mid-thousands of tenants |
| Marketplace / multi-sided SaaS | Mixed Mode | Different sides have different isolation needs |

## Stack-Specific Notes

### Kubernetes-based SaaS
- Silo = namespace per tenant.
- Pool = shared deployments with tenant-routing.
- Pod = K8s cluster per pod (or namespace clusters per region).
- See `kubernetes-saas-delivery` for ArgoCD + progressive delivery patterns.

### Serverless SaaS (Lambda / Cloud Functions)
- Pool is natural (functions scale per-invocation).
- Silo via per-tenant function alias or per-tenant API Gateway.
- See Golding Ch.12 (Serverless SaaS) for canonical patterns.

### Monolith SaaS (PHP / Rails / Django on single app server)
- Pool default; Silo via separate app server + DB per tenant when needed.
- Mixed mode harder to implement without going microservice.

## Anti-Patterns

- Picking Silo "because it feels safer" without quantifying ops cost.
- Picking Pool "because of margins" while ignoring noisy-neighbor risk.
- Refusing to evolve — Pool to Pod transition is a normal scaling step, not a redesign.
- Mixed-mode without documenting which services are silo vs pool — new engineers ship to the wrong half.
- Full-stack-silo as license to customize per tenant — that's MSP, not SaaS.

## See Also

- `saas-deployment-models` — parent skill.
- `multi-tenant-saas-architecture` — isolation patterns at the data layer.
- `kubernetes-saas-delivery` — K8s-specific silo/pool.
- `infrastructure-as-code` — IaC patterns for silo provisioning.
- Golding *Building Multi-Tenant SaaS Architectures* Ch.3.
