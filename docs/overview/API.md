# API

This repository does not expose a runtime HTTP, RPC, GraphQL, or CLI API.

The closest stable interfaces are file conventions:

| Interface | Purpose |
| --- | --- |
| `*/SKILL.md` | Skill entrypoint with YAML frontmatter and execution guidance. |
| `docs/skill-aliases.yml` | Machine-readable routing and alias data. |
| `scripts/skill_catalog_guardrails.py` | Repository guardrail report script. |
| `scripts/routing_smoke_test.py` | Routing precision, fixture coverage (`--coverage`) and description collisions (`--collisions`). |
| `scripts/check_source_register.py` | Source-register review-date check; `--as-of YYYY-MM-DD` previews a date. |

## Guardrail Script Interface

```sh
python3 -X utf8 scripts/skill_catalog_guardrails.py --report-only
```

Useful options:

| Option | Meaning |
| --- | --- |
| `--root <path>` | Add an active catalog root relative to the repository root. |
| `--max-active <number>` | Override the active skill cap. |
| `--report-only` | Print findings and exit with status 0. |
| `--max-skill-bytes <number>` | Report-only size warning threshold for a `SKILL.md` (default 20480). Never changes the exit status. |

API documentation for downstream projects should live inside the relevant skill
or project example, not in this repository overview.
