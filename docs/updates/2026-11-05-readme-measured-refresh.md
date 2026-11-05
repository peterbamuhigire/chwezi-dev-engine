# README measured refresh, 5 November 2026

The README's "Verify" table and "At a glance" list were last measured on 31 October 2026. Two commits since then changed the catalogue (`74c9bda` on 1 November and `13e4cc9` on 5 November), and a date gate in the README's own calendar came due on 4 November. This record holds what was re-run and what changed in the text.

## What was run

Each command is a step of `.github/workflows/skill-guardrails.yml`, run from the repository root on 2026-11-05, in a fresh virtual environment (Fedora Linux, Python 3.14.10, Node 22.23.1, pytest 9.2.0, PyYAML 6.0.3). The working tree was clean before the run.

| Step | Exit | Result |
|---|---|---|
| `scripts/skill_catalog_guardrails.py` | 0 | 168 active skills, 0 errors, 14 size warnings |
| `unittest tests/test_skill_catalog_guardrails.py` | 0 | 10 tests OK |
| `pytest tests -q -p no:cacheprovider` | 0 | 273 passed, 3 skipped |
| `routing_smoke_test.py --min-rank1 89 --lint-fixtures` | 0 | 242 fixtures; precision@1 222/242 (91.7%); precision@3 242/242; 86 owned negatives (82 pass, 4 not assessed); 0 lint findings |
| `routing_smoke_test.py --coverage --max-zero-positive 1` | 0 | 167 of 168 skills have a positive fixture; 14 have three positives and two owned negatives |
| `routing_smoke_test.py --collisions --collision-gate --threshold 0.5` | 0 | 1 allow-listed pair (0.627) |
| `validate_engine_control_plane.py` | 0 | 12 registry entries, 0 findings; installed checkouts not assessed |
| `check_source_register.py` | **1** | 72 active sources, 5 findings, 10 warnings |
| `hooks/test-destructive-bash-gate.js`, `hooks/test-plugin-hook-config.js` | 0 | 61/61 and 7/7 |
| `contract_gate.py --all` | 0 | 162 scanned, 0 errors, 6 exempt |
| `git diff --check` | 0 | clean |

## The failing step

`check_source_register.py` fails on five records whose `review_after` is 2026-11-03: `next16-upgrade-2026-10-29`, `nextjs-release-2026-10-29`, `nextjs-support-policy-2026-10-29`, `next-security-oct14-2026` and `next-security-november-notice-2026`. This is the 2026-11-04 row of the README's date-gate calendar. The check is behaving as designed. No record was re-read or extended in this pass, because a date must never be extended unread. Re-reading the five Next.js pages and adding dated records is still open.

## What changed in the text

- README: the test and source-record bullets in "At a glance"; the "Verify" introduction and every result in its table; a status paragraph under "Date-triggered gates"; the routing-coverage finding (13 of 167 became 14 of 168); a new "Changes after the October kaizen" subsection describing the two standards above.
- AGENTS.md: the routing figures and the first date-triggered failure in "Known baseline", and the date of the Linux check run.
- CHANGELOG.md: one entry.

## Not assessed

Windows steps, the applied examples and the Next.js, Compose, MySQL and Android layers were not re-run. The 2026-10-31 results for those stay as written in the README.
