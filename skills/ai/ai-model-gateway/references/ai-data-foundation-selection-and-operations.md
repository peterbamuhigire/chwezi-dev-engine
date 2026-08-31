# AI Data Foundation Selection and Operations

This reference is a self-contained operational synthesis prepared from Sanjeev
Mohan, *Designing the AI-Driven Data Foundations: Architecture, Principles, and
Practice*. It is a decision aid, not a vendor catalogue or a substitute for
current product, regulatory, or residency verification.

## Selection frame

Evaluate a candidate foundation against the workload and data product, then
score the following dimensions with evidence:

| Dimension | Questions to answer |
|---|---|
| Architecture | Is it modular, interoperable, distributed where needed, and free of accidental lock-in? |
| Availability | What are the failure domains, backup/restore paths, control-plane dependencies, and service objectives? |
| Scale and performance | Which dimension scales, what is measured, and how do indexing, compression, concurrency, and latency tiers behave? |
| Access | How do humans, programmes, agents, semantic layers, and APIs use the data? |
| Trust | How are quality, identity, encryption, privacy, sovereignty, audit, and lineage enforced? |
| Operations | How are deployment, migration, lifecycle, observability, capacity, and cost managed? |
| Exit | What is portable, what is proprietary, and what is the tested migration route? |

## AI-ready data contract

For every data product, define context, unity across sources, freshness, domain
correctness, governance, ownership, access policy, lineage, quality checks, and
feedback. Treat latency as a potential accuracy issue when the decision depends
on current data. Keep data contracts and semantic definitions versioned.

## Operating loop

Observe infrastructure, pipelines, data quality, model or agent behaviour, and
session-level cost. Attribute failures to the stage that introduced them. Use
the smallest repair, replay or rollback that restores a known-good state, then
feed the lesson into the contract, test set, or ownership map.
