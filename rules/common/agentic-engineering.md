# Agentic Engineering — Common Rules

> Distilled from `affaan-m/ECC`'s `skills/agentic-engineering/SKILL.md` (task
> decomposition, model routing, and review-focus doctrine for agent-driven
> engineering work), cross-checked against this engine's own `sdlc-meta/santa-method`
> and the verification gate in `sdlc-meta/world-class-engineering`
> (`references/verification-loop.md`), which already assume both principles below
> without ever stating them as a standalone rule. Kept separate from
> `coding-style.md` because it governs how agentic work is planned and routed, not
> how code is written — a genuinely different axis, and one every skill in this
> engine that delegates to a subagent already depends on.

## Decompose agent work into units a single pass can verify

Before handing work to an agent — yourself in a fresh context, or a subagent —
break it into units that are independently verifiable, have a single dominant
risk, and expose a clear done condition. A unit too large to verify in one pass
hides its own failures; a unit with two unrelated risks makes a failed check
ambiguous about which risk fired. This is the same discipline
the verification gate (`sdlc-meta/world-class-engineering`, `references/verification-loop.md`) assumes when it recommends running the six-phase
gate "after each unit" rather than only at the end of a session.

## Route model tier to task complexity, not to habit

Model selection follows the active runtime's controlling user policy and
available catalogue. Do not infer a live session's model from saved settings.

### Codex

Peter's current Codex policy is authoritative:

- Use GPT-6 Luna with high reasoning by default for orchestration, review and
  execution.
- Use GPT-6 Astra only when Peter explicitly selects it for the task.
- Never select GPT-5.6 or fall back to it; report an unavailable GPT-6 pin.

### Claude and other runtimes

Keep each runtime's own model selection, settings, permissions and capabilities.
Do not translate Codex model pins into another runtime's configuration.

When a runtime's own policy permits a choice among model tiers, match the
available tier to the task:

- Use its efficient tier for classification, boilerplate and narrow edits.
- Use its standard tier for implementation and refactors.
- Use its strongest tier for architecture, root-cause analysis and multi-file
  invariants.

Escalate to a higher tier only when the lower tier has already failed with a
clear reasoning gap, not preemptively or as a default. Running architecture-grade
work through a classification-tier model wastes correctness; running boilerplate
through an architecture-tier model wastes cost for no quality gain in return.

## Do not spend review cycles on what the linter already enforces

When automated format or lint checks already enforce a style rule, treat a
violation as a mechanical fix, not a discussion. Reserve review attention —
human or agent — for invariants, edge cases, error boundaries, security and
auth assumptions, and hidden coupling: the things static tooling cannot catch.
This is the same non-duplication principle the review phase of
the verification gate (`sdlc-meta/world-class-engineering`, `references/verification-loop.md`) states for Phase 3 (Lint).

## Session and compaction boundaries follow the work, not the clock

Continue one session for closely-coupled units; start a fresh session after a
major phase transition. Compact at a milestone boundary, once a checkpoint's
work is verified — not mid-debugging, where compaction can discard the exact
context needed to diagnose the failure in front of you.
