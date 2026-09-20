---
name: parallel-execution-optimizer
description: Use when a task can go faster by doing independent work at the same time — batched reads/searches, concurrent subagents, isolated worktrees, or multiple verification lanes — without letting concurrency create conflicting writes or a false sense of "done." Not for deciding whether a task should be delegated to a subagent at all — this is about running already-independent lanes efficiently once decomposed.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/parallel-execution-optimizer/SKILL.md"
---

# Parallel Execution Optimizer

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
- Use isolated worktrees (`superpowers:using-git-worktrees` where available)
  for large, unrelated implementation lanes running at the same time.
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

## Failure Modes

- More concurrency producing conflicting edits on a shared file.
- Optimizing the tool call count instead of the actual task outcome.
- Reporting "fast" as if it were "done" before correctness is verified per
  `sdlc-meta/verification-loop`.
- Starting a background lane and forgetting to poll it before claiming the
  overall task complete.
- A success summary that quietly omits a lane that was skipped, not run.

## Relationship to This Engine

Pairs with `rules/common/agentic-engineering.md`'s unit-decomposition rule
(each unit independently verifiable, single dominant risk) — decompose first
per that rule, then use this skill to decide which of the resulting units can
actually run concurrently. Gate the merged result with `sdlc-meta/verification-loop`
before claiming the parallel push is complete.
