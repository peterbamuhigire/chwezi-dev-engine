# Scaling and Blast Radius

Scaling and blast radius are usually treated as separate concerns. They are the same concern viewed from two angles: how much load the system can absorb without losing tenants, and how much damage a single failure or noisy tenant can do to the rest. This reference encodes operational rules for designing them together.

## Four Axes of Scaling

Distinguish these and size each independently:

1. **Capacity.** How many tenants, requests, or stored objects the system can hold at steady state.
2. **Throughput.** How fast it can move work through (requests/sec, events/sec, jobs/min).
3. **Concurrency.** How many simultaneous in-flight operations it supports per tenant and globally.
4. **Burst.** How large a spike, of what duration, the system can absorb without degradation.

A system can be capacity-rich and burst-poor (a database with vast storage but low connection count), or throughput-rich and concurrency-poor (a streaming pipeline with high event/sec but a small number of in-flight tenants). Size each axis per SBB and per tenant tier.

## The Blast-Radius Question

For every shared resource, ask: *if a single tenant misbehaves or a single component fails, how many other tenants notice?*

A SaaS architecture without an answer to this question has a blast radius of "all tenants" by default.

### Blast-Radius Levels

| Level | Description | Typical Fit |
|-------|-------------|-------------|
| Global | One tenant or failure affects all tenants | Acceptable only for stateless utility tiers |
| Regional | Affects all tenants in a region | Acceptable for residency-aligned shapes |
| Cell | Affects tenants in one pool/cell | Default for bridge architectures |
| Tenant | Affects only the originating tenant | Required for siloed tier-A capabilities |

Pick the highest blast radius the SLA tolerates, not the lowest the architecture supports — over-isolation has its own cost.

## Cell-Based Architecture as the Default Bridge

Cells (pool of pools) are the practical compromise for most SaaS:

- A cell is a fully self-contained deployment of the platform sized for N tenants.
- Tenants are assigned to a cell on onboarding by some routing key.
- Cells are upgraded, scaled, and incidented independently.
- Cross-cell coordination happens only at the platform-control plane (billing, identity, central reporting).

Rules for cells:

- **Cell capacity is bounded and known.** A cell with unlimited capacity is just a pool.
- **Cell sprawl is managed.** Every new cell costs ops; the rate of cell creation should be predictable.
- **Cells fail individually.** A cell failure should not cascade to other cells; the control plane must survive any single cell loss.
- **Tenants can be moved between cells.** Without this, cells become unbalanced and unmovable tenants accumulate.

## Isolation Boundaries

Isolation is enforced at boundaries; without enforcement, isolation is folklore. Common boundaries:

- **Process / container.** Light isolation; vulnerable to noisy neighbours sharing the host.
- **VM / instance.** Strong CPU/memory isolation; weaker network isolation.
- **Account / project.** Strong administrative isolation, including IAM and quotas.
- **Network segment / VPC.** Strong network isolation; meaningful for east-west blast containment.
- **Region.** Strongest practical isolation, including provider-side failure domains.

Map every named isolation guarantee to a specific boundary. "Isolated" without naming the boundary is a marketing claim, not an architectural one.

## Quotas, Throttles, and Backpressure

Without per-tenant quotas, a single tenant defines the platform's worst case.

- **Hard quotas.** Refuse work above the limit. Required for any pooled resource where excess work degrades others.
- **Soft quotas.** Warn and continue; useful for billing-aligned signals.
- **Token-bucket rate limits.** Smooth bursts within a budget.
- **Backpressure.** Slow producers when consumers are saturated; required for queue-based pipelines.
- **Tenant-aware admission control.** Reject new work for one tenant while accepting for others.

Quotas live at the boundary, not in the application. An application-level quota is a polite suggestion.

## Scaling Failure Modes to Anticipate

Most scaling outages share a small number of root causes:

- **Coordinated retry storms.** Clients retry on failure; without jitter and budgets, the retries become the outage.
- **Connection pool exhaustion.** A downstream slowdown saturates upstream pools, propagating failure.
- **Hot tenant.** A single tenant's traffic dominates a shared resource.
- **Hot key.** A single key dominates a partitioned store.
- **Queue runaway.** A consumer slowdown grows the queue faster than capacity can be added.
- **Stampede on cache miss.** Coordinated re-population of cold cache overwhelms origin.
- **Failover overshoot.** Failover succeeds but the surviving capacity cannot hold the combined load.

For each, the architecture must state the mitigation: jitter + budgets, per-tenant pool caps, tenant rate limits, key sharding, queue admission control, request coalescing on cache miss, and capacity headroom that includes the failover case.

## Capacity Planning Cadence

Capacity is a moving target. Plan it on a cadence:

- **Weekly:** monitor leading indicators (queue depth, p99, saturation).
- **Monthly:** trend review; project 90 days forward.
- **Quarterly:** revise tier mix assumptions, recompute target deployment.
- **On material tenant onboard:** re-run capacity for affected cells.
- **On incident:** capture the actual breaking point; update headroom assumptions.

A capacity plan that is only revised on incident is a capacity plan that lives downstream of outages, not upstream.

## Blast-Radius Drills

Test blast-radius claims with deliberate exercises:

- **Tenant kill.** Simulate a tenant exhausting its quota; confirm others are unaffected.
- **Cell loss.** Take a cell offline; confirm other cells continue and the control plane survives.
- **Region loss.** Exercise the documented RTO/RPO; record actual numbers.
- **Hot-key drill.** Drive synthetic traffic at a single key; confirm shedding works.

Drills that are never run define the boundary at which the platform's blast-radius claims become fiction.

## Output

The scaling-and-blast-radius output for the design is:

- Per-SBB capacity, throughput, concurrency, burst targets.
- Named blast-radius level per shared resource.
- Cell strategy (size, count, growth rule, control plane).
- Quotas and backpressure surfaces.
- Failure-mode mitigations with a named owner each.
- Drill schedule and most recent results.

This output is reviewed on the same cadence as capacity planning, not just at design time.
