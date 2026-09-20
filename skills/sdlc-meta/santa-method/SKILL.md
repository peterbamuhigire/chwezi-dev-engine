---
name: santa-method
description: Use when output must clear two independent adversarial reviewers before it ships — production code, published content, or any deliverable where a single self-reviewing agent shares the blind spots that produced the output. Not for internal drafts or deterministic checks (use build/test/lint pipelines for those).
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/santa-method/SKILL.md (Ronald Skelton, RapportScore.ai)"
---

# Santa Method

Multi-agent adversarial verification with a convergence loop. Two independent reviewers, no shared
context, must both PASS before output ships.

## The Problem This Solves

A single agent reviewing its own output shares the same biases, knowledge gaps, and systematic
errors that produced the output. This engine already has `sdlc-meta/skill-engine-audit` (audits a
whole skill engine) and `digital-research-engine/skills/peer-review-loop` (reviewer independence
for research claims, with a red-team memo and dissent disposition). Santa Method is narrower and
more mechanical than either: it is the specific **dual-independent-PASS gate** for a single
deliverable — code, a generated document, a batch of generated content — not a whole-engine audit
or a research claim review. Use it as the gate; use `skill-engine-audit` or `peer-review-loop` for
their own broader jobs.

## When to Activate

- Output will be published, deployed, or consumed by end users
- Compliance, regulatory, or brand constraints must be enforced
- Code ships to production without human review
- Content accuracy matters (technical docs, educational material, customer-facing copy)
- Batch generation at scale where spot-checking misses systemic patterns
- Hallucination risk is elevated (claims, statistics, API references, legal language)

Do NOT use for internal drafts, exploratory research, or tasks with deterministic verification —
run this engine's build/type/lint/test pipeline for those instead (see
`rules/common/verification.md`).

## Architecture

```
GENERATE  ->  DUAL INDEPENDENT REVIEW (B, C; no shared context, same rubric)
          ->  VERDICT GATE: B=PASS AND C=PASS -> SHIP
                             otherwise         -> FIX CYCLE (max 3 rounds, fresh reviewers each
                                                   round) -> re-review -> escalate to human if
                                                   still NAUGHTY after 3 rounds
```

## Phase 1: Generate

Run the primary task normally. Santa Method is a post-generation verification layer, not a
generation strategy.

## Phase 2: Dual Independent Review

Spawn two review agents (use the `Agent` tool with `subagent_type` other than `fork` — a fork
inherits your context, which defeats the independence requirement here). Critical invariants:

1. **Context isolation** — neither reviewer sees the other's assessment, and neither is a fork of
   the generating session.
2. **Identical rubric** — both receive the same evaluation criteria.
3. **Same inputs** — both receive the original spec AND the generated output.
4. **Structured output** — each returns a typed verdict, not free prose.

Reviewer prompt shape:

```
You are an independent quality reviewer. You have NOT seen any other review of this output.

## Task Specification
{task_spec}

## Output Under Review
{output}

## Evaluation Rubric
{rubric}

## Instructions
Evaluate the output against EACH rubric criterion:
- PASS: criterion fully met, no issues
- FAIL: specific issue found (cite the exact problem, file/line where applicable)

Return:
{
  "verdict": "PASS" | "FAIL",
  "checks": [{"criterion": "...", "result": "PASS|FAIL", "detail": "..."}],
  "critical_issues": ["..."],
  "suggestions": ["..."]
}

Be rigorous. Your job is to find problems, not to approve.
```

### Rubric Design

Every criterion must have an objective pass/fail condition — vague rubrics produce vague reviews.

| Criterion | Pass Condition | Failure Signal |
|---|---|---|
| Factual accuracy | All claims verifiable against source material | Invented statistics, wrong version numbers, nonexistent APIs |
| Hallucination-free | No fabricated entities, quotes, URLs, references | Links or citations that don't resolve |
| Completeness | Every requirement in the spec is addressed | Missing sections, skipped edge cases |
| Compliance | Passes project-specific constraints | Banned terms, tone violations, regulatory gaps |
| Internal consistency | No contradictions within the output | Section A says X, section B says not-X |
| Technical correctness | Code compiles/runs, logic is sound | Syntax errors, logic bugs |

Domain extensions for this engine's typical deliverables:

- **Code (PHP/TypeScript)**: type safety, error handling coverage, no hardcoded secrets, input
  validation, test coverage for new paths — this overlaps with `agents/code-reviewer.md`,
  `agents/php-reviewer.md`, `agents/typescript-reviewer.md`; use one of those agents as a Santa
  reviewer directly rather than re-deriving the rubric.
- **Content/documentation**: banned-slop terms (see `rules/common/coding-style.md` and the design
  engine's anti-slop doctrine where the output is presentation-layer), claims traceable to a real
  source per `digital-research-engine`.

### Phase 3: Verdict Gate

Both reviewers must PASS. No partial credit. If only one reviewer catches an issue, that issue is
real — the other reviewer's blind spot is exactly the failure mode this skill exists to eliminate.

### Phase 4: Fix Until Nice (Convergence Loop)

- Max 3 iterations. Fix ONLY the flagged critical issues — no unrequested refactors.
- Each round spawns **fresh reviewer agents** with no memory of the previous round; prior context
  creates anchoring bias.
- After 3 rounds without a double-PASS, stop and escalate to a human instead of looping further.

### Pattern: Batch Sampling

For large batches (100+ items), full dual review on every item is cost-prohibitive:

1. Run Santa Method on a random sample (10-15% of the batch, minimum 5 items).
2. Classify failures by type (hallucination, compliance, completeness, etc.).
3. If a systematic pattern emerges, apply a targeted fix to the whole batch, not just the sample.
4. Re-sample and re-verify the fixed batch. Repeat until a clean sample passes.

## Failure Modes and Mitigations

| Failure mode | Symptom | Mitigation |
|---|---|---|
| Infinite loop | Reviewers keep finding new issues after fixes | Max iteration cap (3), then escalate |
| Rubber stamping | Both reviewers pass everything | Adversarial prompt: "Your job is to find problems, not approve" |
| Subjective drift | Reviewers flag style, not errors | Tight rubric, objective pass/fail only |
| Fix regression | Fixing A introduces B | Fresh reviewers each round catch it |
| Agreement bias | Both miss the same thing | Mitigated by independence, not eliminated — add a third reviewer for critical output |
| Cost explosion | Too many iterations on large outputs | Batch sampling pattern; budget caps per cycle |

## Integration with This Engine

| Skill/agent | Relationship |
|---|---|
| `rules/common/verification.md` | Run deterministic checks (build, type, lint, test) first; Santa Method handles the semantic checks those pipelines cannot. |
| `agents/code-reviewer.md`, `php-reviewer.md`, `typescript-reviewer.md` | Use as the reviewer agents themselves for code deliverables instead of writing a fresh rubric each time. |
| `sdlc-meta/skill-engine-audit` | Use for whole-engine audits; Santa Method is for a single deliverable. |
| `digital-research-engine/skills/peer-review-loop` | Use for research-claim review; Santa Method is the mechanical dual-PASS gate, narrower in scope. |

## Metrics

- **First-pass rate**: % of outputs that pass on round 1 (target >70%)
- **Mean iterations to convergence**: average rounds to a double PASS (target <1.5)
- **Issue taxonomy**: distribution of failure types
- **Reviewer agreement**: % of issues flagged by both reviewers vs. only one — low agreement means the rubric needs tightening
- **Escape rate**: issues found post-ship that this gate should have caught (target 0)
