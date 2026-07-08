# Skills Web Dev

`skills-web-dev` is the Chwezi Core Systems software-engineering skills engine. It gives agents a routed catalog for AI systems, SaaS, architecture, APIs, databases, security, frontend engineering, mobile, DevOps, reliability, product engineering, and SDLC documentation.

The engine is file-based. Active skills live as `SKILL.md` files under `skills/` and `00-meta-initialization/`. Deep guidance lives in references, templates, examples, source registers, and quality gates so the active routing surface stays small enough to select accurately.

## Current Status

Last upgraded: 2026-07-08

| Metric | Current value |
|---|---:|
| Active `SKILL.md` files | 142 |
| Guardrail hard cap | 200 |
| Duplicate frontmatter names | 0 |
| Routing fixtures | 117 |
| Routing precision@1 | 97% |
| Routing precision@3 | 100% |
| Guardrail findings | 0 |

Run the two gates after routing, frontmatter, template, source-register, or catalog-policy changes:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
python -X utf8 scripts\routing_smoke_test.py --report-only
```

## How To Route Work

Start with the root router:

- `SKILL.md` - domain routing, cross-engine handoffs, release workflow, stop conditions.
- `AGENTS.md` - Codex operating rules for this repository.
- `docs/skill-routing-index.md` - human-readable routing and alias policy.
- `docs/skill-aliases.yml` - machine-readable inactive alias map.

Use the smallest accurate skill. Load its `SKILL.md` first, then only the references or templates needed for the task.

## Core Domains

| Domain | Active area |
|---|---|
| AI systems and agents | `skills/ai/` |
| Architecture and APIs | `skills/architecture/` |
| Databases and data reliability | `skills/backend-databases/` |
| DevOps, cloud, containers, reliability | `skills/devops-cloud/` |
| Frontend engineering | `skills/frontend-ux/` |
| Android, iOS, KMP, PWA | `skills/android/`, `skills/ios/`, `skills/mobile-cross/` |
| Languages | `skills/languages/` |
| SaaS product architecture | `skills/saas/` |
| Security | `skills/security/` |
| Product/business engineering | `skills/product-business/` |
| SDLC and catalog governance | `skills/sdlc-meta/`, `00-meta-initialization/` |

## Cross-Engine Ownership

This engine does not copy doctrine owned elsewhere.

| Concern | Canonical engine |
|---|---|
| Finance, accounting, IFRS, tax, payroll, statutory values | `chwezi-accounting-doctrine` |
| Visual design, typography, UI/UX, document and slide appearance | `design-system-skills` |
| Research, source verification, benchmarking, current-source checks | `digital-research-skills` at `C:\wamp64\www\digital-research-skills` |

Use those engines in addition to this one when the task crosses their boundary.

## July 2026 Upgrade Assets

| Path | Role |
|---|---|
| `docs/source-registers/ai-platforms.md` | Dated official/current sources for volatile AI, Apple, cloud, security, and framework facts |
| `docs/quality-gates/release-blocking-gates.md` | Ship/no-ship gate for engineering deliverables |
| `docs/quality-gates/anti-slop-governance.md` | Engineering-specific anti-slop rules |
| `docs/world-class-exemplars/running-example.md` | FieldOps Ledger running example |
| `examples/full-stack-saas-reference/` | Complete SaaS exemplar: architecture, API, security, reliability, release |
| `templates/delivery-dod/evidence-pack.md` | Required delivery evidence pack template |
| `templates/architecture/` | Architecture decision template |
| `templates/api/` | API contract template |
| `templates/security/` | Threat model template |
| `templates/reliability/` | SLO and runbook template |
| `tests/routing/edge-fixtures.yml` | Edge routing fixtures for near-collision skills |
| `tests/quality/negative-fixtures.md` | Negative examples that must fail release gates |
| `references/engineering-standards.md` | Benchmark and cross-engine ownership reference |

## Running Example

The shared example is **FieldOps Ledger**, a Chwezi Core Systems multi-tenant field-service SaaS. It includes tenant isolation, work orders, technician visits, evidence uploads, posting events, API exports, identity controls, and SLO-backed release rules. Use it when adding examples to related skills so architecture, API, data, security, and reliability guidance stays connected.

## Delivery Rule

Any implementation, architecture, security, data, AI, SaaS, mobile, DevOps, or documentation deliverable should ship with an evidence pack:

1. Decision record.
2. Contract evidence.
3. Test evidence.
4. Security evidence.
5. Operational evidence.
6. Source and currency evidence.
7. Anti-slop gate.
8. Release verdict.

Template: `templates/delivery-dod/evidence-pack.md`.

## Repository Map

| Path | Role |
|---|---|
| `skills/` | Main active engineering catalog |
| `00-meta-initialization/` | Project documentation initialization entrypoints |
| `doctrine/skills/` | Retained finance reference material; not active local doctrine |
| `docs/` | Overview, routing, plans, evaluation, source registers, quality gates |
| `examples/` | Complete, sanitized workflow examples |
| `templates/` | Reusable blank-fill delivery templates |
| `references/` | Shared standards and benchmark references |
| `scripts/` | Guardrail validator and routing smoke test |
| `tests/` | Routing fixtures and quality negative fixtures |
| `.github/workflows/` | CI gates |

## Maintenance Rules

- Do not move, delete, or rename skill directories during routine docs work.
- Deactivate legacy entrypoints by renaming `SKILL.md` to `ALIAS.md` and adding a route in `docs/skill-aliases.yml`.
- Keep active skill count below 200.
- Add or update routing fixtures whenever a skill description changes or a neighbor skill could steal traffic.
- Use `docs/source-registers/ai-platforms.md` before naming current platform capabilities.
- Record substantive documentation repairs under `docs/updates/`.
- Keep Markdown under 500 lines where practical.
- Use ASCII unless an existing file requires another character set.

## Upgrade Record

The July 2026 build record is in `docs/engine-upgrade-july-2026/`:

- `phase1-completion-report.md`
- `phase2-completion-report.md`
- `FINAL-UPGRADE-REPORT.md`
- `book-knowledge-map.md`
- `research-engine-integration-log.md`
