# Operating Cadence and Review Loops

A continuous-improvement system needs a cadence of review loops, not a single annual exercise. The strategy literature is direct on this: even the proudest strategy work eventually becomes obsolete, and good strategy embraces that change rather than fighting it. Strategy is iterative, intellectual, and mechanical at the same time - so the operating cadence has to inspect both the policies themselves and the mechanics of how they roll out.

The most common failure is not absence of cadence; it is presence of empty cadence. A weekly meeting that exists because someone scheduled it once, with no specific question it must answer, no owner, and no decision output, is not a review loop - it is a status meeting that consumes time and produces nothing. The discipline below is built around the principle that meetings are almost always the most expensive operational mechanism, and the job is to iterate toward cancelling every recurring meeting that does not justify itself.

## The four review levels

Each level answers a different question, on a different time horizon, with a different audience.

### Level 1 - Inspection (continuous, automatic)

Question: is the policy doing what it is supposed to do?

This level is closest to what the strategy literature calls an inspection mechanism: a way to evaluate whether a policy is succeeding and whether modest adjustments are needed. The reliable form is not a meeting; it is a recurring data review committed to in writing. A working example: a recurring invitation for the working group members who agreed to review the data, with a link to the relevant data dashboard and a specific chat channel for discussion. The inspection is not synchronous; it is a commitment to independently review the data and discuss anything that feels surprising.

Required components:
- A specified place where the data lives (dashboard link, not "I'll send it round").
- A specified frequency for review.
- A specified channel for surfacing anything surprising.
- A failure mode that is loud, not silent. If the inspection mechanism can fail without triggering anything, it accomplishes nothing.

Failure mode: silent inspection. A dashboard nobody looks at; a metric that drifts without alerting; a policy that "sort of works" because no one is checking whether it is working.

### Level 2 - Operational review (weekly to fortnightly)

Question: is delivery on track for this milestone, and where are the early signals to act on now?

This is the team-level cadence. It addresses leading indicators, current commitments, and small course corrections. The audience is the team that owns delivery; the output is a small number of named decisions and adjustments.

The discipline:
- Time-boxed. Long meetings indicate the wrong question is being asked or the wrong people are in the room.
- Focused on leading indicators (the things that move before the lagging metric does), not on the lagging metrics themselves.
- Ends with a written list of decisions, owners, and check-back dates. Without this, the meeting is consuming time without producing decisions.

Anti-pattern: presenting last week's lagging metrics to a senior audience and reporting that things are on track. Senior audiences who only see lagging metrics learn nothing they can act on.

### Level 3 - Milestone retrospective (per milestone)

Question: did this milestone achieve its intended impact, and what does the next milestone look like?

This is the level that owns evidence-driven retrospectives (covered in detail in evidence-driven-retros.md). The required cadence is "after each milestone", not "at fixed calendar intervals", because the unit of work that justifies a retrospective is the unit of work that produced an outcome to learn from.

The output of Level 3 is the input to the next planning cycle: a revised set of impacts to pursue, validated assumptions to invest more in, invalidated assumptions to back away from, and a refined set of measurements.

### Level 4 - Strategy review (quarterly to half-yearly)

Question: is the diagnosis still right, is the guiding policy still right, and are the coherent actions still aligned to both?

This is Rumelt's three-pillar test, run on the existing strategy: diagnosis (what is the actual nature of the challenge), guiding policy (what tradeoffs are we explicitly accepting), and coherent actions (what specific behaviours those policies imply). A strategy review that does not interrogate all three pillars is a status meeting, not a strategy review.

The strategy literature's specific advice: schedule a review in three months even if you do not feel one is needed, to reflect on how things have worked out. This commitment matters because operational plans deliver policies to the organisation, and it is tempting to skip refining the details. Skipping is a relatively quick step that completely changes the strategy's outcomes.

Required output: a written, timestamped record of (a) what changed in the world since last review, (b) what policies were adjusted, (c) what was kept the same and why. This document is what makes the next strategy review possible - without it, the next review starts from scratch.

## Operational mechanisms inside the cadence

The strategy literature catalogues the mechanisms that actually deliver policy to an organisation. Each has a fit, and most operations need a mix. The cadence should track which mechanism is being used for each policy and whether it is working.

- **Approval and advice forums**: useful when complex policies meet complex circumstances and clean application is non-obvious. Specify in writing where exceptions are reviewed (the specific channel, the specific group). "Exceptions will be reviewed by [the named forum] in [the named channel]."
- **Inspection mechanisms**: covered above as Level 1. Always specify dashboard link, review frequency, and the named group reviewing.
- **Nudges**: providing context to inform a better choice, rather than mandating it. Effective when the issue is unconscious, not deliberate. The Stripe example: teams accidentally introducing large cost spikes were nudged via reach-out on a monthly review, rather than forcing all teams through pre-approval. The nudge approach did not require an authoritative mandate, and only the teams that actually overspent had the conversation. Limit the total number of nudges; ensure each has an explicit action; include clear instructions on how to take it.
- **Documentation and training**: aim for "informational herd immunity" - as long as someone on each team understands the policy, the team will generally be able to follow it. Trying to make everyone in the organisation know everything is the wrong target.
- **Automation**: removes the policy from the level of choice. High-leverage when manual processes are slow and the policy is well-understood; low-leverage when used to enforce a policy that is not yet well-tested.
- **Mandatory training**: two known failure modes - because attendance is required, trainers stop investing in quality, and trainees stop paying attention because they expect low-quality content. The result is people trained annually on a policy who report never having heard of it. Use sparingly.
- **Meetings**: the universal but most expensive mechanism. They can do an adequate job of operating almost any policy, which is why they are easy to suggest and run. Default to non-meeting mechanisms first; iterate toward cancelling every recurring meeting that started for a reason that no longer applies.
- **Explicit deferral**: when there is something a policy should do but no reasonable mechanism currently exists, defer the action explicitly rather than implying coverage. An explicitly deferred action is honest; an implied one quietly fails.

## Cadence anti-patterns

- **Cadence inflation**: more meetings, longer meetings, more attendees. The standard response to a missed signal. Almost always wrong - the right response is a leading indicator, not a longer meeting.
- **Calendar-driven retros**: retrospectives held on a date instead of at a milestone. Produce thin findings because there is no specific outcome to look back on.
- **Status without decisions**: a meeting that ends without a written next action and named owner is consuming time without producing decisions. Default to cancellation.
- **Senior-audience-only reviews**: when only senior leaders see the data, they get cleaned-up versions and the operational signal is muted. Reviews must include the people with hands on the system.
- **Silent inspection**: dashboards no one checks, alerts no one acts on, mechanisms that fail without anyone noticing.

## The three-month commitment

Even when the team is confident in a new operational plan, schedule a review three months out. Two reasons. First, no plan survives contact with the world unchanged, and three months is roughly the half-life of confident assumptions. Second, the act of scheduling the review forces the team to define, now, what evidence would show whether the plan is working - which is often the most useful conversation to have at plan-time.

## Decision rules

- Every cadence has a question, an owner, an exit criterion.
- Every operational policy has an inspection mechanism that fails loudly.
- Default to non-meeting mechanisms; iterate toward cancelling recurring meetings.
- Every strategy review interrogates diagnosis, guiding policy, and coherent actions - not just status.
- Every plan ships with a review date already on the calendar.
- A nudge is not the same as a mandate; treat them differently and budget the total number of nudges.

## Source Grounding

- Rumelt's three-pillar strategy structure (diagnosis, guiding policy, coherent actions) as the spine of the Level 4 strategy review.
- The Crafting Engineering Strategy commitment to "schedule a review in three months to reflect on how things have worked out" even when not using formal strategy testing.
- The inspection-mechanism design pattern (recurring invite, dashboard link, named channel, asynchronous review) used at Stripe and Carta.
- The Stripe nudge example: monthly review of spend spikes, reaching out only to the teams that actually overspent, rather than forcing pre-approval on every team.
- The "informational herd immunity" goal for documentation and training.
- The mandatory-training failure pattern (required attendance produces low-quality content and tuned-out trainees) and its implication that documentation-and-nudge mechanisms outperform mass training.
- The principle that meetings are the most expensive operational mechanism and the discipline of iterating toward cancelling recurring meetings that started for reasons that no longer apply.
