# auto-agents change log (for porting)

Read this before you update another copy of the runner tools: the community copy in `chwezi-engine-agents/auto-agents`, a copy in another engine, or a project install. Each entry says what changed, why (the incident that proved it), which files changed and how to port the change. The canonical copy is `chwezi-development-engine/auto-agents`. Project copies are updated with `propagate.py <repo> --apply` while their driver is stopped. Never hand-edit a project copy without releasing the same change here.

## How to port a release

1. Diff the release commit in this repository (`git log -- auto-agents`; each release commit subject starts `auto-agents <version>:`).
2. Apply the code and its tests together. Keep the copy's own `config.json`, `PLAN.md` and `ENGINE.md` verification profile.
3. Run `python -B -m unittest discover -s auto-agents/tests` in the target, then `python release.py --version <version>` there (add `--add <file>` for new files) so its manifest matches.
4. Record the port in the target's changelog or handoff, with test counts. Unrun checks are `NOT_ASSESSED`.

The community copy (`chwezi-engine-agents`) was at 2.2.7 on 19 Nov 2026, so it lacks every entry below.

## 2.5.5 (25 Nov 2026): a run whose plan the owner finished closes as done

- **Why:** the writing engine run blocked on an owner decision (24 Nov 2026). The owner made the decision, finished the last task on `main` and committed `STATUS: DONE`, but the run stayed "blocked" for good. Nothing told the runner that its job was finished.
- **What:** on `resume`, `run` or `start`, a `blocked` or `stopped` run is marked `done` when all of these hold: the committed owner plan starts `STATUS: DONE`; its plan contract, if configured, is committed, clean and completion-ready; no operation is unresolved; the runner worktree is clean; and the verified head and worktree HEAD are both already in the owner branch, so no runner work is lost. The status records `closed_by: owner`, `closed_from`, `owner_head` and the original block reason, says that runner gates did not run on owner commits, and writes a `closed` event. Otherwise the run stays as it was.
- **Tests:** `test_owner_completed_plan_closes_blocked_run_as_done`, `test_blocked_run_stays_blocked_until_owner_marks_done`, `test_unmerged_runner_commit_prevents_owner_close` in `tests/test_recovery.py`; full suite 156 passed, 1 skipped.
- **Files:** `execution.py`, `tests/test_recovery.py`, `README.md`, `CHANGES.md`, `manifest.json`.
- **Porting notes:** no configuration key and no digest change. Safe to propagate while a run is stopped or blocked; a scheduled `resume` then closes a finished run by itself.

## 2.5.4 (21 Nov 2026): release the two post-2.5.3 fixes

- **Why:** two commits after 2.5.3 changed managed files without a release, so the manifest hashes no longer matched and `upgrade.py` refused to install into Medic8 ("Modified managed file: README.md").
- **What:** 146e58b: README records the Codex-on-Windows trap (a linked worktree's Git metadata stays read-only under `workspace-write`; the owner may set `--sandbox danger-full-access` in `runner_args_by_runner.codex`; the runner never adds it). 2cb6bf9: `register-resume.ps1` accepts the task principal without its domain ("Peter" as well as "TECH-KOP\Peter" or the SID).
- **Tests:** the full suite is rerun; no behaviour change in the Python runner.
- **Files:** `README.md`, `register-resume.ps1`, `CHANGES.md`, `manifest.json`.
- **Porting notes:** no configuration key and no digest change. Safe to propagate while a run is stopped. After a change to any managed file, run `release.py` in the same commit.

## 2.5.3 (20 Nov 2026): the runner is named Jidoka (JAD)

- **Why:** the owner named the unattended runner **Jidoka**, the *Jidoka Automated Development* tool (JAD), so every new repository's auto runner carries one name alongside the engines' Kaizen vocabulary.
- **What:** naming only. The README title and introduction and the `run.ps1` help and error text say Jidoka. The folder `auto-agents`, file names, configuration keys, state files and the logon-resume task name are unchanged.
- **Tests:** unchanged behaviour; the full suite is rerun.
- **Files:** `README.md`, `run.ps1`, `CHANGES.md`.
- **Porting notes:** no configuration key and no digest change. Safe to propagate while a run is stopped.

## 2.5.2 (20 Nov 2026): regenerating generated files keeps the quick check

- **Why:** Medic8 lane `area-09` passed six full gates on one slice between 09:41 and 19:30 on 20 Nov 2026 and never published. Its slice feeds generated files (API inventory, API docs, asset manifest). Every time the target moved, the integration command rebuilt them, the driver treated the rebuild commit as new lane work and re-ran the full gate (about 55 minutes plus queueing), and the target moved again meanwhile.
- **What:** in `Execution.integrate`, when an integration command commits only files matched by `integration_overlap_ignore`, the quick check is kept (if the rebase already qualified for it). A rebuilt file outside those globs still forces the full gate.
- **Tests:** `test_regenerated_ignored_files_keep_the_quick_check` (fails without the change), `test_regenerated_source_file_reruns_full_gate`.
- **Files:** `execution.py`, `CHANGES.md`, `tests/test_lanes.py`.
- **Porting notes:** no configuration key and no digest change. A project whose `integration_overlap_ignore` lists generated outputs should make its quick check cover them (Medic8 adds its API inventory test and JS tests).

## 2.5.1 (20 Nov 2026): research setup line in `check`

- **Why:** the owner asked that every PC that builds or runs the runner contribute to the private research repository, so the PC used for writing a paper only needs to pull. The study repository now syncs itself across PCs (its v0.2.0).
- **What:** `driver.research_status()` adds a `RESEARCH:` line to `check` (`preflight`). It reports the clone it finds (`CHWEZI_RESEARCH_REPO`, `CHWEZI_ENGINES_ROOT`, the repository's parent folder, or `C:\wamp64\www`), the clone's `origin`, and whether the Windows task "Chwezi research daily collect" is registered. The line is informational only: it never blocks and changes no run state. README gains "Research metrics".
- **Tests:** `test_research_status_reports_missing_and_present_clone`.
- **Files:** `driver.py`, `README.md`, `CHANGES.md`, `tests/test_driver.py`.
- **Porting notes:** no configuration key and no digest change. Safe to propagate while a run is stopped.

## 2.5.0 (20 Nov 2026): Explore subagent on the cheapest model class

- **Why:** the owner's rule (20 Nov 2026) is Opus and Sonnet for the work, Haiku only for trivial mechanical work, Fable only on explicit human request. Runner sessions already started Explore subagents even though `Agent` is not on their `--allowedTools` (it needs no approval), and Explore inherited the session model. Garage's three Explore calls on 19 Nov 2026 all ran on Opus. A per-user `~/.claude/agents/Explore.md` fixes one PC only.
- **What:** new config key `subagents` (`economy` by default, or `inherit`).
  - In economy mode, `driver.subagent_args` inserts `--agents <status dir>/subagents-economy.claude.json` after the skill arguments and before the owner's arguments (`driver.managed_args`). The file defines `Explore` with tools Read, Grep and Glob and model `haiku` (`driver.EXPLORE_ECONOMY`). It is rewritten when a run starts or resumes.
  - `execution.Execution.prompt` adds one line: delegate multi-file searches to Explore, and keep judgement, edits and verification in the session.
  - `execution.job` reattaches jobs prepared by 2.4.x (skill arguments only) and before 2.4.0 (neither).
  - Codex is unchanged.
- **Live check** (Claude Code 2.1.329, 20 Nov 2026): `claude -p --agents <file>` with a marker prompt ran Explore from the file, not from the user-level definition. All five Explore responses were `claude-haiku-5-5`. `Agent` was not on `--allowedTools`.
- **Tests:** `test_subagents_mode_is_validated`, `test_economy_subagent_file_pins_read_only_explore_to_haiku`, three prompt tests, and the updated `test_adapters_preserve_explicit_arguments_and_add_no_bypass`. 151 tests, OK (1 skipped).
- **Files:** `driver.py`, `execution.py`, `README.md`, `CHANGES.md`, `tests/test_driver.py`, `tests/test_recovery.py`.
- **Porting notes:**
  - Keep owner arguments last, so an explicit `--agents` in `runner_args` wins.
  - Changing `subagents` in a project config changes the run's configuration digest. Do it only between runs.
  - Upgrading the code alone does not change the digest; the default is not written into the config.
  - The effect is measured in `chwezi-agentic-research` amendment A6.

## 2.4.1 (19 Nov 2026): absolute finder path

- **Why:** a live runner's worktree branch only gains `find_skill.py` after the upgrade commit is integrated, so a relative path could point at a missing file.
- **What:** the prompt names the driver's own copy by absolute path (`Path(execution.__file__).parent / 'find_skill.py'`). The finder still resolves engines from the agent's working directory.
- **Tests:** `test_prompt_points_to_on_demand_skill_finder` checks the absolute path.

## 2.4.0 (19 Nov 2026): skills on demand

- **Why:** each runner session loaded every enabled plugin's skill catalogue up front, 285 skill descriptions on this PC, before doing any work. The owner asked that agents reach the Writing, Development and orchestrator skills only when needed. Measured with `claude -p --output-format json` (Claude Code 2.1.327, 19 Nov 2026): 36,216 start-up tokens per request with the plugins on, 30,050 with them off. The 6,166-token difference is repeated on every turn of a session as a cache read. MCP servers made no difference, because their tools are deferred.
- **What:** new config key `skills` (`on-demand` by default, or `preload`).
  - On demand, `driver.agent_command` inserts `--settings <status dir>/skills-on-demand.claude.json` (Claude) or `-p chwezi-runner-on-demand` (Codex profile `$CODEX_HOME/chwezi-runner-on-demand.config.toml`) before the owner's arguments.
  - `driver.skill_args(cfg, write=True)` regenerates those files at run start or resume. Each file switches off every plugin enabled in the user, project and local Claude settings, or in the Codex `config.toml`.
  - `execution.Execution.prompt` adds one line pointing the agent to `find_skill.py`.
  - `execution.job` accepts a job prepared before 2.4.0 (argv without the skill arguments) so an upgraded stopped run can reattach.
- **New file `find_skill.py`:** a ranked search over the canonical folders only.
  - Development `skills/`, Writing `skills/`, orchestrator `chwezi-engine-agents` (or `skills-engine-agents`) `core/instructions/` and `skills/`, Accounting `skills/`, Knowledge Bank `plugins/*/skills/`. Marketplace, `dist/`, module and test copies are never searched.
  - Engines are found as siblings of the main checkout, or through `CHWEZI_ENGINES_ROOT` or `--engines-root`.
  - About 1.5 s over roughly 370 skills.
- **Files:** `driver.py`, `execution.py`, `find_skill.py`, `README.md`, `CHANGES.md`, `tests/test_driver.py`, `tests/test_recovery.py`, `tests/test_find_skill.py`.
- **Porting notes:**
  - The engine list lives in `find_skill.ENGINES`. Add an engine there, not in prompts.
  - A copy whose host has no plugins gets an empty profile, which is harmless.
  - Keep owner arguments last so an explicit `--settings` or `--profile` wins.
  - Codex live check (codex-cli 0.170.0, 19 Nov 2026): with the profile, a session listed 11 skills instead of 165 and used 18,792 input tokens instead of 25,500.

## 2.3.10 (19 Nov 2026): ANSI-tolerant plan reads

- **Why:** an agent rewrote `PLAN.md` with PowerShell 5.1 `Set-Content` (ANSI). Byte 0x97 then stopped the Garage run.
- **What:** plan reads use `errors='replace'` in three places in `execution.py` and in `driver.py`. The prompt asks agents to write UTF-8.
- **Tests:** an ANSI plan and a UTF-8 prompt test in `tests/test_driver.py`.

## 2.3.9 (19 Nov 2026): integration keeps evidence valid

- **Why:** integrate rebased a slice, so the contract's `tested_revision` named a pre-rebase commit and blocked the run. Contract feedback also blocked its own repair session.
- **What:**
  - `plan_contract._rebased_into_head` accepts a revision whose patch (`git patch-id --stable`) is in `merge-base..HEAD`.
  - The pre-launch contract tolerance also applies while pending gate feedback is being repaired.

## 2.3.8 (19 Nov 2026): CRLF evidence digests

- **What:** `plan_contract._evidence_digest_matches` also accepts the digest of the CRLF→LF-normalised bytes, for `core.autocrlf` checkouts.

## 2.3.7 (19 Nov 2026): one publish turn

- **What:** rebase, verify and push happen in one serialised publish turn per repository (released from macOS).

## 2.3.6 (18 Nov 2026): Windows leftovers

- **What:**
  - `dirty()` restores files whose only difference is line endings (event `eol_restored`).
  - `durable.write_heartbeat` treats a Windows `PermissionError` (antivirus lock) as best effort, not fatal.

## 2.3.5 (18 Nov 2026): recovery repairs an invalid contract

- **What:** if an interrupted session left the plan contract invalid, the next session gets the errors to repair (`contract_repair`, event `contract_feedback` stage `recovery`) instead of the run blocking.

## 2.3.0 to 2.3.4 (17 to 18 Nov 2026)

- `worktree_root` (excluded from the config digest) moves the worktree out of `.git`, because Claude Code refuses edits there. `check` warns.
- Network retries (`network_retry_seconds`, `max_network_retries`) and publish retries (`publish_retry_seconds`, `max_publish_retries`).
- `CREATE_NO_WINDOW` on Windows, and a receipt sharing retry of about 8 s (`durable.SHARING_RETRIES`).
- Gate slots first come, first served (2.3.3), and `integration_overlap_ignore` (2.3.4).
