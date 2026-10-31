# Validation record (pass 2)

Access date: 2026-10-31. Commands ran from the engine root on a Linux workstation (Python
3.14.8, Node 22.23.1, PHP 8.5.12 CLI). `<engines>` is the `skill-engines` folder in the
user's home directory and `<skills>` is the skills folder under `.claude`, where the Dev
Engine and Linux checkouts live. Raw logs were kept in a scratch folder outside the
repository; the results below are copied from them. "Before" is the starting commit
`27a602b`, "after" is the branch head.

## Registered validators (from the engine prompt)

| Command | Before | After |
|---|---|---|
| `python3 scripts/validate_engine_control_plane.py --workspace-root ..` (the prompt's form; `..` is `<skills>`) | exit 1, 11 findings: no sibling layout under `<skills>` | Not rerun in this form: the layout still does not match, which is the environment, not the contract. Replaced by the next two rows. |
| same, `--workspace-root <engines>` | exit 1, 6 findings (4 former repository names, Linux elsewhere, private entry) | superseded |
| same, `--workspace-root <engines> --workspace-root <skills>` with `--engine` for the 11 public engines | not possible (single root, no aliases) | exit 0, 0 findings, "PASS: control-plane registry is valid" |
| same, `CHWEZI_ENGINES_ROOT="<engines>:<skills>"` with four `--engine` flags | not possible | exit 0, 0 findings |
| same, all 12 engines with both parents | n/a | exit 1, 1 finding: the private `political` engine is not installed on this host. It is outside the public catalogue and is `NOT_ASSESSED`, not a pass. |
| `python3 scripts/validate_engine_control_plane.py` (CI form, registry only) | exit 0 | exit 0, 12 entries, 0 findings |
| `python3 scripts/routing_smoke_test.py` | exit 0; 196 fixtures, p@1 177/196, p@3 196/196 | with `--lint-fixtures --min-rank1 89`: exit 0; 239 fixtures, p@1 219/239 (91.6%), p@3 239/239 (100%), negatives 83 (owned 83; pass 79, fail 0, `NOT_ASSESSED` 4), lint 0, failures 0 |
| `python3 -X utf8 scripts/skill_catalog_guardrails.py` | exit 0; 167 skills, 14 warnings, 0 errors | exit 0; 167 skills, 14 warnings, 0 errors. The gate now also runs the machine-path, duplicate-heading and broken-link checks. |

## Other repository checks

| Command | After (exit 0 unless stated) |
|---|---|
| `python3 scripts/routing_smoke_test.py --collisions --collision-gate --threshold 0.5` | one candidate pair, allow-listed, 0 errors |
| `python3 scripts/routing_smoke_test.py --coverage --max-zero-positive 1` | 166 of 167 skills have a positive fixture; `new-project` has none; 13 skills at three positives and two owned negatives; 39 with an owned negative. With a ceiling of 0 it exits 1 as designed. |
| `python3 -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all` | scanned 161, 0 errors, 0 warnings, 6 exempt |
| `python3 scripts/validate_approval_adapters.py --workspace-root <engines> --workspace-root <skills>` | 11 adapters, 0 findings (before: exit 1, 10 findings from hard-coded Windows paths) |
| `python3 scripts/check_source_register.py` (as of 2026-10-31) | 72 active sources, 0 findings, 15 warnings (reviews due within 14 days); the legacy-schema hospitality register is reported as overdue (review date 2026-10-14) and is not enforced |
| Digital Research `validate_source_currency.py --as-of 2026-10-31` on the register | 0 findings (before: 27). Metadata and dates only; claim support `NOT_ASSESSED` by the validator's own definition. |
| `python3 scripts/validate_tenant_invoice_example.py` | PASS |
| `php examples/tenant-invoice-listing/php/test.php` | `15 checks passed; PDO SQLite synthetic fixture` |
| `python3 scripts/check_package_file_budget.py` | 3199 checkout entries including `.git`; 2511 package-oriented; both below 5000 |
| `node hooks/test-destructive-bash-gate.js` and `node hooks/test-plugin-hook-config.js` | 61/61 and 7/7 |
| `python3 -X utf8 -m unittest tests/test_skill_catalog_guardrails.py` | 10 tests OK |
| `python3 -m json.tool` on the currentness register | parses |
| `git diff --check` | clean |

## Test suite

`pytest` is not installed on this host and installing it is not allowed, so the CI command
`python -m pytest tests -q` is `NOT_ASSESSED` here. Substitute: a local stand-in runner that
implements only the pytest features this repository's tests use. It is not pytest and is
labelled "shim-run".

| Run | Result |
|---|---|
| Stand-in runner, whole `tests/` folder, at `27a602b` | 220 passed, 3 skipped, 0 failed. This equals the 220 passed, 3 skipped that pass 1 recorded under real pytest on the same tree, which is the cross-check that the runner collects the same tests. |
| Stand-in runner, whole `tests/` folder, after | 273 passed, 3 skipped, 0 failed (53 new tests: register checker 16, resolver 11, review route 4, content hygiene 19, routing coverage 3) |
| `python3 -m unittest` per file | only 55 tests are collectable because most files use plain pytest functions; not a substitute |
| The 3 skipped | opt-in live checks that need `SKILL_ENGINE_LIVE_TESTS=1` and the original Windows layout; `NOT_ASSESSED` |

Failure cases built to fail, and observed failing: the pre-change register through the new
checker (27 findings, exit 1); the alias test with two aliases removed (2 findings); the
review route test with one gate link renamed (1 failure, file then restored); the coverage
ceiling set to 0 (exit 1); planted drive paths, user profiles, absolute link targets, new
duplicate headings and new broken links in the hygiene tests.

One regression was caught by an existing test during S04: removing the hyphenated engine name
from `AGENTS.md` failed `test_local_router_declares_currentness_gate`; fixed by naming the
engine without a path.

## Independent cross-checks

| Count | Generator | Independent | Agree |
|---|---|---|---|
| Overdue source records before | repository checker: 27 | Digital Research validator: 27 | yes |
| Overdue after | repository checker: 0 | Digital Research validator: 0 | yes |
| Skills with no positive fixture | `--coverage`: 1 | separate script over the fixture files: 1 | yes |
| Skills at three positives plus two owned negatives | `--coverage`: 13 | separate script: 13 | yes |
| Files with a duplicate H2 | module and baseline: 24 | separate fence-aware scan: 24 | yes |
| Test count | stand-in runner before: 220, 3 | pass-1 real pytest: 220, 3 | yes |
| Broken relative links | module (active skill roots, unique targets): 111 before, 84 after | separate scan over all tracked Markdown including `docs/`: 142 before, 109 after | different scopes, both fall |
| Machine-path lines in active content | guard: 30 before, 0 after | separate scan, active scopes: 58 lines before (about 30 real, the rest deliberate examples); the guard's exclusions are the dated records, `tests/`, `benchmarks/`, `.claude/` and `CHANGELOG.md` | consistent |

## Currency and execution limits

Sources, scope, access date and review date for every record are in
`docs/source-registers/skills-engine-currentness-2026-09.json` and
`docs/source-registers/ai-platforms.md`. Pages were read through a fetch tool that returns
a model-written summary, and with `curl` plus text search where a page was large; where the
summary hid a detail the record says so. Items marked `NOT_ASSESSED`:

- OpenAI help article on Codex availability: HTTP 403 to automated fetch (record quarantined, re-verify by 2026-11-30).
- Apple developer documentation: script-rendered, no version text returned (row keeps its 2026-07-08 date and is marked overdue).
- Kubernetes latest version: read from the version selector position, not a labelled "latest".
- PCI DSS and SLSA: version and status read, publication date not shown.
- OWASP ASVS: no statement about a newer version in development.
- Next.js security notice due 2026-11-03: not yet published; the two Next advisory records are due 2026-11-03.
- Legacy hospitality register (review date 2026-10-14): overdue, not reconciled this cycle.
- Real `pytest`; Next.js build; Compose build; MySQL migration run; live-model routing; Tier 3 behavioural runs; independent human review; the four cross-engine owner negatives (evaluated in union mode elsewhere).
- The live portfolio test (`SKILL_ENGINE_LIVE_TESTS=1`) assumes the original Windows layout; skipped.

No paid model call, package installation, `sudo`, service change, push, tag or pull request
was made. No file outside this repository was changed apart from the scratch folder.

## Model currentness (gate requirement)

OpenAI catalogue (2026-10-31) lists `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra` and
`gpt-6-luna`; the `gpt-6-luna` model page shows reasoning levels none to max and a 1,050,000-token context.
The changelog's newest entry (2026-10-30) releases GPT-6 Rosalind for approved
trusted-access organisations. The local Codex model cache, fetched 2026-10-29, lists
`gpt-6-luna` with `high` available. Decision: retain the Luna/high default and Astra only on
explicit selection; GPT-5.6 is never selected. Recency alone is not task-fit evidence. A full
quality, latency and cost comparison is `NOT_ASSESSED`; the next is due by 2026-12-28, three
months after the 2026-09-28 review.
