# Outcome-to-Execution Traceability

Most plans fail not because the work was poor, but because the connection between the work and the outcome was never made explicit. Studies of large IT failures consistently identify "business benefits not clearly communicated or overstated" and "poor alignment with business strategy" as top causes - the work shipped, but no one could say afterward whether it had moved the thing that mattered.

The discipline that fixes this is traceability: a four-level structure where each level explains why the level below exists, and each item at one level points up to the level above and down to the level below. The four levels, from impact mapping: Why (the goal), Who (the actors), How (the impacts on actor behaviour), What (the deliverables). The structure is deliberately a hierarchy, not a flat list - each level constrains the next, and the connections between levels are explicit assumptions that can be tested.

## Level 1 - Why (the goal)

The centre of the structure. The single question: why are we doing this?

Goals must be:
- **SMART**: Specific, Measurable, Action-oriented, Realistic, Timely.
- **About the problem, not the solution**: avoid embedding design constraints into goal definitions.
- **Limited in number per milestone**: ideally one objective per milestone. Five consecutive milestones, each delivering one objective, are generally much better than one milestone trying to deliver five partially - because the landscape may change after a key objective is achieved, invalidating the others.
- **Translatable to money** for commercial work, with an obvious link to saving, earning, or protecting.

Anti-pattern: a goal definition that is actually a feature ("ship the new portal"). Test: ask whose behaviour will change and how. Then ask why that behaviour change is important. Keep asking until the answer connects to money. The lean five-whys version of this works.

The single best test of a goal: "If we achieve the key targets for the metric with a completely different scope than planned, have we succeeded?" If the answer is no, the metrics are wrong.

## Level 2 - Who (the actors)

Actors are the people who can produce the desired effect, obstruct it, consume the product, or be impacted by it. Three types worth considering:

1. **Primary actors**: those whose goals are fulfilled (e.g. players in a gaming system).
2. **Secondary actors**: those who provide a service (e.g. a fraud-prevention team).
3. **Off-stage actors**: those who have an interest but neither benefit directly nor provide a service (e.g. regulators, senior decision-makers).

The discipline is specificity. Avoid generic terms like "users" - different categories of users will have different needs, and not all of them are important for a particular project. Define actors in this priority order: specific individual, then user persona, then role/job title, then group/department.

Common failure: missing the actor who can stop the work. If only positive actors are listed, the plan does not anticipate obstructions, and the team is surprised when an off-stage actor (the regulator, the senior partner who was not consulted) blocks delivery late in the cycle.

## Level 3 - How (the impacts)

Impacts are the changes in actor behaviour we want. They sit between the actor and the goal.

Required form:
- **A change in behaviour, not just a behaviour**. Not "selling tickets" - "selling tickets five times faster". The change is what differentiates an impact from a description.
- **Tied to the goal**. List only the impacts that move toward the central goal; do not list everything an actor might want.
- **Not features**. "Mobile home page with purchase form" is a deliverable, not an impact. The impact would be "purchasing tickets without calling the call centre".
- **Includes negative impacts**. Once the first impact for an actor is identified, ask what else they might do, including obstructive behaviours.

The central question for impacts: how should the actor's behaviour change? How could they help achieve the goal? How could they obstruct or prevent it?

This is the level where business sponsors should be asked to prioritise. Business users think more clearly about business activities and impacts than software features, and they prioritise impacts better than they prioritise deliverables.

## Level 4 - What (the deliverables)

Deliverables are the things the team will build or do to support the impacts. They are explicitly the least important level of the map - the level that should be refined iteratively, not committed to up front.

Discipline at this level:
- **Treat deliverables as options**. Do not assume everything listed will actually be delivered.
- **Stay high-level early**. Break high-level deliverables into smaller items (user stories, use cases) only when their time comes, not at the start.
- **Look beyond software**. Even on software projects, there are often non-software ways to support a business activity. Sometimes paying for advertising to recruit new players is cheaper than rebuilding a recruitment system.
- **Each deliverable points up to a specific impact**. If a deliverable does not connect to an impact on the map, it does not belong on the current plan.

## The chain test

Traceability is verified by walking the chain in both directions and asking, at each link:

- **Is it realistic that the deliverable will contribute to the impact?**
- **Is the impact valid for the actor?** (Does this actor actually behave this way given this deliverable?)
- **Will the impact really contribute to the goal?**

It is surprising how often the answer to at least one of those is no after the first attempt. The questions seem obvious, but until the chain is drawn explicitly, no one is asking them.

## What traceability prevents

The impact-mapping discipline lists the specific failure modes that traceability solves:

- **Scope creep**: when there is a clear mapping from deliverables to goals, the team can see when the goal has been reached and stop. Without traceability, work continues by inertia.
- **Wrong solutions**: with deliverables in the context of impacts, it is trivially easy to spot solutions looking for a problem, or those that contribute to a different goal than the current one.
- **Pet features**: features that nobody can place on the map - they do not connect to any impact - are pet features. Traceability makes them visible.
- **Wrong assumptions**: when assumptions are explicit (each connection between levels is an assumption), they can be tracked and validated. Implicit assumptions cannot be challenged.
- **Ad-hoc prioritisation**: with traceability, prioritisation is between impacts at the same level, not between unrelated features.

## Maintaining traceability over time

A traced plan that is not maintained becomes a fictional document. The maintenance discipline:

- **Update the map iteratively**, after each milestone. The map is not a one-time artefact.
- **Visualise assumptions** as connections, not as a separate document. The assumption that "this deliverable will produce this impact" sits in the line between them.
- **Watch for unintended third-party effects**. Plans that narrow attention to a single outcome have blind spots for anything outside that focus, particularly long-term outcomes and effects on parties not represented on the map.
- **Two-level maps for larger work**. For longer-term product development, maintain a high-level vision map and a medium-term delivery map. Deliverables on the vision map become product milestones, each with its own lower-level map when its turn comes.

## Traceability and metrics

Each level of the map can carry measurements - and should. The four ways to fit metrics into the map:

1. **Bullet points** next to a node: clean and clear when the metrics are simple.
2. **Rephrased nodes**: incorporate the metric into the node name ("between 800K and 1M players over 6 months" instead of just "more players"). Works when there are one or two key metrics.
3. **Separate metrics table** alongside the map: when there are many measurements and the map needs to remain readable.
4. **Additional map nodes**: list metrics as branches. Risks confusion when the structure becomes complex.

The choice of fit is operational; the principle is that every level of the map has measurable expectations attached to it, not just the central goal.

## Decision rules

- A goal that does not pass the SMART test is a feature in disguise; rewrite it.
- An actor described generically ("users") is the wrong actor; refine to a specific individual, persona, role, or group.
- An impact that is just a behaviour, not a change in behaviour, is incomplete; add the change.
- A deliverable that does not point up to an impact does not belong on the current plan.
- Walk the chain in both directions before publishing the plan; expect at least one no.
- Maintain the map across milestones; a stale map is fiction.

## Source Grounding

- The Why-Who-How-What four-question structure for impact maps (Adzic).
- The SMART goal definition (Specific, Measurable, Action-oriented, Realistic, Timely) and the principle that goals should describe the problem, not the solution.
- The "if we achieve the key targets for the metric with a completely different scope than planned, have we succeeded?" test for goal correctness.
- Cockburn's three actor types (primary, secondary, off-stage) and the priority order for naming actors specifically (individual, persona, role, group).
- The "change in behaviour, not just behaviour" rule for impacts ("selling tickets five times faster" rather than "selling tickets").
- The treat-deliverables-as-options principle and the priority of refining deliverables iteratively rather than committing them up front.
- The list of failure modes traceability prevents (scope creep, wrong solutions, pet features, wrong assumptions, ad-hoc prioritisation).
