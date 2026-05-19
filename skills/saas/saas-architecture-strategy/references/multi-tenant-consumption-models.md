# Multi-Tenant Consumption Models

Multi-tenancy is not one decision; it is one decision *per business capability* repeated across the product. This reference encodes the operational rules for picking tenancy patterns and matching them to enterprise consumption profiles.

## The Three Tenancy Patterns

| Pattern | Compute | Storage | Identity | Typical Cost Per Tenant | Typical Isolation |
|---|---|---|---|---|---|
| Pooled | Shared | Shared (logical separation by tenant ID) | Shared directory | Lowest | Logical only |
| Siloed | Dedicated | Dedicated | Dedicated or federated | Highest | Physical |
| Bridge | Shared compute, dedicated storage (or vice versa) | Mixed | Shared with per-tenant scoping | Medium | Partial physical |

There is no globally correct answer. The pattern is selected per capability and per tenant tier.

## Consumption Tiers

Most SaaS products serve a heterogeneous tenant base. Segment the base into tiers before choosing patterns.

### Tier A: Large Enterprise / Vertical

- Bespoke integrations expected.
- Residency, audit, and isolation often regulated.
- Negotiated SLAs, named support contacts.
- Volume per tenant is high; count of tenants is low.
- Default tenancy: **siloed** for regulated capabilities, **bridge** for everything else.

### Tier B: Mid-Market

- Standard integrations with some configuration.
- Residency by region rather than by tenant.
- Standard SLAs.
- Default tenancy: **bridge** for storage-heavy capabilities, **pooled** for stateless capabilities.

### Tier C: SME

- Self-serve onboarding.
- No bespoke integrations.
- Shared regional residency.
- Default tenancy: **pooled** across the board, with per-capability bridge only when storage isolation is unavoidable.

### Tier D: Long Tail

- Self-serve, free or low-cost.
- No residency or isolation negotiation.
- Acceptable to share heavily; cost per tenant must be minimal.
- Default tenancy: **fully pooled**, including identity.

A SaaS that serves all four tiers with the same tenancy pattern is either over-engineered for the long tail or under-engineered for the enterprise.

## Selection Rules

For each capability, walk these gates in order. The first gate that triggers sets the floor for tenancy pattern.

1. **Regulatory floor.** Does any tier have a regulatory requirement (residency, audit isolation, encryption-key tenancy) that forbids pooling? If yes, that tier must be siloed or bridged for this capability.
2. **Blast-radius floor.** Could a single tenant's behaviour in this capability degrade other tenants in a way the SLA cannot tolerate? If yes, isolate at least at the tier where the SLA bites.
3. **Customisation floor.** Does any tier require capability behaviour that diverges from the shared default? If yes, isolate the divergent code path, not the whole capability.
4. **Cost ceiling.** Below which tier does the per-tenant cost of siloed deployment exceed the per-tenant revenue? Below that line, do not silo.
5. **Operational ceiling.** Below which tier can the operating model not afford per-tenant deployments, upgrades, or on-call? Below that line, do not silo.

The intersection of floor and ceiling defines the eligible patterns. Pick the cheapest eligible pattern that satisfies the floors.

## Bridge Pattern Variants

Bridge is the workhorse of mid-market SaaS. Common variants:

- **Shared compute, dedicated database.** Compute scales pooled; storage isolation per tenant or per cohort. Good for capabilities with heavy data customisation.
- **Shared database, dedicated compute.** Compute isolation per tenant or cohort; data shared with tenant ID. Good for capabilities where compute behaviour is the noisy neighbour.
- **Pool of pools.** Tenants assigned to one of N pooled cells; cells scale independently. Good for limiting blast radius without per-tenant deployment cost.
- **Shared with per-tenant key.** Encryption per tenant on shared infrastructure. Good for residency-light, cryptographically-strong isolation.

## Custom Integrations Without Breaking the Platform

Enterprise tenants often demand bespoke integrations. The question is not whether to allow them, but where they live.

- **Inside the shared codebase** (configuration, feature flags): cheapest, but accumulates conditional logic and erodes the platform.
- **As tenant-scoped extensions** (plugins, webhooks, scripted hooks): contained, but requires an extension surface designed in advance.
- **As sidecar services** (per-tenant deployment of bespoke logic alongside the shared platform): expensive, but contained and revertible.
- **As tenant-owned external integration** (the tenant's own systems integrate via the public API): cheapest for the platform, requires a stable public API.

Default policy: bespoke integrations live in tenant-scoped extensions or tenant-owned external systems, not in the shared codebase. Exceptions require a named owner and a sunset date.

## Identity, Residency, Metering

These three orthogonal axes are often conflated with tenancy.

- **Identity tenancy** can be pooled even when storage is siloed (single SSO with tenant scoping).
- **Residency** is about *where* data lives, not *whose* infrastructure. Residency can be satisfied with pooled tenancy across regional cells.
- **Metering** is about *what* the tenant is billed for. Pooled architectures still need per-tenant accounting; siloed architectures still need cross-tenant aggregation for the business.

Decide each axis explicitly. Inheriting all three from the tenancy decision produces architectures that over-isolate or under-isolate one of them.

## Tradeoff Matrix

| Concern | Pooled | Bridge | Siloed |
|---|---|---|---|
| Per-tenant cost | Low | Medium | High |
| Blast radius | Wide | Bounded by cell | Single tenant |
| Upgrade complexity | Low | Medium | High |
| Customisation room | Low | Medium | High |
| Regulatory ease | Hardest | Medium | Easiest |
| Onboarding speed | Fastest | Fast | Slowest |
| Operational load | Lowest | Medium | Highest |

Use this matrix to defend the per-capability decision in review. A decision that does not name which row is being optimised against which is not yet a decision.
