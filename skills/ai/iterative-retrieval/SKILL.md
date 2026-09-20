---
name: iterative-retrieval
description: Progressive multi-pass context refinement for a context-starved subagent — a 4-phase DISPATCH-EVALUATE-REFINE-LOOP cycle, max 3 cycles, for when a subagent cannot predict upfront which files or context it needs. Narrower than skills/ai/ai-rag-patterns (general agentic RAG) and skills/ai/ai-agent-multi-agent-coordination (handoff contracts) — this skill is specifically the retrieval-refinement loop inside one subagent's own context-gathering pass.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/iterative-retrieval/SKILL.md"
---

# Iterative Retrieval Pattern

Solves the "context problem" in multi-agent workflows: a subagent is spawned with limited context
and does not yet know which files are relevant, what patterns exist in the codebase, or what
terminology the project uses. This engine already covers agentic RAG broadly
(`skills/ai/ai-rag-patterns`) and multi-agent handoff contracts
(`skills/ai/ai-agent-multi-agent-coordination`); this skill is the specific missing piece —
progressive, bounded refinement of a single subagent's own retrieval pass before it starts real
work.

## When to Activate

- Spawning subagents that need codebase context they cannot predict upfront
- Building multi-agent workflows where context is progressively refined between passes
- Encountering "context too large" or "missing context" failures in agent tasks
- Optimizing token usage in agent orchestration where a naive first-pass search under- or over-retrieves

## The Problem

Standard approaches fail:
- **Send everything** — exceeds context limits, drowns the signal in noise
- **Send nothing** — the agent lacks critical information and guesses
- **Guess what's needed up front** — often wrong, especially once the codebase's own naming
  conventions diverge from the task's vocabulary

## The Solution: A 4-Phase Loop

```
DISPATCH → EVALUATE → REFINE → LOOP (max 3 cycles, then proceed with best-available context)
```

### Phase 1: DISPATCH

Initial broad query to gather candidate files, using an intentionally loose set of patterns and
keywords derived from the task description.

### Phase 2: EVALUATE

Score each retrieved file's relevance to the task:

| Band | Range | Meaning |
|---|---|---|
| High | 0.8–1.0 | Directly implements the target functionality |
| Medium | 0.5–0.7 | Contains related patterns or types |
| Low | 0.2–0.4 | Tangentially related |
| None | 0–0.2 | Not relevant — exclude |

Alongside relevance, explicitly record **missing context**: what the task still needs that this
pass did not surface. This gap list is what drives refinement — do not skip it.

### Phase 3: REFINE

Update the search criteria from what Phase 2 learned:
- add new patterns discovered in high-relevance files
- add project-specific terminology found in the codebase (the first cycle often reveals that the
  codebase uses different vocabulary than the task description)
- exclude paths confirmed irrelevant (low-relevance files rarely become relevant on a later pass)
- target the recorded gaps specifically, rather than re-running a broader version of the same query

### Phase 4: LOOP

Repeat with refined criteria, capped at 3 cycles. Stop early once either:
- at least 3 high-relevance (≥0.7) files are found with no remaining critical gaps, or
- the cycle cap is reached — proceed with the best context gathered rather than looping indefinitely

3 high-relevance files beat 10 mediocre ones. Exclude confidently; a file scored low-relevance in
cycle 1 will very rarely score high in cycle 3 without new evidence.

## Worked Examples

**Bug fix context** — "Fix the authentication token expiry bug":
- Cycle 1: search "token", "auth", "expiry" → finds `auth.ts` (0.9), `tokens.ts` (0.8), `user.ts` (0.3, excluded)
- Cycle 2: add "refresh", "jwt" (learned from cycle 1's high-relevance files) → finds `session-manager.ts` (0.95), `jwt-utils.ts` (0.85) → sufficient, stop

**Feature implementation** — "Add rate limiting to API endpoints":
- Cycle 1: search "rate", "limit", "api" → no matches; the codebase uses "throttle" instead
- Cycle 2: add "throttle", "middleware" → finds `throttle.ts` (0.9), `middleware/index.ts` (0.7); gap noted: router wiring
- Cycle 3: search "router" patterns → finds `router-setup.ts` (0.8) → sufficient, stop

## Integration into an Agent Prompt

```markdown
When retrieving context for this task:
1. Start with a broad keyword search based on the task description.
2. Evaluate each candidate file's relevance (0-1 scale) and name what is still missing.
3. Refine search criteria from what was learned — new terminology, excluded paths, targeted gaps.
4. Repeat, capped at 3 cycles.
5. Proceed with files scoring ≥0.7, or the best available set if the cap is reached.
```

## Best Practices

1. **Start broad, narrow progressively** — do not over-specify the initial query
2. **Learn the codebase's own terminology** — the first cycle often reveals naming conventions that differ from the task's phrasing
3. **Track what's missing explicitly** — gap identification, not vague dissatisfaction, is what drives refinement
4. **Stop at "good enough"** — a small set of high-relevance files beats a large set of mediocre ones
5. **Exclude confidently** — low-relevance files won't become relevant on a later pass without new evidence

## Related

- `skills/ai/ai-rag-patterns` — general agentic RAG: query rewriting, re-ranking, production retrieval pipelines. Use this skill instead when the "corpus" is code being explored for a single subagent's task, not a document/knowledge-base retrieval system.
- `skills/ai/ai-agent-multi-agent-coordination` — the handoff contract between agents; this skill is what happens inside one agent's own context-gathering pass before or during that handoff.
- `sdlc-meta/santa-method` — for verifying the *output* produced once the subagent has enough context; this skill is about the input side.
