# Strategy Anti-Patterns

Most engineering strategies fail in predictable ways. This reference catalogues the recurring failure modes, the tells that surface them, and the repairs.

## 1. Aspirational List

**Pattern.** A bulleted list of desirable outcomes (be world-class, ship faster, reduce tech debt, raise quality) without diagnosis, policy, or tradeoffs.

**Tells.**
- Every bullet starts with a verb of improvement (improve, increase, reduce, accelerate).
- No bullet names anything the org will *stop* doing.
- The list could be pasted into any other company's strategy without modification.

**Repair.** For each aspiration, force the diagnosis question: *what is in the way of this today, specifically?* Then ask: *what would we have to give up to address that obstacle?* The answers, not the aspirations, are the strategy.

## 2. Vision-Disguised-as-Strategy

**Pattern.** A description of a desired future state ("by 2027 we will operate a unified data platform serving all teams") presented as if it were a strategy.

**Tells.**
- Future-tense prose throughout.
- No present-tense diagnosis of the current state.
- No policy clauses; only outcome descriptions.
- Reads like a launch announcement for a product that does not yet exist.

**Repair.** A vision is a legitimate artefact, but it is upstream of strategy, not a substitute. Pair the vision with: a diagnosis of why the current state is not the vision, the guiding policy that constrains how the gap is closed, and the tradeoffs the org accepts to close it.

## 3. No-Tradeoffs Strategy

**Pattern.** A strategy that promises every stakeholder their preferred outcome.

**Tells.**
- The "tradeoffs accepted" section is empty, missing, or filled with non-tradeoffs ("we tradeoff complexity for capability").
- Every objection in review was answered with "and we'll do that too."
- Nothing in the strategy tells a team they will *not* get something they want.

**Repair.** Force two named tradeoffs in writing. If the org cannot articulate any, the diagnosis is too weak to support a strategy and the brief should return to diagnosis stage. Strategies that cost nothing produce nothing.

## 4. Reorg-as-Strategy

**Pattern.** An org chart change, a renaming of teams, or a new reporting line, published as if it were a strategy.

**Tells.**
- The dominant artefact is an org chart.
- The diagnosis, if present, names structural symptoms (silos, ownership confusion) without naming what behaviour the new structure will produce.
- Operating mechanisms are absent; the structure is assumed to be self-executing.

**Repair.** Treat the reorg as one *coherent action* inside a strategy, not as the strategy itself. Write the diagnosis, the policy, and the operating mechanisms. If the strategy is coherent without the reorg, the reorg may be unnecessary.

## 5. Strategy by Committee

**Pattern.** A strategy produced by aggregating every stakeholder's input until no one objects, producing a document that says nothing controversial and binds no decision.

**Tells.**
- Every clause is qualified ("where appropriate," "as feasible," "subject to context").
- The exception path applies to almost everything.
- The named owner is a group, not a person.
- Reading it changes no one's plan.

**Repair.** A single accountable owner drafts. Stakeholders are consulted, dissent is recorded, but the pen does not pass around. If the org cannot tolerate a single owner for the brief, the strategy is not yet politically possible; defer until it is.

## 6. Borrowed Strategy

**Pattern.** A strategy lifted from a conference talk, a book, or another company's blog post, applied locally without re-running the diagnosis.

**Tells.**
- The diagnosis describes someone else's company.
- Vocabulary that is not native to the local org appears throughout.
- The named tradeoffs match the source's tradeoffs, not the local cost structure.
- Engineers cite the source, not the strategy.

**Repair.** Borrowing patterns is healthy; borrowing diagnoses is not. Re-run the diagnosis in local context using local evidence. If the local diagnosis matches the source, the borrowed policy may apply; if it does not, write a different policy.

## Cross-Cutting Tells

These signals can surface any of the patterns above:

- The strategy has been "almost done" for more than a quarter.
- Engineers in the affected area cannot summarise it in a sentence.
- Every team's existing roadmap is "already aligned" with the new strategy without any change.
- Reviews of the strategy never produce decisions, only updates.
- The exception log is empty months after publication.

## Recovery Sequence

When a strategy is failing for any of these reasons:

1. **Stop.** Do not patch the failing brief in place; failed briefs accumulate authority they no longer deserve.
2. **Re-diagnose.** Return to a fresh diagnosis with current evidence. Do not assume last quarter's diagnosis still holds.
3. **Acknowledge in writing.** Mark the prior brief as superseded with a one-paragraph note explaining why.
4. **Reduce altitude.** If the failed strategy was at portfolio altitude, consider whether a product- or component-altitude version with denser policy would land better.
5. **Restart the loop.** New brief, new sunset, new dissent, new owner if the prior one is no longer credible.

The most expensive thing an org can do is keep a dead strategy alive on paper while operating against an unwritten one. Killing strategies cleanly is part of the discipline, not a failure of it.
