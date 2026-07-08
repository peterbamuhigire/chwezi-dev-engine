# Next Features

This file tracks the next practical work for the skills repository.

## Critical Priority

| Work | Why | Start Point |
| --- | --- | --- |
| Keep active catalog changes intentional | The current count is 142 after treating finance doctrine and design/UI doctrine as external or retained-reference engines. CI enforces the 200 hard cap and the collision detector should be used to keep future additions intentional. | Use `docs/skill-routing-index.md` and `docs/skill-aliases.yml` before adding active entrypoints. |

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
| 2026-07-08 | July 2026 world-class upgrade build | Added root router, source register, release gates, FieldOps Ledger exemplar, delivery evidence-pack template, empty-directory disposition, research integration log, book knowledge map, and 117-fixture routing smoke baseline at precision@1 97% / precision@3 100%. |
| 2026-06-21 | WWDC26 Apple platform skill modernization | Updated active iOS/mobile skills and companion design-system Apple UI guidance for Xcode 27, Swift 6.4, Foundation Models/Core AI, App Intents/Siri, Device Hub, Safari/WebKit 27, SF Symbols 8, and release/security gates. |
| 2026-06-21 | Active catalog root repair | Removed `doctrine/skills` from default active scanning, kept it as retained reference material, validated aliases against retained/external engines, and brought guardrails to 0 findings at 142 active skills. |
| 2026-06-13 | GIZ consulting delivery controls | Added `consulting-delivery-control-room`, `document-spreadsheet-tooling-readiness`, and `world-class-bid-red-team-and-delivery-qc` to support high-stakes bid control, validated file-output readiness, and red-team release gates across engines. |
| 2026-05-30 | C#/.NET skill entrypoint | Added `csharp-dotnet-development` with distilled references for modern C#/.NET, ASP.NET Core, EF Core, MAUI, concurrency, operations, and AI integration; added a routing fixture. |
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
