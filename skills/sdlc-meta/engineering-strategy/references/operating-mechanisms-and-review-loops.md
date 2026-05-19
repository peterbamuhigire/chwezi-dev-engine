# Operating Mechanisms and Review Loops

A strategy is only as durable as the mechanisms that keep it honest. Without a review loop with teeth, strategy decays into folklore: cited when convenient, ignored when costly. This reference encodes the operational rules for the review machinery.

## Operating Mechanisms vs Coherent Actions

These are often conflated. Keep them distinct:

- **Coherent actions** *implement* the policy. They have an end state.
- **Operating mechanisms** *detect drift* from the policy. They are ongoing.

A migration is an action; the migration's weekly status review is a mechanism. A new SLO is an action; the SLO breach escalation path is a mechanism.

## The Five Mechanism Types

Most strategies need at least three of these five:

1. **Cadence reviews.** A standing meeting on a fixed rhythm where the strategy's current evidence is reviewed against expectations.
2. **Exception logs.** A written record of every time the policy was waived, by whom, and why. The exception log is often more diagnostic than the policy itself.
3. **Leading indicators.** A small number of metrics that move *before* the strategy succeeds or fails, not after.
4. **Trip wires.** Pre-committed thresholds that trigger an automatic review (not an automatic decision).
5. **Sunset clauses.** A date by which the strategy must be renewed, revised, or retired regardless of how it is performing.

## Cadence Selection

| Altitude | Cadence | Quorum | Output |
|---|---|---|---|
| Corporate | Quarterly | Exec team + named dissenters | One-page review note |
| Portfolio | Monthly | VP + portfolio EMs | Updated dashboard + decision log |
| Product | Bi-weekly | Senior EM + tech leads | Action / no-action call |
| Component | Weekly during active rollout, monthly steady-state | Tech lead + on-call | Health check, exception count |

A cadence that always concludes "no change" is too frequent or too shallow. A cadence that surfaces surprises every meeting is too infrequent or the strategy is failing.

## Evidence Standards

Each review must be fed by evidence that is:

- **Pre-specified.** The metrics and signals were named in the strategy brief, not invented at review time.
- **Falsifiable.** The evidence could in principle show the strategy is failing.
- **Comparable across periods.** The same source, same definition, same time window.
- **Cheap to produce.** If gathering evidence requires heroics, the review will skip it.

Reject narrative-only reviews. A review that runs on anecdote alone is theatre.

## Kill / Revise Criteria

The strategy brief must commit, in writing, to the conditions under which the strategy will be revised or killed. Without these, a failing strategy quietly absorbs more investment forever.

Use this shape:

> *We will revise this strategy if <leading indicator A> < <threshold> for <duration>, or if <coherent action B> slips by more than <duration>. We will kill this strategy if <falsifying evidence>.*

Examples of well-formed kill criteria:

- "We will kill the platform consolidation strategy if, by end of Q2, fewer than three of the five target teams have committed to migration."
- "We will revise the on-call strategy if the page-per-engineer-per-week metric does not drop below 2 within 90 days of rollout."

Examples of malformed criteria (do not use):

- "We will revise if it isn't working." (Not falsifiable.)
- "We will kill it if leadership loses confidence." (Confidence is not evidence.)

## Trip Wires

Trip wires are pre-committed thresholds that trigger a *review*, not a decision. The discipline is:

- The trip wire fires automatically (alert, dashboard, exception count).
- The review is convened within a fixed window (e.g., 5 business days).
- The review's only output options are: continue, revise, kill. "Note for later" is not an option.

Trip wires prevent the most common drift mode: gradual normalisation of conditions that, if presented all at once, would have triggered immediate revision.

## Exception Log Hygiene

The exception log is the cheapest, highest-value mechanism. Rules:

- Every exception is a written entry with: date, requester, clause waived, reason, expiry.
- Exceptions expire by default; permanent exceptions are policy changes, not exceptions.
- The exception count is reviewed at every cadence meeting. If it is rising, either the policy is mis-specified or it is not being enforced.
- An exception granted to one team is visible to all. Hidden exceptions corrode the policy.

## Review Loop Anti-Patterns

- **Status theatre.** Reviews that consume slides, produce no decisions.
- **Metric of the day.** Each review introduces a new metric to dodge yesterday's bad number.
- **Standing pass.** The same answer ("on track") regardless of evidence.
- **Owner drift.** The named owner is no longer in the room; the review continues without them.
- **Sunset deferral.** The sunset clause arrives and is silently extended without a fresh diagnosis.
- **Exception erosion.** Exceptions accumulate without review until the policy is fictional.

## Closing the Loop

A strategy that is performing as expected should produce **boring** reviews that quickly confirm continuation. A strategy that is failing should produce reviews that *visibly* trigger revision or kill. Both are healthy. Reviews that always feel busy and never resolve to a decision are the failure mode.
