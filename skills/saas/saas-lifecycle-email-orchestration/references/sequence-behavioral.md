# Sequence 2 - Behavioral & Lifecycle

Feature-discovery, approaching-limit, and inactivity nudges. Unlike onboarding (a fixed-length flow on the trial clock), behavioral emails are **stateless reactions** to what a user does or fails to do in-product. There is no T+N schedule - each email fires on a precise event condition and then stops.

## When It Fires

Behavioral emails are triggered by event **presence** or **absence**. The audience is users who have completed onboarding (`user.activated = true`) and are in the active body of the lifecycle. A user can be enrolled in many behavioral triggers simultaneously; the frequency cap (below) decides which actually sends.

## Entry / Exit Conditions

- **Entry:** the specific trigger condition for each email evaluates true at the daily/streaming evaluation tick.
- **Exit:** the condition no longer holds (e.g., the user logs in, so the inactivity email is cancelled), OR the email has already sent within its cooldown window, OR the user is enrolled in a higher-priority sequence (Retention or Upgrade pre-empt Behavioral nudges for the same context).
- **Hard gate:** never enrol a user who is `churned` or `permanently_dormant` - those belong to Reactivation.

## The Triggers

| Email | Trigger condition | Goal | Cooldown |
|---|---|---|---|
| "Try the X feature" | `user.activated AND NOT feature.X.used_first_time AND days_since_signup >= 7` | Drive feature depth | 30d per feature |
| "Approaching your limit" | `usage.approaching_limit` at 80% of a non-plan-tied limit | Prevent silent failure | 7d |
| "We noticed you have not logged in" | `last_login_date < now - 14d AND last_login_date >= now - 30d` | Re-engage before dormancy | 14d |
| "Your team is collaborating" | `collaboration_event_count >= 5 in last 7d` | Positive reinforcement | 14d |
| "How can we help?" | `support.csat_low recent OR repeat-failed-action >= 3 in 24h` | Rescue a frustrated user | 7d |
| "You unlocked a milestone" | crossing a usage threshold (e.g. 100th record created) | Habit reinforcement | per-milestone, once |

Note the boundary: a non-login window of 14-30 days is **Behavioral**; beyond 60 days it becomes **Reactivation**. Keep the windows disjoint so a user is never in both at once.

## Decision Table - Nudge vs Stay Silent

| Situation | Action | Failure mode of the wrong choice |
|---|---|---|
| User skipped feature X but uses Y heavily | Nudge X **only if X complements Y** | Pushing irrelevant features trains users to ignore your mail |
| 80% of a soft limit (not plan-tied) | Behavioral warning | Treating it as an upgrade trigger annoys users who just need to clean up data |
| 90% of a **plan-tied** limit | Hand off to Upgrade sequence, do NOT send behavioral | Two emails about the same limit double-fire and confuse |
| Inactive 14d but mid-trial | Onboarding owns this, stay silent | Behavioral nudge competes with the onboarding clock |
| Low CSAT after support ticket | "How can we help" within 24h | Silence after a bad experience reads as indifference |

## Suppression & Frequency Capping

- Event-driven only; **never** a calendar blast.
- Hard cap: **2 behavioral emails / user / week**, max **1 / 24h**.
- Priority when multiple fire the same day: Retention > Upgrade (plan-tied) > Behavioral. The loser waits in queue or is dropped if stale.
- Suppress any behavioral nudge if the matching in-app prompt fired today (`prompt_dispatcher` check).
- Always honour `lifecycle` category unsubscribe.

## Metrics & Targets

| Metric | Definition | Target |
|---|---|---|
| Feature adoption lift | Adoption of feature X in nudged vs hold-out | +5-10pp |
| Reactivation-on-14d | Login within 72h of inactivity nudge | >= 20% |
| Unsubscribe rate per email | Lifecycle opt-outs / sent | < 0.3% |
| Spam-complaint rate | Complaints / delivered | < 0.08% |

Per-trigger hold-out (5%) is essential here: behavioral mail is the easiest to over-send. If the "try feature X" nudge shows no adoption lift over hold-out, kill it.

## Anti-Patterns

- Running behavioral emails on a fixed weekly calendar instead of on the event - the entire point is reactivity; a calendar drip is just spam with extra steps.
- Sending the "approaching limit" behavioral email for a **plan-tied** limit, when the Upgrade sequence should own that context - double-firing about the same limit.
- No cooldown - a flapping `usage.approaching_limit` event (user hovers at 79-81%) fires the same email five times in a week.
- Nudging a user toward a feature they cannot access on their plan - frustration plus a wasted send; that should be a `gate.denied` Upgrade trigger instead.
- Letting Behavioral and Reactivation windows overlap so a 65-day-inactive user gets both a "we noticed you haven't logged in" and a "we miss you" email.
- Positive-reinforcement emails ("your team is collaborating") with a hidden upsell CTA - it poisons the goodwill and trains users to distrust praise.

## Trigger Config

Each behavioral email is an independent, stateless rule. Define them declaratively so engineering can unit-test the conditions against the event stream.

```yaml
sequence: behavioral
version: 5
shared_guards:
  - user.activated == true
  - lifecycle_stage in [activated, paid]
  - churn_risk_score < 0.7        # churn-risk -> retention owns the user
  - days_since_signup > 7         # let onboarding finish first
frequency:
  category: lifecycle
  cap_per_week: 2
  cap_per_24h: 1
  priority: 3                     # loses to retention(0), upgrade-plan-tied(1)
triggers:
  - id: try_feature_x
    when: "NOT feature.X.used_first_time"
    cooldown: 30d
    goal: feature_depth
  - id: approaching_soft_limit
    when: "usage.approaching_limit AND limit.plan_tied == false AND pct >= 0.80"
    cooldown: 7d
  - id: inactivity_14d
    when: "14d <= days_since_last_login < 30d"   # disjoint from reactivation (>=60d)
    cooldown: 14d
    cancel_on: user.logged_in
  - id: collaboration_praise
    when: "collaboration_event_count_7d >= 5"
    cooldown: 14d
    rules: ["no_upsell_cta"]      # praise only; never bolt on an ask
  - id: help_offer
    when: "support.csat_low_recent OR repeat_failed_action_24h >= 3"
    cooldown: 7d
  - id: milestone
    when: "usage_threshold_crossed"
    cooldown: once_per_milestone
```

## Copy Template - Inactivity Nudge (T+14d no login)

```text
Subject:  Your {product} workspace is waiting
Preheader: Pick up where you left off

Hi {first_name},

You set up {last_meaningful_artifact} two weeks ago and have not
been back. Here is the one thing worth 60 seconds today:

[ {context_specific_cta} ]     <- deep-link to where they left off, not the homepage

If something got in the way, reply and tell us - we will fix it.
```

The CTA must deep-link to the user's own work (the artifact named in the body), not a generic homepage. A nudge that lands on a blank dashboard re-creates the friction that caused the lapse.

## Worked Example - Limit Warning Disambiguation

A project-management tool has a 500-task limit on the Free plan and a "5 GB attachment" soft cap on every plan.

| Signal | Which sequence owns it | Email |
|---|---|---|
| Free user hits 450/500 tasks (plan-tied) | Upgrade (90% rule) | "Upgrade to keep adding tasks" |
| Any user hits 4 GB/5 GB attachments (soft, all plans) | Behavioral (80% rule) | "You are nearing your storage - here is how to free space" |
| Paid Pro user hits 4 GB/5 GB | Behavioral | Same storage-hygiene email |

The discriminator is `limit.plan_tied`. Plan-tied limits are an expansion opportunity (Upgrade); universal soft limits are an operational warning (Behavioral). Mislabel them and you either upsell users who cannot fix the problem by paying, or you fail to monetise a genuine wall.

## Edge Cases

| Case | Handling |
|---|---|
| User triggers three behavioral rules in one day | Frequency cap sends only one (highest-value), queues nothing stale; the rest re-evaluate next tick |
| `usage.approaching_limit` flaps 79-81% | Cooldown plus a hysteresis band (fire at 80%, do not re-arm until <70%) prevents repeat sends |
| User logs in after inactivity email queued but before send | `cancel_on: user.logged_in` voids the queued send - never mail "we miss you" to someone already back |
| Member (not owner) triggers a feature nudge | Allowed; behavioral mail is per-user, unlike onboarding which targets the owner |
| Two events of the same rule within cooldown | Suppress the second; the cooldown timer is per `(user_id, trigger_id)`, not global |
| User in a deliverability throttle window | Behavioral is low priority; defer behind onboarding/transactional, drop if it ages past relevance |

## Testing the Triggers

Because each trigger is a pure predicate over the event stream, it should be unit-tested in CI, not hand-checked in the ESP. Minimum coverage per trigger:

```text
1. Fires when the condition is exactly met (boundary: pct == 0.80, day == 14).
2. Does NOT fire one step before the boundary (pct == 0.79, day == 13).
3. Respects the cooldown (second matching event inside the window -> no send).
4. Respects shared guards (churn_risk >= 0.7 -> no send even if condition met).
5. Cancels correctly (inactivity send voided by an intervening user.logged_in).
```

A trigger with no automated test is a future double-fire incident. Treat the `triggers:` config as code: review it, version it, test it - never edit it live in the ESP console where nobody can diff the change.
