# 2026-09-29: Kaizen M10-06, Methodology and Comprehension Absorption

Phase: my-10-kaizen M10-06. Executor date: 29 Sep 2026. Base commit: `b3161da`. No Git state was
changed by the executor; the orchestrator commits. Zero spend: no paid model or API runs.

## Skill-count ledger

| Measure | Before | After |
|---|---:|---:|
| Active `SKILL.md` (skills/ + 00-meta-initialization/) | 167 | 167 |
| Inactive `ALIAS.md` | 76 | 78 (`plan-implementation`, `spec-architect`) |
| Plugin manifest skills (`generate-plugin-manifest.js --check`) | 165 | 165 |

No `SKILL.md` was added. Two alias files were added (aliases are not counted).

## Tasks

| Task | Status | What changed |
|---|---|---|
| T01 SP-01 | DONE | `new-project` mandatory Superpowers step replaced by the engine's shared-understanding gate plus an optional-helper sentence; `execution-plan-scripts` recasts `superpowers:executing-plans` as optional |
| T02 SP-01 | DONE | Ceremony class (spike, bounded, architectural), upward-only ratchet, stage-scoped approval in `world-class-engineering` §2 |
| T03 SP-03 | DONE | `execution-plan-scripts/references/plan-header-and-proportion.md`; dangling `plan-implementation` / `spec-architect` prose repointed; both names aliased |
| T04 SP-09 | DONE | Claim / required evidence / not sufficient table (8 rows) and banned success phrasing in `rules/common/verification.md`; back-link in `verification-loop.md` |
| T05 SP-10 | DONE | Excuse/Reality table, "suite defines green", string-presence test ban in `test-first-seams-and-oracles.md`; "80%+" removed from `agents/tdd-guide.md` |
| T06 SP-11 | DONE | "Dispatch and review controls" (five rules) in `parallel-execution-lanes.md` |
| T07 SP-12 | DONE | `coding-agent-optimization/references/worktree-safety.md`, linked from SKILL.md and the lanes reference |
| T08 SP-13 | DONE (one description edit) | `git-collaboration-workflow/references/receiving-review-feedback.md`; routing fixture added. The fixture ranked outside the top 5 on the unchanged description, so the description gained "deciding whether reviewer feedback is right" (241 -> 286 characters; cap 350) |
| T09 PT-08 | DONE | "Solution Selection" section with both ladder links and the eight-item ERP never-simplify list |
| T10 AO-17 | DONE_WITH_LIMITATIONS | `world-class-engineering/references/quality-bar-guard.md`; pressure scenario PS02 added to `benchmarks/solution-selection/fixtures.json` (`pressure_scenarios`). Field validation of that array arrives with M10-04-T05; execution belongs to M10-05 |
| T11 CV-02 | DONE | "Output registers" (R0/R1/R2, preserve list, no invented abbreviations, full-sentence warnings) in the English output standard; pointer in `rules/common/agentic-engineering.md` |
| T12 CV-03 | DONE | Per-lane report shapes and five status tokens in `parallel-execution-lanes.md`; `tests/test_report_shapes.py` |
| T13 GR-05 | DONE | `ai-assisted-development/references/graph-first-codebase-comprehension.md` and one routing line; routing fixture added |
| T14 GR-07 | DONE | Evidence-tag column and three worked rows in `drill-down-templates.md` |
| T15 GR-06 | DONE | Two advisory-hook properties in `engine-control-plane` §Hook semantics. Review: `hooks/hooks.json` registers only `destructive-bash-gate.js` (PreToolUse, Bash). It is a safety gate that denies on every attempt and fails closed on missing input, so the advisory properties do not apply; no change |
| T16 UA-02 | DONE | "Topology-ordered tour" section in `code-tour.md`, reconciled with persona budgets |
| T17 UA-03 | DONE | `doc-architect/scripts/validate_tour.py`; fixtures in `tests/fixtures/tours/`; `tests/test_validate_tour.py` |
| T18 UA-04 | DONE | Untrusted-content directive in `doc-architect/SKILL.md`, pointing to the `coding-agent-optimization` paragraph |
| T19 UA-05 | DONE | Class column (SKIP/PARTIAL/ARCHITECTURE/FULL) in the change-to-file map; pathspec staleness step; `generated_from_commit` |
| T20 GR-08 | DONE (pilot KEEP) | `ai-assisted-development/scripts/php_mysql_map.py`, synthetic fixture `tests/fixtures/php-mysql-map/` (5 controllers, 8 tables), `tests/test_php_mysql_map.py`. Read-only pilot on Peter's named repository: 10/10 hand-checked routes recover every table; 6/10 exact, 4/10 add `audit_trails` reached through the permission middleware's denial log (reported with evidence). "What touches `tax_transactions`" and "`journal_reversals`": map finds the routes, a grep on the table name finds none or only the service |
| T21 AR-10 | DONE | `system-architecture-design/references/architecture-as-code.md` with a dated C4 source record; cross-link from `practical-architecture-knowledge.md` |
| T22 AR-11 | DONE | `system-architecture-design/scripts/verify_diagram_evidence.py`; `tests/test_verify_diagram_evidence.py` (throwaway repositories) |
| T23 UX-12 | DONE | `ai-rag-patterns/references/curated-corpus-worked-example.md` |
| T24 IM-15 | DEFERRED | Needs the accepted M10-09 detector command; handed back to M10-09 |
| T25 PT-11 | NOT_ASSESSED / DEFERRED | The reach test needs a live subagent model run, excluded by the zero-spend rule. No hook added |
| Orphan folders (BL-01e) | DONE | 45 tracked folders dispositioned; see `docs/catalog-cleanup/empty-directory-disposition.md` (2026-09-29 M10-06 section) |

## Verification (29 Sep 2026, Windows, Python 3.13.7, Node 24.8.0)

| Check | Result |
|---|---|
| `skill_catalog_guardrails.py` | 167 active; 0 findings |
| `routing_smoke_test.py` | 187 fixtures (184 + 3); p@1 179/187 (95.7 %, was 178/184, 96.7 %); p@3 187/187; 0 failures |
| `routing_smoke_test.py --collisions` | 2 pairs, both pre-existing; none involves a touched skill |
| `contract_gate.py --all` | 161 scanned, 0 errors |
| `engine_compliance.py --root .` | 136 fully compliant of 165, unchanged |
| `pytest tests` | 187 passed, 3 skipped (was 133 passed) |
| Hook tests | 61/61, 7/7 |
| `validate_engine_control_plane.py` | PASS |
| `generate-plugin-manifest.js --check` | current, 165 skills |
| `validate_benchmark_fixtures.py` | PASS, `SPECIFIED_NOT_EXECUTED` |
| `validate-no-book-extractions.py` | 0 findings |
| `validate_work_graph.py templates/work-graph.yml` | 0 findings |
| `quick_validate.py` on 15 touched skills | all valid |

## Open items

- M10-03 has not set a p@1 floor yet; the p@1 comparison against that floor is `NOT_ASSESSED`.
- M10-04-T05 must validate the `pressure_scenarios` array (PS02 already conforms to its field list).
- M10-05 executes PS02. M10-07 reuses `verify_diagram_evidence.py`. M10-09 supplies the T24 command.
- Peter's exact-diff ratification: T01, T02, T05 (agent wording), T09, T10, T11, and the T08
  description edit.
