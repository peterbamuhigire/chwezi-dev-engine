# Slice, Review, and Recovery Practice

Load this when a change needs a scenario contract before implementation, a
risk-focused review, a constrained AI-assisted workflow, a failure-aware
architecture decision, or a safe Git recovery. It is task guidance, not a
summary of any source.

## 1. Frame one vertical slice before choosing implementation

Inputs: one user or operator scenario, the business outcome, the invariant that
must stay true, and the consequence of failure.

Produce a slice contract with:

- actors, trigger, happy path, alternate paths, and failure paths;
- functional acceptance checks and measurable NFR budgets (latency, error
  rate, throughput, cost) stated as numbers with a measurement method;
- data and API boundaries, trust assumptions, dependencies, and the owner of
  each;
- telemetry, rollout, rollback, and recovery evidence.

Decision rule: if the slice cannot name its invariant and failure consequence,
it is not ready to build. Keep small tasks small; the contract can be five
lines for a low-risk change.

Worked example (original): a Kampala SACCO adds mobile-money loan repayment.
Invariant: a member's loan balance never decreases without a matching
confirmed provider transaction. Failure consequence: disputed balances and
regulator complaints. Failure paths: provider timeout, duplicate callback,
callback for an unknown reference. Acceptance: a replayed callback with the
same provider reference changes the balance once; a timed-out request leaves
the repayment `PENDING` and is reconciled by the next statement import.

## 2. Review for risk and intent, not taste

Automate formatting, static analysis, tests, schema checks, and security scans
before a human looks. The human review then asks:

1. Does the change satisfy the stated requirement and its edge cases?
2. Are data structures, boundaries, permissions, and dependency calls safe?
3. Are latency, resource, concurrency, and failure assumptions explicit?
4. Is the change small enough to understand, test, release, and revert?
5. Do documentation, telemetry, migration, and operational handoff match the
   implementation?

Classify every finding as `blocking`, `required before merge`, or `optional`.
Write comments that name the outcome at risk and a concrete fix. Record
positive evidence where it teaches the team something. AI-generated review
comments stay suggestions until a human has checked them against the code and
context.

## 3. Treat AI as a constrained collaborator

Give the tool the scenario, relevant context, constraints, acceptance tests,
negative cases, and output format. Ask it to state assumptions and uncertainty.
The human owner must:

- understand the full diff before accepting it;
- keep secrets, customer data, and sensitive code out of prompts unless the
  tool is approved for that data class;
- verify every new dependency exists, is maintained, and is licensed for use;
- run tests that could falsify the proposal, including negative cases.

Generated code, generated tests, and coverage numbers are never proof on their
own; executable evidence reviewed by a human is.

## 4. Design for behaviour under change and failure

Characterise workload, consistency needs, availability, latency, throughput,
cost, and team operating capability before choosing technology. Record where
truth lives, what is derived, how state changes, and how a dependency failure
is contained. Prefer bounded designs with explicit timeouts, idempotency,
backpressure, retry limits, observability, and a rehearsed recovery path.
Version public schemas and deprecate before removal.

For data-intensive or event-driven systems, make ownership, schema evolution,
lineage, replay or reconciliation, and compatibility checks explicit. Neither
exactly-once delivery nor eventual consistency is free: state the invariant and
the evidence that protects it.

## 5. Make Git history and recovery part of delivery quality

- Stage deliberately; keep each commit one reviewable idea.
- A pull request states what changed, why, scope, tests and evidence,
  operational impact, risk, and rollback.
- Keep branches short-lived and the main branch releasable.
- When a conflict or mistaken change occurs, inspect status, log, and reflog
  before rewriting or discarding anything; create a recovery point (a branch or
  tag) first, then verify the repaired result with the test suite.

## Quality gate

- [ ] Slice contract names invariant, failure consequence, and measurable NFRs.
- [ ] Review findings are classified and outcome-oriented.
- [ ] AI output has human-verified tests, including negative cases.
- [ ] Truth, derived state, and failure containment are recorded.
- [ ] PR states risk and rollback; recovery point exists before history edits.

## Premium versus generic output

| Premium | Generic |
| --- | --- |
| Names the invariant and the evidence that protects it | Lists "best practices" with no invariant |
| NFRs are numbers with a measurement method | "Fast", "scalable", "secure" |
| Review comments name the risk and the fix | "Consider refactoring this" |
| Rollback is rehearsed and written down | "Revert if needed" |

## Deliberate exclusions

Vendor pricing, capacity, and service claims, and Git command variants from
older tool versions, are not doctrine; verify current official documentation
for the chosen platform and Git version.

## Evidence/currentness

Concept guidance only; no version-sensitive claims. Access date 2026-09-24.
Git command behaviour: verify against <https://git-scm.com/docs> for the
installed version (`NOT_ASSESSED` for any specific version here).

Sources: Adrienne Braganza, *Looks Good to Me: Constructive Code Reviews*;
Trisha Gee, *What to Look for in a Code Review*; Chris Belanger and Jawwad
Ahmad, *Mastering Git*; Almantas Karpavicius, *Software Craftsmanship Using AI*;
Daniel R. Holt, *Modern Data Systems*; Drew Hoskins, *The Product-Minded
Engineer*. Publication years `NOT_ASSESSED`. Consolidated from the engine's
2026-09-14 practice note.
