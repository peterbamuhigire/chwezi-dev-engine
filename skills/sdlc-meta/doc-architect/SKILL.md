---
name: doc-architect
description: Use when generating or repairing layered AGENTS.md project guidance, updating project documentation, CLAUDE.md files, and skill module headers after changes or at session close, writing CodeTour .tour onboarding walkthroughs, or fixing Markdown lint without changing meaning. Use sdlc-documentation for SDLC phase document sets.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

## Platform Notes

- Optional helper plugins may help in some environments, but they must not be treated as required for this skill.

# Doc Architect
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Generate Triple-Layer AGENTS.md documentation by scanning a project for its tech stack, data directory, and planning directory. Use when the user asks to standardize project documentation, generate agent files, or create AGENTS.md guides.
- Bring README, architecture, API, schema, agent-hub, and roadmap docs back in line after a significant change, or run the end-of-session documentation close ("update the docs", "close for the day").
- Build a CodeTour `.tour` walkthrough (onboarding, architecture, PR, RCA, security) anchored to real files and lines.
- Clear Markdown lint warnings (MD022, MD031, MD032, MD036, MD040) without changing meaning.

## Do Not Use When

- The deliverable is an SDLC phase document set (plans, SDD, test plans, user manuals) - use `sdlc-documentation`.
- A one-off explanation in chat is enough.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Release evidence | Triple-Layer AGENTS.md output | Generated AGENTS.md covering project tech stack, data directory, and planning directory layers | `AGENTS.md` |
| Release evidence | Documentation update record | Completion record plus roadmap update after a change | `docs/plans/2026-09-24-invoicing-completion.md` |
| Correctness | Markdown lint result | Lint command output and retained exceptions | `markdownlint-cli2 "docs/**/*.md"` clean |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
- `references/doc-maintenance-after-change.md` - load when code, architecture, API, schema, routing, or planning changed and docs must be realigned, or at session close.
- `references/module-header-template.md` - load when refreshing a skill's frontmatter and hero block in a skill engine.
- `references/code-tour.md` - load when the user wants a CodeTour `.tour` walkthrough or a persistent "explain how this works" artefact.
- `references/markdown-lint-cleanup.md` - load when fixing Markdown lint warnings or normalising formatting.
- Use the `templates/` directory when the task needs a structured deliverable.
- Use the `protocols/` directory for formal execution order or handoff rules.
<!-- dual-compat-end -->
Design and generate a portable Triple-Layer AGENTS.md documentation set that reflects the project’s real structure and constraints.

**Modularize Instructions (Token Economy):** Avoid consolidating all AI/dev guidance into a single AGENTS.md. Prefer smaller, focused docs (e.g., docs/setup.md, docs/api.md, docs/workflows.md) and reference them only when needed.

**Documentation Standards (MANDATORY):** ALL generated markdown files must follow strict formatting rules:
- **500-line hard limit** - no exceptions for any .md file
- **Two-tier structure**: High-level TOC (Tier 1) + Deep dive docs (Tier 2)
- **Smart subdirectory grouping** for related documentation
- **See `doc-standards.md` for complete requirements**

## Core Outcome

Produce three aligned AGENTS.md files:

- **Root AGENTS.md**: Project identity, tech stack, global standards
- **Data AGENTS.md**: Data integrity rules and schema governance
- **Planning AGENTS.md**: Spec-driven development workflow

## Trigger Phrases

The skill should activate when the user asks to:

- Standardize project documentation
- Generate agent files
- Update project documentation after a change, or close the session
- Create a code tour or onboarding walkthrough
- Clean Markdown lint warnings

## Absorbed Jobs (load the matching reference)

| Job | Reference | Output |
|---|---|---|
| Realign docs after a change; end-of-session close | [doc-maintenance-after-change.md](references/doc-maintenance-after-change.md) | Updated truth sources, completion record, roadmap |
| Refresh skill frontmatter and hero block | [module-header-template.md](references/module-header-template.md) | Aligned `SKILL.md` header |
| Guided codebase walkthrough | [code-tour.md](references/code-tour.md) | `.tours/<persona>-<focus>.tour` |
| Lint cleanup without meaning change | [markdown-lint-cleanup.md](references/markdown-lint-cleanup.md) | Clean lint run plus retained exceptions |

## Standard Operating Procedure (SOP)

1. **Scan the workspace**
   - Inspect the root for identifiers (README, PROJECT_BRIEF, TECH_STACK, ARCHITECTURE, CLAUDE.md, AGENTS.md, package.json, composer.json, \*.sln, pyproject.toml).
   - Locate likely data directories (database/, schema/, migrations/, sql/, db/).
   - Locate planning/documentation directories (docs/, docs/plans/, planning/, specs/).
   - Identify module/area entry points (menus, docs, feature folders) to group specs.
   - Note template conventions (public/ as web root, per-panel includes, API outside public).

2. **Identify the environment**
   - Determine primary language (PHP/C#/Python or other).
   - Determine DB type (MySQL/PostgreSQL/SQLite/SQL Server/other).
   - Determine deployment environment (Docker/Kubernetes/shared hosting/cloud).

3. **Set up plan grouping (first-time)**
   - Create `docs/plans/<module>/` subdirectories for each discovered module/area.
   - Update `docs/plans/AGENTS.md` with the current module list.
   - Create or update `docs/plans/INDEX.md` as the master plan status index.
   - Ensure the index includes status, urgency, last implementation date, and last modification date.
   - Keep `docs/plans/AGENTS.md` updated whenever plans are added or their status changes.
   - Maintain a folder map at the top of `docs/plans/AGENTS.md` and update it when requested.
   - Note that developers can add new folders and update the list manually.

4. **Generate Triple-Layer docs**
   - Use the templates in [templates/root-agents.md.template](templates/root-agents.md.template), [templates/data-agents.md.template](templates/data-agents.md.template), and [templates/plan-agents.md.template](templates/plan-agents.md.template).
   - Populate with real findings and pull constraints from [references/logic-library.md](references/logic-library.md) as needed.
   - Create files at:
     - **Root**: AGENTS.md at project root
     - **Data**: database/schema/AGENTS.md (or best-fit schema directory)
     - **Planning**: docs/plans/AGENTS.md (or best-fit planning directory)

## Bundled Resources

- [protocols/workflow.md](protocols/workflow.md): 3-step workflow used during generation
- [templates/root-agents.md.template](templates/root-agents.md.template): Root AGENTS.md template
- [templates/data-agents.md.template](templates/data-agents.md.template): Data AGENTS.md template
- [templates/plan-agents.md.template](templates/plan-agents.md.template): Planning AGENTS.md template
- [references/logic-library.md](references/logic-library.md): Domain constraint library for reuse
- [references/doc-maintenance-after-change.md](references/doc-maintenance-after-change.md): post-change and end-of-session documentation workflow
- [references/module-header-template.md](references/module-header-template.md): skill frontmatter and hero-block template
- [references/code-tour.md](references/code-tour.md): CodeTour walkthrough method
- [references/markdown-lint-cleanup.md](references/markdown-lint-cleanup.md): meaning-preserving lint cleanup

## Common Pitfalls

- Do not invent tech stacks. Only infer from files found in the workspace.
- Do not place AGENTS.md in arbitrary locations; follow the best-fit paths above.
- Do not include contradictory rules across the three layers.

## Quick Example

If a project uses Laravel + MySQL with docs/plans and database/schema:

- Root: AGENTS.md → PHP/Laravel, MySQL, deployment standards
- Data: database/schema/AGENTS.md → referential integrity, no-delete rules
- Plans: docs/plans/AGENTS.md → spec.md format and workflow steps

## Cross-References to SDLC Skills

When generating AGENTS.md files, be aware of the complete SDLC documentation ecosystem:

### SDLC Documentation Skills

| Skill | Phase | Documents Generated | When to Reference |
|-------|-------|--------------------|--------------------|
| `sdlc-planning` | Planning | Vision, SDP, SRS, SCMP, QA Plan, Risk Plan, Feasibility | When plans directory contains SDLC planning docs |
| `sdlc-design` | Design | SDD, Tech Spec, ICD, Database Design, API Docs, Code Standards | When referencing architecture and design decisions |
| `sdlc-testing` | Testing | Test Plan, Test Cases, V&V Plan, Test Report, Peer Reviews | When referencing testing and quality standards |
| `sdlc-user-deploy` | Delivery | User Manual, Ops Guide, Training, Release Notes, Maintenance, README | When referencing deployment and user documentation |

### Related Documentation Skills

| Skill | Purpose | Relationship |
|-------|---------|-------------|
| `project-requirements` | Raw requirements interview | Input source for SDLC planning docs |
| `feature-planning` | Feature-level specs + implementation plans | Stored in `docs/plans/` (planning directory) |
| `manual-guide` | End-user manuals and guides | Stored in `/manuals/` (separate from AGENTS.md) |
| `sdlc-documentation` | SDLC phase document sets | Owns planning, design, testing, and deployment documents |

### SDLC Output Directory Structure

When scanning for documentation, expect this structure in projects using SDLC skills:

```
docs/
├── planning/        # sdlc-planning output (7 docs)
├── design/          # sdlc-design output (6 docs)
├── testing/         # sdlc-testing output (5 docs)
├── user-deploy/     # sdlc-user-deploy output (6 docs)
├── plans/           # feature-planning output
│   ├── AGENTS.md    # Plans directory index (doc-architect manages this)
│   ├── INDEX.md     # Plan status tracker
│   └── specs/       # Feature specifications
└── project-requirements/  # project-requirements output
```

**Integration Rule:** When generating the Planning AGENTS.md (`docs/plans/AGENTS.md`), include references to any SDLC documentation directories that exist alongside the plans directory.

## Decision Rules

| Condition | Action |
|---|---|
| Existing guidance is accurate | Preserve and extend it |
| Repository fact is uncertain | Inspect source files first |
| Rule belongs to one subtree | Put it in the nearest scoped file |

## Capability Contract

Read and search are required. Editing requires authorisation.

## Degraded Mode

Fallback: without repository access, return a template and confirmation questions instead of inventing details.

## Domain Anti-Patterns

- Repeating the same long rule at every layer.
- Inferring the stack only from directory names.
- Overwriting authored constraints.
- Linking files that do not exist.
- Putting specialist doctrine in the root navigation file.
## Inputs
| Artefact | Required? | Purpose |
|---|---|---|
| Audience, decisions, source material, document set, and maintenance owner | yes | Design information architecture |
## Outputs
- Produce document architecture, ownership map, navigation, templates, and maintenance rules.
