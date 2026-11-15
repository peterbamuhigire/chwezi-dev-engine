# Auto-Agents recovery and logon resume

This note describes the local sequential driver and the optional Windows resume
task. The task is a convenience for reconnecting to an authorised run after a
logon or interrupted driver process; it does not grant authority, change runner
permissions, select a model, or make the worktree a sandbox.

## Windows logon resume task

From an unelevated, interactive PowerShell session in this repository, preview
the task definition:

```powershell
./auto-agents/register-resume.ps1
```

The default is preview only. After reviewing the current-user task name, repo
identity and settings, register or update only that task with:

```powershell
./auto-agents/register-resume.ps1 -Apply
```

Preview removal, then apply it only after the displayed task passes the
ownership check:

```powershell
./auto-agents/register-resume.ps1 -Remove
./auto-agents/register-resume.ps1 -Remove -Apply
```

The task identity is a deterministic hash of the resolved repository path and
current user SID. An occupied name with a different ownership marker, action,
principal or trigger definition is a collision; the script refuses to replace
or remove it. A valid owned task may be updated when the Python executable
changes. No task is created by preview, `-WhatIf`, or these instructions.
If the repository was moved, the current script can preview/remove its old task
using `-Remove -RepositoryRoot <former-absolute-repository-path>`. It validates
the former deterministic identity and expected action shape without requiring
the old driver files to remain on disk.

Each scheduled `-Run` invocation writes Python stdout and stderr separately to
`<Git-common-dir>/auto-agents/scheduler-resume.stdout.log` and
`scheduler-resume.stderr.log`. These are bounded latest-invocation logs: each
run replaces the prior files; they are not a run history. The launcher waits
for Python and returns its actual exit code, so a startup/configuration failure
before journal creation remains inspectable even though the scheduled window is
hidden. Log paths are resolved through `git rev-parse --git-common-dir`, so
linked worktrees share the repository's runtime log location.

The task has an at-logon trigger for the current user and a five-minute
repeating probe. It invokes `driver.py resume`, not `run` or `recover`. It uses
the current user's interactive token, `RunLevel=Limited`, a hidden PowerShell
action, `IgnoreNew` for overlapping task instances, and no Task Scheduler
execution time limit. The driver retains its own configured `max_hours` budget.
The Python path is resolved to an absolute `.exe`, rejects Windows app execution
aliases, checks for Python 3.9 or later and invokes the driver's read-only
`--help` in isolated/no-bytecode mode. It is passed with the absolute driver
path and repo working directory. The script neither requests a password nor
elevates.

An interactive logon trigger runs only after the user has logged in; this is not
a boot trigger and does not resume before login. It cannot supply credentials,
runner sessions, network access or encrypted-file access that are unavailable
to the logged-in user. Login, execution-policy, task-service and real host
behavior require local verification. No task registration or reboot test is
performed as part of this change.

## Driver commands

Run commands from the repository root. Runtime files live in the Git common
directory's `auto-agents/` folder, shared by both runners. Run, resume, recover
and start require a valid committed plan plus a configured runner and at least
one verification command. Generic copies with empty checks cannot execute;
the engine profiles include checks and a deliberately blocked setup plan.

| Command | Behavior |
| --- | --- |
| `python auto-agents/driver.py start` | Starts a detached supervisor that invokes `run`; inspect its launcher log and status. |
| `python auto-agents/driver.py run` | Starts a configured run or continues its nonterminal journal. An unresolved saved operation can block it. |
| `python auto-agents/driver.py resume` | Reattaches only to an existing nonterminal run. No run or a terminal `done`, `stopped` or `blocked` state is a no-op. It never clears stop/cancel markers. |
| `python auto-agents/driver.py recover` | Explicitly requests bounded recovery under the configured policy; it does not authorize uncertain external effects. See below. |
| `python auto-agents/driver.py status` | Prints a one-time status summary, including supervisor/job state and available log evidence. |
| `python auto-agents/driver.py watch` | Refreshes the status summary; `--once` prints one snapshot and exits. Closing the watcher does not stop the run. |
| `python auto-agents/driver.py stop` | Writes `STOP`. The current agent/check command may finish; the driver stops at its next loop boundary. |
| `python auto-agents/driver.py cancel` | Writes `STOP` and `CANCEL`; the active local worker is asked to terminate. This leaves a cancelled/blocked operation for inspection. |

The scheduled task calls only `resume`. It does not clear `STOP` or `CANCEL`,
start a terminal run, or make the deliberate `recover` decision. Task Scheduler's
`IgnoreNew` policy and the driver's OS-owned `run.mutex` prevent overlapping
driver instances; each detached job also holds its own kernel lease. Lock files
are persistent lease paths: do not delete a lock file to force a restart.

## Receipts, checkpoints and recovery rules

The detached job supervisor writes a command/configuration digest in
`jobs/<job-id>/spec.json`, state and exit receipt in `result.json`, combined
child output in `output.log`, and supervisor diagnostics in `supervisor.log`.
The driver journal, operation pointer, event trail and verified revision
checkpoint are separate durable records. `status`/`watch` report observed state;
a heartbeat is liveness evidence, not proof of accepted progress or successful
completion.

The OS releases a kernel lease when its owning process exits. A process that
dies without a terminal receipt is reported as interrupted. Reattaching to a
prepared job may launch it once; a job with an existing running or terminal
receipt is not launched again under that same job identity. Preserve its
receipt, logs and worktree for reconciliation. Do not delete receipts, reset a
branch, or replay an operation merely to obtain a green result.

`recovery_policy` defaults to `manual`. Under manual policy, inspect the status,
job receipt/log, current worktree diff and relevant external system before
deciding the disposition. The driver does not infer that an external effect did
not happen from an unchanged Git tree. If completion or side effects are
uncertain, keep the run blocked and resolve that uncertainty through the owning
system before any new attempt. Do not switch to `local-only` to bypass that
decision.

`recovery_policy: local-only` is an explicit project/operator declaration that
interrupted work may be reconciled locally using the existing plan and safe
test resources. It is a prompt and replay policy, not a sandbox or technical
proof that the agent made no external call. Use it only for isolated local work
whose authorized operations are safe to inspect and repeat. Dirty local changes
may be preserved for a fresh reconciliation session; the driver does not reset
or delete them. An external side effect that may have occurred is not eligible
for local-only recovery and requires manual reconciliation. The driver cannot
prove its absence from Git state.

`recover` is a deliberate operator action. It requires the saved configuration
to match and the saved run not to be complete. It refuses an active saved job,
an interrupted publication, a changed branch/history, and interrupted
verification unless `verification_replay_safe: true`. It renews the configured
`max_hours` budget, records an operator-recovery event, and only then removes
`STOP`/`CANCEL`. A renewed budget is not an extension of the old deadline by
accident; normal `resume` keeps the original persisted deadline. No recovery
claim covers external effects merely because the operation kind is `agent`.

`verification_replay_safe` defaults to false. Set it true only when the exact
configured verification commands are safe to repeat after interruption; the
runtime also bounds automatic replay attempts with `max_recovery_attempts`.
This setting does not make agent actions, publications, or all test commands
safe to replay.

`usage_wait_seconds` is the delay before a scheduled usage-limit probe. It is
not evidence that the provider reset the limit. The driver records the next
probe time as unconfirmed, checks the unchanged local state before rate-limit
retry, and remains bounded by `max_rate_retries` and the run deadline. A
five-minute scheduled `resume` may reconnect to the existing wait; it does not
confirm service availability.

An unfinished run reuses its recorded `max_hours` deadline after a crash or
restart. The scheduled task has no independent finite execution cap that would
cut it off at Task Scheduler's default limit; the driver's session timeout and
run deadline remain authoritative. A terminal stopped/blocked run is not
silently restarted by the task. Use `status`, reconcile the evidence and choose
`recover` or a new run deliberately.

## Windows evidence and limits

The following Microsoft documentation was checked on 2026-11-15. It supports
the Task Scheduler semantics used here; it does not replace a real host test.

- [Logon trigger](https://learn.microsoft.com/en-us/windows/win32/taskschd/logontrigger): fires when the user logs on.
- [Principal logon type](https://learn.microsoft.com/en-us/windows/win32/taskschd/principal-logontype): interactive-token tasks require the user to be logged on.
- [Repetition duration](https://learn.microsoft.com/en-us/windows/win32/taskschd/repetitionpattern-duration): an omitted duration repeats indefinitely; any specified duration requires an interval.
- [Execution time limit](https://learn.microsoft.com/en-us/windows/win32/taskschd/tasksettings-executiontimelimit): `PT0S` permits an indefinite task duration; Task Scheduler otherwise defaults to 72 hours.
- [PowerShell scheduled-task trigger](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasktrigger?view=windowsserver2025-ps): the available logon, once, and repetition parameters.

The task deliberately does not use a boot trigger. Microsoft documents boot
triggers separately and requires elevated registration for that trigger; this
task is user-scoped and limited-privilege. See [boot trigger](https://learn.microsoft.com/en-us/windows/win32/taskschd/boottrigger).

**Evidence state (2026-11-15):** On Windows PowerShell 5.1.26100.9818, AST
parsing, default registration preview, `-Apply -WhatIf`, removal preview,
former-root removal preview, and in-memory owner/collision checks passed. A
disposable Git fixture with an empty verification config exercised `-Run`:
Python exited 2 before journal creation, the same exit code was returned, and
the configuration error appeared in the durable stderr log. This checks the
launcher and capture path, not live scheduler behavior. Earlier Task Scheduler
query confirmed no task was registered. Actual task registration/removal,
logon behavior, power-loss recovery, authentication, long-running task survival
and cleanup remain `NOT_ASSESSED` until tested on an authorized Windows lab
host. Do not claim unattended-before-login operation or live recovery from
these checks.
