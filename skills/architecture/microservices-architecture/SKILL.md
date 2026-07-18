---
name: microservices-architecture
description: Use when designing, reviewing, or refactoring microservice boundaries, communication, service ownership, deployment independence, resilience, and distributed data flows. Load absorbed microservices fundamentals, models, communication, and resilience references as needed.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Microservices Architecture
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

Use this parent skill as the active microservices entrypoint. It should help decide whether microservices are justified, then shape service boundaries and operating contracts when they are.

<!-- dual-compat-start -->
## Use When

- Defining service boundaries, ownership, API contracts, data ownership, deployment independence, or migration from a monolith.
- Reviewing synchronous and asynchronous service communication, reliability, retries, idempotency, and failure isolation.
- Creating a target architecture for teams that need multiple independently deployable backend services.

## Do Not Use When

- The task is unrelated to this parent skill or is better handled by a narrower active parent named in the workflow.
- The request only needs a trivial answer and no reference module needs to be loaded.

## Required Inputs

- Gather the concrete system, repository, environment, constraints, and deliverable before loading references.
- Identify which absorbed reference file is needed; do not load every migrated reference by default.
## Workflow

1. Start with `system-architecture-design` and `distributed-systems-patterns` for context, constraints, and failure modes.
2. Load only the needed reference:
   - `references/microservices-fundamentals.md` for core principles and when not to split.
   - `references/microservices-architecture-models.md` for decomposition and ownership models.
   - `references/microservices-communication.md` for API, event, queue, and contract patterns.
   - `references/microservices-resilience.md` for retries, circuit breakers, idempotency, and graceful degradation.
3. Pair with `api-design-first`, `database-design-engineering`, `deployment-release-engineering`, and `observability-monitoring` for implementation contracts.

## Quality Standards

- Do not split services without a clear ownership, deployment, data, and reliability reason.
- Every service boundary must define source of truth, API contract, failure mode, observability, and rollback path.
- Prefer fewer services until team topology, data ownership, and release cadence justify more.

## Anti-Patterns

- Treating absorbed reference files as active skills or separate routing entrypoints.
- Loading every migrated child reference instead of the one that matches the task.
- Producing generic advice without constraints, evidence, or next verification steps.
## Outputs

- Service map, boundary decision, API/event contract notes, migration plan, or architecture review.

## References

- Load only the references/<old-skill>.md files named in the workflow when their depth is required.
<!-- dual-compat-end -->

## Inputs
| Input | Required | Purpose |
|---|---|---|
| Domain capabilities and ownership | yes | Draw boundaries |
| Workload and availability targets | yes | Set communication tradeoffs |
| Data ownership and change constraints | yes | Plan migration |

## Capability contract
Recommend boundaries and migration sequences by default. Do not split repositories, databases, deployments, or production traffic without explicit change authority.

## Degraded mode
If ownership or runtime evidence is unavailable, provide a read-only candidate map and retain a modular monolith as the default.

## Decision rules
| Condition | Action |
|---|---|
| Independent scale or ownership absent | Keep a module |
| Cross-service transaction required | Redesign or specify a saga |
| Extraction lacks rollback | Block migration |

## Domain Anti-Patterns
- Splitting by technical layer. Fix: split by business capability.
- Sharing tables between services. Fix: assign one data owner.
- Building long synchronous chains. Fix: shorten or decouple them.
- Treating a broker as transaction magic. Fix: define compensation.
- Creating services without owners. Fix: record ownership first.
