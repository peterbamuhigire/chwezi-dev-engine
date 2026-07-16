# Skills Repository Overview

This repository is a working catalog of reusable AI-assistant skills and
supporting documentation. It combines implementation guidance, product strategy,
security patterns, finance-doctrine orchestration, mobile and game-development guidance, SDLC
documentation templates, and catalog maintenance tooling.

## Latest Update

The 2026-07-15 game-development deepening added focused entrypoints for lean
game-product experiments, game mathematics and deterministic simulation, and
real-time graphics. These sit between orchestration/design and engine-specific
implementation, with explicit evidence, device-performance and ethical-
engagement gates.

## What Is Here

| Area | Location | Notes |
| --- | --- | --- |
| Main skill catalog | `skills/` | Broad software, AI, SaaS, mobile, security, UX, and product skills. |
| Finance doctrine | External `chwezi-accounting-doctrine`; local `doctrine/skills/` reference material | Canonical accounting, audit, reporting, IFRS, controls, and close guidance is loaded from the external engine. |
| SDLC initialization | `00-meta-initialization/` | Entry-point project documentation workflow and examples. |
| Routing docs | `docs/skill-routing-index.md` | Human-readable consolidation and routing policy. |
| Alias data | `docs/skill-aliases.yml` | Machine-readable skill alias map. |
| Source registers | `docs/source-registers/` | Dated official/current references for volatile platform, AI, security, and framework facts. |
| Quality gates | `docs/quality-gates/` | Release blockers and engineering anti-slop governance. |
| Full workflow example | `examples/full-stack-saas-reference/` | FieldOps Ledger end-to-end SaaS evidence pack. |
| Delivery templates | `templates/delivery-dod/` | Reusable evidence-pack template for implementation deliverables. |
| Maintenance scripts | `scripts/` | Guardrail validator, routing smoke test, and setup helpers. |
| CI gates | `.github/workflows/skill-guardrails.yml` | Runs the guardrails and routing smoke test on every push and PR. |
| Integrator + client docs | `docs/USING-IN-A-PROJECT.md`, `docs/CLIENT-VALUE-BRIEF.md` | How to apply the catalogue in a real repo; plain-language client value. |
| Distilled study references | `book-extractions/`, `claude-guides/`, `blog-posts/` | Concise operational synthesis and companion writing; never raw books or whole-work conversions. |

## How To Work In This Repo

1. Identify the relevant skill or routing entry.
2. Read the skill `SKILL.md` and only the references needed for the task.
3. Keep skill frontmatter concise and accurate.
4. Update routing docs when a parent skill absorbs or supersedes another skill.
5. Run both gates before finishing catalog maintenance (CI runs the same two):

   ```powershell
   python -X utf8 scripts\skill_catalog_guardrails.py --report-only
   python -X utf8 scripts\routing_smoke_test.py --report-only
   ```

## Current Catalog Policy

- Active roots are `skills/` and `00-meta-initialization/`.
- Target active catalog size is 150-170 skills.
- The guardrail hard cap is 200 active `SKILL.md` files.
- Finance doctrine is canonical in the external `chwezi-accounting-doctrine`
  engine; local `doctrine/skills/` is retained reference material.
- Current active catalog size is 165 skills.
- Current routing smoke-test suite contains 132 fixtures, with 94% precision@1
  and 100% precision@3.
- Inactive aliases are retained as `ALIAS.md` and routed through
  `docs/skill-aliases.yml`.
- Duplicate finance entrypoints under `skills/finance/` have been deactivated
  and route to retained finance references or the external finance engine.

## Enforced Invariants

The catalogue is a gated engine, not just a document set. Two scripts run in CI
(`.github/workflows/skill-guardrails.yml`) and fail the build on:

- duplicate frontmatter names, over-cap active count, oversized `SKILL.md`,
  over-length descriptions, malformed frontmatter;
- broken `references/`/`templates/` links and stale or dangling aliases;
- a fixtured routing task whose expected skill drifts out of its top matches
  (routing precision is measured, not assumed).

Meaningful implementation work also carries a Delivery Definition of Done pack
(`skills/sdlc-meta/skill-composition-standards/references/delivery-definition-of-done.md`):
tests, release plan, rollback plan, runbook, and maintenance notes, so output is
operable by a team that did not write it.

## Related Docs

- [Project brief](PROJECT_BRIEF.md)
- [Tech stack](TECH_STACK.md)
- [Architecture](ARCHITECTURE.md)
- [Plans index](../plans/INDEX.md)
- [Next features](../plans/NEXT_FEATURES.md)
- [Agent guide](../../AGENTS.md)
- [Using the catalogue in a project](../USING-IN-A-PROJECT.md)
- [Client value brief](../CLIENT-VALUE-BRIEF.md)
- [Production-readiness audit](../evaluation/2026-05-30-production-readiness-audit.md)
