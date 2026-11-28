# Windows validation record

Capture group base. Published output from revision-bound logs.

| Check | Command | Exit | Evidence |
| --- | --- | ---: | --- |
| guardrails | `python -X utf8 scripts/skill_catalog_guardrails.py` | 0 | 171 active skills, 16 size warnings, zero errors |
| unittest | `python -X utf8 -m unittest tests/test_skill_catalog_guardrails.py` | 0 | OK |
| pytest | `python -X utf8 -m pytest tests -q -p no:cacheprovider` | 1 | 1 failed, 289 passed, 3 skipped, 8 subtests passed in 272.94s (0:04:32) |
| routing | `python -X utf8 scripts/routing_smoke_test.py --min-rank1 89 --lint-fixtures` | 0 | - failures: 0 |
| coverage | `python -X utf8 scripts/routing_smoke_test.py --coverage --max-zero-positive 1` | 0 | - zero-positive ceiling: 1 |
| collisions | `python -X utf8 scripts/routing_smoke_test.py --collisions --collision-gate --threshold 0.5` | 0 | - collision gate: 0 error(s) at >= 0.75; allow-list routing-collision-allowlist.yml |
| control | `python -X utf8 scripts/validate_engine_control_plane.py` | 0 | PASS: control-plane registry is valid |
| sources | `python -X utf8 scripts/check_source_register.py` | 1 | Eight overdue records and 50 warnings as of 2026-11-28 |
| bash-hook | `node hooks/test-destructive-bash-gate.js` | 1 | 54/61. Seven synthetic allowed pushes failed closed while reading Git config |
| plugin-hook | `node hooks/test-plugin-hook-config.js` | 0 | 7/7 |
| contract | `python -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all` | 1 | 165 scanned, six exempt. Illustration skill lacks evidence markers and canonical evidence table |
| auto | `python -B -m unittest discover -s auto-agents/tests` | pending | NOT_ASSESSED until this command returns |
| whitespace | `git diff --check` | 0 | See command status |
| install-control | `python -X utf8 scripts/validate_engine_control_plane.py --workspace-root <engine-workspace> --engine accounting --engine business-plan --engine chwezi-dev-engine --engine design --engine digital-research --engine linux --engine proposal --engine social-media --engine srs --engine website --engine windows-admin` | 0 | PASS: control-plane registry is valid |
| approval | `python -X utf8 scripts/validate_approval_adapters.py --workspace-root <engine-workspace>` | 0 | PASS: all approval adapters satisfy the shared contract |
| invoice | `python -X utf8 scripts/validate_tenant_invoice_example.py` | 0 | PASS: tenant invoice example files and security invariants |
| invoice-php | `php examples/tenant-invoice-listing/php/test.php` | 0 | 15 assertions on synthetic PDO SQLite fixture |
| package | `python -B -X utf8 scripts/check_package_file_budget.py` | 0 | 2,726 package-oriented entries against the 5,000 cap |
| ingestion | `python -X utf8 scripts/source_ingestion_guardrail.py` | 0 | findings: 0 |
| workgraph | `python -X utf8 scripts/validate_work_graph.py templates/work-graph.yml` | 0 | work-graph: nodes=1 findings=0 frontier=slice-1 |
| token | `python -X utf8 <engine-workspace>/chwezi-engine-agents/scripts/check_token_budget.py --strict .` | 0 | Zero byte, class-block placement or pin findings. Exact tokenizer count is still unassessed |

Pinned dependencies were present locally in their required versions. Checked with pip show and left the existing environment in place.

Current Linux run, Windows installers, full browser/device/production deployment, exact runtime skill metadata and private repository parity are NOT_ASSESSED.

Codex model policy helper exited 0 in check-only mode. Active reviewer runtime identifies as GPT-6.2 Sol. Release and account evidence is recorded with the cycle-wide model decision.


﻿# Independent catalogue review

Reviewed starting revision 2ef1f97 and product revision 1ad166d on 2026-11-28. Reviewer runtime GPT-6.2 Sol, read-only review.

- Resolved blocking finding. An initial illustration diff inserted an unrelated Next.js evidence block. The final illustration skill has one marker span, the skill’s own applicability, a drawing-proof table and its existing references. The complete evidence gate scanned 165 skills with zero errors, zero warnings and six exemptions.
- The YAML parser adds one line for the opening delimiter and translates the zero-based PyYAML mark to file coordinates. Existing classification, fail paths and input parsing stay in place. Eleven focused tests pass, including the new LF and CRLF malformed input cases. The concise diagnostic intentionally omits parser excerpts and cause detail.
- The community runtime is maintained upstream. Local distribution consumers are directed to authorised update procedures, and the standalone Kaizen prompt now resolves research through host configuration. Missing authority remains NOT_ASSESSED.
- The legacy UX stub and index point to the live psychology skill under the design router, matching the direct alias registry. The registry still lists a historical ux-foundations merge grouping. Direct external routing resolves the tested legacy slug.
- The eight overdue vendor source records were read on 2026-11-28. Commit b69d7cd adds dated records for verified scopes, retains superseded evidence, remaps active references and validates successfully against the existing gate. The reviewed scratch JSON and committed register have the same Git blob ID. The catalogue reviewer authored the register patch and the cycle lead owns its independent review. The sources concern historical advisories, release tags and one lifecycle table. Patch applicability for a deployment remains outside those claims.
- Baseline Windows Bash hook failures were fail-closed refusals. A direct test of its read-only Git configuration probe yielded ETIMEDOUT four times under parallel process load. The 750 ms probe and fail-closed policy remain in force. Rerun under reduced load before attributing the initial results to a regression.

No private workflow content or book passages appear in the reviewed product diff. The registered Debian WSL instance could not mount its backing disk, so current Linux execution, exact host skill metadata discovery, source-register reviews due after 28 November, and legacy local-settings history remain NOT_ASSESSED.



Follow-up at 1b63225 verified the owning Kaizen skill, prompt and AGENTS route to the same configured currentness authority. The updated test checks source evaluation and unsupported claims for the changed engines while retaining the legacy contract checks for scoped peers. The Windows suite passed 291 tests and 10 subtests with three opt-in installed-portfolio checks skipped. Full unattended-runner suite remains pending.


﻿# Post-change validation checkpoint

Windows, Python 3.13.7, Node v24.8.0. Product commit 1ad166d and source commit b69d7cd. A commit was made while the first post-change suite ran. The source register was present as the same working-tree content before the commit.

- Frozen pytest baseline at 2ef1f97. Exit 1 in 272.94 seconds. 289 passed, 3 skipped, 8 subtests passed, one failed current-register assertion (8 overdue).
- First post-change pytest. Exit 1 in 410.30 seconds. 289 passed, 3 skipped, 10 subtests passed, two failures. Active-content machine paths in the evidence pack and a test pinned to the retired research-engine router wording.
- Final pytest against the currentness-policy fix on disk and committed at 1b63225 during the run. Exit 0 in 228.41 seconds. 291 passed, 3 opt-in installed-portfolio checks skipped, 10 subtests passed.
- Evidence path repair verified by catalogue guardrails at b69d7cd, exit 0, 171 active, 16 size warnings, 0 errors. Source ingestion, byte-budget lint and whitespace checks all exit 0.
- Evidence contract exit 0. 165 scanned, six exempt, zero errors and warnings.
- Focused unit tests exit 0, eleven passed, including the new LF and CRLF file-coordinate regression.
- Source register exit 0. 75 active, zero findings and 58 warnings. Earlier baseline had eight overdue failures and 50 warnings.
- Existing routing, coverage, collision, standalone control, installed control, approval adapters, package, invoice, PHP invoice, plugin hook and work graph checks exit 0. The PHP fixture checked 15 synthetic assertions.
- Bash gate checks exit 1. 54/61 baseline and 56/61 on retry. In the direct diagnostic all four read-only Git probes hit the existing 750 ms timeout, with elapsed durations 839, 894, 898 and 877 ms. An expired probe leads to fail-closed refusal. Timing is observed under load and has no release-performance implication.
- Linux is NOT_ASSESSED. The installed Debian WSL instance could not mount its backing disk. The exact assembled skill metadata budget and exact startup tokenizer count are also NOT_ASSESSED.
- Baseline and final unattended runtime suite results are pending. No runtime implementation changed in these revisions.




The final catalogue suite passed 291 tests and ten subtests with three skips in 228.41 seconds at the corrected currentness policy. Linux repeat NOT_ASSESSED: the registered distribution could not mount its backing storage. The Bash-hook repeat passed 56/61 Windows cases, with fail-closed timeouts on the Git probes. No hook policy or timeout was weakened.
