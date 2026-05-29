# Sequence 4 - Retention / Churn Prevention

Churn-risk-triggered save sequences. This sequence exists to catch accounts before they leave and to handle the moments where leaving becomes likely (downgrade, cancel-intent, failed payment). It is the most time-sensitive sequence after onboarding: a save window is measured in days, sometimes hours.

## When It Fires

| Trigger | Email / Flow | Urgency |
|---|---|---|
| `churn_risk_score >= 0.7` | "Are we missing something?" - survey + CS contact | Days |
| `subscription.downgraded` | "Welcome to the new plan - here is what you keep" | Hours (reduce regret/churn) |
| `subscription.cancel_initiated` (in-product) | Save flow - pause / discount / direct CS | Real-time |
| `payment.failed` | Dunning + card-update CTA | Real-time, then dunning ladder |
| `support.csat_low` AND `tenant_mrr > X` | CS-owner escalation, not automated email | Same business day |

Churn-risk score comes from `saas-growth-metrics` or `product-led-growth`. Threshold of 0.7 is the default; tune to your model's precision so you are not over-triggering on noisy scores.

## Entry / Exit Conditions

- **Entry:** any trigger above. Retention **pre-empts** Upgrade and Behavioral for the same user - a churn-risk user must never simultaneously receive an upsell.
- **Exit immediately if:**
  - `subscription.upgraded` or `subscription.renewed` fires (the account saved itself - stop instantly; see anti-patterns).
  - `cancel_initiated` is reversed (user clicks "keep my plan").
  - `churn_risk_score` drops back below 0.5 (hysteresis gap prevents flapping).
  - `subscription.cancelled` completes despite the save flow - hand off to Reactivation in 60-90d, do not keep pinging now.

## The Flows

### Churn-risk track (proactive)
```text
T+0   "Are we missing something?"
      Goal: diagnose, not sell. 1-question survey + a real CS reply-to.
      Branch on response:
        "pricing"      -> CS offers tailored plan / discount
        "missing X"    -> roadmap update or workaround + CS follow-up
        "not using it" -> re-onboarding / value email
        no response    -> T+3 follow-up below

T+3   "A hand from us" (only if no response and risk still >= 0.7)
      Goal: human touch. CS owner introduces themselves, offers a 15-min call.
      Branch: if risk < 0.5 -> exit (recovered).
```

### Cancel-initiated track (reactive, real-time)
```text
Real-time, in the cancel flow itself, mirrored by email:
  Step 1  Capture cancellation reason (mandatory dropdown).
  Step 2  Offer matched to reason:
            "too expensive"   -> pause subscription OR one-time discount
            "missing feature"  -> roadmap timeline + beta access
            "not using"        -> downgrade-to-free instead of full cancel
            "switching tool"   -> direct CS, export-help, win-back later
  Step 3  If cancel completes -> exit survey email, mark for Reactivation enrol +60d.
```

### Payment-failure (dunning) track
```text
T+0    Soft: "Your payment did not go through - update your card" (CTA to billing portal).
T+3    Reminder + reassurance access is not yet cut.
T+5    Warning: access pauses in 48h.
T+7    Final: access paused / downgraded; how to restore.
Exit on payment.succeeded at any step.
```

## Decision Table - Save Offer Selection

| Cancellation reason | Best offer | Failure mode of the wrong offer |
|---|---|---|
| Too expensive | Pause or targeted discount | Feature pitch ignores the real objection |
| Missing feature | Roadmap + beta access | A discount buys a few weeks, then they leave anyway |
| Not using it | Downgrade-to-free, re-onboard | Discounting an unused product just defers churn |
| Switching vendor | Graceful exit + data export | Aggressive discounting damages brand; they have already decided |
| Company shut down / off-boarding | Graceful exit, no offer | An upsell here is tone-deaf |

## Suppression & Frequency Capping

- Retention pre-empts all sequences except transactional and onboarding.
- Stop **instantly** on un-cancel, upgrade, renewal, or payment success - stale "we will miss you" mail to a saved customer destroys trust.
- Dunning emails are **transactional** (account/billing) and bypass marketing opt-out, but still honour hard bounces and global send caps.
- Churn-risk survey is `lifecycle` - honours opt-out.
- Cancellation reason capture is **mandatory**; without it, Reactivation cannot personalise later.

## Metrics & Targets

| Metric | Definition | Target |
|---|---|---|
| Save rate (cancel-intent) | Cancels averted / cancel_initiated | >= 15-30% |
| Dunning recovery rate | `payment.succeeded` / `payment.failed` involuntary | >= 40-70% |
| Churn-risk recovery | Risk back below 0.5 within 14d of enrol | tracked |
| Survey response rate | Responses / sent | >= 10% |
| Saved MRR | MRR retained attributable to flow | tracked monthly |

Involuntary churn (failed payments) is usually the largest, cheapest win - a well-tuned dunning ladder recovers 40-70% of failed charges. Measure it separately from voluntary save rate.

## Anti-Patterns

- Retention emails sent to users who **just renewed or upgraded** - the most common embarrassing bug; exit instantly on save.
- Defaulting to a discount for every cancellation reason - it trains price-sensitive users to threaten cancellation, and it does nothing for feature-gap or "not using it" churn.
- Not capturing the cancellation reason - the win-back sequence later has nothing to personalise on, so it fails.
- Treating dunning as marketing and suppressing it under a marketing opt-out - you silently lose recoverable revenue.
- Running Upgrade and Retention on the same churn-risk user - pitching more spend to someone leaving accelerates the exit.
- A dunning ladder with no exit on `payment.succeeded` - the customer who already fixed their card still gets the "access paused" warning.
- Flapping churn-risk scores re-triggering the sequence repeatedly - use a hysteresis gap (enter at 0.7, exit at 0.5).

## Sequence Config

```yaml
sequence: retention
version: 6
priority: 0                              # pre-empts all non-transactional sequences
tracks:
  churn_risk:
    entry: "churn_risk_score >= 0.70"
    exit:  "churn_risk_score < 0.50 OR subscription.upgraded OR subscription.renewed"
    category: lifecycle
    messages:
      - { id: r_survey, delay: 0 }
      - { id: r_human_hand, delay: 3d, require: "no_response AND risk >= 0.70" }
  cancel_intent:
    entry: "subscription.cancel_initiated"
    exit:  "cancel_reversed OR subscription.cancelled_completed"
    realtime: true
    require: capture_cancellation_reason   # mandatory dropdown
  dunning:
    entry: "payment.failed (involuntary)"
    exit:  "payment.succeeded"
    category: transactional               # bypasses marketing opt-out
    ladder: [0, 3d, 5d, 7d]
hysteresis: { enter: 0.70, exit: 0.50 }
```

## Copy Template - Cancel-Intent Save (reason = "too expensive")

```text
Subject:  Before you go - can we make this work?
Preheader: A couple of options that might help

Hi {first_name},

You started to cancel because of cost - thank you for being straight
with us. Two options before you decide:

1) Pause your subscription for up to 3 months. Your data stays put,
   nothing is billed, pick up exactly where you left off.
   [ Pause instead of cancel ]

2) Move to {cheaper_tier} and keep {features_retained}.
   [ Switch plan ]

Still want to cancel? [ Continue cancellation ] - we will export your
data for you, no hard feelings.
```

Match the offer to the captured reason (see decision table). Always include the no-friction "continue cancellation" path; a save flow that hides the exit button generates complaints and chargebacks, not saves.

## Dunning Ladder Detail

Involuntary churn is the cheapest revenue to recover. The ladder balances recovery against card-network retry limits.

| Step | Timing | Message | Card retry |
|---|---|---|---|
| 1 | T+0 (on fail) | Soft "update your card", reassure access intact | Retry in 24h |
| 2 | T+3 | Reminder, still no service interruption | Retry |
| 3 | T+5 | Warning: access pauses in 48h | Retry |
| 4 | T+7 | Access paused/downgraded; one-click restore | Final retry, then dunning ends |

Exit on `payment.succeeded` at any step and send a single "you are all set" confirmation. Smart-retry timing (align retries to payday, avoid weekends) lifts recovery materially - delegate retry scheduling to the billing system, not the email tool.

## Edge Cases

| Case | Handling |
|---|---|
| Churn-risk and cancel-intent fire together | Cancel-intent (real-time, concrete) takes over; pause the proactive survey track |
| Dunning succeeds then fails again same period | Treat as a new dunning entry only after a clean success; do not stack two ladders |
| User on annual plan downgrades to monthly | `subscription.downgraded` -> reassurance email, not a save flow; they are staying |
| CS already engaged the account manually | Suppress automated retention mail for that account; flag `cs_owned = true` to avoid stepping on the human |
| Voluntary cancel with reason "company closed" | Graceful exit, no offer, no Reactivation enrol - there is no one to win back |
