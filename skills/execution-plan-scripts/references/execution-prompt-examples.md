# Execution Prompt Construction and Review

Load this reference when authoring a multi-prompt script, delegating work, surfacing
operator-only actions, or applying a project-specific task/index convention. The
parent skill owns the required task and recovery contract.

## Self-contained prompt pattern

Adapt this skeleton to the approved plan. Do not add empty sections or repeat the
whole plan in each prompt.

```markdown
## Prompt <N> — <outcome and stable task ID>

You are working in <repository>. Read the applicable repository instructions and
the linked plan sections first:
- <root instructions>
- <plan / task IDs and relevant sections>
- <source-of-truth decisions and constraints>

Before editing, discover the live skill catalogue and available process guidance.
Read these applicable skills by name:
- Domain: <verified skill names>
- Process, if useful and available: <verified skill names>

Task: <observable outcome>
Owner and write scope: <one accountable owner; exact files or bounded discovery>
Dependencies: <ready prerequisite IDs and outputs>
Exclusions and authority: <scope, data boundary, external actions allowed>
Inputs: <paths, revisions, fixtures, and required environment>

Work:
1. <bounded action>
2. <bounded action>

Acceptance:
- <criterion ID>: <observable expected result>
- Check: <verified command and working directory, or evidence oracle>
- Failure case: <meaningful denied/error/interrupted state and expected result>

Checkpoint: <durable location, result/revision fields, next ready task>
Recovery: <what to inspect after interruption; what is safe to repeat>
Do not exceed the existing authority or publication boundary.
```

Use the project’s own document names and task schema. If a needed path, command,
credential, test environment or acceptance fact is unavailable, identify the gap and
mark dependent evidence `NOT ASSESSED`; do not invent a likely command or expand
the task to compensate.

## Skill discovery and prompt scope

At author time, enumerate the live domain skills and any installed process skills
through the active runner's documented mechanism. The taxonomy below helps decide
what to look for; it is not a list of available skills:

- Security, identity, API contract, database/migration, multi-tenancy/RBAC.
- Web UI/UX, mobile, accessibility, performance, content/i18n.
- Testing/SDLC, DevOps/CI, architecture and operations.

Resolve skill paths only through the executor's current `CLAUDE.md`, `AGENTS.md`,
`GEMINI.md` or equivalent. Put verified skill names in each prompt; a worker does
not inherit the parent session's loaded-skill state. Never copy a static sibling list
or machine-specific skills path into a script.

Separate domain guidance from process guidance. Domain skills define the expected
quality and invariants. Process skills may help organise delegation, testing or
review, but the approved acceptance criteria remain the same if they are unavailable.
Keep the coordinator's next blocking task local. Delegate independent work only when
the worker has the required capability/access, its owned files do not overlap, and
the coordinator can reconcile the returned evidence.

## Work graph and delegation

Model each node as a useful user outcome with an owner, exclusive write set, inputs,
acceptance evidence and prerequisites. Add an edge only where one task needs another
task's output, decision or accepted contract. Prefer a thin end-to-end slice where
it provides earlier evidence. For a live contract that cannot change atomically, use
an expand-contract sequence with an explicit compatibility and rollback boundary.
Do not invent task-count, fan-out or phase quotas.

For every delegated task, make the brief self-contained. Include its task IDs, exact
source paths or plan sections, live skills by name, allowed and forbidden files,
acceptance checks, existing commit/publication boundary and return format. Give each
file one writer at a time. Re-inject all applicable skill names in each worker prompt.
Bound parallel work by the coordinator's ability to review every diff and handoff;
otherwise execute sequentially.

Keep dependent nodes serial. Independent nodes may proceed concurrently when they
share no writes or mutable test service. Do not require an operator review between
prompts unless the approved plan or actual authority requires it. A checkpoint is
progress evidence, not a request to repeat authorisation or say “continue”.

## Verification and handoff example

Every prompt needs checks matched to its risk, not a boilerplate suite. Prefer the
smallest normal-path check and one meaningful failure/semantic oracle; add broader
static, security or integration checks when the changed surface warrants them.
Capture the command, working directory, revision, environment, inputs, outcome and
relevant output in a durable location.

```markdown
### Acceptance record
- Criterion: AC-004
- Expected: a user without export permission receives the documented denial;
  no download or export record is created.
- Check: <copy the verified project command>; cwd: <verified repository root>
- Revision and fixture: <tested commit>; <named disposable fixture>
- Result: PASS | FAIL | NOT ASSESSED
- Evidence: <durable path and locator>
- Limitation or next action: <reason and owner, or none>
```

A zero exit alone does not establish semantic acceptance. A wait timeout does not
establish process completion; inspect the process/receipt or keep the check
`NOT ASSESSED`. Preserve a failing result and its output. Retry only when a relevant
condition changed or a concrete repair gives the next attempt a useful oracle. Do
not push, merge, force-push, change permissions, or publish inside a prompt unless
that action is already authorised and remains within its configured controls.

## Operator-only actions

When a task depends on a human-only step (for example, access to a named account,
physical device or signing key):

1. Name the prerequisite at the start of the affected prompt and say what evidence
   it enables.
2. Use existing authorisation and capabilities. Request only a missing input or a
   materially different action that exceeds the existing scope.
3. If it is unavailable, mark the dependent check `NOT ASSESSED`, state its release
   consequence and owner, and continue independent work.

Never hide a real failure, turn an unavailable check into an expected failure, or
ask for the same approval again at routine checkpoints.

## Task status and index conventions

Follow the plan's own status vocabulary and handoff format. Update a task only after
its stated evidence is recorded; completion metadata is not independent acceptance.
Apply phase rows or index conventions only when the plan actually defines them. If
using a plan with `INDEX.md`, change a phase row only after its final prompt and
required exit evidence. Reserve memory-layer updates for the plan's designated
step. Do not create an index or memory artifact merely to match this example.

## Authoring review

Before handing off the script, check that:

- Every approved task maps to a prompt, owner and acceptance result; dependencies
  have a clear order and independent work remains visible.
- Skills are discovered from the live catalogue, used only when relevant and
  named in each prompt; no static list or absolute skill path is embedded.
- Each worker has a non-overlapping write set and enough scope to reconcile safely.
- Checks include expected behavior and a meaningful failure condition; environment,
  input, revision and missing evidence are explicit.
- Operator commands are each one short line runnable from the repository root or
  `PATH`; do not make them depend on a skills, scratch or temporary directory.
- Existing authority, data boundaries and publication rules survive every restart.
- Handoffs preserve completed results, current task, blockers, next action and
  external-effect reconciliation without copying the whole plan.

Avoid single prompts too large for the available context, invented thresholds,
mandatory plugin names, blanket cleanup audits, unbounded delegation, and checks
omitted for brevity. Close out only the risk-relevant integration and recovery work.
