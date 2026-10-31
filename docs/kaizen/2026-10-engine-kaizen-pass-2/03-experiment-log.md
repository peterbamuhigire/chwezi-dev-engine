# Experiment and change log (pass 2)

Baseline frozen at commit `5eb55c8` (observations and scorecard) on top of `27a602b`, before
any change. Each experiment changed one thing, then every registered validator and the full
test suite were re-run (results in [04-validation-record.md](04-validation-record.md)). Hashes
are on branch `kaizen/2026-10-pass2`.

## Kept

| ID | Hypothesis | Change | Result | Commit |
|---|---|---|---|---|
| S01 data | Re-reading each overdue primary page and recording what it showed will clear the 27 lapsed records without false currency. | 18 new dated records, 26 snapshots moved to `superseded_sources`, 1 quarantined (page returned HTTP 403), 15 Step 5 records, 8 unchanged records re-read, `ai-platforms.md` rewritten row by row. Two claims narrowed because the pages no longer support them (Claude Code best practices lost its explore-plan-code section; ShouldProcess nested-operation wording unconfirmed). | Overdue records 27 to 0 (research validator and the new checker agree). Findings from the reading: OpenAI Evals platform read-only 2026-10-31 and shut down 2026-11-30; `v1/prompts` shuts down 2026-11-30; Bedrock Agents is now Agents Classic and closed to new customers; three canonical URLs moved. No skill depended on any of them. | `f970df0` |
| S01 check | A repository-owned check will fail when a record lapses, so debt cannot build up unseen. | `scripts/check_source_register.py`, `tests/test_source_register.py` (16 tests), CI step. | Pre-change register: 27 findings, exit 1 (same 27 as the Digital Research validator). Current: 0 findings. At 2026-12-05 the validator reports 60 findings, showing the gate fires when windows close. | `ca94e6b` |
| S01 model review | Recording the model-currentness review keeps the Luna/high pin evidence dated. | One changelog record and claim. | Newest OpenAI entry (2026-10-30) is a trusted-access specialist model; pin retained; comparison `NOT_ASSESSED`, next full comparison due by 2026-12-28. | `842965b` |
| S02 | One resolver with aliases and repeatable parents makes both validators run on this host. | `scripts/engine_roots.py`; both validators use it; Windows paths removed; docs updated; 11 tests. | Control-plane validator on the 11 public engines with both real parent folders: exit 0 (was exit 1, 11 findings with the default parent and 6 with the engines folder). Approval validator: exit 0 (was exit 1, 10 findings). Mutation check: removing two aliases yields 2 findings. CI registry-only form unchanged (exit 0). | `9979773` |
| S03 | A review row and a domain-owned checks table will connect all four defect owners. | Router row, routing-index section, gate table with five owners, exercise aligned to `LedgerPostingService`, one fixture, 4 tests. | All table links resolve; mutating one link makes the test fail; the exercise names the owning skill. | `a6735a5` |
| S04 | A path guard plus fixes removes host paths from active content. | 30 lines fixed, eight leaked tool-markup tails removed, pass-1 evidence citations of a deleted folder replaced with marked placeholders and an availability note; `content_hygiene.machine-paths`; 13 tests. One regression found and fixed on the way: the portfolio policy test needs the hyphenated engine name, so the router now names `digital-research-engine` without a path. | In-scope findings 30 to 0; planted paths fail. | `39a6898`, `3b7b3f6` |
| S06 | Lossless merges plus a ratchet cut duplicate headings and stop new ones. | 57 skills merged in two committed passes with a per-file line-multiset check (one removed heading and one label added, nothing else); ratchet with baseline; 3 tests. | Duplicate-H2 files 65 to 24. Independent count (a separate script) equals the module's: 24. | `feccc13`, `d12c250`, `f3b0705` |
| S07 | Conservative link repair plus a ratchet reduces broken links and stops new ones. | 33 links rewritten in 19 files; check covers all Markdown under active roots; baseline of 84; 3 tests. | Unique broken targets under active roots 111 to 84. | `0ca42e0`, `625e5e7` |
| S05 | Fixtures for the skills that had none, and a repository measure, lift coverage and keep it. | 42 positive fixtures; `--coverage` and `--max-zero-positive`; CI ceiling 1 and rank-1 floor 89; 3 tests. | Skills with no positive fixture 43 to 1 (independent count agrees); precision@1 177/196 to 219/239 (90.3% to 91.6%); precision@3 stays 100%; lint 0. | `9f0369e`, `c4e691f` |
| S08 | Stating the slice's gaps stops it being copied as finished. | "Known gaps" section in the slice README. | Structure check and 7 tests unchanged. | `8bec17a` |

## Reverted or not kept

| Experiment | Hypothesis | Result | Disposition |
|---|---|---|---|
| Widen the `accounting-engine` description to mention reviewing ledger writes and the posting service | The review prompt would then rank the accounting skill under the lexical proxy. | The skill did not enter the top five before or after (cosine falls as the description lengthens). No measurable gain, and a live-model run is not allowed. | Reverted before commit. The route is carried by the router row and the gate table instead. |
| Merge `Anti-Patterns` pairs in every skill | Same lossless merge as the other classes. | In 19 skills the first section ends in a generated-block marker, so the merged text landed outside its section. | Skipped those 19 skills (they stay in the baseline). The first attempt on all 25 was reverted. |
| Merge the pair in `skill-writing` | Same merge. | The file grew from 20,479 to 20,492 bytes and crossed the 20,480-byte report-only threshold, raising the warning count from 14 to 15. | Reverted that file. |
| Unrestricted link repair | Rewrite every link whose target name is unique. | It rewrote links that name a different skill folder to the nearest ancestor entrypoint, a judgement call. | Reverted; reapplied with the parent-entrypoint rule restricted to `../` segments. |

## Rollback map

Each item is independent. Revert by commit: S01 data and checker, S02 resolver, S03 route,
S04 content then guard, S06 merges then ratchet, S07 repairs then ratchet, S05 fixtures then
tooling. The baseline files under `docs/quality-gates/` must be reverted with their guards.
