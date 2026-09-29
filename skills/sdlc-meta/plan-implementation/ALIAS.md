---
name: plan-implementation
description: Inactive alias for executing a written feature plan task by task with tests and progress tracking. Routes to implementation-status-auditor; the method is kept as a reference there.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

> Inactive alias. Route to `skills/sdlc-meta/implementation-status-auditor` through `docs/skill-aliases.yml`; this file is retained so the old name still resolves.

# Plan Implementation (alias)

The `plan-implementation` skill was absorbed into `implementation-status-auditor` in the May 2026 catalogue consolidation (commit `84d37a5`). Its content now lives at:

- `../implementation-status-auditor/references/plan-implementation.md`: the former entrypoint.
- `../implementation-status-auditor/references/plan-implementation/references/`: execution loop detail, progress tracking and error-recovery patterns (moved there on 29 Sep 2026 in Kaizen phase M10-06).

For writing the plan itself, use `skills/execution-plan-scripts` and `skills/execution-plan-scripts/references/plan-header-and-proportion.md`.
