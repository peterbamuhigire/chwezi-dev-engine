# Practical Architecture Knowledge

This file is self-contained. It was prepared from local EPUB study notes and
must remain useful even if the EPUBs are deleted.

Source inputs: local EPUBs under `C:\Users\Peter\Downloads\Documents\`:
`Software Architecture Metrics.epub`, `Learning Domain-Driven Design.epub`,
`Mastering API Architecture.epub`, `Foundations of Scalable Systems.epub`,
and `Software Architecture for Developers.epub`.

Use this reference when architecture work needs stronger practical judgment on
boundaries, design documentation, measurable quality, and scalability tradeoffs.

## Architecture Decision Frame

Before proposing structure, separate the decision into 4 layers:

| Layer | Question | Evidence to collect |
|-------|----------|---------------------|
| Business capability | What durable business job changes independently? | workflows, policies, invariants, ownership |
| Domain model | Which concepts must stay linguistically consistent? | glossary, ubiquitous language, state transitions |
| Runtime topology | What must deploy, scale, or fail independently? | load, availability, compliance, team boundaries |
| Fitness measure | How will we know the design is still healthy? | coupling, change lead time, incidents, cost, latency |

Do not let deployment topology define the domain model. A service boundary is
justified only when business ownership, operational isolation, scaling profile,
or release independence pays for the added distributed-systems cost.

## Architectural Drivers

Capture drivers before drawing boxes:

| Driver | What to document | Design effect |
|--------|------------------|---------------|
| Functional scope | user journeys, commands, queries, integrations | capabilities and component responsibilities |
| Quality attributes | performance, availability, security, modifiability, usability, compliance | architecture tactics and tradeoffs |
| Constraints | budget, team skill, hosting, legacy systems, deadlines, regulation | viable options and forbidden options |
| Principles | simplicity, reversibility, buy-before-build, data minimisation | tie-breakers when options are close |
| Technical risks | unknown scale, unfamiliar tech, hard integrations, migration risk | prototypes, spikes, ADRs, test strategy |

Architecture work is not finished until the top risks have an explicit mitigation:
prototype, proof of concept, staged rollout, fallback, monitoring, or decision
deferral with owner and date.

## Domain-Driven Design Checks

- Define bounded contexts around language and policy differences, not database
  tables or UI screens.
- Treat aggregates as consistency boundaries. Keep them small and enforce only
  invariants that must be transactionally true.
- Use domain events for facts that already happened; use commands for requested
  intent that can fail.
- Avoid anemic models when rules are complex. Put behaviour where the invariant
  lives.
- Map upstream/downstream relationships explicitly: customer/supplier,
  conformist, anti-corruption layer, shared kernel, or open-host service.
- Introduce an anti-corruption layer when an external model would leak foreign
  terminology or lifecycle rules into the core domain.

### Strategic DDD Pattern Selection

| Situation | Preferred move |
|-----------|----------------|
| Business rules are core differentiators | invest in explicit domain model and ubiquitous language |
| Rules are simple CRUD around data | transaction script or active record can be sufficient |
| Subdomain is necessary but not differentiating | buy, outsource, or keep generic implementation |
| Two teams use the same words differently | split bounded contexts and map translations |
| External system dominates its own model | use anti-corruption layer |
| Two bounded contexts must evolve together briefly | use shared kernel with strict ownership and tests |
| Downstream team cannot influence upstream | conformist or adapter layer, plus documented risk |

### Tactical DDD Pattern Selection

| Pattern | Use when | Avoid when |
|---------|----------|------------|
| Transaction script | simple workflows, low rule complexity | rules duplicate across scripts |
| Active record | data shape and behaviour are simple and local | persistence concerns hide domain rules |
| Domain model | complex business rules and invariants matter | team cannot sustain modelling discipline |
| Aggregate | transactional consistency boundary is clear | aggregate grows into a whole subsystem |
| Domain service | operation spans entities but belongs to domain | service becomes procedural dumping ground |
| Repository | domain needs collection-like persistence abstraction | it becomes a generic CRUD wrapper only |
| Domain event | downstream reaction to committed fact | caller needs synchronous rejection |
| Event sourcing | audit/history and replay are core requirements | query simplicity is more important than history |

Aggregate checklist:

- Each aggregate has one root.
- External objects reference the root identity, not internal entities.
- One transaction modifies one aggregate unless the invariant truly requires more.
- Cross-aggregate workflows use domain events, process managers, or sagas.
- Aggregate methods enforce invariants; application services orchestrate IO.

## Scalable Systems Checks

- Scale the bottleneck, not the diagram. Identify the constrained resource:
  CPU, IO, locks, database write throughput, third-party API quota, queue
  consumers, or human review.
- Prefer stateless application nodes, explicit state stores, and idempotent
  retries before adding complex orchestration.
- Protect every remote call with timeout, retry budget, circuit breaker or
  degradation path, and observable correlation ID.
- Design cache invalidation with ownership: who writes the truth, who can serve
  stale data, and what user harm happens if stale data leaks.
- Keep write paths boring. Partition, queue, batch, or denormalise only after
  proving the write constraint.
- For eventually consistent flows, define reconciliation jobs and operator
  visibility at design time.

### Scalability Tactics

| Constraint | Tactic | Risk to manage |
|------------|--------|----------------|
| CPU-bound app tier | horizontal scale, stateless nodes, load balancing | session state and uneven distribution |
| Slow reads | cache, read replicas, projections, indexes | stale data and invalidation complexity |
| Slow writes | partitioning, batching, queues, denormalised write model | ordering, retries, data repair |
| Burst traffic | queue buffering, backpressure, rate limits | delayed UX and queue overload |
| Remote dependency latency | timeouts, hedging only when justified, fallback | retry storms and duplicate side effects |
| Large payloads | pagination, streaming, compression, field selection | client complexity and partial failures |
| Global users | CDN, regional reads, data locality strategy | consistency and compliance boundaries |

Distributed systems rules:

- Assume partial failure: one dependency can be slow, unavailable, or split-brain
  while the rest of the system appears healthy.
- Use correlation IDs across synchronous calls, async messages, logs, and audit
  records.
- Make retries bounded, jittered, observable, and idempotent.
- Treat exactly-once delivery as a business outcome created by idempotency and
  deduplication, not as a broker guarantee.
- Design poison-message handling and replay before production.
- Prefer monotonic state transitions for long-running workflows.

Caching rules:

- Define source of truth and allowed staleness per cached value.
- Cache keys must include tenant, locale, permissions, and user segment when
  those affect output.
- Do not cache sensitive per-user responses in shared caches.
- Use ETags or version stamps when clients and intermediaries can revalidate.
- Cache invalidation must be triggered by the writer or a reliable projection
  process, not by hope.

## Architecture Metrics

Track architecture with a small fitness-function set instead of a large scorecard:

| Concern | Practical metric | Warning sign |
|---------|------------------|--------------|
| Coupling | modules touched per feature | every change crosses many boundaries |
| Cohesion | reasons a module changes | unrelated policies share one module |
| Change safety | rollback time and migration reversibility | releases require big-bang coordination |
| Operability | flows with logs, metrics, traces, runbooks | failures cannot be located quickly |
| Performance | p95/p99 latency and saturation per critical path | average latency hides tail failure |
| Reliability | error budget burn and retry amplification | retries increase outage pressure |
| Cost | unit cost per tenant/request/job | growth raises cost faster than value |

Use metrics as design feedback, not governance theatre. A metric must point to a
specific decision or intervention.

### Fitness Functions

Architecture fitness functions turn desired qualities into repeatable checks.
Use a mix of:

- static checks: dependency direction, forbidden imports, module boundaries
- dynamic checks: latency under load, timeout behaviour, failover behaviour
- process checks: lead time, review cycle time, deployment frequency
- runtime checks: error budget, saturation, queue lag, cache hit rate
- security checks: vulnerable dependency gates, secret scanning, auth coverage
- documentation checks: ADRs present for irreversible decisions, diagrams current

Keep fitness functions close to the risk. Do not add a check unless a failing
result would trigger a concrete action.

### Goal-Question-Metric

Use GQM when the right metric is unclear:

1. Goal: state what quality or outcome should improve.
2. Question: ask what would prove improvement or deterioration.
3. Metric: choose the smallest measurable signal that answers the question.
4. Action: define what the team will do when the metric crosses the threshold.

Example:

| Goal | Question | Metric | Action |
|------|----------|--------|--------|
| Reduce release risk | Are releases reversible? | rollback tested in staging within 15 minutes | block release until rollback path works |
| Improve modularity | Are unrelated changes touching the same module? | files/modules changed together over 30 days | split or clarify ownership |
| Improve operability | Can we locate failed checkout flows? | traces with order ID across all checkout spans | add instrumentation before feature launch |

### Four Delivery Metrics

Track these for engineering-system health:

- deployment frequency
- lead time for changes
- change failure rate
- mean time to restore service

Architecture should improve these over time. If a proposed architecture worsens
all 4, the added complexity needs a strong business reason.

## Documentation Output Expectations

Every non-trivial architecture output should include:

- context map with bounded contexts and external systems
- ownership map for data, APIs, events, and background jobs
- critical-flow table with transaction boundary, failure mode, retry behaviour,
  reconciliation path, and observability
- ADRs for decisions that are expensive to reverse
- explicit fitness functions and what would trigger redesign

## Diagram Discipline

Use diagrams to communicate decisions, not decoration:

- System context: actors, external systems, trust boundaries, major exchanges.
- Container/deployment: apps, services, databases, queues, caches, networks.
- Component: responsibilities and interfaces inside a deployable unit.
- Dynamic/sequence: critical runtime flows, retries, async handoffs, failures.
- Context map: bounded contexts and integration relationships.

Every diagram needs a title, scope, legend if symbols are non-obvious, and a
short note explaining the decision it supports.

## Architecture Review Questions

- Which business capability owns each rule and each data source?
- What would force this architecture to change: traffic, regulation, team size,
  integration volume, cost, or product direction?
- Which decisions are reversible and which need ADRs?
- Where can the system fail partially, and how does the user or operator know?
- Which metrics will show architecture erosion before it becomes a rewrite?
- What is the simplest architecture that meets the drivers for the next release
  without blocking the plausible next phase?
