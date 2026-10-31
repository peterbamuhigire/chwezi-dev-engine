# Architecture

## System Shape

The repository is a file-based knowledge system. Skill entrypoints live in
`SKILL.md` files, deep references sit beside those skills, and repository-level
docs describe routing, consolidation, planning, and maintenance policy.

## Main Components

The provider-neutral AI contract layer lives under `tools/ai/`: shared context
packets and prompt cards are pure data assembly, tool provenance delegates
consequential approval to the existing gate, and deterministic planning stops
at a plan result. None of these helpers executes external side effects.

| Component | Responsibility |
| --- | --- |
| `skills/` | Main skill catalog for engineering, AI, SaaS, mobile, game development, security, UX, product, and operations, including C#/.NET and consolidated enterprise Java/JVM entrypoints. |
| `skills/languages/php-modern-standards/` | PHP code and application compatibility guidance, with dated runtime-upgrade evidence; host/package cutover remains with the Linux operations engine. |
| External `chwezi-accounting-doctrine` checkout | Canonical finance doctrine; kept outside the runtime skill catalog. |
| `00-meta-initialization/` | Entry-point workflow for SDLC documentation setup. |
| `docs/skill-routing-index.md` | Human routing map for consolidated and legacy skill names. |
| `docs/skill-aliases.yml` | Machine-readable alias registry. |
| `docs/source-registers/` | Dated official/current sources for volatile AI, Apple, cloud, security, and framework guidance. |
| `docs/quality-gates/` | Release-blocking gates and engineering anti-slop governance. |
| `docs/world-class-exemplars/` | Shared running example and benchmark reference outputs. |
| `docs/sept-matt-pocock/` | Verified external-repository comparison, cross-engine ownership map, execution runbook, and 2026-09-11 completion/evidence record. It is evidence, not an active skill root. |
| `examples/full-stack-saas-reference/` | End-to-end SaaS evidence pack exercising architecture, API, security, reliability, and release skills. |
| `examples/tenant-invoice-listing/` | Synthetic read-only invoice slice across PHP, Next.js, OpenAPI, and Compose; runtime limitations are stated in its README. |
| `docs/kaizen/2026-10-engine-kaizen/` and `docs/kaizen/2026-10-engine-kaizen-pass-2/` | Frozen baseline, selected changes, validation, final report, and next-cycle handoff for the two October 2026 engine Kaizen passes. |
| `templates/delivery-dod/` | Shared delivery evidence pack template for implementation outputs. |
| `scripts/skill_catalog_guardrails.py` | Static guardrail scan: active count, duplicate names, frontmatter, UTF-8, description length, `SKILL.md` line count, broken `references/`/`templates/` links, and alias integrity (unrouted, stale, dangling). |
| `scripts/routing_smoke_test.py` + fixture YAML files | Routing precision measurement: scores fixtured tasks from `scripts/routing_fixtures.yml` and `tests/routing/edge-fixtures.yml` against skill descriptions and fails when an expected skill drifts out of its top matches. `--collisions` reports near-duplicate skills. |
| `scripts/check_source_register.py` | Fails on an active source record past its review date, a claim that names a superseded or quarantined record, or missing dates and scope; metadata only, not claim support. `--as-of` previews a future date. |
| `scripts/content_hygiene.py` + `docs/quality-gates/*-baseline.json` | Host-specific paths, duplicate `##` headings and broken relative links under the active roots; the baselines may only shrink. Run by the catalogue guardrails. |
| `scripts/engine_roots.py` | Resolves sibling engine checkouts from repeatable parent folders, `CHWEZI_ENGINES_ROOT`, per-engine overrides and former directory names; used by the control-plane and approval validators. |
| `scripts/validate_work_graph.py` and `scripts/validate_two_axis_review.py` | Deterministic gates for dependency frontiers, evidence-backed completion, and independent spec/standards review verdicts. |
| `docs/engine-control-plane.json` + `scripts/validate_engine_control_plane.py` | Twelve-entry registry with separate registry-only and scoped installed-checkout validation; explicit overrides never fall back silently. |
| `skills/sdlc-meta/skill-writing/scripts/contract_gate.py` | Evidence declarations checked recursively across both active roots; empty inventories and unmatched skill selectors fail. |
| `.github/workflows/skill-guardrails.yml` | CI: ten validation steps on every push to `main` and every pull request (guardrails, guardrail unit tests, test suite, routing, fixture coverage, collisions, control plane, source registers, hook tests, evidence contract gate). |
| `skills/sdlc-meta/skill-composition-standards/references/` | Artifact templates (ADR, entity model, threat model, release/rollback plan, runbook, test plan) and the closing Delivery Definition of Done pack. |
| `skills/languages/python-modern-standards/scripts/desktop_suite_packager.py` | Model-neutral project generator for a committed desktop-suite manifest, generated launcher/spec/installer/CI files, stale-generation check, and release evidence. |
| `skills/languages/java-enterprise-development/` | One active Java/JVM implementation route with progressively loaded references for Spring, Jakarta EE, Oracle, persistence, build/test/security, production operations, and modernisation. |
| `skills/ios/` and `skills/mobile-cross/` | Apple/mobile implementation guidance, including WWDC26-era Xcode, Swift, Foundation Models/Core AI, App Intents, StoreKit, PWA/Safari, KMP, release, and security references. |
| `skills/game-development/` | Game orchestration, lean experiments, design, mathematics/simulation, graphics, Unity/Godot/Unreal, Apple delivery, multiplayer/backend, security, 2D/3D content, audio, performance, build/release, testing, data/live economy, accessibility/player safety, studio operations, and live operations. |
| `claude-guides/` | Skill authoring and Claude-specific usage guidance. |

## Skill Loading Model

An active skill is any `SKILL.md` under:

- `skills/`
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
reconciliation, and finance UX route to the external
`chwezi-accounting-doctrine` engine unless a root skill adds distinct
implementation behaviour. Reference-only finance checkouts stay outside the
runtime skill catalog.

## Validation And Enforcement

The catalogue's invariants are gated, not just documented. These checks run in CI
and fail the build on a violation (the root `README.md` section "Verify" lists every
command and what it needs):

- `skill_catalog_guardrails.py` - structural integrity (count, duplicates,
  frontmatter, line count, description length, broken references, alias
  integrity) and, through `content_hygiene.py`, host paths, duplicate headings and
  broken relative links.
- `routing_smoke_test.py` - routing precision against `routing_fixtures.yml`
  and `tests/routing/edge-fixtures.yml`; catches descriptions drifting into
  ambiguity. `--coverage` and `--collisions --collision-gate` add fixture-coverage
  and description-collision gates.
- `check_source_register.py` - review dates of the dated source registers.
- `validate_engine_control_plane.py`, the hook tests and `contract_gate.py --all`.

Implementation work closes with the Delivery Definition of Done pack
(`skill-composition-standards/references/delivery-definition-of-done.md`), which
bundles tests, release plan, rollback plan, runbook, and maintenance notes so
the output is operable by a team that did not write it.

## Maintenance Flow

1. Read the relevant `SKILL.md`.
2. Load only necessary local references.
3. Apply the smallest accurate edit.
4. Update routing and overview docs if behavior or catalog policy changed.
5. Run the gates: at least the guardrail report and the routing smoke test, and the
   full set in the root `README.md` ("Verify") before a change is called done.
6. Record significant documentation repairs in `docs/updates/`.

## Known Constraints

- Markdown files should stay under 500 lines.
- `AGENTS.md` should remain a short navigation hub.
- Avoid deleting compatibility aliases without a migration decision.
- When deactivating an entrypoint, rename only `SKILL.md` to `ALIAS.md`, keep
  the directory intact, and add the target route to `docs/skill-aliases.yml`.
- `doctrine` currently behaves like a special tracked path and should not be
  modified incidentally.
