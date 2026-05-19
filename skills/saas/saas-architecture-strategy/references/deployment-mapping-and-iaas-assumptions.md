# Deployment Mapping and IaaS Assumptions

Cloud SaaS architectures sit on top of IaaS, and most architectural failures are actually unstated IaaS assumptions. This reference encodes the rules for translating architectural building blocks into deployable IaaS configuration without leaving capacity, isolation, or cost as an exercise for production.

## Building Block Vocabulary

Use the architecture/building-block separation explicitly, even informally:

- **ABB (Architecture Building Block).** A logical capability: "tenant identity," "ingest pipeline," "billing meter."
- **SBB (Solution Building Block).** A concrete realisation: "Keycloak cluster behind ALB," "Kafka topics with N partitions," "metering service writing to time-series DB."

Every SBB has a *minimum deployment configuration* and a *target deployment configuration*. The minimum is what makes it functionally complete; the target is what supports the planned scale and tier mix. Both are documented before infrastructure is provisioned.

## What Hypervisors and IaaS Actually Guarantee

Architectures often assume properties that IaaS does not guarantee. Treat the following as default-false unless explicitly contracted:

- **Noisy-neighbour isolation.** Shared-tenant VMs, containers, and managed services exhibit performance variability under load on the same host. CPU credits, burstable instances, and shared NICs all leak.
- **Auto-scaling speed.** Auto-scaling is reactive and slow relative to traffic spikes; it is not a substitute for headroom.
- **Auto-provisioning correctness.** New capacity boots with default configuration; tenant-aware state must be re-hydrated, which takes time.
- **Cross-AZ symmetry.** Latency, capacity, and pricing differ across availability zones; pretending they are interchangeable causes failover surprises.
- **Single-region durability.** A single region is a single failure domain regardless of how many AZs sit inside it.
- **Identity propagation.** Cloud IAM does not transparently extend into the application's tenant model.

State each assumption in the design and name how it is mitigated.

## Sizing the Minimum Deployment

For each SBB, document the minimum configuration along these axes:

1. **Compute floor.** Smallest instance count, type, and CPU/memory per instance that supports the SBB's invariants (quorum, leader election, replication).
2. **Storage floor.** Minimum durable storage class, replication factor, and snapshot policy.
3. **Network floor.** Required ingress/egress, internal service mesh, latency budget to peer SBBs.
4. **State recovery floor.** Time to bring the SBB back from cold; what state is needed and from where.
5. **Identity floor.** What identity surface the SBB requires (machine identity, service-to-service auth, tenant-scoped tokens).

A SBB that cannot be deployed below a certain footprint defines the minimum cost of running the platform. That number drives the long-tail tenancy decision.

## Sizing the Target Deployment

Target sizing is a function of:

- **Concurrent tenants** and **per-tenant peak load**.
- **Tier mix** (a heavy mid-market tenant may exceed twenty long-tail tenants).
- **Failure domain budget** (how many AZ losses must be survived without degradation).
- **Headroom margin** (how much spare capacity is needed because auto-scaling is too slow).

Target = (sum of expected load) × (1 + headroom) × (failure domain factor) ÷ (per-instance capacity).

Document each input. Recompute when tier mix or peak assumptions change.

## Load Balancing as Architectural, Not Infrastructural

Load balancers are not just IaaS — they are architectural decisions:

- **L4 vs L7.** L7 enables tenant-aware routing (essential for bridge and siloed bridge variants).
- **Sticky sessions.** Stickiness simplifies the application but couples tenant identity to a node, hurting failover.
- **Per-tenant rate limits.** Without these, the load balancer becomes the blast-radius weak link.
- **Health checks.** Tenant-aware health (a node may be healthy globally but degraded for a specific tenant) is rare in default LB configurations and must be added.

State the LB tier (L4/L7), stickiness, rate-limit strategy, and tenant-aware health as part of the SBB definition.

## Auto-Scaling Honestly

Auto-scaling is useful but not magical. Rules:

- **Scale on leading indicators.** Scale on queue depth, request rate, or pending-work — not CPU. CPU lags.
- **Scale-out is asymmetric.** Scaling out is slower than scaling in. Reserve enough warm capacity to survive the scale-out latency.
- **Cold starts are real.** Containers, JVMs, and database connection pools take time to warm. Account for it explicitly.
- **Scaling does not heal noisy neighbours.** Adding instances does not isolate tenants; it spreads them across more hosts.
- **Tenant-aware scaling.** For bridge / pool-of-pools, scaling decisions are per cell, not global. Global auto-scaling on a cellular architecture is a footgun.

If the platform relies on auto-scaling to make tenant tier economics work, write the auto-scaling policy in the design and review it on the same cadence as capacity planning.

## Region and AZ Topology

For each SBB:

- **Single AZ?** Acceptable only for stateless dev/test or for SBBs whose loss is masked by a higher-level failover.
- **Multi-AZ in one region?** Default for most SBBs. Quorum-based systems need three AZs.
- **Multi-region active-active?** Expensive; required for global low-latency reads or cross-region residency.
- **Multi-region active-passive?** The pragmatic compromise; document RPO and RTO and rehearse them.

Residency requirements often dictate region topology more than performance does. Map residency-to-region first, then layer performance and availability on top.

## Cost as an Architecture Input

IaaS cost shape changes the architecture, not just the budget. Rules of thumb:

- **Egress dominates.** Cross-region and cross-cloud egress is the largest variable cost in many SaaS shapes; design data placement to minimise it.
- **Idle is rarely free.** Reserved capacity for tier-A tenants in a siloed pattern costs whether or not the tenant is active.
- **Managed services trade cost for ops.** Managed databases, queues, and caches reduce ops load but raise marginal cost; size the tradeoff per SBB.
- **Per-request pricing is non-linear.** At scale, per-request managed services can exceed self-hosted equivalents; track the crossover point.

Document expected steady-state cost per SBB and per tenant tier. Surprises in cloud bills almost always trace to an architectural decision made without a cost input.

## Deployment Mapping Output

For each capability:

- ABB → SBB list.
- For each SBB: minimum deployment, target deployment, region/AZ topology, LB strategy, auto-scaling policy, identity surface, expected cost.
- Named IaaS assumptions and how each is mitigated.

This output is the bridge between the tenancy decision and the operations runbook. Without it, the architecture is a diagram, not a deployable system.
