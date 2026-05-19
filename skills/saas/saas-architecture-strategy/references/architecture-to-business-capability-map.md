# Architecture to Business Capability Map

Architecture decisions made without an explicit map to business capabilities tend to over-invest in the visible and under-invest in the regulated, the differentiating, or the long-lived. This reference encodes the rules for producing and using the map.

## What "Business Capability" Means Here

A business capability is a *what the business does for its customers*, named in business language and stable across implementation changes. Examples:

- "Onboard a new tenant within 24 hours."
- "Issue a usage-based invoice on a configurable cycle."
- "Allow a customer admin to provision and revoke seats."
- "Provide region-resident storage for regulated data."

Capabilities are not features, screens, or services. A capability is durable; the implementation underneath it can be replaced without changing the capability name.

## Why the Map Matters

Without the map:

- Architecture investment skews toward the most visible component (often the front-end), under-funding regulated or shared back-end capabilities.
- Tenancy decisions are made globally instead of per capability, producing one-size-fits-none architectures.
- Build-vs-buy decisions miss the differentiation question.
- Sunsetting becomes politically difficult because no one knows which capability a system actually serves.

With the map, every architectural building block (ABB / SBB) has a named purpose, and the cost of changing it is visible.

## Producing the Map

1. **List capabilities at consistent altitude.** Not "system handles auth" (too low) and not "we serve customers well" (too high). Aim for 15-40 capabilities for a typical SaaS.
2. **Score each capability on three axes.**
   - **Differentiation.** Is this capability a reason customers choose us, or a commodity?
   - **Regulatory weight.** Is this capability subject to compliance, residency, audit?
   - **Customisation pressure.** Do tier-A tenants demand bespoke behaviour here?
3. **Map ABBs to capabilities.** Each ABB should serve at least one capability; capabilities with no ABB are gaps; ABBs serving no capability are candidates for sunset.
4. **Map SBBs to ABBs.** Concrete components implementing logical building blocks. One ABB may have multiple SBBs across regions or tiers.
5. **Annotate each SBB with its tenancy pattern, isolation level, and expected lifespan.**

## Using the Scores

The three scores drive architectural choices:

| Differentiation | Regulatory | Customisation | Default Strategy |
|---|---|---|---|
| High | Any | Any | Build, own, isolate code path; protect roadmap. |
| Low | High | Any | Buy or use managed; isolate at the boundary required by regulation. |
| Low | Low | Low | Buy or use commodity; pool aggressively. |
| Low | Low | High | Buy a configurable platform or build an extension surface; do not embed customisation in shared code. |
| High | High | Any | Build, isolate, and design the audit surface explicitly; this is usually the most expensive quadrant. |

## Differentiation: The Hardest Score to Get Right

Differentiation is not "we built this in-house." It is "customers would notice and care if this changed." Tests:

- Would removing this capability cost a deal?
- Do prospects mention it in evaluations?
- Does it appear in the product's competitive positioning?
- Has it driven measurable retention?

A capability with no positive answer is not differentiating, regardless of how much engineering investment it has absorbed.

## Regulatory Weight Is Specific

Regulatory weight is not "data is sensitive." It is a named regime (HIPAA, GDPR, SOC 2 controls, regional residency, sectoral rules) with named requirements. For each regulated capability:

- Name the regime.
- Name the controls the architecture must satisfy.
- Name the audit artefact the capability must produce.
- Name the residency or isolation boundary required.

Regulatory weight forces tenancy patterns from pooled toward bridge or siloed in specific places, regardless of what the rest of the platform does.

## Customisation Pressure Without Drift

Customisation pressure is healthy when it is contained. The map names *where* customisation is permitted:

- **Permitted in shared code (configuration, feature flags).** Cheapest, most dangerous; allow only when the customisation surface is small, well-understood, and shared across many tenants.
- **Permitted in tenant-scoped extensions.** Plugins, scripts, webhooks; the platform exposes a stable surface and contains the bespoke logic.
- **Permitted in tenant sidecars.** Per-tenant deployments alongside the shared platform; expensive but contained.
- **Permitted only via the public API.** The tenant builds it; the platform owes only the API.

For each customisation-pressure capability, name the permitted location. Without this, customisation drifts into shared code by default.

## Capability Lifespan and Sunsetting

Each capability has a lifespan. Tag capabilities as:

- **Growing.** Investment is increasing; expect new SBBs and tenancy refinement.
- **Steady.** Maintenance mode; protect against drift, do not over-invest.
- **Declining.** Usage is shrinking; plan a sunset path.
- **Sunset.** Active deprecation; named owner and date.

Architectural investment should match lifespan. Investing heavily in declining capabilities or under-investing in growing ones is a frequent strategic error visible only when the map is explicit.

## Map Maintenance

The map is a living artefact:

- Reviewed quarterly at minimum.
- Updated whenever a new capability is launched, deprecated, or materially refactored.
- Linked from the product roadmap and the architecture decision records.
- Owned by a single named architect or technical lead.

A map that is more than two quarters out of date is misleading and is worse than no map. If maintenance lapses, mark it as out of date and treat it as advisory until refreshed.

## Output Shape

For each capability:

- Name (business language).
- Differentiation score (high / medium / low) with one-line justification.
- Regulatory regime and controls (or "none").
- Customisation pressure (high / medium / low) and permitted location.
- ABBs serving the capability.
- SBBs realising each ABB, with tenancy pattern, isolation level, expected lifespan.
- Lifespan tag (growing / steady / declining / sunset).

The output is a single table or document, not a diagram. Diagrams obscure the scoring; the scoring is the map's value.
