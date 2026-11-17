# Community engine capabilities: 17 November 2026

The README and overview now describe the community checkout at `0646c8c`.
Four upstream commits were fast-forwarded without rewriting history. This
documentation change does not import private-engine skills or research notes.

## Runner features present in this checkout

| Release | Implemented change | Local evidence |
|---|---|---|
| 2.2.0 | Optional lanes with separate plans, branches, worktrees and state; bounded target integration | `7be76e0`; [lane configuration](../../auto-agents/README.md#parallel-lanes) and [lane tests](../../auto-agents/tests/test_lanes.py) |
| 2.2.1 | STOP received before a prepared job launches stops the run cleanly | `389982a`; [driver tests](../../auto-agents/tests/test_driver.py) |
| 2.2.2 | Recognises additional Claude usage-limit responses | `7b8d8e8`; [provider-limit tests](../../auto-agents/tests/test_provider_limit.py) |
| 2.2.3 | Integration quick checks use a separate slot pool from full gates | `0646c8c`; [execution implementation](../../auto-agents/execution.py) |

The default remains sequential. Lanes require disjoint ownership and isolated
test data/services. Target integration requires publishing authority and
explicit configuration; a clean rebase of disjoint files does not prove semantic
independence. Keep a broad final verification gate. The runner retains existing
host permissions and does not grant credentials or establish a security sandbox.

The guide's opening sequential description and its no-rebase statement describe
the default mode. The opt-in `integrate` behaviour is specified in its Parallel
lanes section. Managed runner files are unchanged by this documentation refresh.

## Validation and limits

Checks ran on Windows on 17 November against this community checkout:

| Check | Result |
|---|---|
| `python -B -X utf8 -m pytest tests -q -p no:cacheprovider` | 277 passed, 3 skipped in 103.05 seconds; installed-portfolio tests remain opt-in |
| Catalogue and content guardrails | 170 active skills; 0 errors, 16 size warnings |
| Routing with fixture lint and rank-one floor of 89% | 248 fixtures; 227 first-place matches (91.5%), all 248 in the top three; no failures |
| Owned routing negatives | 87 passed, 0 failed, 4 NOT_ASSESSED |
| Fixture coverage and collision gates | Passed; one skill has no positive fixture; 16 skills have three positives and two owned negatives |
| Control-plane registry | Passed; installed-checkout coverage not exercised |
| Destructive-command and plugin-hook tests | Passed |
| Evidence declarations | 164 scanned, 6 exempt; 0 errors or warnings |
| Source registers, `--as-of 2026-11-17` | Exit 1: 75 active sources, 9 overdue findings, 53 warnings |

Source-currentness is an existing unresolved gate. Review dates were not
extended, baselines were not relaxed and no full-green CI claim is made.
Routing measures are lexical proxies, not observed Codex or Claude activation.
The documentation review checked claims against the community code and dated
records, removed stale headline counts and distinguished available features
from untested operational outcomes. No independent reviewer was run.

Historical runtime results remain in [EVIDENCE.md](../../auto-agents/EVIDENCE.md)
with their original platform and release scope. This documentation refresh does
not constitute a new runtime-suite execution or live rollout. Live multi-lane
throughput, shared-service isolation, quota reset and physical power-cut recovery
remain NOT_ASSESSED. No model policy, host configuration, startup registration,
application deployment or lane activation changed.
