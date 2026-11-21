# Windows publication check: 17 November 2026

Release 2.2.3, upstream baseline `90fddba`, with a documentation-only refresh.
Scope: `python -B -m unittest discover -s auto-agents/tests`.
The final run used an external standard unittest discovery harness with verbose
logging and a result callback that saves fixture state on failure before cleanup.
Tests, configuration and acceptance criteria were unchanged by that harness.
The suite ran **107 tests in 707.822 seconds: 106 passed, 1 skipped**.
The skip requires a real Mac. The combined fake-agent suite includes optional
lane integration, separate gate/integration slot pools, stop-before-launch,
provider-limit responses, owner-intent checks and receipt-read recovery.
This is Windows fixture evidence, not a live lane rollout, performance claim,
real quota-reset trial or physical power-cut test.

The initial concurrent validation run had one failure in
`test_progress_and_evidence_can_complete_original_contract` (blocked result
instead of success). The unchanged case passed in isolation, then this complete
serial rerun passed. The initial cause was not established; failure evidence
is retained in the private publication workspace. No timeout was increased.

The engine suite passed 532 tests with 1 skip (1755 subtests); maintenance
passed 7. Runtime Python sources match upstream; project configuration,
PLAN.md and ENGINE.md remain unchanged. The README now distinguishes default
sequential execution from optional lanes and opt-in target integration.
Managed documentation hashes were regenerated; no application-project rollout
or host cache activation was performed. Earlier entries retain their dated scope.

# Publication integration: 16 November 2026

The owner authorised commits and pushes to main after the earlier hold.
The incoming 2.0.1 macOS/BSD boot-identity fix and its two tests were retained
alongside the 2.1.1 owner-intent and receipt-read hardening. Documentation
conflicts retained both dated evidence records; no published history was rewritten.

The combined Windows suite ran **83 tests in 385.762 seconds**:
**82 passed, 1 skipped**. Command: `python -B -m unittest discover
-s auto-agents/tests`. The skipped test requires a real Mac; the stubbed macOS
parsing/fallback test passed. This is not fresh live macOS or reboot evidence.
Managed hashes verify and project config, PLAN.md and ENGINE.md remain unchanged.
The earlier suite counts below describe their pre-integration snapshots.

# Live owner intent and receipt reads: 16 November 2026

Release 2.1.1. The full Windows runtime suite passed **81 tests in 522.707
seconds** after the final behavioral changes. New cases cover owner-plan or
contract changes during a run, both provider profiles, prepared/active operation
recovery, unrelated owner work, and transient/persistent receipt-read denial.
The active-recovery case uses mocked inspection/wait; it is not a live crash test.

Owner inputs are rechecked at operation boundaries and before checkpoint
acceptance. An already active job may finish; CANCEL remains the immediate-stop
control. These checks are not atomic revocation or a hostile-host boundary.

Windows PermissionError reads receive up to eight attempts with 0.28 seconds
of total requested backoff. Only the local read is retried, never the job.
Missing files, corrupt JSON and persistent denial remain failures. Injected
denial regressions failed before the fix and passed afterward. One real local
job executed once; a simulated denial while rereading its completed receipt did
not launch it again. The original denial's lock holder and real contention
behavior under other host conditions remain NOT_ASSESSED.

Independent read-only review found no confirmed material defect and identified
the simulation limits above. No new live provider run, physical power-cut test,
deployment, schedule or model/permission change is inferred. Earlier evidence
below remains historical, tied to its stated version and scope.

# Approved-contract regression evidence: 16 November 2026

Release 2.1.0. The final full Windows runtime suite passed **71 tests in 326.346 seconds**, including the recovery-context regression accepted in independent review.
Disposable Git fixtures and fake agents exercise dirty owner contracts, worker
acceptance-definition changes under both Codex and Claude runner profiles, and
legitimate state/evidence progress. No live provider implementation or external
side effect is inferred from these fixtures. Task metadata remains an assertion;
independent configured verification and actual-diff review remain necessary.

The Codex project default is now `gpt-6.1-terra`, medium, by the owner's explicit
16 November decision. `gpt-6-astra`, high, remains explicitly selected only.
Claude arguments, runtime permissions and publication authority are unchanged.
The older smoke results below describe the models actually tested at that time;
they are not new Terra throughput or cost evidence.

Known limits: a fingerprint detects drift, not a privileged actor rewriting its
own tools; unchanged commands may run weakened test code. Physical power loss,
live quota resets, multi-hour execution and comparative efficiency remain
NOT_ASSESSED. The owning engine's Kaizen record holds the current review result.

# Unattended execution Kaizen evidence: 2026-11-15

Scope: shared source tools and relevant skills in the four owner-named development/coordinator/SDLC engines. This update does not run a client implementation plan or install a startup task. Historical evidence below remains dated to its original revision.

## Observed runtime and source currentness

Digital Research source evaluation and verification were applied. Access/review date for every source below: **2026-11-15**. Platform/API claims are volatile; recheck on CLI, Python, OS or authentication changes. Undated pages have unknown publication dates. Books inform durable design choices only.

| Claim and scope | Primary source / installed evidence | Decision and uncertainty |
|---|---|---|
| Noninteractive Codex execution and JSONL events | [OpenAI automation example](https://developers.openai.com/blog/eval-skills); installed `codex exec --help`, CLI 0.169.0 | Used the installed stdin/exec contract. A real bounded smoke returned the exact expected final agent message with exit 0. This is not a full implementation or quota-recovery test. |
| Claude print mode and JSON output | [Claude CLI reference](https://code.claude.com/docs/en/cli-usage); installed `claude --help`, 2.1.325 | A real bounded print-mode smoke returned the exact expected result with exit 0, with tools disabled for that smoke. Runtime permissions/model configuration remain separate. |
| Usage windows depend on current account/plan | [OpenAI usage limits](https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits), [Claude plan usage](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-max-or-ultra-plan) | Persist a bounded next probe. Do not label a configured five-hour wait as a known reset or bypass limits. Actual account reset and quota recovery: NOT_ASSESSED. |
| Windows process creation and lifetime | [Python 3.13 subprocess](https://docs.python.org/3.13/library/subprocess.html), [Microsoft creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags), [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) | Installed Python 3.13.7; docs cover the 3.13 maintenance line. Dedicated worker joins a kill-on-close job before spawning. Nested-job assignment and child cleanup exercised on this Windows host. WMI/service-created processes are outside ordinary descendant containment. |
| Checkpoint writes | [Python 3.13 os](https://docs.python.org/3.13/library/os.html) | Temporary write, flush/fsync and replacement; bounded retry for observed Windows sharing denial. Tests cover partial temporary files and malformed state. Physical disk/power-cut durability is NOT_ASSESSED; no unconditional NTFS guarantee is claimed. |
| Restart scheduling | [Microsoft logon trigger](https://learn.microsoft.com/en-us/windows/win32/taskschd/logontrigger), [logon types](https://learn.microsoft.com/windows/win32/api/taskschd/ne-taskschd-task_logon_type) | Current-user interactive logon is distinct from before-login boot execution. Script preview is not registration or proof of post-reboot authentication. |
| Model currentness | [OpenAI release notes](https://help.openai.com/en/articles/9624314-model-release-notes), [Sol/Luna release](https://openai.com/index/introducing-gpt-6-sol-and-luna/), [Anthropic lifecycle](https://docs.anthropic.com/en/docs/about-claude/model-deprecations); local `codex debug models` safe fields | Luna `gpt-6-luna` remains listed with medium default; newer 6.1 variants were observed. Retain the owner's pins. No comparable quality/cost/latency/task-fit study supports replacement. Claude account model entitlement and full model comparison: NOT_ASSESSED. Running root configuration was not changed. |

The two real CLI smokes returned exactly `RUNNER_SMOKE_OK`, verified from Codex's final agent-message event and Claude's result field, not by searching echoed input. Codex reported input_tokens 21820, cached_input_tokens 7168 and output_tokens 9. Claude reported input_tokens 2, cache_creation_input_tokens 31091 and output_tokens 16. These provider-specific counters show substantial session context overhead; they are not comparable total costs or evidence of token savings. No credentials were printed and no API-key billing mode was selected by the harness.

## Verification scope

**2.3.10 (2026-11-19, Windows 11):** Plan reads tolerate non-UTF-8 bytes (`errors='replace'`). The driver only needs the first line's `STATUS:` marker. The runner prompt gains one sentence: write text files as UTF-8, because Windows PowerShell 5.1 `Set-Content`/`Out-File` default to ANSI. In Garage on 19 Nov, a repair session rewrote `PLAN.md` and `handoff.md` in Windows-1252, an em dash became byte 0x97, and the next session blocked with `'utf-8' codec can't decode byte 0x97`. New tests: a plan with an ANSI byte completes (this test fails on 2.3.9), and the prompt asks for UTF-8. **Research note:** this is the second prompt change since 2.3.0; runs are split by runner version. The suite passed **138 tests (1 skipped)** on Windows; `scripts/test_engine.py`: 525 passed, 14 skipped; maintenance tests passed.

**2.3.9 (2026-11-19, Windows 11):** Two fixes for `integrate` with plan contracts. (1) **Rebased evidence:** a `tested_revision` that the integration rebase rewrote counts as in HEAD's history when a commit with the identical stable patch ID is among the commits since the merge base (`git patch-id --stable`). In Garage on 19 Nov, the first integration after a branch consolidation rebased the slice, and its CLOSE evidence still named the pre-rebase commit. (2) **Repair can start:** when the gate hands a contract defect back as feedback, the pre-launch check no longer blocks the repair session that feedback asks for. Before, the 2.3.0 feedback path could never reach its repair session. Changed approved definitions still block. New tests: a rebased (cherry-picked) tested revision is accepted while an unrelated commit is rejected; gate contract feedback leads to a repair session and an accepted slice. Both tests fail on 2.3.8. The suite passed **136 tests (1 skipped)** on Windows; `scripts/test_engine.py`: 525 passed, 14 skipped; maintenance tests passed.

**2.3.8 (2026-11-19, Windows 11):** Plan-contract evidence digests now also match when the only difference is CRLF line endings. A Windows checkout with `core.autocrlf=true` stores CRLF on disk, while the recorded SHA-256 was taken from the committed LF content. In Garage on 19 Nov, `check` and `start` blocked on `QG-001.evidence[0].sha256 does not match` for an evidence file unchanged since it was recorded, and then on a second one. Any other difference still fails. New test: exact, CRLF-only and uppercase-digest matches pass; changed content fails with either line ending. Garage's real contract validates with the fix. The suite passed **134 tests (1 skipped)** on Windows; `scripts/test_engine.py`: 525 passed, 14 skipped; maintenance tests passed. This is the third CRLF case on Windows this week, after 2.3.6's leftover restore.

**2.3.7 (2026-11-19, macOS):** Publishing is serialised by a shared publish turn (the same kernel-locked first-come-first-served queue as the gate slots). A run holds the turn from rebasing onto the target through the quick check to the push, so another run cannot move the target underneath a passed check; a slice that needs its full gate again releases the turn first. In Medic8 on 18 Nov two lanes passed every quick check (about 23 minutes each under load) but the target moved during each one, and both exhausted their integration attempts. New test: a run whose gate passed waits in the turn queue while another run holds the turn, then publishes and leaves no ticket; without the turn the test fails. Commit 096ca83 carried this code but mislabelled the manifest as 2.3.5 (Windows 2.3.5 and 2.3.6 were published in parallel); this release corrects the number. The suite passed **133 tests (4 skipped)** on macOS.

**2.3.6 (2026-11-18, Windows 11):** Two Windows fixes. (1) **Line endings:** a tracked file whose only difference is CR/LF at line ends is restored instead of blocking the run as `agent left uncommitted changes` (event `eol_restored`). Only unstaged, unquoted modifications are considered, and only when `git diff --ignore-cr-at-eol` shows nothing. In Garage on 18 Nov, a menu file blocked the run while `git diff` was empty. (2) **Heartbeats:** the supervisor's 0.25 s heartbeat write to `result.json` is now best-effort on Windows. In Aqar on 18 Nov, one heartbeat replace denied for longer than the 8 s retry (WinError 5, probably antivirus under memory pressure) failed the job, and the Windows job object then killed the healthy agent. Start and terminal receipts still must succeed. New tests: a line-endings-only leftover is restored and the run completes (this test fails on 2.3.5); a real leftover change still blocks; a denied heartbeat returns instead of raising on Windows and still raises elsewhere; the worker loop uses only the best-effort write. The suite passed **132 tests (1 skipped)** on Windows.

**2.3.5 (2026-11-18, Windows 11):** Recovery no longer blocks on a plan contract that the interrupted local work left invalid. In Garage on 18 Nov, a session hit the Claude usage limit after naming an unstaged evidence file in the contract. After the wait, every recovery blocked with `Invalid plan contract` before the recovery session could start, and the watchdog's recoveries kept re-blocking for 2.5 h. The errors now go into the recovery prompt (event `contract_feedback`, stage `recovery`), and the gate re-checks the contract before anything is accepted. Changed approved definitions still block, as before. New tests: the recovery session repairs the contract and its slice is accepted (this test fails on 2.3.4), and changed definitions still block during recovery. The suite passed **127 tests (1 skipped)** on Windows; `scripts/test_engine.py`: 519 passed, 14 skipped; maintenance tests passed.

**2.3.4 (2026-11-18, macOS):** `integration_overlap_ignore` lists files that do not count as overlap after the target moved, so a clean rebase touching only rebuilt files or append-only shared lists uses the quick check instead of a full gate. In Medic8 a lane's slice passed its full gate five times without publishing, because each time the incoming commits touched generated API docs or shared translation files and forced another hour-long gate. New test: an ignored overlap uses the quick check and runs the full gate once; the same run without the list re-gates. The suite passed **125 tests (4 skipped)** on macOS.

**2.3.3 (2026-11-18, macOS):** Gate and integration slots are first come, first served. Each waiting run holds a kernel-locked ticket (`durable.Lease`) and takes a free slot only when no older live ticket exists; a ticket nobody holds is cleared once it is 5 seconds old. With polling alone, a Medic8 lane waited six hours overnight while other lanes took slots repeatedly. New test: a run does not take a free slot while an earlier live waiter exists, then clears a dead waiter's ticket and proceeds. The suite passed **124 tests (4 skipped)** on macOS; Windows is NOT_ASSESSED for this release (the ticket uses the same `durable.Lease` as the slots).

**2.3.2 (2026-11-17, Windows 11):** This combines the macOS 2.2.5 lane fix, which was published at the same time, with the Windows 2.3.0 and 2.3.1 changes. There is no new behaviour. Version 2.3.1 had been copied into projects before the two lines were merged, so this release gets its own number. On Windows 11 this tree passed **122 runner tests (1 skipped)**; `scripts/test_engine.py`: 519 passed, 14 skipped; maintenance tests passed.

**2.3.1 (2026-11-17, Windows 11):** The retry for a Windows sharing denial on receipt writes and reads goes from 8 tries (about 0.3 s) to 40 tries with capped backoff (about 8 s). If the final replace fails, the temporary file is removed. This was Garage's local patch `ec6a5278`: on 15 Nov a live agent job died because status watchers held `result.json` open (WinError 5). The receipt-read test now asserts the bounded budget. The suite passed **121 tests (1 skipped)** on Windows.

**2.3.0 (2026-11-17, Windows 11):** This release folds in runner fixes that two Windows project copies had made locally, so an upgrade no longer removes them. (1) `worktree_root` places the runner worktree outside `.git`. Claude Code refused every edit under `.git/auto-agents/worktrees`, which blocked Garage on 15 Nov and Aqar on 17 Nov with `agent made no commit`. The key is left out of the config digest, so a run can be moved with `git worktree move` and then `recover`. `check` warns when the worktree is inside `.git`. The default path is unchanged. (2) A failed agent session whose output shows the model API unreachable (`ENOTFOUND`, connection errors) waits `network_retry_seconds` and starts a fresh session, up to `max_network_retries`. (3) A push that the remote did not reject is retried, up to `max_publish_retries` within the deadline. A rejected push is not retried. Recovery after a failed push replays it only if the remote branch is an ancestor of the candidate. (4) An invalid plan-contract sidecar at a candidate becomes gate feedback instead of a block. (5) Detached jobs use a hidden console (`CREATE_NO_WINDOW`), so child consoles stop opening visible windows. (6) Plan-contract git calls allow 60 s instead of 5 s. New tests: network retry and its bound, unreachable-remote push retry, no retry of a rejected push, the `check` warning, validation of the new keys, worktree paths including lanes, and the digest staying compatible with earlier runs. The suite passed **121 tests (1 skipped)** on Windows. `scripts/test_engine.py`: 519 passed, 14 skipped. Maintenance tests: 7 passed. A live network outage and a live push outage on this release remain `NOT_ASSESSED`.

**2.2.5 (2026-11-17, macOS):** A lane commit whose identical patch is already on the moved target (`git cherry` marks it equivalent) counts as superseded even when later lane commits changed the same files again. Seen in Medic8 when a lane's starting plan commit had also been published separately. New test: the plan commit published separately, then edited by the lane, is accepted. The suite passed **111 tests (4 skipped)** on macOS.

**2.2.4 (2026-11-17, macOS):** An integration session may leave out a lane commit that the moved target already superseded: every file the commit changed was also changed upstream, and the integrated head keeps the upstream version of each (event `integration_superseded`). Seen twice in Medic8 when lanes fixed the same flaky timing test; 2.2.3 blocked the lane. Any other missing or renamed commit still blocks, and the full gate still runs after an integration session. New tests: a superseded commit is accepted, and a dropped commit blocks when upstream did not change its file or when the integrated file differs from upstream. The suite passed **110 tests (4 skipped)** on macOS.

**2.2.3 (2026-11-17, macOS):** Integration quick checks take a slot from their own pool (`integration_slots`, default 1) instead of the full-gate pool. In Medic8 with three gate slots, 5-minute quick checks waited 30 to 80 minutes behind full gates; the target moved during each wait and lane area-10 exhausted its integration attempts without publishing. New tests: a quick check starts while every gate slot is busy and respects STOP when its own pool is full; a lane run with `gate_slots: 1` publishes through the integration pool. The suite passed **107 tests (4 skipped)** on macOS.

**2.2.2 (2026-11-17, macOS):** A provider usage limit reported in Claude Code's wording ("You've hit your 5-hour limit · resets 7:10am (Africa/Kampala)") now waits instead of blocking the run. Earlier releases matched only the words "usage limit", so the first Medic8 main run and one lane blocked when the subscription limit was reached. The stated reset time plus two minutes sets the wait; `usage_wait_seconds` stays the ceiling and the fallback when no time can be read. New tests: the classifier (reset today, tomorrow, am/pm, unknown zone, rate limit, unrelated failure) and a driver run that waits on the CLI wording and then finishes. The suite passed **105 tests (4 skipped)** on macOS. A live reset was observed in Medic8 but the waiting path under a real limit is NOT_ASSESSED.

**2.2.1 (2026-11-17, macOS):** STOP that arrives while a job is prepared but not yet launched now drops that job and stops the run (`launch_withheld` event, state `stopped`) instead of blocking it with an unresolved operation; nothing ran, and a resumed run repeats the step. Found when the first five Medic8 lanes were stopped. An expired run budget still blocks as before. New test: STOP before a prepared gate, then a clean resume that publishes. The suite passed **98 tests (4 skipped)** on macOS.

**2.2.0 (2026-11-17, macOS):** parallel lanes. `tests/test_lanes.py` (14 tests) runs lanes against a local bare remote with a second clone that publishes during the gate: lane overlay, paths and name validation; lane branch and worktree; a disjoint upstream change rebased and accepted after the quick check with the full gate run once and no merge commits; an overlapping clean rebase that re-runs the full gate; a conflicting change resolved by the next session and re-gated; a fresh session that starts from the published target; the subject-preserving integration check; shared gate slots with a STOP-aware wait; and six crash or interruption windows an independent AI review found (rebase finished but not recorded, driver rebase interrupted, integration command committed before a crash, crash inside sync, integration session hit a usage limit mid-rebase, STOP while waiting for a slot). The full suite, merged with this copy's 2.1.1, passed **97 tests (4 skipped)** on macOS, Python 3.9.6. Not assessed: Windows, real multi-lane throughput, host resource limits and semantic conflicts between disjoint files.

**2.0.1 (2026-11-15, macOS):** `boot_identity()` returned nothing on macOS, so a partial gate receipt was never reused after a crash and `test_crash_after_gate_receipt_skips_only_that_exact_gate` failed (63 of 64). It now reads `sysctl -n kern.bootsessionuuid`, falling back to the parsed `kern.boottime`. Two new tests cover the parsing and fallback with a stubbed `sysctl` and check a stable live value on a Mac. The full suite passed **66 tests (3 skipped)** on macOS, Python 3.9.6. Behaviour across an actual Mac reboot: NOT_ASSESSED.

The final full runtime suite passed **64 tests in 218.268 seconds** after all runtime corrections. Release review extended text hash normalization to Windows CMD/BAT launchers, protected project-owned ENGINE.md, corrected PowerShell output/exit-code handling, and recomputed saved job-specification digests before inspection or execution. Prepared-spec input/timeout/login changes and terminal-spec drift are rejected; original job timeout and prompt remain authoritative on reattachment. Hashes detect inconsistent state, not an adversary able to rewrite both data and hashes. The suite covers both runner branches using fake agents; independent gates and publication guards; detached output and launcher exit; duplicate launch; Windows descendant termination; malformed state/receipt identity; live driver-process death and reattachment to the same gate; saved budget/limit wait; candidate and gate receipt crash windows; distinct agent/gate timeouts; final-only expensive gates; optional plan-contract validation; preflight; and launcher controls. Repository gate results are recorded in the owning engine's Kaizen report.

A specialist review found the prepared-job budget-expiry gap, mismatched receipt identity gap and STOP/CANCEL recovery ordering gap. Corrections preserve the job identity and stop barrier; none weaken permission, branch, revision or independent verification controls. Another observed Windows failure was transient replacement denial while a reader held a state file; retry is limited to that local write, never the underlying action.

An intermediate 56-test run exposed a final-gate failure and cleanup error. Investigation found that a brief observer-held job lease could make a starting worker exit as if another supervisor already owned the action. Startup now waits for that transient lease for at most five seconds and still respects an existing terminal receipt. The dedicated lease-contention regression and final-gate regression passed, followed by a 61-test pass and the final 64-test pass above. Failed intermediate runs are not counted as passes.

The watch is plain terminal text using the operator's terminal typography. It exposes meaning through labels and state, without color-only signals, decorative animation, a fabricated percentage or a made-up ETA. Task totals come from the optional sidecar and are explicitly reported metadata; verified revision and job liveness are separate. Legacy Markdown-only plans remain supported with unknown task totals.

## Remaining evidence boundaries

NOT_ASSESSED: actual power cut/reboot and storage durability; installed scheduled-task/logon authentication; a real multi-hour provider implementation; real five-hour/weekly exhaustion and reset; Linux service-manager crash containment; project-specific test adequacy; comparative retry/token/cost improvement; production deployment. Local-only recovery and replay safety are explicit project declarations, not enforcement of external-effect isolation. Missing evidence is not a pass.

## Historical evidence

# Evidence and second review: 2026-11-11

Scope: the local unattended driver and its use by Codex and Claude Code. The user-provided driver-pattern PDF is the baseline, not evidence that a real long-running run has succeeded. The local files by Nicosia, Volkhover, Bhati and the Claude Code guide were inventoried and text-extracted; targeted passages informed task decomposition, feedback loops, constraints and verification. Comprehensive review of all book content is NOT_ASSESSED. They are not evidence for current vendor capabilities.

Current, primary sources accessed 2026-11-11 (review when the CLI changes; page publication date not established):

- https://developers.openai.com/blog/codex-as-a-platform : `codex exec` is described as a noninteractive interface. Local `codex exec --help` also exposes it. Scope: CLI entrypoint, not proof of runtime permissions.
- https://code.claude.com/docs/en/troubleshooting : noninteractive permission behavior can differ by configuration. Scope: permission failure diagnosis, not an unconditional grant.
- https://developers.openai.com/api/docs/guides/agents-api/environments/security : agent-generated code can access the environment granted to it. Scope: the documented environment; a Git worktree alone is not a sandbox.
- https://developers.openai.com/api/docs/models and https://docs.anthropic.com/en/docs/about-claude/model-deprecations were inspected for model currency. Account/runtime model catalogue and comparable task-fit, cost, latency and quality evidence were not established. Model-currentness: NOT_ASSESSED. No model-policy change is proposed. The local model-policy checker reported drift; no automated repair was applied because the engine's medium-effort setting conflicts with the user's high-effort policy.

Second-review findings and disposition:

1. A committed DONE marker after a failed independent gate could otherwise be mistaken for successful completion after restart. The driver records the accepted and pending commits, and directs a fresh session to repair a failed gate without treating the completion marker as accepted. Regression: failed gate followed by restart and repair. Unknown unverified commits still block.
2. Windows can resolve an extensionless npm shim that CreateProcess cannot execute. Prefer `.cmd` on Windows; `codex.cmd --version` was exercised locally. Live Codex and Claude agent sessions remain NOT_ASSESSED.
3. Existing driver branches without an accepted checkpoint must not be silently treated as verified. The driver blocks for inspection.
4. The worktree is isolation from the operator's checkout, not a permission boundary. Publishing is configurable and disabled by default; the runtime's own policy remains in force. A non-force push and command exit statuses do not prove that the verification commands are adequate or that external side effects were absent.
5. Completion, failure, stop, lock, rate-limit retry, gate failure/restart/repair and publication to a disposable local remote were exercised by deterministic tests. Production safety, process-tree termination, real login/quota recovery, multi-hour runtime, cross-process resource isolation and application-level test coverage remain NOT_ASSESSED.

Measure for a future supervised pilot: completed slices, failed checks, blocked runs, unverified commits and independently reviewed regressions per run. The EWMA idea in the supplied pattern is a candidate; retry backoff is implemented but has no measured live-run benefit. Do not claim speed or safety improvements without a comparable baseline.

## Managed update review (2026-11-11)

A versioned manifest and managed updater preserve project configuration and plans, reject changed managed files and occupied new paths, and share the driver lock. An interrupted update retains a journal and requires inspection. A second pass found that raw hashes drift under Git CRLF conversion; the manifest now records its hash mode and normalises supported text line endings, while accepting the previous raw mode for migration. Tests cover modified targets, new-file collisions, removals, interrupted journals, locks and Git checkout behavior. Hashes detect accidental drift and do not authenticate a source. Process-crash atomicity across all files, adversarial concurrent writes and live-agent deployment remain NOT_ASSESSED.

## Follow-up review (2026-11-11)

A verification command could previously create a clean commit or change branches after the agent session, causing a different revision to be published or checkpointed. The driver now blocks if a verification command changes HEAD or the driver branch, and pushes the verified commit by object ID. Regression fixtures exercise both cases. Configuration also rejects non-finite runtime and retry limits. These checks do not constrain an adversarial concurrent process or establish that a configured verification command is meaningful.

Volkhover (2026), *Agentic Spec-Driven Development*, Korostyshevskiy (2026), *Claude Code: The Definitive Guide to Agentic Development*, and Bhati (2026), *Agentic AI in the Software Development Lifecycle*, inform the plan template: persistent outcomes, boundaries, acceptance examples, ordered slices, and a compact recovery handoff. The Bhati work is an under-review preprint; quantitative claims and vendor capabilities were not adopted as facts. The Claude Markdown edition omits reference tables; check original and current official documentation for CLI behaviour. The separate optimization anthology has not been read in full.

As of 2026-11-11, the official [Claude programmatic-use documentation](https://code.claude.com/docs/en/headless) supports the non-interactive CLI entry point; runtime permissions and live unattended use remain unassessed. The [OpenAI model catalogue](https://developers.openai.com/api/docs/models) and [Anthropic model overview](https://platform.claude.com/docs/en/models/overview) were consulted; task-fit, cost, latency and quality comparisons for this portfolio are NOT_ASSESSED. Retain the owner-authorised model policy; no model change is proposed.
