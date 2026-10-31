# README kaizen record, 2026-10-31

Scope: a micro-cycle on the root `README.md` only. Peter Bamuhigire asked for READMEs that are smarter and easier to read. The cycle followed Observe, Baseline, Select, Experiment, Check, Standardise, Teach, Re-measure. It published no score, and nothing here changes the 62.5/100 rating held in the [pass-2 final report](../2026-10-engine-kaizen-pass-2/05-final-report.md). Skill bodies, scripts and tests were not touched.

Branch `kaizen/2026-10-readme-kaizen`, created from `main` at `9711346`.

## Observe

Baseline measured on `main` before any edit, with the shared `readme-metrics.py` (kept outside this repository):

| Measure | Baseline |
|---|---:|
| Words | 12,579 |
| H2 sections | 5 |
| Contents list | none |
| First fenced command (line) | 15 |
| Longest H2 section (words) | 5,567 |
| Lines over 300 characters | 55 |
| Longest line (characters) | 1,524 |
| Mean sentence length (words) | 20.1 |
| Flesch reading ease | 39 |
| List items, table rows | 524, 228 |

What the baseline showed:

- **Walls of text.** The purpose took two paragraphs of 207 and 140 words. The skill table had 167 rows and the reference lists had 384 books plus about 115 other entries.
- **Section sizes.** References 5,673 words, Capabilities 3,230, Quality and improvement 1,998, Installation 1,178. The validation commands sat inside Installation as a bold paragraph, not a heading.
- **Who reads the README.** `tests/test_engine_control_plane.py` reads one row only: ``| Active `SKILL.md` files | 167 |``. `REPLICATE-ROUTING.md` links `README.md#installation`. `AGENTS.md`, `CONTRIBUTING.md`, `docs/overview/ARCHITECTURE.md` and `docs/overview/TECH_STACK.md` cite the sections "Verify", "Quality and improvement" and "Date-triggered gates" by name. No script, test, manifest or router reads the skill table or the reference lists.

Validators before (run from the repository root on the clean `main` tree, Linux, Python 3.14.8, Node 22.23.1): 16 commands, all exit 0. The test suite ran in a scratch virtual environment outside the repository, because the system `python3` has no pytest. See the Check section for the list.

## Select

| Item | Decision | Reason |
|---|---|---|
| R1 Front door | Applied | Purpose, audience, six measured facts and a three-step start sit in the first 37 lines. |
| R2 Contents | Applied | A contents list of the 12 H2 sections follows the opening paragraphs. It is a bold label and a list, not a heading, so it sits before the third H2. |
| R3 Structure | Applied | 5 H2 sections became 12. The longest is 1,288 words. "Installation" has one H3 per route. |
| R4 Find the right skill | Applied | 12 rows from the routing fixtures. Every link target exists on disk. |
| R5 No walls of text | Applied | Dense paragraphs became bullets. Lines over 300 characters fell from 55 to 9. |
| R6 Plain English | Applied | Mean sentence length 20.1 to 11.7. Terms defined at first use: fixture, CI, kaizen, ratchet, `NOT ASSESSED`. |
| R7 Say it once | Applied | The pointer from Installation to the improvement passes, and the accounting sentence in the opening, were folded into the sections that own them. The improvements section is kept and tightened, with all 13 items. |
| R8 Relocate bulk | Applied to two blocks | The 167-row skill table went to `docs/skill-catalogue.md`. The book, repository, standards and website lists went to `docs/references/`. |
| Date calendar | Not moved | `AGENTS.md` cites it by section name, it names the first failure date (2026-11-04), and it is 358 words. |
| Catalogue size table | Not moved | A test reads its first row. |

## Experiment

| Commit | Change |
|---|---|
| `792963a` | Relocation. New `docs/skill-catalogue.md` (167 rows by category, with a jump list) and `docs/references/` (index, books, sources). README keeps the category table, the catalogue-size table and a summary with links. |
| `32d232d` | Structure and front door. Contents, At a glance, Start here, Find the right skill, How it works, What is inside. `Verify`, the improvements section and the date gates become H2 sections. Existing prose unchanged. |
| `d3645cd` | Plain English and finer headings. Installation, Verify, Quality, improvements and date gates rewritten in short sentences, with one heading per install route. |
| `5561993` | Terms defined at first use. No figure or command changes. |
| This commit | This record, the `docs/README.md` index rows, the `CHANGELOG.md` entry, and the link from README "Contributing and licence" to this record. |

## Check

**Validators.** Same 16 commands before and after, all exit 0 both times (identical exit codes):

| Command | Before | After |
|---|---|---|
| `scripts/skill_catalog_guardrails.py` | 0 (167 active, 14 size warnings) | 0 (same) |
| `unittest tests/test_skill_catalog_guardrails.py` | 0 | 0 |
| `pytest tests -q -p no:cacheprovider` (scratch environment, pytest 9.0.3) | 0 (273 passed, 3 skipped) | 0 (273 passed, 3 skipped) |
| `routing_smoke_test.py --min-rank1 89 --lint-fixtures` | 0 | 0 |
| `routing_smoke_test.py --coverage --max-zero-positive 1` | 0 | 0 |
| `routing_smoke_test.py --collisions --collision-gate --threshold 0.5` | 0 | 0 |
| `validate_engine_control_plane.py` | 0 | 0 |
| `check_source_register.py` | 0 | 0 |
| `node hooks/test-destructive-bash-gate.js` | 0 (61/61) | 0 (61/61) |
| `node hooks/test-plugin-hook-config.js` | 0 (7/7) | 0 (7/7) |
| `contract_gate.py --all` | 0 (161 scanned) | 0 (161 scanned) |
| `git diff --check` | 0 | 0 |
| `validate_tenant_invoice_example.py` | 0 | 0 |
| `check_package_file_budget.py` | 0 (2519 package entries) | 0 (2524) |
| `source_ingestion_guardrail.py` | 0 | 0 |
| `validate_work_graph.py templates/work-graph.yml` | 0 | 0 |

The README table of results in "Verify" still matches these outputs. `NOT_ASSESSED` here: the live installed-portfolio tests (3 skipped), `install.ps1`, the Codex `debug prompt-input` invocation, the PHP, Next.js, Compose, MySQL and Android layers of the invoice example, and GitHub's own rendering of the pages.

**Preservation check.** `readme-preserve-check.py <repo> main kaizen/2026-10-readme-kaizen`, run on the final tree:

```text
links: old README 314 targets; new README 61; moved to docs 262; LOST 0
commands: old README 27; kept in README 27; moved to docs 0; LOST 0
in-page links: 12 anchors used; BROKEN 0
RESULT: OK
```

The anchors line is left out of the block above, because its literal text matches the checker's own anchor pattern. It reported 2 links to README headings in tracked files (`#installation` from `REPLICATE-ROUTING.md` and `#find-the-right-skill` from the catalogue page) and 0 broken.

An earlier run, with the checker version that compared link strings without resolving the file location, flagged 154 links as lost. They were the skill links re-based from `skills/x/SKILL.md` to `../skills/x/SKILL.md` in the catalogue page. I confirmed with an independent normalising script that all 262 moved targets resolve to the same files and that every relative link in the README and the new pages exists on disk. The updated checker now agrees.

**Independent counts.** The catalogue page has 167 rows, and the set of linked paths equals the set of 167 `SKILL.md` files that `git ls-files` lists under `skills/` and `00-meta-initialization/`. The old README held 384 book entries (89 by title only), 14 adapted and 35 cited repositories, 53 standards entries and 13 websites; these were counted from the old text, not from the new index. Hygiene baselines: 24 skills with a duplicate heading and 84 broken links in 52 files, as the README states. `tests/test_tenant_invoice_example.py` has 7 tests. The date-gate calendar was re-run with `--as-of` on every listed date and the day before; all 12 totals match.

**Metrics after** (`readme-metrics.py README.md`):

| Measure | Before | After | Target | Result |
|---|---:|---:|---|---|
| words | 12,579 | 4,685 | at most baseline plus 5 percent; aim minus 10 percent | Met (minus 63 percent, by relocation and tightening) |
| h2 | 5 | 12 | n/a | n/a |
| toc | 0 | 1 | 1 | Met |
| first_cmd | 15 | 37 | 40 or less | Met (later than before because the contents list now precedes the first command) |
| longest_sec | 5,567 | 1,288 | 1,500 or less; 1,200 preferred | Met; **preferred 1,200 missed** (the improvements section, which keeps all 13 items) |
| long_lines | 55 | 9 | cut by half | Met |
| max_line | 1,524 | 372 | 700 or less | Met |
| sent_len | 20.1 | 11.7 | 16.5 or less | Met |
| fre | 39 | 59 | not lower than baseline; aim plus 5 | Met (plus 20) |

The 9 remaining long lines are the opening paragraph and list items or table rows that carry several linked facts (open findings, improvement items, the rating row).

**Facts deliberately changed or condensed.**

- Package-oriented entries, from 2519 to 2524, because this cycle added five files (three reference pages, the catalogue page and this record).
- "Verify", "What the October 2026 kaizen improved" and "Date-triggered gates" are now H2 sections. Their anchors are unchanged, except that "Verify" is a heading where it was a bold label.
- The long opening list of topics (languages, platforms and so on) is condensed. The category table and the "What the skills produce" list carry the same coverage. All 19 named standards are kept under "Standards applied".
- The pointer from Installation to the improvement passes was dropped. The same warning now opens the Quality section.
- The accounting sentence moved from the opening to the neighbouring-engines list under "Find the right skill", and keeps its link.
- Added facts, each checked in the repository: 10 agents in `agents/`, the hooks, templates and examples folders, MIT licence in `LICENSE`, the two always-on skills named in the root `SKILL.md`.
- Before and after figures inside the improvement items keep their original provenance. This cycle re-measured only the figures named under "Independent counts", plus the Verify table results.

## Standardise

Conventions for editing the root README:

1. **Skeleton.** Title and purpose; contents; At a glance; Start here; Find the right skill; How it works; What is inside; Installation; Verify; Quality and improvement; dated gates; References; Contributing and licence.
2. **Limits.** No H2 section over 1,200 words. No paragraph over 90 words. No table cell over 35 words. Mean sentence length 16 words or fewer. First fenced command before line 40. A contents list of in-page links before the third H2.
3. **Bulk goes to `docs/`.** Tables of more than about 50 rows, and source lists, live in `docs/` with a summary and link in the README. Skill rows go in `docs/skill-catalogue.md`; citations go in `docs/references/`.
4. **Keep cited headings.** `Installation`, `Verify`, `Quality and improvement` and `Date-triggered gates` are cited by other files. Rename one only in the same commit as those citations.
5. **Say each number once, then check it.** The counts 167, 165, 239, 219 and 273 appear in At a glance, Catalogue size and the Verify table. Change them together and re-run the check in the Verify section.
6. **Add a skill.** Update the README count row, `docs/skill-catalogue.md` and the routing fixtures in one change.

## Teach

- Run `readme-metrics.py` and `readme-preserve-check.py` before and after every README edit, and read the output instead of assuming it.
- When a section feels long, move the reference material out and leave a summary and link. Do not shorten the facts.
- A table that has moved to `docs/` needs its relative links re-based. Resolve them from the new file's folder.

## Re-measure and next cycle

Re-measured: see "Metrics after". No score is published, because this was a scoped README cycle.

Open items for the next cycle:

- **Guard the catalogue page.** `docs/skill-catalogue.md` is checked only by hand. A test that compares its rows with the tracked `SKILL.md` files would close that gap. This cycle was not allowed to touch tests.
- **One section is above the preferred size.** "What the October 2026 kaizen improved" is 1,288 words. When the next pass adds items, move the older ones to a `docs/` page and keep a summary.
- **Counts are hand-kept in four places.** At a glance, Catalogue size, the Verify table and `AGENTS.md` repeat the same figures. A small script that prints them from the validators would remove the drift risk.
- **Package-entry count drifts.** The README states 2524. Any new file changes it, so the line needs a date-and-tree qualifier or a generated value.
- **Date gate.** Five Next.js source records lapse on 2026-11-04. The calendar in the README is the reminder.
