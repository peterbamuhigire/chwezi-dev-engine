# Sequence 1 - Welcome & Onboarding

The branched welcome flow with an activation check. The single highest-leverage sequence in the catalogue: it owns the trial-to-activation conversion, which is the strongest predictor of revenue retention. Get this wrong and every downstream sequence inherits a smaller, weaker audience.

## When It Fires

| Entry trigger | Enrol? | Rationale |
|---|---|---|
| `user.signed_up` (single-user signup) | Yes | Standard path |
| `tenant.created` with >=2 users in 60s | Yes, enrol the owner only | Avoid 4 welcome emails to one team |
| `user.signed_up` AND `tenant_plan != free` | No - route to enterprise onboarding | Paid trials get a CS-led flow, not drip |
| `user.invited_teammate` accepted | No - route to teammate-join micro-flow | Invitees already have context |

Fire on the **owner/admin** contact. Members who join later get a 2-email teammate orientation, not the full sequence.

## Exit Conditions

Exit (and stop all remaining sends) the moment any of these is true:

- `subscription.created` fires (route to "welcome to paid", then end).
- `user.activated` AND `feature.X.used_repeat` past T+3d (user is clearly in-product; further nudges read as robotic).
- Explicit unsubscribe from the `lifecycle` category.
- `tenant.deleted` or hard bounce.

Do **not** exit merely on a single `user.activated`. One activation event is not stickiness; keep the value-reinforcement emails running until repeat usage confirms the habit.

## The Messages

```text
T+0       Welcome
          Goal: confirm signup, deliver the ONE core CTA, set expectations.
          Copy structure: 1 sentence welcome / 1 CTA button to the aha-moment action / 1 line on what happens next.
          Send instantly (<60s) via the lifecycle stream, NOT the transactional stream.

T+1d      Getting Started
          Goal: the concrete first step toward activation.
          Branch: if user.activated already -> skip, jump to T+3 power-feature branch.

T+3d      Feature Discovery
          Goal: surface one high-value feature the user has not touched.
          Branch on user.activated:
            activated     -> "you are flying" + next power-feature
            not activated -> "having trouble? here is the 2-minute version" + support offer

T+5d      Social Proof
          Goal: reduce risk via a case study from a similar firmographic (match on industry/company_size).
          Branch: suppress for self-serve free-tier where no case study segment matches.

T+7d      Activation Check
          Branch on user.activated:
            activated     -> "next milestone" + invite-a-teammate CTA
            not activated -> human support offer (reply-to a real inbox) + troubleshooting doc

T+(trial-3)  Trial-End Warning
          Goal: value-led, not fear-led. "Here is what you have built / done so far."
          Only sends if trial.started exists and trial.converted does not.

T+trial   Trial-End Conversion
          Goal: paywall CTA + offer.
          Branch on subscription.created  -> "welcome to paid", end sequence.
          Branch on no subscription       -> downgrade-to-free OR one-time 7-day extension (pick one per policy).
```

Adjust absolute days to the trial length. For a 14-day trial the cadence above is correct; for a 7-day trial, compress to T+0 / T+1 / T+3 / T+5 / T+6 and drop the social-proof email.

## Branch Decision Table

| Signal at checkpoint | Branch taken | Failure mode if you do not branch |
|---|---|---|
| `user.activated = true` at T+3 | Power-feature track | Sending "getting started" to an active user looks broken; trust erodes |
| `user.activated = false` at T+7 | Human-support track | Generic case study to a stuck user feels tone-deaf; they churn silently |
| `subscription.created` mid-trial | End + paid welcome | Continuing to send "convert now" to a paying customer is the classic embarrassing bug |
| No login since T+0 | Re-onboard / different first-step copy | Assuming progress that never happened wastes the whole sequence |

## Suppression & Frequency Capping

- Skip entirely if `tenant_plan != free` at signup (paid trials -> enterprise onboarding).
- Honour `lifecycle` category unsubscribe; transactional confirmations still send.
- Respect the global cap: max 1 lifecycle email / user / 24h. If a behavioral email is also queued today, onboarding wins (it is time-sensitive to the trial clock).
- Coordinate with in-app via `prompt_dispatcher`: if the in-app product tour fired the same lesson today, suppress that day's email.

## Metrics & Targets

| Metric | Definition | Target (median B2B SaaS) |
|---|---|---|
| Activation rate | `user.activated` within trial window, enrolled cohort | >= 40% |
| T+0 open rate | Welcome email opens | >= 60% (it is wanted mail) |
| T+0 -> first action CTR | Click on the core CTA | >= 25% |
| Trial-to-paid conversion | `subscription.created` / enrolled | >= 10-15% self-serve |
| Incremental lift | Treatment vs 5% hold-out cohort activation delta | Positive and significant |

Maintain a 5% random hold-out that receives **no** onboarding emails. If activation in the treatment cohort is not measurably higher, the sequence is decorative - fix the copy/timing or kill emails that show no lift.

## Anti-Patterns

- Welcome email sent **after** the user has already activated and explored the product - looks robotic and damages trust on the very first touch.
- Treating the welcome email as transactional and sending it from the no-reply transactional stream - it loses the reply-to and the human voice that drives early engagement.
- A flat T+1/T+3/T+5 drip with no activation branch - stuck users and power users get identical mail; both feel unseen.
- Trial-end email that fires regardless of `trial.converted`, hitting customers who already paid.
- Sending the full sequence to every member of a 10-person team that signed up together - one tenant, ten inboxes, one annoyed admin.
- No hold-out cohort - you cannot prove the sequence earns its place, so it ossifies forever.

## Sequence Config (Customer.io / Braze shape)

A machine-readable spec the email tool and engineering can both reason about. Keep this in version control alongside the product, not buried in the ESP UI.

```yaml
sequence: welcome_onboarding
version: 3
entry:
  trigger: user.signed_up
  guards:
    - tenant_plan == "free"        # paid trials route to enterprise_onboarding
    - role in [owner, admin]
    - lifecycle_consent == true
exit:
  any_of:
    - event: subscription.created      # -> welcome_to_paid, end
    - event: user.activated AND feature.X.used_repeat AND days_since_signup > 3
    - event: unsubscribe(category=lifecycle)
    - event: tenant.deleted
    - hard_bounce == true
frequency:
  category: lifecycle
  global_cap_per_24h: 1
  priority: 2                         # below retention(0) and upgrade(1)
messages:
  - id: w0_welcome
    delay: 0
    stream: lifecycle                 # NOT transactional; keep reply-to human
    reply_to: founders@example.com
  - id: w1_getting_started
    delay: 1d
    skip_if: user.activated
  - id: w3_feature_discovery
    delay: 3d
    branch_on: user.activated
    branches: { true: w3_flying, false: w3_help }
  - id: w5_social_proof
    delay: 5d
    skip_if: no_matching_case_study_segment
  - id: w7_activation_check
    delay: 7d
    branch_on: user.activated
    branches: { true: w7_next_milestone, false: w7_support_offer }
  - id: wt_trial_warning
    delay: "trial_end - 3d"
    require: trial.started AND NOT trial.converted
  - id: wt_conversion
    delay: "trial_end"
    branch_on: subscription.created
    branches: { true: welcome_to_paid_END, false: downgrade_or_extend }
```

## Copy Template - T+0 Welcome

Structure, not prose. One job per block; one primary CTA. Keep under 120 words above the fold.

```text
Subject:  You are in - here is your first step
Preheader: 2 minutes to your first {core_outcome}

Hi {first_name},

Welcome to {product}. Most teams get their first {core_outcome}
in under two minutes - here is how:

[ {primary_cta_label} ]      <- single button, links to the aha-moment action

That is the whole job for today. Tomorrow we will show you {next_step}.

Reply to this email if you get stuck - a real person reads it.
- {founder_first_name}, {role}
```

Forbidden in the welcome email: a feature tour, multiple CTAs, a discount, a "follow us on social" footer that competes with the core CTA. Every element that is not the primary action lowers click-through.

## Edge Cases

| Case | Handling |
|---|---|
| User signs up, never confirms email (double opt-in) | Confirmation is transactional and sends regardless; the lifecycle flow waits for confirmation before T+1 |
| Two signups, same email, different tenants | Enrol once per `(email, tenant_id)`; dedupe on the contact key so they are not double-mailed |
| User activates within minutes of signup | T+0 still sends (it is a welcome, not a nudge); T+1 onward branches to the power-feature track immediately |
| Trial extended by CS mid-flow | Recompute `trial_end`-relative delays; re-anchor wt_warning and wt_conversion to the new date |
| Signup during a deliverability throttle | Welcome (lifecycle) is high-value; let it through the throttle ahead of behavioral/reactivation batches |
