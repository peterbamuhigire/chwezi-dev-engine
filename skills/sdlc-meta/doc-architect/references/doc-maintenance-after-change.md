# Documentation Maintenance After Change

Parent skill: [doc-architect](../SKILL.md). Absorbed from the retired
`update-claude-documentation` skill (2026-09-24); its original text is retained in
`skills/sdlc-meta/update-claude-documentation/ALIAS.md`.

Load this reference when a feature, architecture, dependency, API, schema, routing, or
planning change has landed and the project documentation must be brought back into line
with the code, or when the user closes a work session ("update the docs", "close for the day").

## Core principle

Documentation tells one story. Each file serves a different reader, but every file must
describe the same reality. Update the precise documents first and the summaries last, and
never record planned behaviour as shipped behaviour.

## When to run, and when not to

| Run it | Skip it |
|---|---|
| Feature added or removed | Typo fixes (just fix them) |
| Architecture or design-pattern change | Code comments |
| Dependency or tech-stack change | Work in progress not yet merged |
| API endpoint or database schema change | Internal refactor with no boundary or behaviour change |
| Directory restructuring or workflow change | |
| End of a work session | |

## Typical documentation set and owners

Adapt to what the project actually has; do not create files the project does not use.

| File | Reader | Purpose | Update trigger |
|---|---|---|---|
| `PROJECT_BRIEF.md` | Stakeholders, new developers | 30-second overview | Major changes |
| `README.md` (or `docs/overview/README.md`) | Developers | Setup and usage | Feature additions |
| `TECH_STACK.md` | Developers, DevOps | Technology inventory and environments | Stack changes |
| `ARCHITECTURE.md` | Senior developers, architects | System design and boundaries | Architecture changes |
| `docs/API.md` | API consumers | API reference | API changes |
| `docs/DATABASE.md` | Backend developers, DBAs | Schema reference | Schema changes |
| `AGENTS.md` / `CLAUDE.md` | Coding agents | Navigation hub and project rules | Pattern or workflow changes |
| `docs/plans/NEXT_FEATURES.md` | Team, agents | Priority roadmap | Every session |
| `docs/plans/INDEX.md` | Team, agents | Plan status index | Plan status changes |
| Agent memory file (for example `MEMORY.md`) | Agents | Durable learnings | End of session |

## Change-to-file map

| Change | Always update | Update when affected |
|---|---|---|
| New feature | README usage, `docs/plans/NEXT_FEATURES.md`, `docs/plans/INDEX.md` | API, DATABASE, ARCHITECTURE, AGENTS, PROJECT_BRIEF, memory |
| Tech-stack change | TECH_STACK | README setup, ARCHITECTURE, AGENTS workflows |
| Architecture change | ARCHITECTURE | README overview, AGENTS patterns, PROJECT_BRIEF |
| API or schema change | `docs/API.md` or `docs/DATABASE.md` | ARCHITECTURE contracts, AGENTS patterns, README usage |
| Skill or routing change (skill engines) | Touched `SKILL.md` frontmatter and hero block, router, routing index, fixtures | Update note under `docs/updates/` |

When a project runs in several environments (for example Windows development, Ubuntu
staging, Debian production), keep the environment table and cross-platform rules in
TECH_STACK and the agent hub current whenever either file is touched.

## Workflow

1. **Understand the change.** Record type, a one-sentence description, who is affected, and
   whether it breaks anything.
2. **Map to files**, specific to general: technical specs (API, DATABASE) -> architecture and
   stack -> agent instructions -> user guides -> overview -> roadmap.
3. **Read the current state** of every affected file before editing.
4. **Review module headers.** In skill engines, open every touched `SKILL.md` and check the
   frontmatter `name`/`description` and opening sections against
   [module-header-template.md](module-header-template.md).
5. **Update systematically.** Per file: primary section, related sections, examples and
   snippets, migration notes for breaking changes.
6. **Verify consistency** across files: terminology, version numbers, file paths, component
   names, feature descriptions.
7. **Run or mark examples.** Execute changed examples where possible; otherwise label them
   unverified. Never claim an example works without evidence.
8. **Update the roadmap** (`docs/plans/NEXT_FEATURES.md`): move completed items to
   "Recently completed" with date and one-line summary, re-rank priorities, revise estimates,
   and refresh the recommended next-session plan.

## End-of-session procedure

When the user closes a session:

1. Write a completion record `docs/plans/YYYY-MM-DD-<feature>-completion.md`: what changed,
   bugs fixed, patterns introduced, lessons learned, and verification evidence.
2. Update `docs/plans/INDEX.md` status and completion dates.
3. Update `docs/plans/NEXT_FEATURES.md` (mandatory, even when nothing else changed).
4. Record durable learnings in the agent memory file: patterns, mistakes to avoid, response
   shapes, key file locations.
5. Optionally write a short end-of-day summary with next-session priorities.

Roadmap template (plain headings, no emoji):

```markdown
## Critical priority
<feature> - why critical, estimate, starting point

## High priority
<feature> - why, estimate, starting point

## Medium priority
<feature> - why, estimate, starting point

## Recently completed
<feature> - completion date, one-line summary
```

## Agent hub discipline

- Keep `AGENTS.md` / `CLAUDE.md` a navigation hub, roughly under 10,000 characters: essential
  rules, routing, safety, and links. Move long workflows and module guides into `docs/<area>/`.
- Keep new documentation under `docs/<area>/`; the root README should point into `docs/`.
- Respect the 500-line limit per Markdown file; split into a table-of-contents file plus
  topic files when a document grows past it.

## Common mistakes and fixes

| Mistake | Fix |
|---|---|
| Updating only the README | Walk the change-to-file map; update every affected truth source |
| Three names for one component across files | Pick one term and apply it everywhere |
| Renamed endpoint, old path still in examples | Add migration notes wherever the old path appears |
| Summary updated before the specification | Update API/DATABASE first, overview last |
| 40k-character agent hub duplicating guides | Replace sections with links to `docs/` topic files |
| Recording roadmap items as completed behaviour | Separate current state from plan |
| Rewriting unrelated docs for style | Keep the edit scoped to the actual delta |

## Quality gate

- A new developer can set up and run the project from the README alone.
- The agent hub reflects the new pattern or workflow.
- Breaking changes are marked everywhere they apply.
- Examples are executed or explicitly marked unverified.
- No contradictions remain between files.
- The roadmap reflects this session.

## Degraded mode

Without source or diff access, produce a change plan and a list of documents to verify rather
than asserting current behaviour.
