# Sequence 3 - Upgrade / Upsell / Expansion

The PQL-triggered upgrade flow. This is the sequence that turns product usage into expansion revenue. It fires on **product-qualified-lead signals** and hard plan gates - never on a calendar, never on "it's been 30 days, want to upgrade?". The discipline that separates this from spam is: only ask when the data says the user has hit a wall the next tier removes.

## When It Fires

| Trigger | Email | Why it qualifies |
|---|---|---|
| `usage.approaching_limit (90%)` on a **plan-tied** limit | "You are close to your limit - upgrade to keep moving" | Concrete, imminent wall |
| `gate.denied (feature=X)` repeated **3x in 7d** | "Try X free for 14 days" (in-app feature trial) | Demonstrated demand for a gated feature |
| `pql_score >= threshold` (Pro-tier behaviour on Free) | "It looks like you are ready for Pro" | Behavioural fit |
| `active_users / max_seats >= 0.8` | "Add 5 seats and save 20%" | Seat expansion signal |
| `subscription.annual_renewal in 30d AND usage_growth > 0` | "You have grown - lock in annual" | Expansion at renewal |

The single repeated `gate.denied` should **not** fire - one accidental click on a locked feature is not demand. Require the 3x/7d threshold so you only pitch features users genuinely keep reaching for.

## Entry / Exit Conditions

- **Entry:** PQL threshold crossed OR gate-denial threshold met OR seat-ratio threshold met. Contact must be on a plan **below** the target tier.
- **Exit immediately if:**
  - `tenant_plan` is already the highest tier (never pitch up from the top - see anti-patterns).
  - `subscription.upgraded` fires (route to "welcome to your new plan", end).
  - The triggering condition resolves on its own (user deletes data and drops below 90%).
  - `churn_risk_score >= 0.7` - a churn-risk user must go to Retention, not Upgrade. Pitching more spend to someone about to leave accelerates the exit.

## The Flow (PQL track)

```text
Day 0   PQL Trigger
        Goal: name the wall the user just hit, tie the next tier to removing it.
        Copy: "You created 480 of your 500 records this month" -> specific, data-led.
        Branch: if in-app session active today, prompt_dispatcher suppresses email, in-app fires instead.

Day 3   Value Reframe (only if no upgrade and no in-app conversion)
        Goal: ROI framing, not feature list. "Teams on Pro ship 2x faster" with a one-line proof.
        Branch: if subscription.upgraded -> end.

Day 7   Offer / Friction-Remover (only if still not upgraded)
        Goal: remove the last objection. Options (pick ONE per policy):
          - "Try Pro free for 14 days, no card"
          - "Talk to us about volume pricing" (for seat-expansion track)
        Branch: if upgraded -> end. If still on free after Day 7 -> exit, return to Behavioral.
```

Keep it to **three touches maximum**. Upgrade pressure that runs longer reads as nagging and inflates unsubscribes among your most valuable (high-usage) users.

## Coordination with In-App Prompts

This sequence collides most often with in-app upsell prompts. The rule:

```text
On upgrade_signal_for_user:
  prompt_dispatcher.check(user, context="upgrade", window=24h)
  if in_app_session_active:
      fire in-app prompt; suppress email for this context today
  else:
      fire email; suppress in-app for 24h after click
```

Both channels read and write the same `prompt_dispatcher` state keyed on `(user_id, upgrade_context, day)`. Without it, the user sees the identical upgrade nudge in-app and by email within minutes - the canonical double-fire bug.

## Suppression & Frequency Capping

- Never enrol top-tier plans.
- Never enrol while `churn_risk_score >= 0.7`.
- Max 3 upgrade touches per qualifying event; min 14d cooldown before the same user can re-enter on a new signal.
- Honour `marketing`/`lifecycle` category opt-out (upgrade pitches are not transactional - they must respect opt-out).
- Suppress the email-channel touch on any day an in-app upgrade prompt fired.

## Metrics & Targets

| Metric | Definition | Target |
|---|---|---|
| PQL -> upgrade conversion | `subscription.upgraded` within 14d of enrol | >= 5-8% |
| Net expansion revenue | MRR delta from upgrades attributed to sequence | tracked monthly |
| Unsubscribe rate | Opt-outs / sent | < 0.4% |
| Incremental MRR vs hold-out | Treatment minus 5% hold-out, per signal | Positive |

Attribute revenue with the `send_id` lineage: sum `subscription.upgraded` MRR delta within 7d post-click, net of the hold-out cohort's organic upgrade rate. Report **incremental** MRR, not gross - many high-PQL users upgrade anyway.

## Anti-Patterns

- Upgrade emails sent to users already on the **highest plan** - annoying, and it corrupts attribution because there is nothing to convert.
- Firing on a single `gate.denied` (one stray click) instead of the 3x/7d threshold - pitching features the user does not actually want.
- Pitching an upgrade to a `churn_risk_score >= 0.7` user - Retention must own them; asking for more money speeds the churn.
- More than three touches - high-usage users (your best customers) get nagged and opt out.
- Calendar-based "you've been a customer 30 days, upgrade?" with no usage signal - that is acquisition spam, not PQL.
- No `prompt_dispatcher` - in-app and email upgrade prompts double-fire within minutes.
- Reporting gross upgrade revenue with no hold-out - you take credit for upgrades that would have happened anyway and can never prove incremental lift.

## Sequence Config

```yaml
sequence: upgrade
version: 4
entry:
  any_of:
    - "usage.approaching_limit AND limit.plan_tied AND pct >= 0.90"
    - "gate.denied(feature=X) count >= 3 within 7d"
    - "pql_score >= pql_threshold AND tenant_plan < target_tier"
    - "active_users / max_seats >= 0.80"
  guards:
    - tenant_plan < highest_tier          # never pitch up from the top
    - churn_risk_score < 0.7              # churn-risk -> retention, not upsell
    - marketing_consent == true
exit:
  any_of:
    - event: subscription.upgraded        # -> welcome_to_new_plan, end
    - condition_resolved: true            # user dropped below 90%, etc.
    - churn_risk_score >= 0.7             # hand to retention
    - touches_sent >= 3
frequency:
  category: lifecycle
  max_touches: 3
  re_entry_cooldown: 14d
  priority: 1                            # above behavioral, below retention
coordination:
  prompt_dispatcher:
    context: upgrade
    rule: "in_app_session_active -> in_app, suppress email today"
messages:
  - { id: u0_named_wall, delay: 0 }
  - { id: u1_value_reframe, delay: 3d, skip_if: subscription.upgraded }
  - { id: u2_friction_remover, delay: 7d, skip_if: subscription.upgraded }
```

## Copy Template - T+0 Named Wall (PQL/limit trigger)

```text
Subject:  You are at {usage_current} of {usage_limit} {unit}
Preheader: Here is what {next_tier} unlocks

Hi {first_name},

You have used {usage_current} of your {usage_limit} {unit} this {period}.
At your current pace you will hit the ceiling in about {days_to_limit} days.

{next_tier} removes that limit and adds {one_concrete_benefit}.

[ See {next_tier} ]      <- single CTA to the plan page, pre-selected tier

Not ready? Reply and tell us what you need - we will help you make the
most of your current plan.
```

Lead with the user's own number, not a feature list. "480 of 500 records" converts; "Upgrade for more power" does not. The data proves the wall is real and imminent.

## Worked Example - PQL Score Composition

A PQL score that drives this sequence should be auditable, not a black box. Example weighting for a Free-to-Pro pitch:

```text
pql_score = 0.35 * (weekly_active_days / 5)
          + 0.25 * (distinct_pro_relevant_features_used / 4)
          + 0.20 * (teammates_invited >= 1 ? 1 : 0)
          + 0.20 * (min(usage_pct_of_free_limit, 1.0))

Enrol when pql_score >= 0.65 AND tenant_plan == free.
```

Tie the score to behaviours the next tier actually serves (collaboration, volume, gated features). A score built on generic "engagement" pitches upgrades to people whose usage the higher plan does not change - low conversion, high annoyance.

## Edge Cases

| Case | Handling |
|---|---|
| User is mid-onboarding (trial) and hits a limit | Onboarding's trial-end conversion owns the ask; suppress Upgrade until trial resolves |
| Seat-ratio and PQL both trigger same week | Pick the higher-value path (usually seats for B2B); do not run two upgrade flows in parallel |
| User upgrades via sales, not self-serve, mid-flow | `subscription.upgraded` exits the flow regardless of channel; never keep pitching a closed deal |
| Annual renewal approaching + growth | Route to the renewal-expansion message, not the generic PQL flow - timing and framing differ |
| In-app prompt converted yesterday | `prompt_dispatcher` records the conversion; email flow exits, no T+3 follow-up |
