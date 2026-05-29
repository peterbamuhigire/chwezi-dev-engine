# Next Features

This file tracks the next practical work for the skills repository.

## Critical Priority

| Work | Why | Start Point |
| --- | --- | --- |
| Keep active catalog inside the 150-170 target | The current count is 171, just over the soft target. CI enforces the 200 hard cap and the collision detector confirms no true duplicates, so this is discipline, not an emergency. | Use `docs/skill-routing-index.md` and `docs/skill-aliases.yml` before adding active entrypoints. |

## High Priority

| Work | Why | Start Point |
| --- | --- | --- |
| Grow the routing fixture set with each new skill | The smoke test only guards routes it has fixtures for. | Add a case to `scripts/routing_fixtures.yml` for any skill a neighbour could shadow. |
| Review inactive aliases for deeper consolidation | `ALIAS.md` preserves content, but durable material should eventually move into retained parent references. | Start with finance and data aliases from `docs/skill-aliases.yml`. |

## Medium Priority

| Work | Why | Start Point |
| --- | --- | --- |
| Promote `--collisions` to an enforced gate with an allowlist | It is a report tool today; an allowlisted threshold would auto-block future near-duplicate skills. | Add the intentional platform/concern-split pairs to an allowlist, then fail CI on new high-similarity pairs. |
| Review `docs/skills-trimminhg.md` filename | The apparent typo makes discovery harder. | Rename only if references are updated in the same change. |
| Add `requirements.txt` for Python tooling | PyYAML is the only dependency; CI installs it ad hoc. | Pin `pyyaml` so local and CI environments match. |

## Recently Completed

| Date | Work | Summary |
| --- | --- | --- |
| 2026-05-30 | Production-readiness hardening | Six-point audit; extended the guardrail to catch broken references and alias drift; added CI running both gates; repaired all 55 broken references to 0; added the Delivery Definition of Done handoff gate; added the routing smoke test (precision@1 84%, @3 100%); merged the one true duplicate (172 -> 171); added integrator and client docs. See `docs/evaluation/2026-05-30-production-readiness-audit.md`. |
| 2026-05-17 | Catalog alias cleanup | Deactivated 47 legacy entrypoints by renaming `SKILL.md` to `ALIAS.md`, bringing active skills to 169 and clearing duplicate frontmatter names. |
| 2026-05-17 | README expansion | Replaced the short root landing page with a fuller guide to skill benefits, domains, routing, aliases, and maintenance rules. |
| 2026-05-17 | Documentation reconstruction | Restored root README, agent guide, overview docs, plan index, next-feature tracker, API/database notes, and update record. |

## Recommended Next Session

1. Add a routing fixture for every newly added skill, and widen coverage of the
   AI and SaaS clusters where near-synonyms cluster.
2. Decide whether to promote the collision detector to an allowlisted hard gate.
3. Convert the highest-value `ALIAS.md` content into retained parent
   `references/` files where the parent does not already contain the material.
