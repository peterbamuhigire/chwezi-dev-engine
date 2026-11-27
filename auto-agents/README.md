# Jidoka (JAD): unattended plan execution for Codex and Claude

**Jidoka** (自働化, "automation with a human touch") is the name of this runner, adopted by the owner on 20 November 2026; **JAD** is the *Jidoka Automated Development* tool. Like a Toyota Jidoka machine it works unattended but stops itself when it detects a defect and calls a person: a failed gate or review, or `STATUS: BLOCKED` (the *Andon*). Kaizen is the improving; Jidoka is the engine that does it unattended. Every new repository's auto runner is a Jidoka installation of this folder (`propagate.py <repo> --apply`). The folder, files and configuration keep the name `auto-agents` so installed copies keep working.

This is a project-local runner for Codex and Claude Code, sequential by default with optional parallel lanes. Each run uses fresh agent sessions, an isolated Git worktree, independently supervised verification jobs and durable recovery records. Model arguments come from the project configuration; the runner does not grant permissions or bypass the CLI's sandbox. A worktree and a prompt are not security boundaries.

## Current capabilities and evidence

Release **2.3.10**, checked on **17 November 2026**, provides:

- Separate agent-session, verification-job and overall run budgets, with expensive checks reserved for completion candidates when configured.
- Persisted job identity, verified revisions, quota-wait probes and recovery records. Reattach to a running check after observer failure; reconcile interrupted work under the declared replay policy.
- A descriptive watch with the current operation, gate, checkpoint age, wait/retry reason, logs and optional reported task counts.
- Optional parallel lanes: several runs of one repository, each with its own plan, state, worktree and branch, sharing a cap on concurrent gates and integrating onto the moved target branch before each push (see "Parallel lanes").
- Optional task-contract validation, separate Codex/Claude argument profiles, PowerShell/CMD launchers and a preview-first Windows logon-resume helper.

The 16 November Windows baseline ran **83 tests: 82 passed, 1 skipped**. It covered owner-intent drift, prepared/active recovery and receipt-read denial without replay. Dated checks of the current release are in [EVIDENCE.md](EVIDENCE.md); historical provider response smokes do not establish live lane acceptance. Actual power cuts, post-reboot authentication, live quota exhaustion/reset and multi-hour implementation remain `NOT_ASSESSED`. The logon-resume helper is supplied but not registered automatically.

The upstream 2.0.1 macOS/BSD boot-identity fix is retained: `sysctl` supplies `kern.bootsessionuuid`, falling back to `kern.boottime`. Its dated macOS test result is preserved in EVIDENCE.md; this integration is validated separately on Windows.

2.2.0 added parallel lanes; 2.2.1 corrected stop-before-launch handling, 2.2.2 recognised additional Claude usage-limit responses, 2.2.3 separated integration quick-check slots from full gates, 2.2.4 accepted lane commits that the moved target had already superseded, 2.2.5 also counted a lane commit as superseded when an identical patch was already upstream, 2.3.0 brought in fixes proven in installed project copies (`worktree_root`, network-failure and push retries, plan-contract repair feedback), 2.3.1 widened the Windows receipt sharing retry to about 8 s, and 2.3.2 combined the macOS 2.2.5 lane fix with these Windows changes. Dated platform results are in EVIDENCE.md. Fake-agent tests do not establish live multi-lane throughput or shared-service isolation.

## One-command launcher

From this `auto-agents` directory, run `./run.ps1` in PowerShell or `run.cmd` in Command Prompt. It checks readiness, starts the detached driver, then opens the watch. `./run.ps1 -Action Help` explains all controls; `-NoWatch` returns after startup. Neither launcher changes execution policy. Engine-specific checks and setup are in the project-owned `ENGINE.md` where supplied.

## Prepare a run

Commit the tools and a bounded plan under `docs/plans/` (or the existing configured plan path). Use [PLAN-TEMPLATE.md](PLAN-TEMPLATE.md) for stable tasks, dependencies, acceptance criteria and a compact handoff. Configure `auto-agents/config.json`; a generic installation must configure meaningful `verify` commands. These four engine copies include baseline verification profiles and a deliberately blocked setup plan; select a real owner-authorised plan before starting.

- `runner`: `codex` or `claude`; `runner_args`: fallback CLI arguments. Optional `runner_args_by_runner` selects separate argument lists for each provider, so Codex-specific flags never leak into Claude. Before launching Codex, check the model in the project profile against the active catalogue. The runtime passes the configured arguments to the CLI.
- `plan`: committed relative Markdown path. First line `STATUS: DONE` requests completion verification; `STATUS: BLOCKED - reason` records a blocker.
- `verify`: nonempty command argument arrays for checks appropriate to each slice.
- `final_verify`: optional command arrays run on completion candidates. Put an expensive full gate here when it is only needed at completion. For example, `["composer", "check"]` is one command array; confirm the actual project's command and safe test environment first.
- `plan_contract`: optional committed JSON sidecar, validated by `plan_contract.py`. It supplies task IDs, dependencies and evidence references for completion checks and watch output. It is not proof of semantic acceptance.
- `session_timeout_seconds`: maximum duration of one agent session. `verification_timeout_seconds`: separate gate timeout, defaulting to the configured run budget. A long check is never capped by the agent-session timeout.
- `max_hours` and `max_sessions`: finite run limits. The saved deadline survives an interrupted driver; restarting does not silently renew it. A changed owner plan is not silently substituted into saved work. Verification also respects the remaining run budget.
- `max_gate_failures`: bounded repair attempts (default 3). Failed independent checks feed a bounded diagnostic tail to the next agent. An invalid plan-contract sidecar at a candidate counts as one such failure, and its errors become repair feedback. The same applies when an interrupted session (for example one stopped by a usage limit) left the sidecar invalid: the recovery session gets the errors to repair instead of the run blocking before it starts. Changed approved definitions, or `STATUS: DONE` over incomplete tasks, still block.
- `max_rate_retries`: bounded limit probes (default 3). Rate waits use `initial_backoff_seconds` and `max_backoff_seconds`. `usage_wait_seconds` defaults to 18000 seconds for a conservative five-hour probe; this is configurable and is **not** a claim about the account's reset time. The overall deadline still applies.
- `max_network_retries` (default 24) and `network_retry_seconds` (default 300): an agent session that fails because the model API is unreachable (DNS or connection errors such as `ENOTFOUND`) does not block. The driver pauses, then starts a fresh session on the same worktree. The count resets after each accepted slice.
- `worktree_root`: where the runner worktree lives, absolute or relative to the repository root, for example `"../<repo>-autorun"`. Without it the worktree stays at `.git/auto-agents/worktrees/<runner>`, which is compatible with earlier releases. **Set it for Claude Code:** Claude Code refuses every edit under `.git`, so sessions there end without commits; `check` warns about this. The key only relocates files and is left out of the run's configuration digest. An unfinished run can therefore be moved with `git worktree move <old> <new>` followed by `recover`. Lanes use `lane-<lane>-<runner>` under the same root. **Codex on Windows:** a linked worktree keeps its Git metadata in the main checkout's `.git`, which Codex's `workspace-write` sandbox keeps read-only even when listed as a writable root or with `--approve-for-me` (measured 21 Nov 2026, codex-cli 0.171.0). The agent's `git commit` then fails on `index.lock` and the run stops with "agent left uncommitted changes". On a PC where the owner accepts it, put `"--sandbox", "danger-full-access"` in `runner_args_by_runner.codex`; the runner itself never adds it.
- `skills`: `on-demand` (default from 2.4.0) or `preload`. On demand, each agent session starts without the host's plugin skill catalogues: Claude Code gets `--settings <status dir>/skills-on-demand.claude.json`, Codex gets `-p chwezi-runner-on-demand` (`$CODEX_HOME/chwezi-runner-on-demand.config.toml`). Both files switch off every plugin the host has enabled; they are rewritten from the host settings whenever a run starts or resumes, and the argument names only the file, so a reattached job keeps its identity. The prompt tells the agent to find skills with `python auto-agents/find_skill.py "<task words>"`, which searches only the canonical skill folders of the Development, Writing, orchestrator (`chwezi-engine-agents`), Accounting Doctrine and Knowledge Bank engines (siblings of the repository's main checkout, or `CHWEZI_ENGINES_ROOT`), then read the engine router and the one `SKILL.md` it names. Global and project `CLAUDE.md`/`AGENTS.md` still load. Your own `--settings` or `-p` in the runner arguments come later and win. Measured on 19 Nov 2026 (Claude Code 2.1.327, seven plugins enabled, 285 skills): start-up context fell from 36,216 to 30,050 tokens per request; Codex (codex-cli 0.170.0) went from 165 listed skills and 25,500 input tokens to 11 skills and 18,792. Use `preload` only when a plan depends on a plugin's slash commands or hooks.
- `subagents`: `economy` (default from 2.5.0) or `inherit`. In economy mode each Claude Code session gets `--agents <status dir>/subagents-economy.claude.json`, which defines a read-only Explore subagent (Read, Grep, Glob) on Haiku, the cheapest model class (class map: Development engine `docs/operations/model-routing.json`). The prompt gains one line: delegate searches that would take more than a few lookups across many files to Explore, and keep judgement, edits and verification in the main session. The `--agents` definition outranks user and project subagents, so a new repository or another PC gets the same routing without any per-user file. The main session model, permissions and billing are unchanged. Codex gets nothing (no equivalent). Before 2.5.0, Explore inherited the session model: 42 Explore calls on this PC before 20 Nov 2026, 41 of them on Opus, cost an estimated USD 66.56 at list price (median 33 requests per call). Use `inherit` to opt out.
- `recovery_policy`: `manual` (default) or explicitly declared `local-only`. The latter allows a fresh agent to inspect and reconcile partial local edits after interruption. It does not prove that external effects are absent or restrict host permissions. Use it only for tasks whose effects are confined to the authorised local workspace/test resources.
- `verification_replay_safe`: false by default. Set true only for checks safe to repeat after an interrupted supervisor; `max_recovery_attempts` bounds replays (default 2).
- `publish`: false by default. If explicitly authorised, a regular non-force push sends the verified commit to `remote` / `target_branch`. Without `integrate`, a moved target requires reconciliation. A push that fails without being rejected by the remote (a network or DNS outage) is retried every `publish_retry_seconds` (default 300), up to `max_publish_retries` (default 72) within the run deadline. A recovery after a failed push replays it only when the remote branch is still the candidate or one of its ancestors. With explicitly configured `integrate: true`, the bounded rebase and re-verification rules under "Parallel lanes" apply. Force push is not used; uncertain publication requires reconciliation.
- `login_mode`: `plan` removes OPENAI_API_KEY, ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN from the agent environment; `inherit` keeps them. Other credentials remain unchanged. Verify actual login/billing mode separately.

Do not run another orchestrator against the same worktree or shared test resources. Isolate databases and other services across concurrent repositories. Missing executables and invalid contracts fail before a model call; project-specific service/auth readiness still belongs in the plan.

## Preserve the approved task definitions

When `plan_contract` is configured, both the Markdown plan and JSON sidecar must
be committed and clean in the owner checkout. The run records the sidecar's Git
blob and a canonical fingerprint of task IDs, titles, dependencies, write scopes
and acceptance specifications. Worker changes to those definitions block before
the candidate is accepted. Updates to task state and evidence remain permitted;
list ordering alone does not change the definitions.

The runner rechecks the owner plan and sidecar before each new operation and
after receiving its result, including before accepting a candidate. Uncommitted
edits, deletion or a different committed blob block further work. Unrelated
owner-checkout edits do not block the run. These checks happen at operation
boundaries; they do not cancel an already running job or detect a change that is
made and restored between checks. Use `cancel` when the current job must stop.

Changing the owner sidecar during an unfinished run also blocks and preserves
recovery evidence. Reconcile the existing operation, record the owner's decision and
re-baseline through a deliberate new run; do not delete state or silently adopt
a changed criterion. Without a sidecar this extra definition check is unavailable.

This is a drift check, not a security boundary or proof that the tests are good.
The executor may have permission to edit test files, the Markdown plan or tools;
review the real diff and verification configuration for weakened oracles and
unauthorised effects. Actual permissions and independent review still govern.

## Parallel lanes

A lane is an independent run of the same repository. Create `auto-agents/lanes/<lane>.json` with only the keys that differ from `config.json` (normally `plan`), commit a separate plan for it, then use `--lane <lane>` with any action (`check`, `start`, `run`, `watch`, `status`, `stop`, `cancel`, `resume`, `recover`). Lane state lives in `auto-agents/lanes/<lane>/` under the Git common directory; its branch is `auto-agents/lane-<lane>-<runner>`. Give lanes disjoint work: separate plans, registers and test databases. Two runs of the same lane are refused.

Settings, normally in `config.json` so every lane and the default run share them:

- `integrate: true` (needs `publish`): before a fresh agent session the lane fast-forwards to the published target; before each push it fetches the target and, when the target moved, rebases the verified commits onto it. A conflict is handed to the next agent session, which may rebase only onto the fetched revision and must keep every lane commit (checked by subject). A rejected push (another lane published first) integrates again. `max_integration_attempts` (default 6) bounds attempts per slice.
- `integration_commands`: project commands run after a clean rebase, for example regenerating generated files and committing the result. They must leave a clean tree and must not rewrite history.
- `integration_verify`: a quick check. It replaces the full gate only when the rebase was clean, no integration command made a commit, and the incoming changes touch none of the lane's files. Otherwise the full gate runs again on the integrated revision. Semantic interference through disjoint files is possible; later gates and any full scans remain the safeguard, so keep a broad final gate.
- `gate_slots`: the most full verification jobs that run at once across all lanes of the repository; `gate_slot_poll_seconds` (default 10) sets the wait poll. Waiting runs are served first come, first served (a kernel-locked ticket per waiter; a ticket nobody holds is cleared). A lane waiting for a slot shows `WAITING_GATE`.
- `integration_slots` (default 1 when `gate_slots` is set; 0 removes the cap): the most integration quick checks (`integration_verify`) that run at once. They have their own pool so a short check never waits behind full gates while the target keeps moving.
- `integration_overlap_ignore` (fnmatch globs, default none): files that do not count as overlap when the target moved, so a clean rebase can still use the quick check. Use it for files the integration commands rebuild and for append-only shared lists the project merges line by line.
- Publishing takes one shared **publish turn** (first come, first served) when `integrate` is on: the run rebases onto the target, runs the quick check and pushes while holding it, so the target cannot move underneath a passed check. A slice that needs its full gate again releases the turn first. Full gates still run in parallel.

## Research metrics (every PC that runs the runner)

Runner and interactive sessions on each PC feed the private research repository for agentic AI software development [chwezi-agentic-research](https://github.com/peterbamuhigire/chwezi-agentic-research): token economy, iterations, gate results and defect escape. It also holds the pre-registered model-routing experiments, such as A6 (Explore on Haiku).

On each PC, clone it next to the engines (normally `C:\wamp64\www\chwezi-agentic-research`), run `scripts\daily-collect.ps1` once, then `scripts\daily-collect.ps1 -Register`.

Each night the task pulls, collects this PC's data and pushes content-free daily shards. It then rebuilds the shared results from every PC's data and pushes them. Each PC's raw transcripts and full metrics database stay on that PC. The PC used for writing the paper only pulls.

`check` prints a `RESEARCH:` line with the clone found, its remote and whether the nightly task is registered. This line is informational and never blocks a run. Point it at a clone elsewhere with `CHWEZI_RESEARCH_REPO`.

## Run and observe

```powershell
python auto-agents/driver.py start       # hidden detached driver, returns promptly
python auto-agents/driver.py watch       # descriptive refresh; Ctrl+C only closes watch
python auto-agents/driver.py status      # one snapshot
python auto-agents/driver.py stop        # finish current operation, then stop
python auto-agents/driver.py cancel      # persist stop and cancel the current job
python auto-agents/driver.py resume      # reattach unfinished work; respects terminal/stop state
python auto-agents/driver.py recover     # deliberate local reconciliation and budget renewal
```

A run always ends `done` once its plan is finished. If it blocked or stopped and the owner then finished the plan on the target branch (committed `STATUS: DONE`, a completion-ready contract, every runner commit already merged and a clean worktree), the next `resume`, `run` or `start` marks it `done` with `closed_by: owner` and keeps the original block reason. Runner gates do not run on the owner's commits. In any other case the run stays as it was.

Host sleep is not run time. A job's timeout counts only the time the host was awake: a gap of more than 30 seconds between the supervisor's quarter-second ticks is recorded as `suspended_seconds`, and the run deadline is extended by it. On Windows the supervisor also asks the system not to idle-sleep while a job runs; a closed lid or the power button still sleeps it. A gate that still times out across a sleep is replayed when `verification_replay_safe` is true.

A gate cut short by the run budget (its configured limit was longer than the budget left) stops the run on its budget instead of blocking it, when `verification_replay_safe` is true; `recover` replays that gate. Likewise, under `recovery_policy: local-only`, an agent session cut short by the run budget stops the run, keeps its partial work, and `recover` starts a reconcile session. The owner checkout may be pulled during a run: when it only catches up with the run's own published commits (its HEAD is an ancestor of the worktree HEAD), the changed plan or contract blob is accepted and logged as `owner_checkout_followed`. An owner commit the run does not hold still blocks.

`run` executes in the foreground and is useful for controlled tests. `start` confirms process launch, not readiness or success: inspect status and `launcher.log`. `recover` requires the saved local-only policy, unchanged configuration and safe replay for interrupted verification. It never resets or deletes partial edits. Read [RECOVERY.md](RECOVERY.md) before configuring restart automation.

Status lives under the repository's Git common directory in `auto-agents/`. The watch names the plan/worktree, reported task states when configured, independently verified revision, current gate, job heartbeat, last output, retries/wait time, budget and log. A heartbeat proves liveness, not progress or acceptance. Unknown task totals and provider reset times remain unknown.

## Recovery boundaries

The driver writes intent before starting a job. Each detached job has a unique identity, kernel lock, flushed state/receipt and streaming output file. Losing the calling shell or observer does not start another copy. On Windows, the dedicated supervisor joins a kill-on-close Job Object before spawning work; failure to establish containment fails before execution. A dead observer can reconnect to the same running gate. A dead supervisor yields an interrupted outcome, never a pass. Finished gate receipts are reused only for the same revision/configuration and stage. A changed or unavailable boot identity invalidates earlier partial gate reuse unless safe replay was declared. Project checks must still establish service/data freshness; boot identity is not that proof.

Power loss stops processes. The persisted journal supports reconciliation after restart; [register-resume.ps1](register-resume.ps1) can configure a current-user logon/periodic resume task through an explicit preview/apply workflow. It is not installed automatically. Before-login recovery and unavailable user authentication are not promised. Physical power-loss durability and actual reboot/authentication acceptance require separate machine-level tests.

An explicit stop/cancel survives restarts. Corrupt or mismatched state, unexpected branch/history changes, unresolved external effects and unsafe replay block. Legacy PID-only lock files require inspection; new kernel locks recover after process death without trusting a reused PID. Logs and prompt files can contain sensitive project material; retain them within the project's access and retention controls.

On POSIX, normal timeout/cancel uses process-group cleanup; abrupt supervisor SIGKILL cannot guarantee descendant cleanup without a host service manager. Windows and POSIX evidence must not be conflated.

## Validate and update

```powershell
python -B -m unittest discover -s auto-agents/tests
```

Tests use disposable Git repositories and fake agents. [EVIDENCE.md](EVIDENCE.md) distinguishes those checks from live provider and machine recovery evidence. The driver does not certify test semantics, exact-once external effects, token savings or production readiness.

The owning engine's repository instructions identify its canonical source. After reviewed changes, regenerate the manifest with `python auto-agents/release.py --version <version>` and `--add <file>` for new managed files. Preview `python auto-agents/propagate.py <repo-root>...`, inspect the result, then apply with `--apply`. Alternatively use a project's `upgrade.py --source <trusted-auto-agents-directory>` and `--apply`. Configuration, project plans, ENGINE.md and runtime state remain project-owned.

The updater preserves local edits, refuses occupied new paths and running/interrupted update locks, and leaves an update journal for inspection on interruption. It does not force recovery or silently overwrite drift. Manifest hashes detect drift; they are not signatures. Limit propagation to the authorised repositories and report actual results. Host plugin-cache activation and trust review are separate from source changes.
