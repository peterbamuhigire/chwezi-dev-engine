# Evidence-Driven Retros

A retrospective without evidence is a feelings exchange. A retrospective with the right evidence produces a refined plan, validated assumptions, and the discard of invalidated ones. The structure below pulls from two sources: the impact-mapping discipline of treating delivery as a series of assumption tests rather than a feature factory, and the strategy-refinement discipline of treating strategy as iterative work that improves through deliberate testing rather than waterfall pronouncement.

The starting point: deliverables on an impact map are options, not commitments. Each connection - between deliverable and impact, between impact and goal - is an assumption that may turn out to be wrong. The retrospective's primary job is to identify which assumptions held, which broke, and what to do about each.

## Two distinct retros, often confused

### The milestone retro

Held after a milestone (a unit of delivery scoped to achieve one expected business goal) is complete. Its specific question: did this milestone achieve its intended impact, and what does that tell us about the next one?

The impact-mapping discipline frames this as: deliverables that fail to produce results should point to invalid assumptions. Validated assumptions should justify further investment in the same part of the map. The retro is the moment where this judgment is made formally.

### The strategy retro

Held against a strategic plan over multiple milestones (typically three months). Its specific question: is the strategy still right - diagnosis, guiding policy, coherent actions - or does the evidence demand a rethink?

The strategy literature warns that the most common reason strategy fails is the assumption that strategy will roll itself out, and the second most common is forgetting to validate the details. Both are caught by a strategy retro that holds the original assumptions next to the observed evidence.

These two retros use the same tools but have different inputs and outputs. Conflating them - running a strategy retro at milestone tempo, or vice versa - produces poor outputs from both.

## The four phases of an evidence-driven retro

### Phase 1 - Convene the right room

The strategy literature is direct: workshops with the wrong people produce useful-looking documents that nobody owns. The mistakes to avoid:

- **Too many people**: difficult to facilitate, and the discussion fragments. Limit a focused retro to five or six people for the goals/measurements conversation; up to twenty for the broader review, with a dedicated facilitator whose job is the meeting, not the content.
- **Wrong people**: the ideal mix is technical experts and business decision-makers. Without decision-makers the exercise is pointless because they have to approve the response. Without technical experts, the response will be unfeasible.
- **People who do not want to be there**: if the participants are not interested, the workshop is being run at the wrong altitude. Stop the workshop and find the right people higher in the organisation.

The retro convenor's job is to refuse to start until the right room is in the room.

### Phase 2 - Pull the evidence

Two categories of evidence are required:

**Outcome evidence**: did the milestone produce the impacts it was supposed to? For each impact on the map, what was measured, what was the benchmark before, what was the constraint (minimum acceptable) and target (desired) value, and what was actually observed?

The measurement structure that works (Gilb, via the impact-mapping discipline): scale (what is being measured), meter (how it is being measured), benchmark (what the situation was before), constraint (minimum acceptable / break-even), target (desired value). All five must be explicit. Discussing measurements at this granularity routinely reveals that 17 of 20 stated goals were not really goals - they were not important enough to justify the measurement infrastructure.

**Assumption evidence**: which of the connections on the impact map turned out to be true, false, or untested? Each connection (deliverable supports impact, impact contributes to goal) is an explicit assumption. The retro names each one and classifies it.

Both kinds of evidence are written up before the retro starts, not generated in the meeting. The meeting's job is to interpret the evidence, not to produce it.

### Phase 3 - Diverge then converge

The structure that produces the best findings, lifted from design thinking and embedded in the impact-mapping facilitation: a divergent phase first, then a convergent phase.

In the divergent phase, the room generates explanations, alternative interpretations, and options for the next milestone, without anyone criticising. Even seemingly silly ideas may inspire someone else to a realistic alternative. Critique kills divergent thinking; the facilitator names the phase explicitly.

In the convergent phase, the room narrows. Specific questions:
- What are the obstructions that could block the next milestone before it starts?
- Where is the high-value, low-hanging-fruit impact?
- What are the key assumptions to test next?

Use silent voting techniques (dot-voting, virtual cash distribution to invest in goals) when the discussion does not converge naturally. Two-colour dot-voting (red for critical, green for low-hanging fruit) can speed the convergence.

### Phase 4 - Decide and document

The retro ends with three written outputs:

1. **What is validated**: which assumptions held, justifying further investment.
2. **What is invalidated**: which assumptions broke, justifying backing out, redirecting, or removing functionality. The strategy literature is direct: seriously think about removing functions that fail to meet expectations.
3. **What is the next test**: the specific assumption to test in the next milestone, and the learning budget allowed for it (the maximum cost or length of work whose primary justification is learning, not earning).

Three named outcomes per assumption: validated, invalidated, or still-untested-and-here-is-how-we-test-it-next. No fourth category. The vagueness of "we should keep an eye on this" is what produces meetings that recur for a year without producing decisions.

## Common retro mistakes (named after the impact-mapping mistake archetypes)

- **The Astronaut**: retro held without good metrics. With no measurements, the room cannot tell if it is making progress or fooling itself. Fix: pull the measurement work back to before the milestone starts, not after it ends.
- **The Optimist**: retro that only catches what went well or what users wanted. Misses obstructions and negative signals. Fix: explicitly ask "what could prevent the next milestone from starting" and "who could block us".
- **The Dreamer**: retro that drifts into solving every customer need rather than addressing the milestone that just ran. Fix: anchor the retro to the specific milestone goal; defer everything that does not contribute to it.
- **The Robot**: retro whose only outputs are technical implementation tasks. Fix: ask explicitly what assumption could be tested without implementing more software, including manual experiments, partner deals, or simply asking customers.
- **The Octopus**: retro that tries to evaluate too many goals at once. Fix: split into multiple retros, one per goal.
- **The Surrealist**: retro built on metrics that are not actionable - the team cannot do anything with what is measured. Fix: redefine the objective with the team that has to deliver it.

## The "rinse and repeat" rhythm

The impact-mapping discipline's term for the iterative loop: deliver, measure, decide whether to keep going in the same direction or do something different. After the first few items are delivered, measure the results. Deliverables that fail to produce results point to invalid assumptions. Validated assumptions justify further investment. Add more deliverables to the same impact and measure again. Remember to check the higher-level assumption: if invitations go out but new players are not arriving as expected, the whole idea of supporting invitations should be questioned, not just the implementation of one feature.

When the milestone target is achieved, stop - even if the entire budget has not been spent. The unspent budget is a feature, not a failure. Schedule a fresh mapping session for the next milestone, with senior actors in the room.

If the milestone fails to deliver minimum targets, the retro must address whether to change deliverables for the impact, work on a different area of the map, or revisit the central goal. If delivery fails several times consecutively, consider whether the plan is realistic at all.

## Decision rules

- Every retro must have outcome evidence (did the impacts happen) and assumption evidence (did the connections hold).
- Diverge before converging. Name the phases.
- Every retro ends with named validated assumptions, invalidated assumptions, and the next test.
- A retro held without the right people is rescheduled, not run.
- A retro without a milestone to look back on produces thin findings; do not run them on the calendar.
- "Keep an eye on this" is not an output; either name a test or close the item.

## Source Grounding

- The impact-mapping principle that deliverables are options, and that deliverables which fail to produce results point to invalid assumptions while validated assumptions justify further investment.
- The Gilb measurement structure (scale, meter, benchmark, constraint, target) used in impact-mapping preparation, and the finding that discussing these can drop 17 of 20 stated goals because they were not really important.
- The "rinse and repeat" iterative-delivery cycle (deliver, measure, decide whether to continue) and the "stop when you reach the target even if budget remains" discipline.
- The impact-mapping facilitation mistakes (Astronaut, Optimist, Dreamer, Robot, Octopus, Surrealist) used as a checklist of retro failure modes.
- The diverge-then-converge structure from design thinking, with the facilitation discipline of naming the phases and forbidding criticism in the divergent phase.
- The strategy-refinement principle that strategy is iterative and that the most common failure is forgetting to validate the details.
