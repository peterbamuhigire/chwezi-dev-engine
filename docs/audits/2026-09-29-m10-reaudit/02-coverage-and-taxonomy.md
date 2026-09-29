# Coverage and taxonomy

**Taxonomy and structure: 54 / 100 (judged).** Prior audit (6 September): 52. Movement +2.

## Active catalogue by group (measured by glob)

| Group | Active skills | With `references/` | Note |
|---|---:|---:|---|
| ai | 26 | 23 | 12 `ai-agent-*` skills |
| android | 1 | 1 | single-skill group; 2 alias stubs |
| architecture | 7 | 7 | |
| backend-databases | 4 | 4 | 5 alias stubs, 4 still holding references |
| devops-cloud | 8 | 8 | |
| execution-plan-scripts | 1 | 0 | group-level SKILL.md, no skill folder |
| finance-accounting | 4 | 3 | doctrine external by design |
| frontend-ux | 9 | 7 | 3 migrated UI skills as aliases |
| game-development | 25 | 25 | 15 % of the catalogue |
| gis | 2 | 2 | |
| ios | 4 | 4 | 4 alias stubs, all holding references |
| languages | 12 | 12 | |
| mobile-cross | 3 | 3 | |
| product-business | 15 | 12 | |
| saas | 18 | 18 | |
| sdlc-meta | 20 | 16 | |
| security | 6 | 5 | |
| 00-meta-initialization | 2 | - | SDLC entry root |
| **Total** | **167** | | 78 `ALIAS.md` stubs |

## What improved since 6 September

- The router's intent table now has explicit rows for desktop (Avalonia, Python packaging, C#), GIS and
  games; the prior audit named their absence as a discovery gap.
- The `ux-for-ai` and `ux-principles-101` destination conflict between the index and the alias
  registry was resolved (commits `9fd98a9`, `67ae982`).
- The 24 September consolidation cut the catalogue from 185 to 167 with alias routing preserved.

## Named deficiencies

1. **Orphan and near-orphan groups.** `android` holds one active skill; `gis` two;
   `execution-plan-scripts` is a group with a SKILL.md and no skill folder. Android and iOS are
   asymmetric (1 versus 4 active) for comparable output weight.
2. **Grab-bag groups.** `sdlc-meta` (20) mixes SDLC documentation, catalogue maintenance and
   agent-workflow utilities (`council`, `santa-method`, `strategic-compact`, `regex-vs-llm-structured-text`,
   `github-ops`). `product-business` (15) mixes document tooling (Word, Excel), a hospitality systems
   design, a project-specific BDS monitoring specification, content writing and pricing.
3. **Over-splitting in AI agents.** Twelve `ai-agent-*` skills separate concerns such as drill
   cadence, memory-erasure proof, SLA commitments and commercial operations that an agent must then
   compose; the 19 identical operating-contract blocks in this group suggest the split outran the content.
4. **Depth parked in inactive directories.** 37 of 78 alias stubs keep a `references/` tree. The active
   `postgresql-engineering` sends readers to `../postgresql-operations/ALIAS.md` for operations depth,
   while that alias says "route to postgresql-engineering": a circular pointer. The migrated
   `ux-principles-101` alias still holds 9 reference files that the design engine now owns.
5. **Cross-platform coverage hole.** Mobile-cross covers KMP and PWA; React Native appears only as a
   reference checklist inside `mobile-platform-operations`; Flutter appears in no mobile skill.
6. **Engineering documentation has no clear owner for ADRs.** ADRs are mentioned in 17 active
   SKILL.md files (among them `system-architecture-design`, `cloud-architecture`, `infrastructure-as-code`,
   `graphql-patterns`, `ai-app-architecture`) with no single owning skill; formal SRS routes externally, which is correct, but the local ADR/runbook
   owner is not named in the router.
7. **Balance.** Game development is 25 of 167 skills while cross-platform mobile is 3 and Android 1.

## Why not higher

A 60+ score would need balanced groups with no orphans, a clear owner for every output type, and no
active skill that depends on content in an inactive directory. Items 1, 4 and 5 fail that test.
