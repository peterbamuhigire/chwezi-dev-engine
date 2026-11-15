# Unattended plan execution for Codex and Claude

This is a sequential, project-local runner for Codex and Claude Code. It uses fresh agent sessions, an isolated Git worktree, independently supervised verification jobs and durable recovery records. Model arguments come from the project configuration; the runner does not grant permissions or bypass the CLI's sandbox. A worktree and a prompt are not security boundaries.

## Current capabilities and evidence

Release **2.0.1**, checked on **15 November 2026**, provides:

- Separate agent-session, verification-job and overall run budgets, with expensive checks reserved for completion candidates when configured.
- Persisted job identity, verified revisions, quota-wait probes and recovery records. Reattach to a running check after observer failure; reconcile interrupted work under the declared replay policy.
- A descriptive watch with the current operation, gate, checkpoint age, wait/retry reason, logs and optional reported task counts.
- Optional task-contract validation, separate Codex/Claude argument profiles, PowerShell/CMD launchers and a preview-first Windows logon-resume helper.

The shared runtime passed **64 tests** on Windows (2.0.0) and **66 tests** on macOS with Python 3.9.6 (2.0.1, three platform-specific skips). Boot identity comes from `/proc` on Linux, PowerShell on Windows and `sysctl` (`kern.bootsessionuuid`, else `kern.boottime`) on macOS and BSD. Both installed provider CLIs passed bounded response smokes. Actual power cuts, post-reboot authentication, live quota exhaustion/reset and multi-hour implementation remain `NOT_ASSESSED`; see [EVIDENCE.md](EVIDENCE.md). The logon-resume helper is supplied but not registered automatically.

## One-command launcher

From this `auto-agents` directory, run `./run.ps1` in PowerShell or `run.cmd` in Command Prompt. It checks readiness, starts the detached driver, then opens the watch. `./run.ps1 -Action Help` explains all controls; `-NoWatch` returns after startup. Neither launcher changes execution policy. Engine-specific checks and setup are in the project-owned `ENGINE.md` where supplied.

## Prepare a run

Commit the tools and a bounded plan under `docs/plans/` (or the existing configured plan path). Use [PLAN-TEMPLATE.md](PLAN-TEMPLATE.md) for stable tasks, dependencies, acceptance criteria and a compact handoff. Configure `auto-agents/config.json`; a generic installation must configure meaningful `verify` commands. These four engine copies include baseline verification profiles and a deliberately blocked setup plan; select a real owner-authorised plan before starting.

- `runner`: `codex` or `claude`; `runner_args`: fallback CLI arguments. Optional `runner_args_by_runner` selects separate argument lists for each provider, so Codex-specific flags never leak into Claude. The engine profiles pin newly started Codex runs to the owner's Luna/medium default; the runtime code itself does not select a model.
- `plan`: committed relative Markdown path. First line `STATUS: DONE` requests completion verification; `STATUS: BLOCKED - reason` records a blocker.
- `verify`: nonempty command argument arrays for checks appropriate to each slice.
- `final_verify`: optional command arrays run on completion candidates. Put an expensive full gate here when it is only needed at completion. For example, `["composer", "check"]` is one command array; confirm the actual project's command and safe test environment first.
- `plan_contract`: optional committed JSON sidecar, validated by `plan_contract.py`. It supplies task IDs, dependencies and evidence references for completion checks and watch output. It is not proof of semantic acceptance.
- `session_timeout_seconds`: maximum duration of one agent session. `verification_timeout_seconds`: separate gate timeout, defaulting to the configured run budget. A long check is never capped by the agent-session timeout.
- `max_hours` and `max_sessions`: finite run limits. The saved deadline survives an interrupted driver; restarting does not silently renew it. A changed owner plan is not silently substituted into saved work. Verification also respects the remaining run budget.
- `max_gate_failures`: bounded repair attempts (default 3). Failed independent checks feed a bounded diagnostic tail to the next agent.
- `max_rate_retries`: bounded limit probes (default 3). Rate waits use `initial_backoff_seconds` and `max_backoff_seconds`. `usage_wait_seconds` defaults to 18000 seconds for a conservative five-hour probe; this is configurable and is **not** a claim about the account's reset time. The overall deadline still applies.
- `recovery_policy`: `manual` (default) or explicitly declared `local-only`. The latter allows a fresh agent to inspect and reconcile partial local edits after interruption. It does not prove that external effects are absent or restrict host permissions. Use it only for tasks whose effects are confined to the authorised local workspace/test resources.
- `verification_replay_safe`: false by default. Set true only for checks safe to repeat after an interrupted supervisor; `max_recovery_attempts` bounds replays (default 2).
- `publish`: false by default. If explicitly authorised, a regular non-force push sends the exact verified commit to `remote` / `target_branch`. No automatic merge, rebase or force push occurs. An uncertain publication requires reconciliation.
- `login_mode`: `plan` removes OPENAI_API_KEY, ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN from the agent environment; `inherit` keeps them. Other credentials remain unchanged. Verify actual login/billing mode separately.

Do not run another orchestrator against the same worktree or shared test resources. Isolate databases and other services across concurrent repositories. Missing executables and invalid contracts fail before a model call; project-specific service/auth readiness still belongs in the plan.

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
