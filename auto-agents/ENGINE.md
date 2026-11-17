# chwezi-dev-engine: Kaizen autorun

From this `auto-agents` directory, run `./run.ps1` (PowerShell) or `run.cmd` (Command Prompt). The launcher checks configuration, starts a hidden driver and opens the watch. Closing the watch does not stop the driver.

## Configure the authorised plan

Choose only ready tasks. Check write ownership, migrations and integration capacity before starting concurrent slices.

If work can overlap, choose disjoint owners and identify the first shared acceptance check. If an upstream input changes, identify the dependent results that require revalidation before resuming.

See [Sadhu and Konar, chapter 4](https://doi.org/10.1002/9781119699057.ch4) on individual and joint success and [Graham (1966)](https://doi.org/10.1002/j.1538-7305.1966.tb01709.x) on scheduling with precedence constraints.

1. Write/review a bounded Kaizen plan in `docs/plans/`, with task IDs, dependencies, write ownership, acceptance criteria and recovery notes. Commit it and the required tools. The setup PLAN.md deliberately blocks execution until a real plan is selected.
2. Set `plan` in `config.json` to that repository-relative path. Optionally set `plan_contract` to the matching JSON sidecar. Keep one authoritative task graph; do not hand-maintain two conflicting manifests.
3. Choose `runner`: `codex` or `claude`. Provider-specific arguments are in `runner_args_by_runner`. Codex defaults to the owner's GPT-6.2 Sol/medium pin for newly launched sessions; Claude retains its own configured model. This does not change this interactive session or global CLI settings.
4. Confirm Sol/medium in the host catalogue. If unavailable, configure the approved Terra/medium fallback and report it. If neither is available, stop before launch. Check login and the test environment, then run `./run.ps1 -Action Check`. This is read-only and makes no model call. Inspect any blocked reason before starting.

## Engine verification profile

Per-slice checks:
- `python -B -X utf8 scripts/skill_catalog_guardrails.py`

Completion-candidate checks:
- `python -B -X utf8 -m pytest tests -q -p no:cacheprovider`
- `python -B -m unittest discover -s auto-agents/tests`

These are engine-wide baseline gates, not substitutes for the plan's behaviour-specific tests. Add those tests to the plan and configuration. A nonzero, missing or interrupted check remains a failure or NOT_ASSESSED; no gate is skipped to obtain a green result.

This local-only profile is for source changes and disposable validation. It enables reconciliation of partial local work and safe replay of those checks after interruption. Before adding a migration, deployment, remote write, non-disposable fixture or other external effect, change the replay policy and provide its reconciliation contract. A worktree/prompt does not enforce isolation.

The run budget is 24 hours; agent sessions are capped separately at 3 hours and a verification job at 4 hours, subject to the remaining run budget. Adjust these finite limits to the real plan. Usage-limit probes default to five hours, which is not a guaranteed provider reset. `publish` remains false.

## Daily controls

- `./run.ps1 -Action Watch`: descriptive progress.
- `./run.ps1 -Action Status`: machine-readable status snapshot.
- `./run.ps1 -Action Stop`: finish the current operation, then stop.
- `./run.ps1 -Action Cancel`: stop and request cancellation of the active job.
- `./run.ps1 -Action Resume`: reconcile an unfinished run without clearing stop intent.
- `./run.ps1 -Action Recover`: deliberate local reconciliation and a renewed budget after inspection; this clears stop/cancel only under the configured replay policy.
- `./run.ps1 -Action Help`: launcher help.

For logon/periodic restart, preview `./register-resume.ps1`, then explicitly apply it only when that host setup is wanted. No task was installed by this Kaizen. Read [RECOVERY.md](RECOVERY.md) for limits, logs and removal. Before-login execution and actual post-reboot authentication remain unverified.

For a Kaizen that changes the runner itself, edit and test its isolated candidate; do not upgrade the running supervisor in place or propagate over an active lock. Stop the old run before applying a reviewed tool release. This file, config.json and PLAN.md are project-owned and are excluded from managed tool updates.
