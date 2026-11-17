# Publication integration: 16 November 2026

The owner authorised commits and pushes to main after the earlier hold.
The incoming 2.0.1 macOS/BSD boot-identity fix and its two tests were retained
alongside the 2.1.1 owner-intent and receipt-read hardening. Documentation
conflicts retained both dated evidence records; no published history was rewritten.

The combined Windows suite ran **80 tests in 361.555 seconds**:
**79 passed, 1 skipped**. Command: `python -B -m unittest discover
-s auto-agents/tests`. The skipped test requires a real Mac; the stubbed macOS
parsing/fallback test passed. This is not fresh live macOS or reboot evidence.
Managed hashes verify and project config, PLAN.md and ENGINE.md remain unchanged.
The earlier suite counts below describe their pre-integration snapshots.

# Live owner intent and receipt reads: 16 November 2026

Release 2.1.1. The full Windows runtime suite passed **78 tests in 486.008
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

Release 2.1.0. The final full Windows runtime suite passed **68 tests in 310.926 seconds**, including the recovery-context regression accepted in independent review.
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

**2.2.2 (2026-11-17, macOS):** A provider usage limit reported in Claude Code's wording ("You've hit your 5-hour limit · resets 7:10am (Africa/Kampala)") now waits instead of blocking the run. Earlier releases matched only the words "usage limit", so the first Medic8 main run and one lane blocked when the subscription limit was reached. The stated reset time plus two minutes sets the wait; `usage_wait_seconds` stays the ceiling and the fallback when no time can be read. New tests: the classifier (reset today, tomorrow, am/pm, unknown zone, rate limit, unrelated failure) and a driver run that waits on the CLI wording and then finishes. The suite passed **105 tests (4 skipped)** on macOS. A live reset was observed in Medic8 but the waiting path under a real limit is NOT_ASSESSED.

**2.2.0 (2026-11-17, macOS):** parallel lanes. `tests/test_lanes.py` (14 tests) runs lanes against a local bare remote with a second clone that publishes during the gate: lane overlay, paths and name validation; lane branch and worktree; a disjoint upstream change rebased and accepted after the quick check with the full gate run once and no merge commits; an overlapping clean rebase that re-runs the full gate; a conflicting change resolved by the next session and re-gated; a fresh session that starts from the published target; the subject-preserving integration check; shared gate slots with a STOP-aware wait; and six crash or interruption windows an independent AI review found (rebase finished but not recorded, driver rebase interrupted, integration command committed before a crash, crash inside sync, integration session hit a usage limit mid-rebase, STOP while waiting for a slot). The full suite, merged with 2.1.1, passed **94 tests (4 skipped)** on macOS, Python 3.9.6. Not assessed: Windows, real multi-lane throughput, host resource limits and semantic conflicts between disjoint files.

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
