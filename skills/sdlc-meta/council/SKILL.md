---
name: council
description: Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls where multiple valid paths exist and structured disagreement is more useful than a single confident answer. Not for code review, implementation planning, or architecture design — use the dedicated agents/skills for those.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/council/SKILL.md"
---

# Council

Convene four advisors for ambiguous decisions:
- the in-context voice (this session)
- a Skeptic subagent
- a Pragmatist subagent
- a Critic subagent

This is for **decision-making under ambiguity**, not code review, implementation planning, or
architecture design — this engine already has `agents/planner.md` and `agents/architect.md` for
those, and `sdlc-meta/santa-method` for adversarial verification of a finished deliverable.

<!-- dual-compat-start -->

## Use When

- a decision has multiple credible paths and no obvious winner
- you need explicit tradeoff surfacing
- the user asks for second opinions, dissent, or multiple perspectives
- conversational anchoring is a real risk (you have been arguing for one path for a while)
- a go / no-go call would benefit from adversarial challenge

Examples: ship an engine's install surface now vs. hold for the full profile system; adopt a rules
layer everywhere vs. per-engine; import a skill wholesale vs. cherry-pick one clause into an
existing skill (the exact kind of call this Kaizen operation makes repeatedly).

## Do Not Use When

| Instead of council | Use |
|---|---|
| Verifying whether output is correct | `sdlc-meta/santa-method` |
| Breaking a feature into implementation steps | `agents/planner.md` |
| Designing system architecture | `agents/architect.md` |
| Reviewing code for bugs or security | `agents/code-reviewer.md`, `agents/security-reviewer.md`, or `santa-method` |
| Straight factual questions | answer directly |
| Obvious execution tasks | just do the task |

## Roles

| Voice | Lens |
|---|---|
| Architect (in-context) | correctness, maintainability, long-term implications |
| Skeptic | premise challenge, simplification, assumption breaking |
| Pragmatist | shipping speed, user impact, operational reality |
| Critic | edge cases, downside risk, failure modes |

The three external voices are launched as fresh subagents with **only the question and relevant
context**, never the full ongoing conversation transcript. That is the anti-anchoring mechanism —
use the `Agent` tool with a fresh (non-fork) agent type for each, per this engine's own
`superpowers:dispatching-parallel-agents` pattern where applicable.

## Required Inputs

- One decision question: what is being decided, which constraints bind, and what counts as success.
- The minimum context that changes the answer (files, snippets, metrics), not the conversation transcript.
- Authority to run three fresh, non-fork subagents; without it, see Degraded Mode under Quality Standards.

## Workflow

### 1. Extract the real question

Reduce the decision to one explicit prompt: what are we deciding, what constraints matter, what
counts as success? If vague, ask one clarifying question before convening the council.

### 2. Gather only the necessary context

Collect the minimum relevant files, snippets, or metrics. Skip repo-wide context unless it
materially changes the answer.

### 3. Form your own position first

Before reading other voices, write down your initial position, the three strongest reasons for it,
and the main risk in your preferred path. Do this first so the synthesis does not simply mirror the
external voices.

### 4. Launch three independent voices in parallel

Each subagent gets the decision question, compact context, a strict role, and no unnecessary
conversation history:

```
You are the [ROLE] on a four-voice decision council.

Question:
[decision question]

Context:
[only the relevant snippets or constraints]

Respond with:
1. Position — 1-2 sentences
2. Reasoning — 3 concise bullets
3. Risk — biggest risk in your recommendation
4. Surprise — one thing the other voices may miss

Be direct. No hedging. Keep it under 300 words.
```

Role emphasis: Skeptic challenges framing and proposes the simplest credible alternative;
Pragmatist optimizes for speed, simplicity, and real-world execution; Critic surfaces downside
risk, edge cases, and failure reasons.

### 5. Synthesize with bias guardrails

You are both a participant and the synthesizer:
- never dismiss an external view without explaining why
- if an external voice changed your recommendation, say so explicitly
- always show the strongest dissent, even if you reject it
- if two voices align against your initial position, treat that as real signal
- keep the raw positions visible before the verdict

### 6. Present a compact verdict

```markdown
## Council: [short decision title]

**Architect:** [1-2 sentence position] — [1 line why]
**Skeptic:** [1-2 sentence position] — [1 line why]
**Pragmatist:** [1-2 sentence position] — [1 line why]
**Critic:** [1-2 sentence position] — [1 line why]

### Verdict
- **Consensus:** [where they align]
- **Strongest dissent:** [most important disagreement]
- **Premise check:** [did the Skeptic challenge the question itself?]
- **Recommendation:** [the synthesized path]
```

Keep it scannable on a phone screen.

## Quality Standards

- Each external voice starts from a fresh context holding only the question and the compact context.
- The in-context position, its three reasons and its main risk are written before any external voice is read.
- The strongest dissent is shown in the verdict, even when it is rejected, with the reason for rejecting it.
- Degraded mode: when subagents cannot be launched, say so, write the three voices as separate passes after
  fixing your own position, and label the verdict "single-context council" so readers weigh it accordingly.

## Outputs

- The compact council verdict (step 6), shown to the user.
- A dated decision record, persisted only under the Persistence Rule below.

## Persistence Rule

Only persist a council outcome when it changes something real: update the relevant plan/backlog
file, or a durable engine doc (e.g. this engine's `docs/`), never an ad-hoc scratch note. Do not
persist every decision regardless of importance.

## Multi-Round Follow-up

Default is one round. If another round is needed, keep the new question focused, include the
previous verdict only if necessary, and keep the Skeptic as clean as possible to preserve
anti-anchoring value.

## Anti-Patterns

- using council for code review
- using council when the task is just implementation work
- feeding the subagents the entire conversation transcript
- hiding disagreement in the final verdict
- persisting every decision as a note regardless of importance

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Release evidence | Dated council decision record: question, the four positions, strongest dissent, premise check, recommendation, and whether an external voice changed the in-context position | Markdown section appended to the plan, backlog or `docs/` record the decision changes (Persistence Rule) | `docs/plans/NEXT_FEATURES.md` entry "Council 2026-09-29: land the rules layer before importing gap skills; dissent: Skeptic says half the gaps are false" |
| Correctness | In-context position fixed before the external voices were read (position, three reasons, main risk) | Bullet list kept with the verdict working notes | "Position: defer imports. Reasons: session budget, unverified gaps, roster dependency. Risk: roster ships with missing skills" |

A verdict that changes nothing real is shown to the user and not persisted; its only evidence is the verdict in the session.

## References

- `sdlc-meta/santa-method` — adversarial verification of a finished deliverable
- `sdlc-meta/skill-engine-audit` — whole-engine audit and scoring
- SRS engine's `architecture-decision-records`-equivalent practice — formalize the outcome when the
  decision becomes long-lived system policy (this engine's `agents/architect.md` ADR template)

## Example

Question: "Should this Kaizen pass import the full `~25 gap skills` list now, or land the agent
roster and rules layer first and defer skill imports to a follow-up session?"

Likely council shape: Architect weighs structural completeness against session risk; Skeptic
questions whether all 25 are really gaps (per the verification-and-corrections pass, several
weren't); Pragmatist asks what fits in the current session's budget without half-finishing
everything; Critic flags the cost of an unfinished import (an agent roster with no skills it
references). The value is not unanimity — it is making the disagreement legible before choosing.

<!-- dual-compat-end -->
