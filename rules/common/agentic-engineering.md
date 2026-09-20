# Agentic Engineering — Common Rules

> Distilled from `affaan-m/ECC`'s `skills/agentic-engineering/SKILL.md` (task
> decomposition, model routing, and review-focus doctrine for agent-driven
> engineering work), cross-checked against this engine's own `sdlc-meta/santa-method`
> and `sdlc-meta/verification-loop`, which already assume both principles below
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
`sdlc-meta/verification-loop` assumes when it recommends running the six-phase
gate "after each unit" rather than only at the end of a session.

## Route model tier to task complexity, not to habit

Match the model to what the task actually demands:

- **Haiku** — classification, boilerplate transforms, narrow mechanical edits
- **Sonnet** — implementation and refactors
- **Opus** — architecture decisions, root-cause analysis, multi-file invariants

Escalate to a higher tier only when the lower tier has already failed with a
clear reasoning gap — not preemptively, and not as a default. Running
architecture-grade work through a classification-tier model wastes correctness;
running boilerplate through an architecture-tier model wastes cost for no
quality gain in return.

## Do not spend review cycles on what the linter already enforces

When automated format or lint checks already enforce a style rule, treat a
violation as a mechanical fix, not a discussion. Reserve review attention —
human or agent — for invariants, edge cases, error boundaries, security and
auth assumptions, and hidden coupling: the things static tooling cannot catch.
This is the same non-duplication principle the review phase of
`sdlc-meta/verification-loop` states for Phase 3 (Lint).

## Session and compaction boundaries follow the work, not the clock

Continue one session for closely-coupled units; start a fresh session after a
major phase transition. Compact at a milestone boundary, once a checkpoint's
work is verified — not mid-debugging, where compaction can discard the exact
context needed to diagnose the failure in front of you.
