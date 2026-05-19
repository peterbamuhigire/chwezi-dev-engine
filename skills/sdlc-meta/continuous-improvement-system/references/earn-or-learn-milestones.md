# Earn-or-Learn Milestones

The earn-or-learn discipline, drawn directly from impact mapping, holds that every deliverable in a plan must be justified in one of two ways: either the underlying assumption is validated and the work earns toward the goal, or the underlying assumption is uncertain and the work fits inside a learning budget. Anything outside both categories is sunk cost the team has not noticed yet.

In an ideal world, every deliverable would contribute directly to the goal in the centre of the map. That ideal assumes the team will always make the right decisions - which is an illusion. Sometimes there is no way to know up front whether something will work. The honest response is to try, see, and treat the result as data; the dishonest response is to ship and assume.

## The two categories

### Earn

A deliverable earns when its underlying assumption is already validated by prior evidence, and shipping it advances toward the goal in a known way. Examples:

- A capability that has been tested in a smaller form and is now being scaled.
- A feature that completes a workflow whose other steps have been validated.
- An integration that is required by an external commitment whose timing is fixed.

Earning deliverables can carry weight - they are the bulk of most plans. But they only earn if the validating evidence actually exists. A deliverable assumed to earn because "everyone agreed" is not earning; it is uncategorised work waiting to surprise the team.

### Learn

A deliverable learns when its primary justification is to discover whether an assumption holds. The team does not yet know whether shipping it will move the needle; the experiment is the point. Senior people may have a good gut feel about the direction, and that is enough justification to invest - but only inside a learning budget.

The learning budget is the maximum cost or length of work whose primary justification is learning rather than earning. On real projects this is often between one day and one week per experiment. The budget protects the team from the failure mode where "we'll learn from this" becomes the cover story for unbounded speculative work.

## The four growing-deliverables questions

When growing the third level of the map (the deliverables level), use these questions to keep work in one category or the other:

1. **What is the simplest way to support this activity?** Forces the team to consider the minimum-viable form before investing more.
2. **What else could we do?** Forces alternatives, preventing premature commitment to one solution.
3. **If we are unsure about the assumption, what is the simplest way to test it?** This is the explicit gate to the learn category.
4. **Could we test it without software?** Manual experiments, partner deals, customer interviews, paper prototypes - sometimes the cheapest test is not technical at all.

The follow-up question that often unlocks alternatives: **Could we start earning with a partly manual process?** Many features that look like prerequisites are actually optimisations of a manual workflow that could be tested in operation before being automated.

## Decision rule: assumption-or-budget

For every deliverable on the plan, the team must answer one question: is the assumption behind this validated, or does the work fit inside the learning budget?

The strategy literature's framing: the team's job at the start of a milestone is to ask "are we sure that the assumption behind our number-one item is correct?" If the answer is no, find a way to test the assumption within the learning budget before committing to deliver it. Either category - validated assumption or budgeted learning - is acceptable. Neither category - work justified only by inertia or politics - is not.

## What earning looks like in practice

A milestone is earning when:

- The team can name the assumption each major deliverable depends on.
- The evidence for each validated assumption is reachable (a measurement, a previous milestone's outcome, a documented external fact).
- The cumulative deliverables, if all shipped, would plausibly hit the milestone target.
- The cumulative deliverables would not noticeably overshoot - the goal is to deliver enough, not all-of-the-list. Once the milestone target is reached, stop, even with budget unspent.

Anti-pattern: a plan where the answer to "why this deliverable" is "because it was on the list". List-presence is not justification. Every item must trace back to either earning or learning.

## What learning looks like in practice

A learning experiment is well-formed when:

- The assumption being tested is named in one sentence.
- The evidence that would validate or invalidate it is named in advance, so the test cannot be reinterpreted afterward.
- The cost is bounded by the learning budget.
- The experiment has a stop condition - not just "we ran it", but "we ran it and the answer is X".

The Tom Gilb-influenced rule: deliver in iterations not larger than 2% of the overall investment. That is a useful heuristic for sizing experiments. Eric Ries's lean-startup framing is complementary: schedule regular pivot meetings to decide whether to stay on the same course or fundamentally change something.

## Reading the results

After each milestone (or each experiment), the team has three possible findings:

1. **Validated**: the assumption held; the deliverable produced the expected impact. Action: invest more in this branch of the map.
2. **Invalidated**: the assumption broke; the deliverable did not produce the expected impact. Action: back out of the branch. Seriously consider removing the functionality from the product, not just leaving it in. Question the higher-level assumption (does the impact-to-goal connection still hold).
3. **Inconclusive**: the test could not distinguish. Action: design a sharper test or accept that this branch is not worth further investment given current evidence.

Acting on the result is the part that operations skip most often. A team that runs experiments and never acts on the findings has not run experiments; it has run theatre.

## Pivot conditions

If the milestone fails to achieve minimum targets:

- Discuss whether to change deliverables for an impact, or to work on another area of the map altogether.
- Consider whether long-term effects, off-stage actors, or third-party impacts are missing from the plan.
- If delivery fails several times consecutively, consider whether the plan is realistic at all, and whether to keep investing further or stop.
- Be willing to revisit key targets and measurements. Measurements are not sacred; they are tools for decisions, and they should be adjusted as the team learns what is actually informative.

## Stopping conditions

The hardest discipline of earn-or-learn is stopping when the goal has been achieved. Even if the entire budget has not been spent - in fact, especially if it has not - stop. The unspent budget is a signal that the team executed efficiently, not a problem to be solved by continuing to ship.

Once the milestone is reached, regardless of what was actually delivered, the team is done with that milestone. The next mapping session, with senior actors, picks up the next goal.

## Anti-patterns

- **Open-ended learning**: experiments without a stop condition or a learning budget. They drift indefinitely and consume resources that should have been spent earning.
- **Earning by assumption**: deliverables shipped on the basis of "we all agreed" rather than validated evidence. The most common form of sunk-cost-in-disguise.
- **Result-not-acted-on**: experiments completed, evidence captured, and then the team builds whatever was originally planned regardless. Theatre, not learning.
- **Continuing past the goal**: the team has hit the target but keeps shipping because there is budget remaining. Pure waste.
- **Proceeding without a sharp question**: experiments that "explore the space" rather than test a specific assumption. They produce stories, not signal.

## Decision rules

- Every deliverable is in earn or learn. No third category.
- Earning requires validated assumption; cite the evidence.
- Learning requires bounded budget and a named stop condition.
- Validated assumptions justify more investment in the same branch; invalidated assumptions justify backing out, including removal of shipped functionality.
- Stop at the goal even with budget remaining.
- A team that runs experiments and never acts on the findings has not run experiments.

## Source Grounding

- The impact-mapping "earn or learn" mapping step (Adzic), with the principle that deliverables are either justified by a validated assumption or fit inside a learning budget.
- The four growing-deliverables questions (simplest way, what else, simplest test, test without software) and the "could we start earning with a partly manual process" follow-up.
- The "are we sure that the assumption behind our number-one item is correct?" gate for committing a deliverable.
- The Gilb 2%-per-iteration sizing heuristic and the Ries lean-startup pivot-meeting cadence.
- The "stop when you reach the milestone, regardless of what was delivered" rule and the "seriously think about removing functions that fail to meet expectations" rule.
- The post-milestone three-finding structure (validated, invalidated, inconclusive) and the requirement to act on each.
