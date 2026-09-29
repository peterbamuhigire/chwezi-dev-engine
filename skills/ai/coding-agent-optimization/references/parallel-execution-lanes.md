# Parallel Execution Lanes

Load when already-decomposed, independent work can run concurrently (batched reads and
searches, subagents, worktrees, verification lanes) and you need the lane matrix, execution
rules, and completion gate that stop concurrency creating conflicting writes or false "done"
claims. This file does not decide whether to delegate; the device worker cap and fresh-context
rules in `SKILL.md` do.

Absorbed from the retired `sdlc-meta/parallel-execution-optimizer` skill (origin: adapted from
affaan-m/ECC `skills/parallel-execution-optimizer/SKILL.md`).

Speed comes from doing independent work at the same time — repo inspection,
file reads, API or build checks, multiple verification lanes, multi-worktree
implementation passes — without letting concurrency create conflicting writes
or paper over a lane that never actually finished.

## Core Pattern

Turn urgency into a dependency graph before acting, not into a race:

1. Define the objective and the done signal.
2. Split the work into lanes.
3. Mark each lane parallel, sequential, or gated on another lane.
4. Run independent reads, searches, and status checks together, in one batch.
5. Keep writes isolated — by file, worktree, branch, service, or dataset — so
   parallel lanes cannot collide on the same write surface.
6. Merge only after evidence shows the lanes are compatible, not on the
   assumption that "they ran, so they're fine."
7. Report with a verification table, not a speed claim alone.

## Lane Matrix

Before a large push, write a compact matrix so write-surface collisions are
visible before they happen:

```text
Lane            | Parallel? | Write surface | Risk   | Verification
Repo scan       | yes       | none          | low    | grep/git status output
Backend patch   | maybe     | src/api       | medium | unit tests
Frontend patch  | maybe     | app/components| medium | screenshot/visual check
Deploy readback | after build | remote service | high | live URL + logs
```

Only run lanes concurrently when their write surfaces genuinely do not overlap.

## Execution Rules

- Batch file reads, searches, status checks, and metadata queries into a single
  round of tool calls whenever they have no dependency between them.
- Use isolated worktrees for large, unrelated implementation lanes running at
  the same time, following [worktree-safety.md](worktree-safety.md) (consent,
  provenance, cleanup of only what this session created). The Superpowers
  worktree skill is an optional helper where installed.
- Start long-running builds, tests, backfills, or deploys as background
  processes and poll deliberately — do not block a turn waiting on one when
  other lanes can proceed.
- If a lane discovers a blocker that changes the plan, pause every lane that
  depends on it and update the matrix before continuing.
- **Never parallelize destructive commands**, database migrations, concurrent
  writes to the same table, or a live customer-impacting deploy without an
  explicit, stated gate — see `rules/common/security.md` on stating blast
  radius before any destructive action.

## Output Shape

```text
Parallel execution result:
- Lanes run: 5
- Lanes completed: 4
- Blocked lane: deploy readback, waiting on DNS propagation
- Fast path found: batched repo scan + focused tests
- Verification: lint pass, unit pass, live smoke pass
```

### Per-lane report shapes

A lane writes its report for the controller, not for a person. Use one line per finding, in the
shape for its lane type:

| Lane type | Line shape | Example |
|---|---|---|
| Locate | `path:line — finding` | `app/Services/InvoiceService.php:142 — credit note posts without period check` |
| Edit | `path:start-end — change` | `app/Services/InvoiceService.php:140-155 — added period lock guard before post` |
| Review | `path:line: severity: problem. fix.` | `app/Http/Controllers/PosController.php:88: high: tenant id read from request body. Take it from the session.` |

Severity is one of `critical`, `high`, `medium`, `low`.

A lane that cannot finish starts its report with exactly one status token, then says why in one
sentence:

- `blocked.` a dependency, credential or other lane is missing;
- `too-big.` the lane's scope needs splitting before it can be done safely;
- `needs-confirm.` the next step is destructive or outside the stated scope;
- `ambiguous.` the instruction supports two readings that lead to different changes;
- `regressed.` a check that passed before the lane now fails.

These lines are R2 (machine-facing) register. The controller rewrites them into R1 working prose
before a human reads them, and keeps every path, number, identifier and error text exactly as
written (see `docs/continuous-improvement/english-output-standard-2026-09-02.md`, "Output
registers"). `tests/test_report_shapes.py` checks the three line shapes and the five tokens.

(Report shapes and status tokens adapted from JuliusBrussee/caveman, MIT,
https://github.com/JuliusBrussee/caveman, commit `2fd153c`.)

## Dispatch and review controls

1. **No steering of reviewers.** The controller never tells a reviewer what to ignore and never
   pre-rates the severity of a finding. It passes the diff, the acceptance criteria and the
   files; the reviewer decides what matters.
2. **Declined to judge.** Every review report ends with a "declined to judge" list: the areas the
   reviewer did not assess and why (no access, outside competence, not in the diff). An empty
   list is stated as "declined to judge: none".
3. **Capability tier, not model.** Each dispatch names a capability tier (`fast`, `standard` or
   `deep`) and never a provider model identifier. The runner maps the tier to whatever it has.
4. **No nested dispatch.** Subagents do not spawn subagents. A lane that needs more help returns
   `too-big.` and the controller re-plans.
5. **Fix-round circuit breaker.** A review-and-fix loop runs at most three rounds by default. If
   the fourth round would be needed, stop and hand the task to the human owner with the
   reviewer's open findings and the diff so far.

(Dispatch controls adapted from obra/superpowers, MIT, https://github.com/obra/superpowers,
commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d.)

## Failure Modes

- More concurrency producing conflicting edits on a shared file.
- Optimizing the tool call count instead of the actual task outcome.
- Reporting "fast" as if it were "done" before correctness is verified per
  the verification gate (`sdlc-meta/world-class-engineering`, `references/verification-loop.md`).
- Starting a background lane and forgetting to poll it before claiming the
  overall task complete.
- A success summary that quietly omits a lane that was skipped, not run.

## Relationship to the engine

Decompose first per `rules/common/agentic-engineering.md` (each unit independently verifiable,
single dominant risk), then use this file to decide which units can actually run concurrently.
Gate the merged result with the six-phase verification gate in
`sdlc-meta/world-class-engineering` (`references/verification-loop.md`) before claiming the
parallel push is complete.
