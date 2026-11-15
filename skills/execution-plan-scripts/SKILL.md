---
name: execution-plan-scripts
description: Use when converting an approved long-running plan into self-contained execution prompts across sessions or workers. Covers dependency order, checkpoints, capability fallback and evidence handoff; use world-class-engineering for a single implementation slice.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  - gemini-cli
---

# Execution Plan Scripts

<!-- dual-compat-start -->

## Required Inputs

| Input | Owner | If absent |
|---|---|---|
| Approved plan, current task states and acceptance criteria | Task owner | Draft the plan before generating execution prompts |
| Repository instructions, live skill inventory and supported capabilities | Executing environment | Discover them; do not assume a named plugin or tool exists |
| Dependencies, file ownership and last verified checkpoint | Coordinator | Sequence dependent work and resolve overlapping writes |
| Existing authorisation and external-action limits | User and host policy | Carry forward the existing scope; stop only for work outside it |

## Capability and degraded modes

Authoring requires read/search access and the plan-authoring scope. Execution
and delegation are optional: use sequential prompts when workers are unavailable.
An optional process skill may help but is never a prerequisite. If a required
source, capability, test environment or credential is unavailable, mark the
affected evidence `NOT ASSESSED` and continue independent work. Do not turn a
missing required test into an expected failure to make a suite green.

## Decision rules

| Condition | Prompt design | Evidence required |
|---|---|---|
| A task consumes another task's output | Run after the producer's acceptance gate | Producer artefact and result |
| Independent tasks have disjoint write sets and delegation is available | Assign one owner per write set | Reconciled diffs and worker results |
| A slice delivers one end-to-end user outcome | Represent it as a tracer-bullet node with blocking edges | Runnable thin-slice evidence |
| A live contract or schema cannot change atomically | Use expand-contract nodes and preserve a green compatibility boundary | Version-skew and rollback checks |
| Delegation or a named process skill is unavailable | Execute the same tasks sequentially | Same acceptance criteria and checkpoint |
| A session resumes or compacts | Read the checkpoint and inspect current state | Remaining work, prior results and user corrections |
| An action exceeds existing authority | Finish independent preparation, then request that specific authority | Reviewable proposal and scope boundary |

## Workflow

1. Read the plan, user corrections and repository instructions; enumerate live skills and capabilities.
2. Partition work by outcome, dependency and exclusive write ownership. Keep the next blocking task with the coordinator; delegate only when the worker is available and ready.
3. Write self-contained prompts using the task contract below. Quote applicable skills by name, never a machine-specific path.
4. Name exact acceptance checks, semantic expected results, relevant failure states, unresolved prerequisites and the recovery point.
5. Check every prompt against the plan: owner, required inputs, allowed scope, output, acceptance evidence and checkpoint.

## Durable task and recovery contract

Give each independently verified task a stable ID, prerequisites, one accountable
owner, exclusive write set, exact inputs or producer outputs, expected result and
acceptance oracle. Bind evidence to revision, configuration/runtime, environment,
command, inputs, date and outcome; a zero exit alone is not semantic acceptance.
Keep a durable checkpoint outside chat. After interruption, reboot, quota expiry,
session replacement or wait timeout, inspect the worktree and checkpoint, reconcile
task state and external effects, then resume at the first dependency-ready incomplete
task. Repeat only when relevant inputs or conditions changed. A timeout is not proof
of completion; supervise the process/result or mark it `NOT ASSESSED` with an owner
and recovery action. Record watch status with time, source and inspected scope;
silence or an empty poll does not establish clearance. See the on-demand
[prompt construction and review guide](references/execution-prompt-examples.md)
for templates and conditional plan-status rules.

Before delegation, verify the specialist's live skills, tools, readiness and scoped
authority. Preserve independent review evidence and unresolved disagreement. Keep
context to relevant plan sections, files and constraints; select checks by risk.
Continue already authorised phases in dependency order without a routine fresh
permission request at each checkpoint. Pause only for a missing decision, required
approval, genuine blocker or governing instruction; continue independent work.

## Quality standards

Prompts preserve existing authorisation, corrections and incomplete work. Completion
requires observed acceptance evidence. A tool call, generated file or unrun test is
not completion. Use concise, self-contained prompts that retain the handoff a fresh
session needs.

## Dynamic skill discovery

When authoring a software/app execution script, load this skill and discover the
current domain catalogue from the executing environment's repository instructions.
Select only relevant domain skills and available process guidance; quote skill names
in each prompt and re-quote them in each delegated prompt. Never freeze a list of
skill names or hardcode the library path. Self-load this skill for multi-prompt
software/app plans; use `world-class-engineering` and the relevant domain skill for a
single implementation slice.

Each prompt distinguishes:

- **Domain guidance:** what good work looks like. Resolve its path from the live
  environment and load the skills that apply to that task.
- **Process guidance:** how to organise testing, review, verification or delegation.
  Discover what is available; use only what adds value, without making a named
  plugin a prerequisite.

## Prompt construction and execution

Make every prompt runnable in a fresh session without relying on prior conversation.
State its task/outcome, repository, required source files, discovered skill names,
scope and exclusions, dependencies, acceptance evidence, next checkpoint and
authority boundary. Detailed examples, delegation mechanics, operator-action blocks,
verification format and project-specific status conventions are in the linked
reference; load only the sections needed for the plan.

Do not hardcode a skills-library path. Use the executor's `CLAUDE.md`, `AGENTS.md`,
`GEMINI.md` or equivalent to resolve names. A prompt may name a skill only after the
authoring session has checked the live catalogue.

## Closeout rules

- Use the project's own task/status format. Update task state only after evidence; apply phase/index conventions only when the plan defines them.
- Surface an operator-only prerequisite before the affected task. Use existing authority; request new authority only for the specific action that exceeds it. Continue independent work.
- Run risk-matched integration and cleanup checks; do not impose blanket security, tenancy, i18n, memory or other sweeps where the work does not affect them.
- Keep publication within existing authority and configured controls. Prompts must not expand authority, bypass gates or push/merge on their own.
- Review every delegated diff against its write scope and reconcile it with the acceptance criteria before integration.

## References

- [Prompt construction and review guide](references/execution-prompt-examples.md): load for a prompt skeleton, delegation and verification examples, operator actions, and plan-specific status controls.
- [Tracer-bullet work graphs and expand-contract](references/tracer-bullet-work-graphs.md)
- [Plan header and proportion check](references/plan-header-and-proportion.md): spec pointer, constraints, per-node interfaces, review focus and proportion.

## Outputs

- A Markdown script with purpose, task order, domain/process skill sources, authority boundary and self-contained prompts for each task.
- A prompt-to-task mapping with owners, dependencies and acceptance checks.
- Operator notes for run order, prerequisites, and deferred checks.

## Evidence Produced

| Category | Artifact | Format | Example |
|---|---|---|---|
| Correctness | Task-to-prompt coverage with dependencies and acceptance checks | Markdown table | Each approved task maps to one owner and an acceptance oracle |
| Operability | Resume checkpoint and capability fallback | Markdown | Completed task evidence, remaining work and sequential fallback |
| Release evidence | Verification results and unresolved prerequisites | Markdown | Failed and unavailable checks with release consequence |

<!-- dual-compat-end -->

## Unattended execution handoff

For an owner-authorised unattended development plan, use the project-local
`auto-agents/README.md` and `auto-agents/config.json`. Keep the plan and authority
explicit; configure project-specific verification commands and a durable handoff.
Publishing, remote, branch, runner and limits remain project settings. A worktree is
checkout isolation, not a sandbox. Preserve host permissions and security controls.
Failed or unavailable checks are never passes. Verify the actual driver version and
runtime before relying on it.

### Propagate tool upgrades

When this engine changes `auto-agents`, update the canonical copy in
`skills-engine-agents` first, regenerate its manifest, run its tests, then discover
and update installed project and engine copies through its managed propagation
workflow. Preserve local configuration, plans and edits; report blocked or missing
targets. Batch required host plugin-cache refreshes at the end and retain hook-trust
checks. See `auto-agents/README.md`.

### Durable execution plan and verification

Use the project-owned plan for scope, authority, decisions, acceptance, ordered
slices and recovery handoff. The local plan template is optional; adapt it rather
than filling it mechanically. Configure meaningful checks before execution and
record unrun or failed checks accurately. Resume from durable evidence, verify the
resulting revision independently before configured publication, continue independent
authorised work, and correct material review findings.
