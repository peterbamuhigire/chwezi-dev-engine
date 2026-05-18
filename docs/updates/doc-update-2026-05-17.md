# Documentation Update: 2026-05-17

## Summary

Recreated the missing project documentation entrypoints for the skills
repository, then updated the catalog documentation after the active skill alias
cleanup.

## Files Added

| File | Purpose |
| --- | --- |
| `README.md` | Short root landing page. |
| `AGENTS.md` | Agent navigation and working rules. |
| `docs/overview/README.md` | Canonical project overview. |
| `docs/overview/PROJECT_BRIEF.md` | Project purpose, users, outcomes, risks. |
| `docs/overview/TECH_STACK.md` | Tooling and platform context. |
| `docs/overview/ARCHITECTURE.md` | Repository structure and maintenance flow. |
| `docs/overview/API.md` | Clarifies there is no runtime API. |
| `docs/overview/DATABASE.md` | Clarifies there is no repository database. |
| `docs/plans/INDEX.md` | Planning document index. |
| `docs/plans/NEXT_FEATURES.md` | Current priorities and next work. |

## Verification

Guardrail command:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
```

Current result after cleanup:

- Active `SKILL.md` files: 169.
- Duplicate frontmatter names: 0.
- Guardrail findings: 0.

## Follow-Up Update

| File | Change |
| --- | --- |
| `README.md` | Expanded into a fuller guide to skill benefits, active roots, domains, routing, aliases, and maintenance rules. |
| `docs/skill-routing-index.md` | Updated baseline counts and recorded inactive alias routes. |
| `docs/skill-aliases.yml` | Added current active count and machine-readable inactive alias targets. |
| `docs/overview/README.md` | Updated current catalog policy and alias behavior. |
| `docs/overview/PROJECT_BRIEF.md` | Replaced resolved duplicate-count risks with ongoing catalog-discipline risks. |
| `docs/overview/ARCHITECTURE.md` | Documented `ALIAS.md` as the inactive entrypoint preservation mechanism. |
| `docs/plans/NEXT_FEATURES.md` | Moved count reduction and finance duplicate cleanup to recently completed work. |
