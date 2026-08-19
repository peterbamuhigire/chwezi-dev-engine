---
name: engine-control-plane
description: Use when coordinating or auditing multi-engine workflows, agent roles, command surfaces, hooks, evidence contracts, handoffs, or bounded recovery. Keeps domain doctrine in the owning engines.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Engine Control Plane

Use this skill as the shared operating layer above domain engines. Domain
skills remain authoritative for content and technical doctrine; the control
plane governs ownership, lifecycle, evidence, handoff, and recovery.

<!-- dual-compat-start -->
## Use When

- Designing or auditing a workflow that crosses two or more skill engines.
- Defining agent roles, thin commands, lifecycle hooks, evidence contracts, or handoffs.
- Reviewing release controls, bounded recovery, or a control-plane registry.

## Do Not Use When

- A single domain skill can own the work without an orchestration decision.
- The task needs domain doctrine rather than routing, ownership, or release control.
- A safety-only review is required; load `skill-safety-audit` instead.

## Required Inputs

- The participating engines, authoritative routers, intended output, and decision owner.
- Required capabilities, permissions, dependencies, evidence, stop conditions, and recovery constraints.
- The applicable registry or adoption document, if the workflow is already registered.

## Prerequisites

- Read the primary domain skill for each participating engine.
- Load `skill-writing` and `skill-composition-standards` when changing a reusable contract.

## Workflow

1. **Preflight.** Confirm scope, routers, permissions, dependencies, risk, and the exact mutation boundary.
2. **Assign ownership.** Select one coordinator and the smallest set of independent domain workers. Give each worker a single decision or artefact owner.
3. **Load context.** Carry forward requirements, decisions, constraints, evidence gaps, open risks, and the next owner. Do not reload unrelated doctrine.
4. **Execute thinly.** Use commands and hooks as entrypoints to canonical skills. Keep vendor adapters and command syntax outside model-neutral doctrine.
5. **Check evidence.** Require source, check, result, reviewer, timestamp, and release consequence for each material gate.
6. **Recover or stop.** Preserve the last safe state. Retry only with a named changed approach; escalate after two zero-progress cycles or when authority is missing.
7. **Handoff and learn.** Publish the artefact, evidence, unresolved risks, recovery path, and next owner. Promote a successful repeated lesson only after an independent check.

## Core content

### Required control surfaces

| Surface | Minimum contract |
|---|---|
| Router | One authoritative router and a discoverable catalogue |
| Agent | Role, inputs, outputs, permission boundary, and stop condition |
| Command | Thin entrypoint to a canonical skill; no duplicated doctrine |
| Hook | Event, action, failure mode, adapter, and evidence |
| Handoff | Context, decisions, artefacts, open risks, and next owner |
| Evidence | Source, check, result, reviewer, timestamp, and release consequence |

### Agent topology

Use one coordinator. Assign independent decisions to a Router/Planner, Domain
Worker, Evidence Collector, Adversarial Reviewer, Gatekeeper/Release Captain,
or Librarian as needed. Never assign two agents the same decision; the
coordinator carries decisions, constraints, risks, and artefact paths forward.

### Hook semantics

Implement the same contract through native hooks, scripts, CI, or explicit
steps. The minimum lifecycle is `preflight`, `context`, `before_write`,
`after_write`, `release`, and `stop`. Advisory telemetry may fail open; safety,
evidence, destructive-action, and release gates fail closed or return
`NOT ASSESSED`.

## Non-negotiables

- Keep domain rules in their owning engine; do not create a second source of truth.
- Treat missing tools, sources, screenshots, tests, or approvals as `NOT ASSESSED`, never as `PASS`.
- Default review and analysis to read-only. Require explicit authority for mutation or external side effects.
- Make stop conditions, rollback or recovery, and release consequences visible before work advances.

## Quality Standards

- A router is authoritative, discoverable, and checked against the registered catalogue.
- An agent has a role, inputs, outputs, permission boundary, and stop condition.
- A command is a thin entrypoint and does not duplicate domain doctrine.
- A hook names its event, action, failure mode, adapter, and retained evidence.
- A handoff names context, decisions, artefacts, open risks, and the next owner.

## Anti-Patterns

- Two agents own the same decision. Fix: assign one accountable owner and make the other a reviewer.
- A command copies a specialist workflow. Fix: route to the canonical skill and keep the command thin.
- A missing approval is treated as an implicit approval. Fix: stop and record `NOT ASSESSED`.
- A retry repeats the same failed approach. Fix: preserve the prior result and name the changed approach.
- A handoff contains prose but no evidence or next owner. Fix: use the evidence and handoff fields as a release gate.
- A hook mutates a domain it does not own. Fix: require an explicit cross-engine handoff.

## Outputs

| Artifact | Consumed by | Template |
|---|---|---|
| Ownership and routing plan | Coordinator and domain owners | `docs/engine-control-plane.json` plus inline rationale |
| Evidence record | Reviewer or gatekeeper | Evidence contract in `docs/engine-control-plane.md` |
| Handoff record | Next owner or release captain | Inline: context, decisions, artefacts, risks, recovery |
| Release verdict | Maintainer and operator | `PASS`, `FAIL`, or `NOT ASSESSED` with consequence |

## Evidence Produced

| Category | Artifact | Format | Example |
|---|---|---|---|
| Correctness | Registry and route validation result | Command output | `python scripts/validate_engine_control_plane.py` |
| Security | Permission and mutation-boundary record | Markdown | Preflight and before-write evidence |
| Operability | Recovery or stop handoff | Markdown | Last safe state and next owner |
| Release evidence | Gate verdict with residual risk | Markdown | `PASS`, `FAIL`, or `NOT ASSESSED` |

## Read next

- `skill-engine-audit` for whole-engine inventory and scoring.
- `skill-safety-audit` for unsafe instructions, dependencies, and provenance.
- `advanced-testing-strategy` for risk-based test depth and retained evidence.
- `world-class-engineering` for implementation and release gates.

## References

- `docs/engine-control-plane.md` - shared vocabulary and lifecycle contract.
- `docs/engine-control-plane.json` - machine-readable eleven-engine registry.
- `../../../scripts/validate_engine_control_plane.py` - deterministic registry validator.
- `skill-writing` and `skill-composition-standards` - authoring and composition rules.
<!-- dual-compat-end -->

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---|---|
| Participating engines and authoritative routers | Task owner or coordinator | yes | Establishes ownership and routing |
| Required capabilities, permissions, and recovery constraints | Preflight or risk owner | yes | Bounds execution and side effects |
| Registered control-plane contract | Maintainer | conditional | Keeps registry and adoption evidence aligned |

## Capability contract

Read and search are required. Editing and execution require an authorised
implementation scope. Network access is optional and must remain source-
disciplined. Delegation is optional and must use disjoint ownership.

## Degraded mode

If a router, registry, tool, source, approval, or test is unavailable, return a
scoped plan with the unavailable check marked `NOT ASSESSED`. Do not infer
success from a declaration, model confidence, or an unexecuted hook.

## Decision rules

| Condition | Action | Failure avoided |
|---|---|---|
| One engine owns the decision | Route directly and keep orchestration out | Duplicate doctrine and unnecessary hops |
| Two or more engines contribute independent artefacts | Use one coordinator, named owners, and a reconciled handoff | Conflicting edits and lost context |
| Mutation, external side effect, or irreversible action | Require explicit authority, exact target, recovery, and evidence before execution | Unbounded blast radius |
| Required evidence or approval is unavailable | Stop or issue `NOT ASSESSED` with an owner and next check | False release confidence |
| A failure repeats with no changed approach | Escalate or defer after the bounded retry budget | Retry loops and hidden failure |
