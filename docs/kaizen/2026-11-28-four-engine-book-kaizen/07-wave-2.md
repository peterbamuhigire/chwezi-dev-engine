# Second wave, 28 November 2026

Starting revision `3e45a2b` on `kaizen/2026-11-28-four-engine-book-kaizen`.
The worktree was clean. No active catalogue JAD process was observed in the
local preflight query.

## Keep decision

The README said the source-register gate was open. AGENTS.md called 12 November
the next failing date. On the starting revision the current check exited 0 with
75 active records, zero findings and 58 warnings. A dated calendar had fallen
out of sync with the register after the first-wave renewals.

The README and AGENTS.md now send maintainers to the existing validator.
The README links the November results, and the handoff identifies the first
review boundary. The gate, source dates and catalogue inventory are identical.
A maintainer can find the affected source IDs with one command:

```sh
python3 -X utf8 scripts/check_source_register.py --as-of 2026-11-30
```

The direct check and the as-of probes used Python 3.13.7 on Windows.

| As of | Exit | Findings | Warnings |
| --- | ---: | ---: | ---: |
| 2026-11-28 | 0 | 0 | 58 |
| 2026-11-29 | 0 | 0 | 58 |
| 2026-11-30 | 1 | 6 | 52 |
| 2026-12-01 | 1 | 42 | 16 |

The first six are the OpenAI changelog, model selection, skills context budget,
plugin package format, plugin submission errors and Claude plugin marketplace
records. These are date and metadata results. Source support for the next
renewal and the legacy hospitality warning remains to be assessed.

For the historical check, the old README calendar used this command against
the 6 November snapshot. The current register has since changed.

```sh
python3 -X utf8 scripts/check_source_register.py --as-of 2026-11-14
```

One discrepancy in the first-wave scoring evidence remains visible in the
frozen scorecard. Both the captured baseline `2ef1f97` and `3e45a2b` show
171 active skills in the routing index. A fresh tracked inventory found
171 live skills and 78 alias files. No credit is claimed for correcting the
inventory. The frozen baseline remains 69.4 raw and 65 capped. The first-wave
78.4 score remains the last broad score. This wave measures the documentation
failure and the correction without increasing that score.

If the date or evidence route is wrong, revert the README, AGENTS and handoff
changes together. Use the validator output to recover the correct source IDs.
Re-audit on 29 November, or after a change to the register or its gate.

## Model currentness

Anthropic currency check 2026-11-28: no change. Its official model inventory
listed Claude Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5 when accessed on
28 November. OpenAI's 17 November release and API release notes, checked on
28 November, identify `gpt-6.2-sol` for day-to-day work and
`gpt-6.2-astra` for harder work. The active Codex delegation surface lists
Sol at medium. The local model-policy check exited 0. Retain the existing
Sol pin for this bounded maintainer task. Authenticated API/Claude catalogues,
local cost, latency and quality comparisons and account charges are
`NOT_ASSESSED`. The October model-comparison checkpoint remains due
28 December. [Anthropic inventory](https://platform.claude.com/docs/en/models/overview) ·
[OpenAI announcement](https://openai.com/index/introducing-gpt-6-2-astra-sol/) ·
[OpenAI release notes](https://help.openai.com/en/articles/9624314-model-release-notes).

The prior wave used Nystrom (2021), *Crafting Interpreters*, for actionable
diagnostics. This documentation experiment needed no further book material.
It adds no framework, protocol or version claims to the catalogue.

## Validation and review

Windows, Python 3.13.7 and Node 24.8.0. The existing environment had the pinned
pytest 9.0.3 and PyYAML 6.0.2. Commands below ran from the catalogue root.
The guardrail checks cover both LF and CRLF malformed YAML cases.

| Command | Exit | Observation |
| --- | ---: | --- |
| `python -X utf8 scripts/skill_catalog_guardrails.py` | 0 | 171 active skills and 16 existing size warnings |
| `python -X utf8 -m unittest tests/test_skill_catalog_guardrails.py` | 0 | 11 cases |
| `python -X utf8 -m pytest tests -q -p no:cacheprovider` | 0 | 291 passed, 3 opt-in installed-portfolio skips, 10 subtests passed, 185.27 s |
| `python -X utf8 scripts/routing_smoke_test.py --min-rank1 89 --lint-fixtures` | 0 | 233/253 rank-1, 253/253 rank-3, 89 owned negatives pass, 4 unassessed |
| `python -X utf8 scripts/routing_smoke_test.py --coverage --max-zero-positive 1` | 0 | 170 of 171 skills with a positive fixture |
| `python -X utf8 scripts/routing_smoke_test.py --collisions --collision-gate --threshold 0.5` | 0 | One allow-listed pair, zero gate errors |
| `python -X utf8 scripts/validate_engine_control_plane.py` | 0 | 12 registry entries |
| `python -X utf8 scripts/check_source_register.py` | 0 | 75 active sources, 0 findings, 58 warnings |
| `node hooks/test-destructive-bash-gate.js` | 0 | 61/61, run before launching the Python suites |
| `node hooks/test-plugin-hook-config.js` | 0 | 7/7 |
| `python -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all` | 0 | 165 scanned, six exempt, zero errors or warnings |
| `python -X utf8 scripts/validate_engine_control_plane.py --workspace-root .. --engine accounting --engine business-plan --engine chwezi-dev-engine --engine design --engine digital-research --engine linux --engine proposal --engine social-media --engine srs --engine website --engine windows-admin` | 0 | 11 named installations, zero findings |
| `python -X utf8 scripts/validate_approval_adapters.py --workspace-root ..` | 0 | 11 adapters, zero findings |
| `python -X utf8 scripts/validate_tenant_invoice_example.py` | 0 | Fixture files and tenant safety invariants |
| `php examples/tenant-invoice-listing/php/test.php` | 0 | 15 synthetic PDO SQLite checks |
| `python -B -X utf8 scripts/check_package_file_budget.py` | 0 | 2,734 package-oriented entries against 5,000 |
| `python -X utf8 scripts/source_ingestion_guardrail.py` | 0 | Zero findings |
| `python -X utf8 scripts/validate_work_graph.py templates/work-graph.yml` | 0 | One node, zero findings |
| `python -X utf8 docs/plans/ai-engine-kaizen/evidence/ER2/check_readme.py` | 0 | Existing task links and anchors pass. A synthetic broken task link is rejected. |
| `python -X utf8 ../chwezi-engine-agents/scripts/check_token_budget.py --strict .` | 0 | Zero byte and placement findings |
| `git diff --check` | 0 | No whitespace findings |

The first wave’s closing runtime command was
`python -B -m unittest discover -s auto-agents/tests`. It exited 0 for all
167 cases. That run and the second-wave starting tree have identical
`auto-agents` Git tree IDs, `77378dcab3bf16e5bcc6e9c834405b1537789a77`.
The second wave only edits Markdown outside that tree.

The Bash hook rerun reproduces all 61 expected synthetic decisions without
a hook change. The first-wave 54/61 and 56/61 results remain recorded. Load
sensitivity remains open because the successful rerun does not test the
earlier concurrent workload.

The Debian WSL check exited 1 with `ERROR_PATH_NOT_FOUND` while mounting
its registered disk. Current Linux execution, real installers, production
behaviour, native skill inventory, exact tokenizer counts, legacy settings
history and catalogue parity remain `NOT_ASSESSED`.

The scope and claims review covered the changed prose, source assertions and
links. No unsupported claims or book text were added. Third-party runtime
delivery and the previous unresolved security and privacy findings remain
outside this evidence. The independent cycle lead review accepted the date
gate and requested retention of the earlier command and model checkpoint.
