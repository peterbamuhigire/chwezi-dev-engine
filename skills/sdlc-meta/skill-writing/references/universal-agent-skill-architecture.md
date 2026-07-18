# Universal Agent and Skill Architecture

Parent: [Skill Writing](../SKILL.md)

Use this reference when a project needs one maintainable instruction library across Claude Code, Codex, Copilot, or another runner.

## Source-of-truth decision

Choose one canonical location and record it in the project operating instructions. A common project layout is:

```text
.ai/agents/       model-neutral specialist roles
.ai/skills/       model-neutral reusable procedures
.ai/standards/    shared engineering and domain rules
.ai/workflows/    multi-role assignments and handoffs
```

Runner directories are compatibility layers. They must link to canonical files and add only metadata or behaviour the runner requires.

| Surface | Purpose | Keep out |
|---|---|---|
| `AGENTS.md` | Project rules, architecture constraints, safety, routing links | Full bodies of dozens of roles |
| `.claude/agents/` | Claude subagent metadata, tool allow-list, model policy, canonical links | Duplicated domain expertise |
| `.agents/skills/` | Codex/open-agent triggers and procedure adapters | Unrelated project policy |
| `.github/` instructions | Copilot repository or path-specific adaptation | Another canonical copy |

If a repository already treats `skills/**/SKILL.md` as canonical, preserve that convention. Do not introduce `.ai/` merely to imitate a sample layout.

## Role-definition contract

A specialist role definition must state:

1. Mission and responsibility boundary.
2. Positive triggers and explicit exclusions.
3. Required project context and standards.
4. Capability policy: read, search, edit, execute, network, delegate.
5. Ordered operating workflow.
6. Stop and escalation conditions.
7. Output schema and evidence requirements.
8. Handoff target and unresolved-question format.

Default review, architecture, security-assessment, and planning roles to read-only. Writing access follows an explicit implementation request. Production mutation, credential access, destructive commands, and external publication require separately stated authority.

## Skill-definition contract

A skill describes a repeatable procedure, not an employee persona. It must contain:

- A narrow trigger with neighbour exclusions.
- Required inputs and their producers.
- Ordered steps and decision rules.
- Capability requirements and fallback behaviour.
- Failure modes, stop conditions, and recovery.
- Output artefacts, consumers, evidence, and acceptance tests.

Prefer twelve precise, non-overlapping roles or skills over thirty vague ones. Add a new item only when its trigger, permissions, workflow, or output contract is materially distinct.

## Capability-based wording

Canonical instructions must describe capabilities, not command brands:

| Avoid in canonical source | Prefer |
|---|---|
| "Use the Task tool" | "Delegate bounded independent work when parallel workers are available" |
| "Use apply_patch" | "Use the runner's safest reviewable editing mechanism and inspect the diff" |
| "Use Grep" | "Search the repository before proposing changes" |
| "Run model X" | "Use a model tier adequate for the risk and reasoning depth" |

Adapter files may translate these requirements to runner-specific tools and metadata.

## Thin-adapter pattern

An adapter should contain only:

- Runner-valid frontmatter.
- A sharp trigger description.
- Tool or permission declarations.
- Model selection only when justified; otherwise inherit or omit it.
- Paths to project rules, standards, and the canonical role or skill.
- Runner-specific output or delegation mechanics.

Add an automated drift check when adapters are generated. At minimum, verify that every canonical path exists and that adapters do not reproduce large canonical sections.

## Multi-agent workflow rules

Use multiple workers only when tasks are independent enough to proceed concurrently or require genuinely distinct review lenses.

1. Define one owner for the final decision.
2. Give each worker a bounded question, inputs, permissions, and output schema.
3. Prevent overlapping edits unless an explicit merge strategy exists.
4. Wait for all required reports.
5. Reconcile disagreements against evidence and project constraints.
6. Return one consolidated result, not a transcript bundle.

Do not delegate a chain of dependent decisions as though they were parallel. Do not let specialist recommendations silently override project-wide rules.

## Acceptance tests

For each role, skill, and adapter set, test:

| Test | Pass condition |
|---|---|
| Positive trigger | Correct item loads for a representative request |
| Negative trigger | Minor or neighbouring work does not load it |
| Collision | The closest competing route loses for a documented reason |
| Capability degradation | A useful safe result is returned without optional tools |
| Permission boundary | Read-only work does not edit; mutation requires authority |
| Failure path | Missing context or failed tools produce a named stop/recovery action |
| Output contract | Required artefacts, evidence, risks, and questions are present |
| Adapter drift | Every adapter resolves its canonical sources and contains no stale copy |

## Common failure modes

- **Role-skill blur:** a persona and several procedures are fused into one huge file. Split identity from SOPs.
- **Prompt duplication:** the same expertise is copied into every runner directory. Select one owner and reduce adapters to links plus metadata.
- **Permission inflation:** all roles receive shell, write, or network access. Grant the minimum capability required by the role.
- **Model pinning by habit:** a named model becomes stale. Inherit by default and pin only against an explicit quality/cost/latency reason.
- **Context flooding:** `AGENTS.md` embeds the entire library. Keep it as an operating and routing manual.
- **Unverified execution:** instructions assume edits or tools succeeded. Require result inspection and evidence.
