---
name: continuous-improvement-system
description: Use when designing or running an operating cadence (daily/weekly/monthly/quarterly review loops), running an evidence-driven retro, applying kill/pivot/double-down criteria to a strategy, tracing business goals through to execution evidence, building a capability development plan, defining earn-or-learn milestones for a premium engagement, or feeding retention/churn signals back into strategy. Encodes review-loop structure, root-cause-to-policy-change discipline, and outcome-to-execution traceability.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Continuous Improvement System
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Establishing or auditing the operating cadence (daily, weekly, monthly, quarterly).
- Running a retro that needs to produce a policy change, not just a list of feelings.
- Applying kill, pivot, or double-down criteria to a live strategy or initiative.
- Tracing a business goal through measurable outcomes, interventions, and evidence.
- Building a capability development plan for skill, system, and process gaps.
- Defining earn-or-learn milestones for a premium engagement (delivery proof or learning capture).
- Closing the loop from retention/churn signals back into strategy.

## Do Not Use When

- The work is a single-issue customer recovery; use `customer-service-excellence`.
- The work is a sales conversation; use `premium-client-sales`.
- The work is product validation before build; use `product-discovery`.
- The work is a one-off retrospective with no operating-cadence implication.

## Required Inputs

- Stated business goals and the time horizon (quarterly minimum).
- Current outcome metrics (or the absence of them, which is itself a finding).
- Initiative or intervention list with owners and deadlines.
- Evidence available: customer signals, financial signals, delivery signals, churn data.
- Prior retro outputs and which policy changes were actually adopted.

## Workflow

1. Verify the **operating cadence** exists at four levels (daily, weekly, monthly, quarterly). If a level is missing, build it before reviewing content.
2. Run the **evidence-driven retro** path: data -> pattern -> root cause -> policy change. Stop a retro that ends at "we should do better"; that is not a policy change.
3. Apply **kill / pivot / double-down** criteria to live initiatives. Decide explicitly; "continue with no change" is also a decision and must be recorded as such.
4. Walk **outcome-to-execution traceability** from business goal to measurable outcome to intervention to evidence. Any link without evidence is a gap.
5. Build or refresh the **capability development plan** with three axes: skill (people), system (tooling and data), process (the playbook).
6. For premium delivery, set **earn-or-learn milestones**: every milestone produces either a delivered outcome or a captured learning that updates the playbook.
7. Feed **retention and churn signals** into the strategy review. Premium businesses live or die on retention; treat retention deltas as strategic input, not as an operations report.

## Quality Standards

- Every retro produces a policy change (or an explicit accepted-loss note); discussions without changes are not retros.
- Every initiative has kill criteria, pivot triggers, and double-down signals defined at start, not at review.
- Every quarterly review can answer: which goal moved, which intervention moved it, what is the evidence, what next.
- Capability gaps are named per axis (skill, system, process), not lumped into "we need to be better".
- Earn-or-learn milestones reject "we tried, it didn't work" without a captured learning.

## Anti-Patterns

- Treating a status meeting as a review. Status describes; review decides.
- Retros that end at feelings or generic resolutions ("more communication"). Surface a policy change or close the retro as inconclusive and reschedule.
- Goals without paired outcome metrics. Unmeasured goals are aspirations.
- Adding new initiatives without killing or completing prior ones. The portfolio bloats; capacity drops.
- Treating churn as a service metric only. It is also a strategy signal.
- "We will revisit this next quarter" as a default outcome. It is the slowest form of paralysis.

## Outputs

- A documented operating cadence with named owners per level.
- Retro records that include data, pattern, root cause, and the specific policy change adopted.
- Initiative decisions: kill, pivot, double-down, or continue-as-is, with the reason.
- A traceability map from goals to evidence with explicit gaps marked.
- A capability development plan across skill/system/process.
- Earn-or-learn milestone records with delivery or learning attached to each.
- A retention/churn signal feed into the next strategy review.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Release evidence | Continuous-improvement cadence | Markdown calendar with daily, weekly, monthly, and quarterly loops | `docs/improvement/cadence.md` |
| Correctness | Outcome traceability ledger | Markdown or CSV mapping goals, assumptions, actions, evidence, and verdicts | `docs/improvement/outcome-ledger.csv` |
| Operability | Earn-or-learn milestone plan | Markdown table with target, constraint, learning signal, and decision state | `docs/improvement/milestones.md` |
| Performance | Capability development plan | Markdown plan linking recurring gaps to skill, system, or process improvements | `docs/improvement/capability-plan.md` |

## References

- `references/operating-cadence-and-review-loops.md` for the four-level cadence with agenda, owner, and exit criteria.
- `references/evidence-driven-retros.md` for the data-pattern-root-cause-policy path.
- `references/outcome-to-execution-traceability.md` for the goal-outcome-intervention-evidence chain.
- `references/earn-or-learn-milestones.md` for the discipline that converts non-delivery into captured learning.
- `references/capability-development-plan.md` for the skill/system/process triad.
- Use `customer-service-excellence` to source prevention-loop entries and retention-impact data.
- Use `premium-client-sales` to source win/loss patterns for strategy review.
<!-- dual-compat-end -->

## The Four-Level Cadence (summary)

| Level | Cadence | Purpose | Owner |
|-------|---------|---------|-------|
| Daily | 10-15 min | Block clearance, today's commitments | Team lead |
| Weekly | 45-60 min | Outcome metric review, intervention adjustments | Function head |
| Monthly | 90 min | Initiative kill/pivot/continue, capability check | Leadership team |
| Quarterly | half-day | Strategy review, goal-outcome traceability, earn-or-learn rollup | Executive owner |

Skip a level and the levels above and below it absorb the missing work, which makes them slower and worse.

## The Retro Closing Test

A retro is closed only when one of three outputs is recorded: (1) a named policy change with an owner and adoption date, (2) a captured learning that updates the playbook with an owner and date, or (3) an explicit accepted-loss note with rationale and the next time the topic is allowed to be raised. Anything else is a meeting, not a retro.

## Retention as Strategy Input

Retention deltas are leading indicators of strategy health. A 5-point drop in renewal rate is more strategically important than a 5-point miss on revenue this quarter, because the renewal drop will compound into next quarter's revenue miss while remaining easier to fix now than later. Pull retention into the quarterly review at the same level of weight as revenue.
