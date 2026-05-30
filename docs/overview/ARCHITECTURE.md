# Architecture

## System Shape

The repository is a file-based knowledge system. Skill entrypoints live in
`SKILL.md` files, deep references sit beside those skills, and repository-level
docs describe routing, consolidation, planning, and maintenance policy.

## Main Components

| Component | Responsibility |
| --- | --- |
| `skills/` | Main skill catalog for engineering, AI, SaaS, mobile, security, UX, product, and operations, including language entrypoints such as C#/.NET. |
| `doctrine/skills/` | Canonical finance and accounting doctrine. |
| `00-meta-initialization/` | Entry-point workflow for SDLC documentation setup. |
| `docs/skill-routing-index.md` | Human routing map for consolidated and legacy skill names. |
| `docs/skill-aliases.yml` | Machine-readable alias registry. |
| `scripts/skill_catalog_guardrails.py` | Static guardrail scan: active count, duplicate names, frontmatter, UTF-8, description length, `SKILL.md` line count, broken `references/`/`templates/` links, and alias integrity (unrouted, stale, dangling). |
| `scripts/routing_smoke_test.py` + `scripts/routing_fixtures.yml` | Routing precision measurement: scores fixtured tasks against skill descriptions and fails when an expected skill drifts out of its top matches. `--collisions` reports near-duplicate skills. |
| `.github/workflows/skill-guardrails.yml` | CI: runs both gates on every push and PR touching skills, doctrine, aliases, fixtures, or the scripts. |
| `skills/sdlc-meta/skill-composition-standards/references/` | Artifact templates (ADR, entity model, threat model, release/rollback plan, runbook, test plan) and the closing Delivery Definition of Done pack. |
| `claude-guides/` | Skill authoring and Claude-specific usage guidance. |
| `book-extractions/` | Long-form source notes and reference summaries. |

## Skill Loading Model

An active skill is any `SKILL.md` under:

- `skills/`
- `doctrine/skills/`
- `00-meta-initialization/`

Reference material should be stored under directories such as `references/`,
`sections/`, `templates/`, `assets/`, or examples, not as extra `SKILL.md`
files. This keeps active skill count controllable.

Legacy entrypoints that should not be active are kept in-place as `ALIAS.md`.
Those files preserve historical content without participating in loader
routing.

## Routing Model

When multiple narrow skills overlap, prefer one retained parent skill and route
legacy names through:

- `docs/skill-routing-index.md` for human-readable policy.
- `docs/skill-aliases.yml` for machine-readable aliases.
- `ALIAS.md` in the old skill directory when the original content is retained
  but no longer active.

Finance, accounting, audit, close, reporting, controls, IFRS, banking,
reconciliation, and finance UX route first to `doctrine/skills/` unless a root
skill adds distinct implementation behavior.

## Validation And Enforcement

The catalogue's invariants are gated, not just documented. Two scripts run in CI
on every push and PR and fail the build on a violation:

- `skill_catalog_guardrails.py` - structural integrity (count, duplicates,
  frontmatter, line count, description length, broken references, alias
  integrity).
- `routing_smoke_test.py` - routing precision against `routing_fixtures.yml`;
  catches descriptions drifting into ambiguity.

Implementation work closes with the Delivery Definition of Done pack
(`skill-composition-standards/references/delivery-definition-of-done.md`), which
bundles tests, release plan, rollback plan, runbook, and maintenance notes so
the output is operable by a team that did not write it.

## Maintenance Flow

1. Read the relevant `SKILL.md`.
2. Load only necessary local references.
3. Apply the smallest accurate edit.
4. Update routing and overview docs if behavior or catalog policy changed.
5. Run both gates: the guardrail report and the routing smoke test.
6. Record significant documentation repairs in `docs/updates/`.

## Known Constraints

- Markdown files should stay under 500 lines.
- `AGENTS.md` should remain a short navigation hub.
- Avoid deleting compatibility aliases without a migration decision.
- When deactivating an entrypoint, rename only `SKILL.md` to `ALIAS.md`, keep
  the directory intact, and add the target route to `docs/skill-aliases.yml`.
- `doctrine` currently behaves like a special tracked path and should not be
  modified incidentally.
