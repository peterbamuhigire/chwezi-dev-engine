# Next Features

This file tracks the next practical work for the skills repository.

## Critical Priority

| Work | Why | Start Point |
| --- | --- | --- |
| Keep active catalog inside the 150-170 target | The current count is 169, so new skill additions need consolidation discipline. | Use `docs/skill-routing-index.md` and `docs/skill-aliases.yml` before adding active entrypoints. |

## High Priority

| Work | Why | Start Point |
| --- | --- | --- |
| Add a lightweight catalog verification workflow | Guardrails are manual today. | Consider a GitHub Actions workflow for `scripts/skill_catalog_guardrails.py`. |
| Review inactive aliases for deeper consolidation | `ALIAS.md` preserves content, but durable material should eventually move into retained parent references. | Start with finance and data aliases from `docs/skill-aliases.yml`. |

## Medium Priority

| Work | Why | Start Point |
| --- | --- | --- |
| Review `docs/skills-trimminhg.md` filename | The apparent typo makes discovery harder. | Rename only if references are updated in the same change. |
| Add dependency notes for Python tooling | PyYAML is required but no requirements file exists. | Add `requirements.txt` or document install steps. |

## Recently Completed

| Date | Work | Summary |
| --- | --- | --- |
| 2026-05-17 | Catalog alias cleanup | Deactivated 47 legacy entrypoints by renaming `SKILL.md` to `ALIAS.md`, bringing active skills to 169 and clearing duplicate frontmatter names. |
| 2026-05-17 | README expansion | Replaced the short root landing page with a fuller guide to skill benefits, domains, routing, aliases, and maintenance rules. |
| 2026-05-17 | Documentation reconstruction | Restored root README, agent guide, overview docs, plan index, next-feature tracker, API/database notes, and update record. |

## Recommended Next Session

1. Convert the highest-value `ALIAS.md` content into retained parent
   `references/` files where the parent does not already contain the material.
2. Add an automated check for `scripts/skill_catalog_guardrails.py`.
3. Review whether `docs/skills-trimminhg.md` should be renamed after updating
   all references.
