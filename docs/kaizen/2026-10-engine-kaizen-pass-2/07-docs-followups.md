# Documentation follow-ups (2026-10-31 documentation wave)

The documentation wave updated the root `README.md`, `AGENTS.md`, `CONTRIBUTING.md`,
`CHANGELOG.md`, `docs/README.md` (new), the overview documents, the plans index, the
next-features list, and two one-line name corrections. It did not touch skill content. The items
below are things the wave found and left alone, with the reason.

## Skill content and contracts (outside the wave's scope)

| Item | Where | Why it was left |
|---|---|---|
| The router's release workflow gives Windows commands with backslashes (`scripts\skill_catalog_guardrails.py`, `scripts\routing_smoke_test.py`) | root `SKILL.md`, "Release workflow", steps 5 and 6 | A skill body; it needs the same forward-slash, `python3` wording as `README.md`. |
| The router and `AGENTS.md` name the research engine `digital-research-engine`; the shared router wording names the catalogue id `digital-research-skills` | root `SKILL.md` line 25; `AGENTS.md` "Mandatory Digital Research currentness gate" | The sentence is portfolio-managed. The renderer (`--render-router-blocks --dry-run`, then a real run, then a second run) changed nothing, because it only rewrites the legacy form that carries a host path. Not hand-edited. `scripts/engine_roots.py` accepts all three directory names. |
| `docs/approval-contract.md` says "the eleven local skill engines" | line 3 | Contract text; the registry has twelve entries, eleven of them public. |
| `.skills-engine/engine-manifest.yaml` declares three validation gates; CI runs ten | `validation:` block | A manifest change that the portfolio catalogue also lists (`catalog/engines.yaml` in `chwezi-engine-agents` carries the `--workspace-root ..` form, which fails on a host with two parent folders). |

## Repository state

| Item | Where | Note |
|---|---|---|
| `install.sh` is tracked with mode 100644 | `git ls-files -s install.sh` | `./install.sh` fails with "Permission denied" on a fresh Linux clone. The README now says `bash install.sh`. Setting the executable bit is a repository change for the maintainer. |
| `.claude/settings.local.json` is tracked and names Windows user-profile paths | tracked in 11 commits | Standing finding D-13. Not touched. Untracking keeps the file on disk but history keeps it. |
| The row "Produce applied proof for the Pocock workflow Kaizen" names a re-audit on 2026-10-11, which has passed | `docs/plans/NEXT_FEATURES.md` | Status unknown to the wave; the owner decides whether to reschedule or close it. |
| Dated records still name Windows checkout paths | `docs/engine-upgrade-july-2026/`, `docs/superpowers/`, `docs/plans/2026-06-21-wwdc26-apple-platform-skill-modernization.md` | They are history; the hygiene guard excludes dated records. |

## Not re-verified by the wave

- The standards list and the Repositories, Standards and Websites parts of the README
  "References" section were not re-read. The book count (384) was re-counted by bullet; the
  figure of 89 entries without an author was not.
- The introductory claim that the engine "applies" the listed standards is the engine's own
  statement; no validator assesses it.
- Windows: `install.ps1`, `scripts/install-pdf-binaries.ps1` and the PowerShell examples were
  not run (no `pwsh` on the host).

## Measured by the wave, for the record

- A real pytest 9.0.3 run (Python 3.14.8, PyYAML 6.0.3) on a copy of the repository gave
  273 passed, 3 skipped, equal to pass 2's stand-in count. This narrows, but does not close,
  the "real pytest not run" gap: the pinned PyYAML is 6.0.2 and CI uses Python 3.12.
- A real `install.sh` install into an empty home folder, `doctor`, a dry-run uninstall and a
  real uninstall all exited 0 (copy of the repository, throwaway home folder).
- The date-triggered gate calendar in the README was produced by running
  `scripts/check_source_register.py --as-of` on each date and the day before it; every row
  matched.

## Name finding for the maintainer

`gh repo view peterbamuhigire/digital-research-skills` resolves to
`peterbamuhigire/chwezi-research-engine`, and `gh repo list` shows `chwezi-research-engine`
as the repository name. The other three renamed repositories (`chwezi-dev-engine`,
`chwezi-design-engine`, `chwezi-sdlc-documentation`) are the current names. The documentation
therefore avoids a GitHub link for the research engine and uses its catalogue id and
`scripts/engine_roots.py` aliases instead; confirm which name the portfolio intends.
