---
name: engineering-strategy
description: Use when drafting, reviewing, or repairing an engineering strategy — including diagnosing the real problem, choosing the right altitude, separating guiding policy from operating mechanisms, and producing a written strategy brief that survives contact with reality.
metadata:
  portable: true
  compatible_with:
  - Codex
  - codex
---

> Inactive alias. Route to `skills/world-class-engineering` through `docs/skill-aliases.yml`; this file is retained for historical content.


# Engineering Strategy
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When
- An engineering org is about to commit to a multi-quarter direction (platform rewrite, migration, hiring shape, deprecation, build-vs-buy).
- A leader has produced a "strategy" that is actually a vision, an aspiration list, or a reorg announcement.
- Conflicting local decisions across teams suggest the implicit strategy is incoherent and needs to be made explicit.
- An existing strategy is failing in the field and needs a structured review and revision.
- A working-level engineer or staff+ IC needs to influence direction without executive authority.

## Do Not Use When
- The decision is a single-team technical choice with no cross-team policy implication — use a design doc or ADR instead.
- The work is execution against an already-coherent strategy and only needs planning or sequencing.
- The org is in acute crisis where any written strategy will be ignored; stabilise first, then write.

## Required Inputs
- The presenting problem in the words of the person asking, plus at least one alternative framing.
- Current constraints: people, money, time, regulatory, technical debt, dependencies on other orgs.
- Recent decisions (last 6-12 months) that touch the same surface — these are the *implicit* strategy.
- The altitude of the requester (corporate, portfolio, product, component) and who will be bound by the result.
- A named accountable owner. If none exists, the strategy is not ready to write.

## Workflow
1. **Diagnose before prescribing.** Refuse to draft policy until the diagnosis is written in one paragraph that an opponent could agree is accurate. Load `references/diagnosis-and-leverage.md` for the framing → constraints → leverage-points sequence.
2. **Pick the altitude deliberately.** Identify whether this is corporate, portfolio, product, or component altitude work. Higher altitude = fewer, more permissive policies; lower altitude = denser, more prescriptive ones. See `references/strategy-altitude-and-policy.md`.
3. **Separate the three artefacts.** Write the *guiding policy* (what we will and will not do), the *coherent actions* (the small set of moves that follow from the policy), and the *operating mechanisms* (how we will detect drift). Do not let any one collapse into another.
4. **Stress-test for tradeoffs.** A strategy with no opponent and no thing-given-up is a vision. Force at least two named tradeoffs the strategy accepts.
5. **Set the review loop before publishing.** Define cadence, the evidence that would falsify the strategy, and explicit kill / revise criteria. See `references/operating-mechanisms-and-review-loops.md`.
6. **Write the brief.** Use `references/written-strategy-brief-template.md`. Keep it under five pages. Circulate as a draft, name the dissent, then sign and date.
7. **Audit for failure modes.** Run the strategy through `references/strategy-anti-patterns.md` before publishing. Most strategies die from one of six recurring mistakes; catch them on paper, not in the field.

## Quality Standards
- The diagnosis names a specific obstacle, not a desired outcome.
- A reader who disagrees with the strategy can point to the exact policy clause they disagree with.
- Every coherent action traces back to a clause of the guiding policy.
- The strategy says what the org will *stop* doing, not only what it will start.
- The review cadence and falsification evidence are written in the brief, not in someone's head.
- The strategy is signed by an accountable owner and dated.

## Anti-Patterns
- Aspirational lists ("be world-class," "ship faster," "reduce tech debt") with no policy or tradeoff.
- Vision-disguised-as-strategy: the destination is described, the route is not.
- No-tradeoffs strategy that promises every stakeholder their preferred outcome.
- Reorg announcements published as strategy when the underlying diagnosis is unwritten.
- Strategy by committee that averages every objection into incoherence.
- "Living document" framing used to avoid commitment; revision is healthy but unsigned drift is not.
- Borrowing another company's strategy verbatim without re-running the diagnosis in local context.

## Outputs
- A written strategy brief (diagnosis, guiding policy, coherent actions, operating mechanisms, review loop, named owner, date).
- A list of the explicit tradeoffs accepted and the dissent recorded against them.
- A review cadence entry with falsification evidence and kill / revise criteria.
- A short companion note for affected teams translating the strategy into their decision context.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Release evidence | Engineering strategy brief | Markdown with diagnosis, policy, actions, owner, and review loop | `docs/strategy/engineering-strategy-2026-q2.md` |
| Correctness | Strategy review checklist | Markdown table mapping actions to policy clauses and tradeoffs | `docs/strategy/strategy-review.md` |
| Operability | Strategy operating cadence | Calendar or markdown cadence with falsification evidence and revise/kill criteria | `docs/strategy/operating-cadence.md` |

## References
- references/diagnosis-and-leverage.md — how to frame the real problem and locate the leverage point before writing any policy.
- references/strategy-altitude-and-policy.md — choosing altitude, and what guiding policy looks like at each level.
- references/operating-mechanisms-and-review-loops.md — cadence, evidence, kill criteria, and how strategies stay honest over time.
- references/written-strategy-brief-template.md — the canonical brief structure with section prompts and length budgets.
- references/strategy-anti-patterns.md — the six recurring failure modes and the diagnostic questions that catch each.
<!-- dual-compat-end -->
