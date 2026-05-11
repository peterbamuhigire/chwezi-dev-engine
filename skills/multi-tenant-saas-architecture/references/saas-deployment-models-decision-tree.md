# SaaS Deployment Models — Decision Tree (Reference)

For full coverage, see the dedicated skill `saas-deployment-models`. This file is the quick-reference table.

## Five Models

| Model | Compute | Storage | Best For |
|---|---|---|---|
| **Full Stack Silo** | Per-tenant | Per-tenant | Strict compliance, legacy lift-and-shift, premium tier |
| **Full Stack Pool** | Shared | Shared (+ RLS) | B2C scale, margin-sensitive, simple ops |
| **Mixed Mode** | Per service | Per service | **Default for production B2B SaaS** |
| **Hybrid Full Stack** | Pool basic, silo premium | same | Two-tier business model with clear premium |
| **Pod** | Per-pod group | Per-pod group | Scale > 10k tenants, geography, bounded blast |

## Decision Rules (in order)

1. Any tenant has strict per-tenant regulatory boundary (HIPAA, PCI-per-tenant, sovereign EU data) →
   **Full Stack Silo** for those tenants (Hybrid if mixed; Mixed if only certain services).

2. Migrating a legacy single-customer codebase to SaaS quickly →
   **Full Stack Silo** as starting point; refactor toward Mixed Mode over 12-24 months.

3. > 10,000 tenants expected →
   **Pool or Pod** (Pool if no geography/residency; Pod if either).

4. Clear premium tier ($50K+ ACV) with isolation expectations →
   **Hybrid Full Stack** OR **Mixed Mode** with siloed premium services.

5. Default for new B2B SaaS →
   **Mixed Mode** — start pooled, silo as compliance / noisy-neighbor demands.

## Per-Service Silo/Pool Map (Default for B2B Mixed Mode)

| Service | Compute | Storage | Why |
|---|---|---|---|
| API gateway | Pool | n/a | Routes by tenant context |
| Auth service | Pool | Pool (RLS) | Cross-tenant identity OK |
| Tenant core service | Pool | Pool | Hot path |
| Reporting engine | Pool (autoscale per tier) | Pool | Isolated workers per request |
| Document storage | Pool | Pool (per-tenant prefixes) | Cheap to silo if needed |
| Search index | Pool | Pool (per-tenant indexes) | Per-tenant indexes when scale demands |
| Financial ledger | Pool compute | **Silo storage** | Strict isolation for audit/compliance |
| AI / LLM workers | Pool | Pool | Per-tenant rate limits |
| Heavy analytics | Pool (queue partition per tenant) | Pool | Noisy-neighbor controlled by partition |
| Email worker | Pool | Pool | Per-tenant suppression list |

## What the Choice Drives

- **Routing layer:** silo needs per-tenant ingress; pool routes by JWT/subdomain.
- **Deployment automation:** silo = rolling waves; pool = single shot + canary.
- **Cost attribution:** silo = native cloud per-tenant; pool = apportionment.
- **Onboarding latency:** silo = minutes (provisioning); pool = seconds.
- **Blast radius:** silo = naturally bounded; pool = global; pod = per-pod.

## Migration Paths

- Pool → Mixed: silo noisy/regulated services; rest stay pool.
- Pool → Hybrid: add premium tier with siloed stacks.
- Mixed → Pod: split big pool by tenant size / geography.
- Silo → Pool: rare; usually needs better isolation primitives first.

## See Also

- `saas-deployment-models` — full skill.
- Golding, *Building Multi-Tenant SaaS Architectures*, Ch.3.
