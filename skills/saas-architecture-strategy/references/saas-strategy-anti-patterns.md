# SaaS Architecture Anti-Patterns

Most SaaS architectures fail in a small number of recurring ways. This reference catalogues the patterns, the tells that surface them on paper, and the repairs.

## 1. The Hosted-Pretending-to-Be-SaaS

**Pattern.** A single-tenant product is deployed N times for N customers and called SaaS.

**Tells.**
- Each customer has a dedicated environment by default, regardless of size.
- Upgrades are coordinated per-customer.
- The on-call team must know which customer is on which version.
- The cost-to-serve scales linearly with customer count.

**Repair.** Decide whether the product is genuinely SaaS or a managed-hosting offering. If SaaS, define a target tenancy pattern and migrate at least the long-tail and SME tiers to it. Hosted offerings can coexist for tier A but must not define the platform.

## 2. One Tenancy Pattern Across All Capabilities

**Pattern.** A single decision ("we are pooled multi-tenant") is applied to every capability in the platform.

**Tells.**
- Regulated capabilities and stateless utilities have the same isolation level.
- Customisation requests are refused or stuffed into shared code.
- A single noisy tenant can degrade a regulated capability.

**Repair.** Run the per-capability tenancy decision in the capability map. Expect a heterogeneous answer: pooled for stateless utility, bridge for storage-heavy, siloed for regulated or differentiating capabilities under tier-A demand.

## 3. Designing for the Largest Tenant

**Pattern.** Architecture is shaped by the requirements of the biggest enterprise prospect, then deployed to all tenants.

**Tells.**
- Onboarding takes days because every tenant gets a siloed deployment.
- The cost-to-serve makes the long tail unprofitable.
- SME and long-tail tenants pay for isolation they do not need.

**Repair.** Tier the architecture. Tier-A gets the heavy isolation; long tail gets the pool. The platform serves both because the patterns differ, not because everyone gets the heavy version.

## 4. Auto-Scaling as a Capacity Plan

**Pattern.** Capacity planning is replaced with "we'll auto-scale."

**Tells.**
- No documented headroom margin.
- No leading-indicator metrics for scaling decisions.
- Scaling is reactive to CPU.
- Cell or shard sizing is not bounded.

**Repair.** Treat auto-scaling as a smoothing mechanism, not a sizing strategy. Compute target capacity, plan headroom for failover and burst, scale on leading indicators (queue depth, request rate), and bound cells.

## 5. Bespoke Code in the Shared Codebase

**Pattern.** Enterprise customisation accumulates as feature flags and conditional branches in the shared platform.

**Tells.**
- Files contain conditionals keyed to specific tenant IDs.
- Test matrices grow per enterprise customer.
- Refactoring the shared platform requires consulting per-tenant owners.
- The shared codebase becomes the slowest-moving part of the system.

**Repair.** Define a tenant extension surface (plugins, scripted hooks, webhooks, sidecars). Move existing bespoke logic out by tenant; refuse new bespoke code in the shared path. Set a sunset for any remaining tenant-keyed conditionals.

## 6. Logical Multi-Tenancy with Operational Single-Tenancy

**Pattern.** The data model has a tenant ID column, but operations (deployment, on-call, SLO, support) are conducted per-tenant.

**Tells.**
- One tenant's incident is a global outage.
- Releases are gated on the most-conservative tenant.
- The operations team holds tenant-specific runbooks.
- SLOs cannot be reported in aggregate because each tenant has bespoke targets.

**Repair.** Decide whether the goal is operational multi-tenancy. If yes, unify deployment, SLO, and on-call across the pooled tenants; separate tier-A out into a different operating regime. If no, stop calling the architecture multi-tenant.

## 7. Residency, Isolation, and Identity Conflated

**Pattern.** A single tenancy decision is assumed to satisfy residency, isolation, and identity simultaneously.

**Tells.**
- Residency is satisfied by region pinning, but identity is global, breaking residency for tokens.
- Isolation is at the storage layer, but compute is shared without tenant rate limits.
- Identity tenancy is shared, but residency requires data not leaving a region.

**Repair.** Decide each axis separately. Identity, residency, and isolation can have different boundaries. Document each per capability.

## 8. Sales-Driven Architecture Drift

**Pattern.** Sales commits to a tier-A prospect on terms (custom integration, dedicated SLA, in-region deployment) the architecture does not support; the architecture is then reshaped after signature.

**Tells.**
- The platform's tenancy patterns shift after each large deal.
- The capability map is months out of date.
- Architecture decisions are presented as fait accompli to engineering.
- Engineering velocity drops mid-quarter without a strategy reason.

**Repair.** Pre-publish the tier-A acceptance criteria: what bespoke commitments are accepted, in which form (extension, sidecar, or contract), at what cost. Sales sells inside that envelope. Out-of-envelope deals require an explicit strategy decision, not a silent architecture rewrite.

## 9. Cost Surprises

**Pattern.** Cloud bills exceed expectations by multiples; architecture review treats cost as out of scope.

**Tells.**
- No per-SBB cost estimate at design time.
- Egress is not a named architectural input.
- Managed services are chosen on convenience without unit-economic comparison.
- Reserved capacity is locked for tenants that have churned.

**Repair.** Bring cost into design as a first-class input. Estimate per-SBB and per-tier cost at design time; track actuals; revisit on a cadence. Sunset reserved capacity tied to churned tenants.

## 10. Blast-Radius Folklore

**Pattern.** The architecture claims tenant isolation that has never been tested.

**Tells.**
- No documented isolation boundary per shared resource.
- No drills (tenant kill, cell loss, region loss, hot key).
- Incidents reveal tenants affecting tenants the design said were isolated.
- The phrase "should be isolated" appears in the design doc.

**Repair.** Name the boundary per shared resource. Run the drills. Update the design when drills reveal the documented isolation is not real. Replace "should be isolated" with "isolated at <boundary>, last verified on <date>."

## Cross-Cutting Tells

These signals can surface any of the patterns above:

- The architecture diagram has not changed even though the tenant tier mix has.
- "Multi-tenant" is used without naming what is shared and what is isolated.
- The on-call team cannot draw the cell topology from memory.
- New capabilities are added without updating the capability map.
- The design document and the running system have diverged and no one is tracking the delta.

## Detection Routine

Before signing off on a SaaS architecture or a major change to one, walk this checklist:

- [ ] Capability map is current and lists every ABB.
- [ ] Tenancy decision is per capability, not global, with named tradeoffs.
- [ ] Tier matrix exists; long-tail through tier-A defaults are documented.
- [ ] IaaS assumptions are listed and mitigated.
- [ ] Blast radius per shared resource is named and bounded.
- [ ] Cells (if used) have bounded capacity and a tested control plane.
- [ ] Customisation surface is named; bespoke code is contained.
- [ ] Cost is estimated per SBB and per tier.
- [ ] Operating model can run the architecture at the planned mix.
- [ ] Drills are scheduled and the most recent results are documented.

Any unchecked item is an open risk surfaced before launch, which is much cheaper than after.
