# Diagnosis and Leverage

A strategy without a diagnosis is a wish. The diagnosis is the load-bearing element of every engineering strategy: if it is wrong, no amount of clever policy will recover. This reference encodes the operational rules for producing a diagnosis that is honest, specific, and actionable.

## Three-Layer Frame

Work the diagnosis through three layers in order. Skipping or collapsing layers produces aspirational strategy.

### Layer 1: Problem Framing

The *presented* problem is rarely the *real* problem. Before writing anything else, run these checks:

- **Restate in one sentence.** If you cannot, the problem is not yet a problem; it is a topic.
- **Name the obstacle, not the outcome.** "We want faster releases" is an outcome. "Our staging environment cannot represent production traffic" is an obstacle.
- **Locate it in time.** Is this new, chronic, or worsening? Each calls for a different intervention.
- **Find the alternative framing.** Force a second framing of the same situation by a stakeholder with a different role (engineer, PM, support, finance). If both framings are valid, the strategy must reconcile them or pick one explicitly.

Output of layer 1: a single paragraph titled *Diagnosis* that an informed opponent could agree is factually accurate, even if they disagree with what to do about it.

### Layer 2: Constraints

A diagnosis without constraints produces unbounded policy. Catalogue:

- **Hard constraints**: regulatory, contractual, physical, cash, headcount caps.
- **Soft constraints**: cultural debt, political sensitivity, executive preferences, recent failed initiatives that have used up trust.
- **Coupling constraints**: dependencies on other orgs, vendor lock-in, shared infrastructure that cannot be changed unilaterally.
- **Time constraints**: the window in which the strategy must produce visible movement before sponsor patience expires.

Write each constraint as a single bullet. If a constraint is unwritten, it will silently veto the strategy later.

### Layer 3: Leverage Points

The leverage point is the place where a small, achievable action produces disproportionate change in the diagnosed problem. Most strategies fail because they intervene at a low-leverage point that is merely visible.

Use this ranking, from highest leverage to lowest:

1. **Goal of the system.** What the org is implicitly optimising for. Changing the goal changes everything downstream.
2. **Rules and policies.** What is allowed, required, or forbidden. Cheap to change on paper, expensive to enforce.
3. **Information flows.** Who sees what, when. Often the cheapest real intervention.
4. **Feedback loops.** Cadence and gain of review, alerting, learning loops.
5. **Structure.** Org shape, repo shape, system topology. Slow to change, slow to undo.
6. **Parameters.** Headcount, budget, SLO targets. Visible, easy to tune, rarely sufficient on their own.

Pick the highest-leverage point you can credibly act on within the constraint set. Lower-leverage interventions belong in operations, not strategy.

## Diagnosis Quality Gates

Before moving from diagnosis to policy, the diagnosis must pass all five gates:

- **Falsifiable.** Name the evidence that would prove the diagnosis wrong.
- **Specific.** Replace every abstract noun (quality, velocity, alignment) with a concrete behaviour or metric.
- **Bounded.** State what is *not* part of the diagnosis to prevent scope creep.
- **Owned.** A single person can speak for the diagnosis and answer questions about it.
- **Recent.** The diagnosis was tested against the last 90 days of data, not last year's narrative.

A diagnosis that fails any gate is sent back. Do not write policy on top of a weak diagnosis.

## Common Diagnosis Failure Modes

| Failure | Tell | Repair |
|---|---|---|
| Outcome-as-diagnosis | The diagnosis names what we want, not what is in the way. | Ask "and the obstacle to that is…?" three times. |
| Symptom-as-diagnosis | The diagnosis names a metric movement, not its cause. | Trace upstream until you reach a decision or a constraint. |
| Blame-as-diagnosis | The diagnosis names a team or person. | Restate the diagnosis without naming any person; if it dissolves, the diagnosis was politics. |
| Vendor-as-diagnosis | The diagnosis assumes a tool change will fix it. | Force the diagnosis to be true even if no tool changes. |
| Everything-as-diagnosis | The diagnosis is a list of ten things. | Pick the one that, if solved, makes the others tractable. |

## From Diagnosis to Policy

The bridge from diagnosis to guiding policy is a single sentence:

> *Given <diagnosis>, under <constraints>, our highest-leverage intervention is to <leverage point>.*

If you cannot write that sentence, the diagnosis is not yet load-bearing. Go back to layer 1.
