---
name: strategic-compact
description: Use when a long session is approaching a context limit, or is between task phases (research/plan/implement/test), to decide whether this is a good point to manually compact — rather than waiting for arbitrary auto-compaction to hit mid-task and discard state you actually needed.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/strategic-compact/SKILL.md (doctrine only — ECC's automated context-size hook is not vendored into this engine; see Note on Automation below)"
---

# Strategic Compact

Auto-compaction fires at an arbitrary point in a session, with no awareness of
task boundaries — it can as easily interrupt the middle of a multi-step edit as
land cleanly between phases. Compacting deliberately at a logical boundary
instead — after exploration and before execution, after a milestone, before a
major context shift — preserves the state that matters and discards the state
that does not, rather than leaving the outcome to timing.

## When to Consider Compacting

- The session is long and approaching a context limit
- A task phase has just completed: research → planning → implementation → testing
- About to switch to an unrelated task within the same session
- A milestone just finished and the next phase is starting fresh
- Responses are slowing down or losing coherence — a sign of context pressure

## Compaction Decision Guide

| Phase Transition | Compact? | Why |
|---|---|---|
| Research → Planning | Yes | Research context is bulky; the plan is the distilled output that survives |
| Planning → Implementation | Yes, once the plan is written to a file | Frees context for code without losing the plan |
| Implementation → Testing | Maybe | Keep context if tests reference recent code; compact if switching focus |
| Debugging → Next feature | Yes | Debug traces pollute context for unrelated work |
| Mid-implementation | No | Losing variable names, file paths, and partial state is costly |
| After a failed approach | Yes | Clear the dead-end reasoning before trying a different approach |

## Write the Plan Down Before Compacting

Do not rely on an in-session task list surviving compaction — whether one
exists at all depends on which task-management tools the current harness and
model combination has enabled, which is an environment setting, not something
a skill can guarantee. **Write the plan to a file before compacting.** A file
persists across every compaction, every session, and every model; an in-memory
task list might not exist in the first place.

## What Survives vs. What Is Lost

| Persists | Lost |
|---|---|
| `CLAUDE.md` / router instructions | Intermediate reasoning and analysis |
| Files written to disk | File contents you previously read but did not re-save |
| Durable memory files, where the harness has them | Multi-step conversation context |
| Git state (commits, branches) | Tool-call history and counts |
| A task list — only if the tools exist and were used | Nuanced preferences stated only verbally |

## Best Practices

1. Compact after a plan is finalized **and written to a file**, not before.
2. Compact after debugging is resolved, to clear error-resolution noise.
3. Do not compact mid-implementation — preserve context for related changes.
4. Add a custom summary to the compact instruction when useful (e.g. "focus on
   implementing the auth middleware next") so the distilled context stays
   actionable.

## Token Discipline Alongside Compaction

- **Load skills on demand, not upfront.** This engine's own narrowest-surface
  principle (`skills/sdlc-meta/skill-composition-standards` and the rules-vs-skills
  test in `rules/README.md`) already does the "trigger-table lazy loading" job
  ECC's version of this skill describes separately — skills here load only when
  triggered, not at session start.
- **Watch for duplicate instruction sources** — the same rule stated in both a
  rules file and a loaded skill wastes context twice for one fact; consolidate
  toward the rules file and have the skill link to it, per this engine's own
  `rules/README.md` guidance.

## Note on Automation

ECC's version of this skill ships a `suggest-compact.js` PreToolUse hook that
reads live token counts from the transcript and fires threshold-based
reminders automatically. That hook is **not vendored into this engine** — this
skill captures the decision doctrine only. If automated compact suggestions
become worth building here, they belong in `hooks/`, following the same
pattern as this engine's existing `destructive-bash-gate.js` and
`banned-font-gate.js` (see `hooks/hooks.json` and `rules/README.md`'s
hooks-vs-rules-vs-skills split) — not inside this skill file.
