# Book-informed engineering practice synthesis

Status: adopted as a concise, independently worded practice note on 2026-09-14.

This note records only practices that improve decisions in the engineering
catalogue. It is not a book summary and does not reproduce source text.

## Practices to standardise

### Frame a vertical slice before choosing implementation

For meaningful work, describe one user or operator scenario, the business
outcome, the invariant that must remain true, the boundary conditions, and the
failure consequence. Convert that slice into a contract containing:

- actors, trigger, happy path, alternate and failure paths;
- functional acceptance checks and measurable NFR budgets;
- data/API boundaries, trust assumptions, dependencies, and ownership;
- telemetry, rollout, rollback, and recovery evidence.

This joins product scenarios, system-design requirements, and release proof
without turning every task into a large design exercise.

### Review for risk and intent, not taste

Before a human review, automate formatting, static analysis, tests, schema
checks, and security scans where practical. The review then asks:

- Does the change satisfy the stated requirement and edge cases?
- Are data structures, boundaries, permissions, and dependency calls safe?
- Are latency, resource, concurrency, and failure assumptions explicit?
- Is the change small enough to understand, test, release, and revert?
- Does the documentation, telemetry, migration, and operational handoff match
  the implementation?

Classify findings as blocking, required before merge, or optional/nit. Make
comments specific and outcome-oriented; record positive evidence where it
helps the team learn. AI-generated review comments remain suggestions until a
human verifies the context and the code.

### Treat AI as a constrained collaborator

Give an AI tool the scenario, relevant context, constraints, acceptance tests,
negative cases, and output format. Ask it to state assumptions and identify
uncertainty. The human owner must understand the resulting diff, protect
secrets and sensitive code, verify external dependencies, and run tests that
could falsify the proposed solution. Never use generated code, tests, or
coverage numbers as proof without human review and executable evidence.

### Design systems around behaviour under change and failure

Choose technologies after characterising workload, consistency needs,
availability, latency, throughput, cost, and operational capability. Record
where truth lives, what is derived, how state changes, and how a dependency
failure is contained. Prefer simple bounded designs with explicit timeouts,
idempotency, backpressure, retry limits, observability, and a rehearsed
recovery path. Version public schemas and deprecate before removal.

For data-intensive or event-driven systems, make ownership, schema evolution,
lineage, replay/reconciliation, and compatibility checks explicit. Do not
assume exactly-once or eventual consistency is free; state the invariant and
the evidence that protects it.

### Make Git history and recovery part of delivery quality

Keep changes staged deliberately and commits logically reviewable. A pull
request should state what changed, why, scope, tests/evidence, operational
impact, risk, and rollback. Keep branches short-lived and main releasable.
When conflicts or mistaken changes occur, inspect status, history, and
references before rewriting or discarding work; preserve a recovery point and
verify the repaired result.

## Deliberate exclusions

- Vendor-specific product pricing, capacity, and service claims are not
  doctrine; verify current official documentation for the chosen platform.
- Git command examples from an older edition are not a substitute for current
  repository policy or safe local inspection.
- Generic JSON recipes are not a new skill; use contract, schema, validation,
  error, and security guidance where the system boundary requires it.
- Architecture examples from the supplied Google-focused book are used for
  decomposition, workload, cost, and failure questions only, not as current
  Google product specifications.

## Source register

- Adrienne Braganza, Looks Good to Me: Constructive Code Reviews.
- Trisha Gee, What to Look for in a Code Review.
- Chris Belanger and Jawwad Ahmad, Mastering Git: Understanding Git Internals
  and Commands.
- Almantas Karpavičius, Software Craftsmanship Using AI.
- Ray Rischpater, JavaScript JSON Cookbook.
- Daniel R. Holt, Modern Data Systems: Designing Reliable, Scalable, and
  Intelligent Applications.
- Drew Hoskins, The Product-Minded Engineer.
- Nordic APIs, Identity and APIs: Techniques to Mature Platform Security.
- Michael Mangialardi, Design Systems for Developers: Learn How to Code
  Design Systems That Scale.
- Aditya Chatterjee, Ue Kiao, Chew Chee Keng and contributors, System Design
  at Google: Engineering Peak for Interviews.

The supplied originals were inspected locally on 2026-09-14. No source files,
OCR output, full-text conversion, or download metadata belongs in this
repository.
