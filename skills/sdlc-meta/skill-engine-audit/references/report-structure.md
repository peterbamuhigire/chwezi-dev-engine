# Reference: The Audit Report Structure

Write the audit as a multi-file set under `docs/<audit-name>/` (e.g. `docs/initial-analysis/`),
one concern per file, with a README index. This is the proven structure.

| File | Owner | Contents |
|---|---|---|
| `README.md` | synthesis | Index + the overall engine score + a one-paragraph verdict. |
| `00-executive-summary.md` | synthesis | The verdict, the headline findings (5±), what's strong, the path to the bar. Start-here. |
| `01-methodology-and-rubric.md` | synthesis | How the audit ran (the fleet) + the strict rubric. |
| `02-coverage-and-taxonomy.md` | agent | Taxonomy sufficiency /100; proposed revised structure. |
| `03-existing-groups-audit.md` | agent | Per-group + per-skill scores /100, with justifications. |
| `04-gap-analysis-new-skills.md` | agent | Missing skills, P0/P1/P2, with target skill count. |
| `05-per-output-type-readiness.md` | agent | Every output type scored /100 + ranked table. |
| `06-standards-benchmark.md` | agent (cited) | What world-class looks like now; primary sources. |
| `07-hardening-existing-skills.md` | agent | Concrete `references/*` + `examples/*` per skill. |
| `08-reading-list.md` | agent (cited) | Material to buy & extract, tiered, mapped to groups. |
| `09-master-scorecard.md` | synthesis | Every dimension + group + output type + overall /100. |
| `10-roadmap-to-world-class.md` | synthesis | Phased plan with a target score after each phase. |

## Rules
- **Numbers everywhere.** Every aspect carries a /100. The headline is the overall engine score.
- **Justify, don't assert.** Each score names concrete deficiencies.
- **Actionable tail.** The roadmap lists specific skills (priority-tagged), hardening moves (named
  files), and the believable target score per phase.
- **Comparable.** Use the fixed rubric/dimensions so a re-audit later shows movement.
- Adapt file names to the engine's domain, but keep the executive-summary → scorecard → roadmap
  spine.
