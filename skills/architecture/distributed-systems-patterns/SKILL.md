---
name: distributed-systems-patterns
description: Use when designing or reviewing multi-service, message-driven, or eventually consistent systems. Covers service boundaries, consistency tradeoffs, event workflows, outbox and inbox patterns, sagas, ordering, and idempotency.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Distributed Systems Patterns
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Use when designing or reviewing multi-service, message-driven, or eventually consistent systems. Covers service boundaries, consistency tradeoffs, event workflows, outbox and inbox patterns, sagas, ordering, and idempotency.

## Do Not Use When

- The change is a single-process transaction with no remote dependency, asynchronous delivery, or independently failing component.
- The task is mainly service decomposition or API shape; use `system-architecture-design` or `api-design-first` and return here for cross-boundary failure semantics.

## Required Inputs

| Input | Required | Why it matters |
|---|---|---|
| Workflow steps and system boundaries | yes | Identifies where atomicity ends and partial failure begins |
| Delivery, ordering, and consistency requirements | yes | Determines idempotency, sequencing, and reconciliation choices |
| Failure and recovery expectations | yes | Sets timeout, retry, compensation, and operator intervention rules |
| Throughput and latency constraints | conditional | Tests whether the coordination pattern is viable |

## Workflow

Draw state transitions and ownership boundaries, enumerate failure windows, choose consistency and coordination patterns, define idempotency and recovery, then verify duplicate, reordered, delayed, and partially applied events.

## Quality Standards

Every remote interaction has a timeout and failure policy. Every retried side effect has an idempotency rule. Consistency claims state their scope, and recovery does not assume exactly-once delivery.

## Outputs

| Output | Consumer | Acceptance condition |
|---|---|---|
| Distributed workflow model | Architecture and implementation teams | Shows state ownership, message boundaries, consistency guarantees, and failure windows |
| Failure-handling contract | Service owners | Defines timeout, retry, deduplication, compensation, replay, and reconciliation behavior |
| Verification scenarios | Test and operations teams | Cover duplicates, reordering, concurrency, dependency outage, and partial completion |

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Operability | Service consistency and idempotency note | Markdown doc covering chosen consistency model, idempotency keys, and saga sequences | `docs/dist/consistency-note-checkout.md` |
| Operability | Failure-mode catalogue | Markdown doc listing partition, retry, and replay failure modes with mitigations | `docs/dist/failure-modes-checkout.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
- Load `references/event-driven-architecture.md` for event choreography, event contracts, brokers, and asynchronous workflow design.
- Load `references/realtime-systems.md` for WebSocket, SSE, pub/sub, and realtime delivery concerns.
<!-- dual-compat-end -->
Use this skill when a design crosses process, service, queue, or region boundaries. The goal is to keep distributed complexity deliberate and bounded rather than accidental.

## Load Order

1. Load `world-class-engineering`.
2. Load `system-architecture-design` first for the overall shape.
3. Load this skill only when the system genuinely needs multiple services, asynchronous workflows, or weakly consistent boundaries.

## Decision Workflow

### 1. Justify Distribution

State why distribution is necessary:

- team ownership and release independence
- scaling asymmetry
- fault isolation
- compliance or tenancy isolation
- long-running or bursty workflows

If none of these are strong, prefer a modular monolith.

### 2. Define Boundaries and Contracts

For each service or asynchronous component, define:

- owned data
- API or event contracts
- consistency expectation
- failure effect on upstream and downstream flows
- observability and ownership requirements

### 3. Choose Interaction Patterns

Use:

- synchronous calls when the caller needs immediate confirmation
- messaging when work is slow, bursty, or naturally eventual
- outbox and inbox patterns when reliability across boundaries matters
- sagas or compensations when one business workflow spans multiple durable states

### 4. Design Consistency and Recovery

Make explicit:

- source of truth
- ordering requirements
- deduplication strategy
- reconciliation path
- timeout and retry policy
- compensation or manual repair path

### 5. Prove the Design

Before calling it production-ready, provide:

- consistency model
- failure-mode examples
- idempotency and replay notes
- contract evolution rules
- operational signals for stuck or divergent workflows

## Non-Negotiable Standards

### Service Boundaries

- Each service owns its data and rules.
- Do not share databases across services as a convenience.
- Keep contracts narrow and versionable.
- Avoid chatty request chains on critical paths.

### Messaging

- Assume at-least-once delivery unless proven otherwise.
- Design consumers to be idempotent and replay-safe.
- Define ordering needs explicitly; unordered by default is safer to assume.
- Include correlation IDs and causation metadata.

### Consistency

- Strong consistency has operational cost; use it where business correctness needs it.
- Eventual consistency requires visible user and operator handling.
- If divergence is possible, define reconciliation before shipping.

### Sagas and Compensation

- Use compensation when the workflow spans multiple irreversible boundaries.
- Compensation must be explicit, auditable, and tested.
- Never describe a workflow as atomic if it crosses systems that cannot commit atomically.

## Deliverables

For distributed-system work, produce:

- service and ownership map
- contract list
- consistency decision table
- event and retry flow notes
- reconciliation or compensation plan
- stuck-workflow and replay detection signals

## Review Checklist

- [ ] Distribution is justified by real constraints.
- [ ] Data ownership is explicit and not undermined by shared persistence shortcuts.
- [ ] Idempotency and replay behavior are defined.
- [ ] Ordering assumptions are explicit.
- [ ] Consistency and compensation strategy match business risk.
- [ ] Operational detection exists for stuck, duplicated, or divergent workflows.

## References

- [references/consistency-decision-matrix.md](references/consistency-decision-matrix.md): How to choose synchronous, asynchronous, strong, or eventual consistency.
- [references/messaging-checklist.md](references/messaging-checklist.md): Event, queue, and saga review prompts.

## Capability contract
Model boundaries, messages, and failure semantics by default. Do not provision brokers, replay events, or mutate production state unless explicitly authorised.

## Degraded mode
If topology or failure evidence is unavailable, return a read-only pattern comparison and assumptions register; withhold recommendations dependent on unknown delivery guarantees.

## Domain Anti-Patterns
- Assuming exactly-once delivery. Fix: define idempotency and deduplication.
- Sharing one database across autonomous services. Fix: assign data ownership.
- Publishing before the state change commits. Fix: use a transactional outbox.
- Retrying non-idempotent commands blindly. Fix: add keys and retry limits.
- Omitting poison-message handling. Fix: define dead-letter and replay controls.
