# Skills Repository

This repository is a curated catalog of reusable AI skills: compact execution
guides that help agents and humans do higher-quality work with less repeated
setup. The skills cover software engineering, AI systems, SaaS operations,
security, product work, mobile platform code, architecture, documentation
workflows, and finance-doctrine orchestration.

The catalog is designed to be routed by name. A small active surface keeps
skill selection reliable, while deeper references stay available without making
every topic an active entrypoint.

## Latest Update: WWDC26 Apple Platform Modernization

As of 2026-06-21, the active Apple/mobile guidance is current for WWDC26-era
development while staying under the active catalog cap. Existing iOS and
cross-platform mobile skills were updated rather than promoted into new active
entrypoints.

Key Apple updates now covered by the catalog:

- Xcode 27, Apple Silicon build assumptions, Device Hub, Xcode Cloud,
  TestFlight, and release-evidence gates.
- Swift 6.4-ready testing/concurrency guidance and latest-SDK availability
  discipline.
- Foundation Models, Language Model providers, Dynamic Profiles, Core AI,
  Core ML, Evaluations, and privacy-preserving AI fallbacks.
- App Intents, App Entities, App Schemas, View Annotations, Siri, Spotlight
  semantic indexing, widgets, and App Intents Testing.
- Safari/WebKit 27 PWA checks and Apple platform operations for mixed
  Android/iOS delivery.
- Design-layer routing to `design-system-skills` for current Apple UI:
  Liquid Glass, SF Symbols 8, Dynamic Type, haptics, accessibility settings,
  and resizable iPhone/iPad/Mac-designed-for-iPhone QA.

## Architecture & cross-cutting engines (updated 2026-06-21)

- **Relocated.** This engine (`skills-web-dev`, the engineering catalog) moved on
  2026-06-21 from `C:\Users\Peter\.claude\skills` to `C:\wamp64\www\skills-web-dev`.
- **No native discovery.** No skill engine — this one included — is natively
  discovered by Claude Code anymore. ALL engines are consulted via the user's
  global routing table (`~/.claude/CLAUDE.md` / `AGENTS.md`) by globbing their
  `SKILL.md` files directly (read those files; do not rely on the Skill tool).
- **What this engine keeps.** Engineering skills only: backend and databases,
  devops and cloud, security, languages, mobile platform code, architecture, AI
  systems, SaaS, product, documentation, and finance-doctrine orchestration.
- **Design moved out.** ALL design / typography / UI/UX / visual-formatting
  skills plus the anti-AI-slop doctrine now live in the cross-cutting
  **`design-system-skills`** engine (`C:\wamp64\www\design-system-skills`). It is
  **referenced, not mirrored** — resolve its path per device from the global
  routing table and consult it IN ADDITION to this engine for any
  presentation-layer work. Skills migrated out of here include the frontend-ux
  design cluster (`design-audit`, `healthcare-ui-design`, `motion-design`,
  `practical-ui-design`, `webapp-gui-design`, `interaction-design-patterns`,
  `enterprise-ux-process`), `ai-agent-ux`, `ai-output-design`,
  `android-ui-ux-design`, `ios-ui-ux-design`, and the dedup canonicals
  `data-visualization`, `form-ux-design`, and `premium-ui-ux-design`.
- **Finance is referenced, not mirrored.** Canonical finance/accounting doctrine
  (`chwezi-accounting-doctrine`) is a separate cross-cutting engine, resolved per
  device from the global routing table and consulted alongside this one.

## Why These Skills Matter

| Benefit | What it gives you |
| --- | --- |
| Faster execution | Reusable workflows reduce repeated prompting and rediscovery. |
| Better routing | Clear frontmatter, aliases, and parent skills help agents pick the right guidance. |
| Higher quality | Skills encode checklists, quality gates, anti-patterns, and evidence expectations. |
| Safer specialization | Finance, security, AI, and platform work keep domain constraints close to implementation guidance. |
| Portable knowledge | Markdown, YAML, templates, and scripts work across Windows, Ubuntu, and Debian consumers. |
| Lower catalog noise | Legacy and narrow topics route through aliases instead of competing as duplicate active skills. |
| Enforced quality | CI gates fail the build on broken references, stale aliases, duplicates, oversized files, or a routing regression - the catalogue stays an engine, not a stale pile. |
| Maintainable handoff | Meaningful work closes with a Delivery Definition of Done pack (tests, release, rollback, runbook, maintenance notes). |

## Active Catalog

Active skills are `SKILL.md` files under these roots:

| Root | Purpose |
| --- | --- |
| [`skills/`](skills/) | Main active catalog for engineering, AI, SaaS, mobile, security, UX, product, and operations. |
| [`00-meta-initialization/`](00-meta-initialization/) | SDLC documentation initialization and new-project entrypoints. |

`doctrine/skills/` remains in this repository as retained reference material.
It is not part of this engine's active catalog. Current finance/accounting
doctrine routes through the external `chwezi-accounting-doctrine` engine from
the global routing table.

Current guardrail baseline:

| Metric | Value |
| --- | ---: |
| Active `SKILL.md` files (`skills/` + `00-meta-initialization/`) | 142 |
| Target active catalog size | 150-170 |
| Guardrail hard cap | 200 |
| Duplicate frontmatter names | 0 |
| Near-duplicate skill pairs (collision-checked) | 0 |
| Inactive aliases retained as `ALIAS.md` | 48 |

The guardrail script is the source of truth for these numbers; the table above is
a convenience snapshot. Rerun the report after any catalog change rather than
trusting the prose. The active `skills/` count now sits below the 150-170 soft
target after the 2026-06-21 migration of design/UI/UX skills to the
`design-system-skills` engine (well under the 200 hard cap). Routing quality is
no longer judged by raw count alone:
`scripts/routing_smoke_test.py` measures routing precision against a task fixture
(currently 39 fixtures, precision@1 92%, precision@3 100%) and its
`--collisions` mode reports five known neighbour pairs. Those pairs are
intentional concern splits such as engineering vs operations, analytics vs AI
analytics, and SaaS vs AI entitlements. The remaining skills are distinct and
deliberately retained.

Run the guardrail report with:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
```

## Skill Domains

| Domain | Examples |
| --- | --- |
| AI and agent systems | AI architecture, RAG, evaluations, model gateways, agent runtime, HITL, governance, observability, cost controls, and AI UX. |
| Software engineering | Architecture, APIs, C#/.NET, TypeScript, JavaScript, PHP, Python, Node.js, testing, validation, release engineering, and reliability. |
| SaaS and product | Multi-tenancy, entitlements, pricing, billing, onboarding, metrics, sales operations, product discovery, and product-led growth. |
| Security and compliance | Web app audits, code safety, network security, Linux hardening, DPIA work, and AI security controls. |
| Frontend engineering | React, Next.js, Tailwind, frontend performance, image/asset optimization, and PWA/offline patterns. (Design/typography/UI/UX skills moved to the `design-system-skills` engine — see "Architecture & cross-cutting engines".) |
| Mobile | Android, iOS, Kotlin Multiplatform, mobile persistence, Apple WWDC26-era AI/App Intents/platform capabilities, app quality, StoreKit, PWA/Safari checks, and release workflows. |
| Finance doctrine | Local orchestration skills plus external `chwezi-accounting-doctrine` for accounting, audit, controls, close, reporting, IFRS, payroll, inventory, and finance UX doctrine. |
| Documentation and operations | SDLC documentation, project requirements, professional document output, catalog maintenance, skill writing, and update records. |
| Consulting delivery and bid control | Control-room operations, document/spreadsheet tooling readiness, and red-team quality gates for high-stakes bids, donor submissions, workbooks, dashboards, and consulting deliverables. |
| Quality guardrails (cross-cutting) | `anti-ai-slop` is a real-time guardrail applied continuously on every generated output. `ai-slop-audit` runs after each major iteration and auto-runs on any request to analyse/review/audit/de-slop any artefact type (app, website, business plan, SRS/spec, proposal, blog, social post, document, image, or codebase); a grade-F verdict blocks progression. |

## How To Use The Catalog

1. Start with the active roots above or the overview in
   [`docs/overview/README.md`](docs/overview/README.md).
2. If an old skill name is mentioned, check
   [`docs/skill-routing-index.md`](docs/skill-routing-index.md) or
   [`docs/skill-aliases.yml`](docs/skill-aliases.yml).
3. Read the selected skill's `SKILL.md`.
4. Load only the specific `references/`, `templates/`, or `scripts/` files the
   skill tells you to use.
5. When changing routing, frontmatter, or active skill behavior, update the
   routing docs and rerun the guardrail report.

## Routing And Aliases

The catalog intentionally keeps aliases outside the active skill count. Legacy
entrypoints that should no longer compete for routing are retained as
`ALIAS.md` files in their original directories. Their targets are recorded in:

- [`docs/skill-routing-index.md`](docs/skill-routing-index.md) for human-readable policy.
- [`docs/skill-aliases.yml`](docs/skill-aliases.yml) for machine-readable routing.

Finance aliases may resolve to retained `doctrine/skills/` reference material,
but active finance doctrine should be loaded from the external
`chwezi-accounting-doctrine` engine. Root-level finance skills remain active
only when they add implementation or orchestration behavior beyond doctrine.

## Repository Map

| Path | Role |
| --- | --- |
| [`docs/`](docs/) | Overview docs, architecture, routing policy, plans, analysis, and update records. |
| [`.github/workflows/`](.github/workflows/) | CI gates: catalog guardrails and routing smoke test on every push and PR. |
| [`scripts/`](scripts/) | Catalog guardrail validator, routing smoke test (`routing_smoke_test.py` + `routing_fixtures.yml`), and setup helpers. |
| [`claude-guides/`](claude-guides/) | Claude-specific skill creation and invocation guidance. |
| [`book-extractions/`](book-extractions/) | Curated source notes and long-form reference material. |
| [`blog-posts/`](blog-posts/) | Draft educational and marketing content. |

## Maintenance Rules

- Do not delete or move skill directories casually.
- Deactivate legacy entrypoints by renaming `SKILL.md` to `ALIAS.md` and adding
  a route in `docs/skill-aliases.yml`.
- Keep finance and accounting doctrine in the external
  `chwezi-accounting-doctrine` engine; keep local `doctrine/skills/` as retained
  reference material only.
- Keep Markdown files below 500 lines where practical.
- Use ASCII unless an existing file requires another character set.
- Preserve user edits and inspect the worktree before modifying files.
- Record substantive documentation repairs under [`docs/updates/`](docs/updates/).

## Key Docs

| Document | Purpose |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Short working rules for coding agents. |
| [`docs/overview/PROJECT_BRIEF.md`](docs/overview/PROJECT_BRIEF.md) | One-page project brief. |
| [`docs/overview/ARCHITECTURE.md`](docs/overview/ARCHITECTURE.md) | Repository structure and ownership boundaries. |
| [`docs/overview/TECH_STACK.md`](docs/overview/TECH_STACK.md) | Tooling, runtime assumptions, and platform notes. |
| [`docs/plans/INDEX.md`](docs/plans/INDEX.md) | Planning document index. |
| [`docs/plans/NEXT_FEATURES.md`](docs/plans/NEXT_FEATURES.md) | Current priorities and next work. |
| [`docs/USING-IN-A-PROJECT.md`](docs/USING-IN-A-PROJECT.md) | How to apply the catalogue in a real project without copying doctrine. |
| [`docs/CLIENT-VALUE-BRIEF.md`](docs/CLIENT-VALUE-BRIEF.md) | Plain-language value statement for clients (architecture-free). |

<!-- design-system-skills:trigger v1 -->
### Design / typography / UI/UX (cross-cutting — consult IN ADDITION)

Any work touching how an artifact LOOKS — font/typeface choice, type scale, colour, layout/grid,
visual identity, web/desktop/mobile UI screens, or the visual formatting of a DOCX/PPTX/PDF/XLSX
— routes to the **`design-system-skills`** engine, the single home for ALL design/UI/UX skills
and the anti-AI-slop doctrine.

**Resolve its location on THIS device from your global engine-routing table** (`~/.claude/CLAUDE.md`,
or `AGENTS.md` for Codex) — never assume an absolute path; it varies per machine. Then read its
`README.md` → `doctrine/design-doctrine.md` → glob `skills/**/SKILL.md` fresh and route by
frontmatter (read SKILL.md directly, not via the Skill tool). Content and structure stay in THIS
engine; presentation comes from design-system-skills. Hard rule: never use a banned AI-slop font
(Inter, Geist, Roboto, Arial, Open Sans, Lato, Space Grotesk, bare system stacks) as primary
type — state the chosen typeface and reason before producing any artifact.
<!-- /design-system-skills:trigger -->
