---
name: engine-control-plane
description: "Coordinate routed skill engines through explicit agents, thin commands, lifecycle hooks, evidence contracts, handoffs, and bounded recovery. Use when designing or auditing multi-engine workflows, agent orchestration, command surfaces, hooks, presets, adapters, or release controls."
---

# Engine Control Plane

Use this skill as the shared operating layer above domain engines. Domain
skills remain authoritative for content and technical doctrine. The control
plane decides who acts, what entrypoint is used, which always-on controls run,
what evidence is required, and when work may advance.

## Contract

Every registered engine exposes:

| Surface | Required contract |
|---|---|
| Router | One authoritative router and a discoverable skill catalogue |
| Agent | Role, inputs, outputs, permission boundary, stop condition |
| Command | Thin entrypoint that routes to a skill; no duplicated doctrine |
| Hook | Event, action, failure mode, implementation adapter, and evidence |
| Handoff | Context, decisions, artifacts, open risks, next owner |
| Evidence | Source, check, result, reviewer, timestamp, release consequence |

The machine-readable registry is `docs/engine-control-plane.json`. Validate it
with:

```powershell
python scripts/validate_engine_control_plane.py
python scripts/validate_engine_control_plane.py --workspace-root C:\wamp64\www
```

The second form also checks the ten local engine routers.

## Routing sequence

1. Identify the primary domain engine and additive cross-cutting engines.
2. Select the smallest accurate skill from the engine router.
3. Select only the agents needed for the decision or deliverable.
4. Run the preflight and context hooks before external research or writes.
5. Use thin commands to invoke the canonical skill workflow.
6. Require an evidence record before handoff or release.
7. On failure, preserve state, retry only within the declared budget, and
   escalate with a structured handoff when progress stops.

## Agent topology

Use one coordinator only. Run independent specialists in parallel, then pass
their evidence to a reviewer or gatekeeper. Never ask two agents to own the
same decision. A coordinator must provide each agent with the minimum context
needed and must carry forward decisions, constraints, unresolved risks, and
artifact paths.

Preferred roles are:

- **Router/Planner** — selects the route, scope, dependencies, and work plan.
- **Domain Worker** — produces the domain artifact or implementation.
- **Evidence Collector** — verifies sources, tests, calculations, renders, or
  operational results.
- **Adversarial Reviewer** — looks for contradictions, omissions, unsafe
  assumptions, and false readiness claims.
- **Gatekeeper/Release Captain** — issues PASS, FAIL, or NOT ASSESSED and
  records the release consequence.
- **Librarian** — proposes skill updates from repeated failures; never silently
  edits or promotes a new skill.

## Hook semantics

Native hooks are optional. Where a host cannot run event hooks, implement the
same contract through a script, CI job, pre-commit check, or explicit skill
step. Hooks must be fail-open only for advisory telemetry; safety, evidence,
destructive-action, and release gates fail closed or produce an explicit
NOT ASSESSED result.

Minimum hook set:

- `preflight`: verify router, workspace, permissions, dependencies, and risk.
- `context`: load the canonical context and avoid duplicate or stale reads.
- `before_write`: verify scope, backup/reversibility, and required approval.
- `after_write`: run targeted validation and update the evidence record.
- `release`: require tests, security, accessibility/quality, operations,
  source/currency, rollback, and reviewer evidence as applicable.
- `stop`: write a resumable handoff when work is incomplete or interrupted.

## Recovery and learning

Use a bounded loop: observe → classify → fix → verify → record. Do not count a
model confidence statement as evidence. A retry must identify the failed check,
preserve the prior attempt, and use a changed approach. Two consecutive
zero-progress cycles require escalation or deferral. Successful changes become
references, fixtures, routing rules, or release gates only after an independent
check.

## Safety

- Never bypass a gate only in conversation.
- Never treat missing tools, sources, screenshots, tests, or approvals as
  PASS.
- Never let an agent mutate a domain it does not own without an explicit
  handoff.
- Never create a second source of truth for requirements, accounting doctrine,
  design doctrine, research evidence, or release state.
