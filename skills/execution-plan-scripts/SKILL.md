---
name: execution-plan-scripts
description: Author multi-prompt execution scripts for long-running plans across sessions and subagents. Use when a plan must be split into self-contained prompts. Refer to required skills by name, never a hardcoded path, so each environment can resolve its own library.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  - gemini-cli
---

## About this skill (self-awareness)

This skill is itself a member of the **domain engine** — the same library of craft skills it instructs you to reference when authoring a script. It is the meta-skill for the *planning* and *documentation* surface of software and app development. Other engine members (e.g. `mysql-best-practices`, `php-security`, `healthcare-ui-design`, `android-tdd`, `swiftui-design`, `multi-tenant-saas-architecture`) are the *implementation* surface.

Because it lives inside the engine, this skill MUST:

1. **Discover siblings dynamically.** Do not paste a static list of available skills into a script. Instead, enumerate the skills library at author-time and pick the relevant ones by name. On any environment, the listing command is whatever the local `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` documents (e.g. `ls $SKILLS_HOME` or `ls <web-dev-library>/skills/`). The author session runs the command, reads the listing, picks the relevant skill names, and quotes them by name in the script.
2. **Refer to siblings by name only.** This skill never paths to a sibling (`/Users/.../skills/mysql-best-practices/SKILL.md`) — it names it (`mysql-best-practices`). The executor's environment resolves the path.
3. **Refresh its category knowledge each use.** New skills land in the library all the time. Treat the categories table at the bottom of this file as a stable taxonomy of *kinds* of skill (security, db, ui, mobile, etc.) — not a frozen registry of skill names. Re-list the library before authoring.
4. **Self-load when relevant.** Whenever a plan or runbook is being written or executed for software/app development, this skill SHOULD be loaded — the project's `CLAUDE.md` "mandatory pairings" entry for `execution-plan-scripts` enforces this. If a sibling skill is being applied to a multi-prompt deliverable, this skill is its companion.

## Use When

- A plan has more open tasks than one session can credibly execute (rule of thumb: > ~30 tasks, or > 10 file surfaces, or mixes web + mobile + infra).
- The work crosses dependency boundaries that benefit from session-level checkpoints (operator review between prompts).
- Subagents will be dispatched from inside one or more of the prompts (per-prompt fan-out).
- The deliverable is a runnable script (a markdown file the operator pastes prompt-by-prompt), not the implementation itself.
- A sibling domain skill is being applied to a multi-prompt workstream — this skill is the companion that wraps it.

## Do Not Use When

- The task fits in a single session — use the plan directly with `superpowers:executing-plans` or `plan-implementation`.
- The work is open-ended research or design — use `superpowers:brainstorming` or `feature-planning` first.
- You don't have a written plan yet — write it first with `superpowers:writing-plans` or `feature-planning`.

## The Two-Engine Skills Model

Every prompt in an execution-plan script names skills from **two engines**:

| Engine | Purpose | How to enumerate |
|---|---|---|
| **Process engine** (e.g. `superpowers:*`) | HOW work is done — TDD cadence, subagent fan-out, verification gates, code review | Loaded by the host platform (Claude Code plugin manager / Codex / Gemini CLI). The session lists them via the platform's skill discovery (`Skill` tool listing, `/skills`, etc.). |
| **Domain engine** (the craft library this skill lives in) | WHAT good looks like — language standards, framework patterns, security baselines, UX rules | The session lists them by enumerating the library's `skills/` directory. Path is resolved from the local environment's `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` — never hardcoded. |

Author-time discipline:

1. **List both engines** before writing the script — do not work from memory of "what skills exist."
2. **Pick by name** — the author session quotes only the names that apply to each prompt.
3. **Re-quote in subagent prompts** — subagents do not inherit the parent session's skill state, so each subagent prompt repeats the names it needs.
4. **Never path** — a name in this script is a contract that the executor will resolve to a path on its own machine.

Process-engine examples (current as of this skill's last edit; the host platform is authoritative):

  `superpowers:executing-plans`, `superpowers:test-driven-development`,
  `superpowers:subagent-driven-development`, `superpowers:dispatching-parallel-agents`,
  `superpowers:verification-before-completion`, `superpowers:systematic-debugging`,
  `superpowers:requesting-code-review`, `superpowers:receiving-code-review`,
  `superpowers:brainstorming`, `superpowers:writing-plans`,
  `superpowers:finishing-a-development-branch`.

Domain-engine taxonomy (kinds, not a frozen registry — re-list the library at author-time):

  Security · API contract · Database/migration · Multi-tenancy/RBAC ·
  Web UI/UX · Mobile (Android / iOS / KMP) · Healthcare-UI / domain-UX ·
  Performance · Testing/SDLC · DevOps/CI · Content/i18n · Architecture.

This skill (`execution-plan-scripts`) sits in the SDLC + Architecture corner of the domain engine. When you author a script, list its siblings and pick from the categories above — do not work from a frozen list inside this file.

## Path-Resolution Rule (cross-platform)

> **Never hardcode the skills library location.** Each environment (mac, linux, windows, codespaces, CI) keeps its own `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` (or equivalent) that tells the executing session *where* its skills live. The execution-plan script only quotes skill names; the executor resolves them.

In your script, write:

> Read these skills in full before any code: `mysql-best-practices`, `php-security`, `multi-tenant-saas-architecture`, `dual-auth-rbac`, `sdlc-testing`, `healthcare-ui-design`, `api-error-handling`.

NOT:

> Read `/Users/alice/skills/mysql-best-practices/SKILL.md` …

The executor finds the file by following the path rule its own environment defines (e.g. macOS: `~/Sites/skills-web-dev/skills/<name>/SKILL.md`; Linux dev box: `~/skills-lib/<name>/SKILL.md`; CI: `$SKILLS_HOME/<name>/SKILL.md`). Skill names are stable; paths are not.

## Prompt Anatomy

Every prompt in the script follows this structure:

```
## Prompt N — <one-line scope>

```
You are <doing what> in <repo>. Read these files first, in this order:

1. <project root>/CLAUDE.md
2. <plan-root>/INDEX.md
3. <plan-root>/AGENT_BRIEF.md (or equivalent invariants doc)
4. <phase>/README.md
5. <phase>/plan.md (focus: lines A–B if a sub-range)

Then invoke these skills in order, before any code:

  Skill tool (process engine):
    - superpowers:<process-skill-1>
    - superpowers:<process-skill-2>
    - superpowers:verification-before-completion   ← always last in the list

  Read these domain skills in full (resolve paths from your environment):
    - <domain-skill-1>
    - <domain-skill-2>
    - <healthcare-ui-design or other PRIMARY skill, re-read per page Task>

Track each Task with TaskCreate.

Work plan:

A. <serial pre-requisite tasks the parent session owns>

B. <fan-out section> — dispatch in a single message with N Agent calls,
   subagent_type: general-purpose. Each subagent prompt MUST include:
     - The Task IDs and plan.md line ranges it owns
     - The exact list of domain skills to read first (by NAME)
     - The file scope it is allowed to touch
     - The RED-GREEN-COMMIT discipline sentence
     - Subagents do NOT inherit the parent's skill state — re-state every skill name.

C. Verification gate (no claim without evidence):
     <exact commands to run, with expected green outcome>

D. Status updates in plan.md (`- [ ] **Status:** pending` → `- [x] complete (<hash>)`)

E. Final report ≤200 words: commits, tests added, deviations.

Do NOT push. Do NOT touch other phases. Do NOT modify INDEX until the
phase's final prompt.
```
```

## Fan-Out Rules

- **Bucket subagents by file scope.** Two subagents must never write to the same file. If they would, fold them into one subagent or split the file first.
- **One message, N tool calls.** Parallel subagents are dispatched in one assistant message containing N `Agent` tool uses. Sequential dispatch wastes time.
- **State the file scope explicitly.** `Allowed: src/Imaging/Services/*, tests/Unit/Imaging/*. Forbidden: anything else.` Subagents will respect a clear scope.
- **Re-inject skills.** Every subagent prompt repeats the skill names it must read. They do not inherit parent skill state.
- **Cap fan-out at ~7.** Beyond that, results are hard for the parent session to review. Split into two prompts.

## Sequencing Rules

- **Critical-path serial.** If Prompt N produces an artefact (frozen API spec, schema, design tokens) consumed by Prompt N+1, run them in order.
- **Independent siblings.** When two phases have no shared state, they can be siblings — but still keep them as separate prompts so the operator can review between.
- **No prompt pushes.** Push, PR, and release decisions live with the operator after the final prompt completes.
- **Final prompt is always cleanup.** Static analysis, security audit, multi-tenant leak hunt, i18n parity, dead-code/yellow-flag sweep, INDEX flip. Never bury this work inside a feature prompt.

## Verification Gate (per prompt)

Every prompt ends with the same gate, drawn from `superpowers:verification-before-completion`:

```
Run and capture output verbatim:
    <test-suite command>
    <static-analysis command>
    <linter command>
    <multi-tenant / leak / parity grep>
Every command must be green. If anything is red, fix in this session —
do NOT defer to a later prompt.
```

A "done" claim without the output pasted is forbidden.

## Operator-Action Surfacing

Some work needs human-only steps (signing keys, cloud accounts, real-device tests, App Store / Play Console). The script must:

1. Surface the prerequisite at the **top** of the prompt that needs it.
2. Tell the executor: "STOP and ask if absent."
3. If the answer is "skip", leave the affected test `@Ignore`d / `xfail`ed and surface it in the final report.

Never silently skip operator actions.

## Index / Status Hygiene

- Phase Tasks: every prompt flips `- [ ] **Status:** pending` to `- [x] **Status:** complete (<hash>)` at the end.
- Phase status in `INDEX.md`: only the **last prompt of a phase** flips the row to `complete`.
- Authoring-progress log in `INDEX.md`: append a dated entry referring to the session.
- Memory layer: only the cleanup prompt may write to long-term memory (frozen-contract pointer, post-launch follow-ups location).

## Anti-Patterns

- Hardcoded skill paths (`/Users/alice/skills/...`) — environments differ.
- Skill names in the script header but not re-stated in subagent prompts — subagents lose them.
- A single mega-prompt covering > ~30 Tasks — context exhaustion, lost discipline.
- Verification commands omitted "to keep the prompt short" — verification is the prompt.
- Fan-out without file-scope — subagents collide on the same file.
- Final prompt without static analysis + security audit + INDEX flip.
- Pushing or merging from inside a prompt — operator decides.
- Re-implementing scaffolded code "to be clean" instead of verifying what's there (violates TDD's iron law against tests-after-code).

## Authoring Checklist

Before handing the script to the operator, verify:

- [ ] Every prompt names process skills (`superpowers:*`) AND domain skills (by name only).
- [ ] No absolute path to a skill file appears anywhere in the script.
- [ ] Every fan-out subagent prompt re-injects the skill names it needs.
- [ ] Every fan-out has explicit, non-overlapping file scope.
- [ ] Every prompt ends with a verification gate that names exact commands.
- [ ] Operator-action prerequisites are surfaced at the top of the affected prompt with a STOP-and-ask instruction.
- [ ] The final prompt does cleanup: static analysis, security audit, multi-tenant leak hunt, i18n parity, dead-code/yellow-flag sweep, INDEX flip, memory write.
- [ ] No prompt pushes, force-pushes, or opens PRs.
- [ ] Status updates: each prompt flips its Task statuses; only the last prompt of a phase flips the phase row in `INDEX.md`.
- [ ] The script preface lists the sequence overview as a table (prompt #, scope, parallelism, subagent count) so the operator sees the shape at a glance.

## Companion skills (named, not pathed)

The companions below are the *kinds* of skill you will most often pair with this one. Re-enumerate the library at author-time to confirm names and discover new arrivals — never work from this list as a frozen registry.

- `superpowers:writing-plans` or `feature-planning` — author the underlying plan first.
- `superpowers:executing-plans` or `plan-implementation` — what each prompt invokes when it runs.
- `superpowers:subagent-driven-development` — fan-out discipline.
- `superpowers:dispatching-parallel-agents` — when to parallelise.
- `superpowers:verification-before-completion` — the closing gate of every prompt.
- `sdlc-testing` — test pyramid + RED→GREEN→COMMIT cadence the prompts enforce.
- `code-safety-scanner` — used in the cleanup prompt.
- `web-app-security-audit` — used in the cleanup prompt.
- The relevant *domain* skills for the workstream (security, db, framework, UI, mobile, etc.) — picked by enumerating the library each time.

## Outputs

- A markdown file (e.g. `docs/<scope>/clear-debt.md`, `docs/runbooks/<release>.md`) containing:
  - Preface (purpose, how-to-use, sequence-overview table, hard-rule for skills).
  - A "Skills Engine" section that names the two engines and lists which skills apply where.
  - N self-contained prompts (each runnable in a fresh session, never assuming prior conversation context).
  - Operator notes (run order, no-push rule, prerequisite list, deferred-test policy).
