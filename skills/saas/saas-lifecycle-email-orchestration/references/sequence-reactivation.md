# Sequence 5 - Reactivation

The long-dormant win-back. This sequence targets users who have already gone quiet - past the Behavioral nudge window, and either churned or effectively abandoned. It is the riskiest sequence for deliverability: dormant addresses are where spam traps, bounces, and complaints concentrate. Run it with discipline or it will poison your sending reputation for the whole catalogue.

## When It Fires

| Entry trigger | Enrol? | Notes |
|---|---|---|
| `last_login_date < now - 60d` (active free/paid, no churn) | Yes | The dormant-but-subscribed case |
| `subscription.cancelled` completed | Yes, **+60d after cancel** | Give space; immediate win-back is annoying |
| `last_login_date < now - 60d AND already in Behavioral` | No - Behavioral exits first | Windows must be disjoint |
| Hard bounce or spam complaint ever recorded | No - permanent suppression | Re-mailing these wrecks reputation |
| `unsubscribed_categories includes lifecycle/marketing` | No | Legal liability + spam |

The 60-day threshold is configurable per product (a weekly-use tool dormancy starts sooner than a quarterly-use tool). Set it to roughly 3x the median active-usage interval.

## Entry / Exit Conditions

- **Entry:** dormancy threshold crossed AND address is mailable (no bounce/complaint history) AND `lifecycle` consent intact.
- **Exit immediately if:** `user.logged_in` fires (re-engage - route back to Behavioral / re-onboarding), OR the user clicks any CTA and returns, OR explicit unsubscribe.
- **Terminal exit:** if the full sequence completes with no engagement, mark `permanently_dormant` and move the contact to **broadcast-only suppression** - they receive no further automated lifecycle mail, only major product announcements (if at all).

## The Messages

```text
T+60d   "We miss you"
        Goal: emotional, value-led re-entry. Remind them what they built / achieved.
        Copy: warm, 1 CTA back into the product. No discount yet.

T+67d   "What is new"
        Goal: features and improvements shipped since they left.
        Personalise on cancellation_reason if available:
          reason="missing feature" AND feature now shipped -> lead with that feature.
        Branch: if logged_in -> exit (recovered).

T+74d   "Special offer"
        Goal: lower the cost of return.
        Options (pick ONE per policy):
          - discount on return
          - extended free use / restored trial
          - "restore your data" (data still retained, one click to resume)
        Branch: if logged_in or subscription restored -> exit.

T+81d   "Final goodbye"
        Goal: last chance + a clean, respectful exit.
        Explicitly offer to fully unsubscribe / delete data.
        After send -> mark permanently_dormant, move to broadcast-only suppression.
```

Four touches over three weeks is the ceiling. More than that, to people who have ignored you for two months, is how you collect spam complaints.

## Decision Table - Mail or Suppress

| Dormant contact state | Action | Failure mode of the wrong choice |
|---|---|---|
| 60d dormant, mailable, consented | Run the 4-email flow | (correct) |
| Ever hard-bounced | Permanent suppress | Re-mailing dead addresses spikes bounce rate, throttles the IP |
| Spam complaint on file | Permanent suppress | Re-mailing complainers is a direct path to blocklisting |
| Cancelled <60d ago | Wait | Immediate win-back reads as desperate |
| Engaged with email 2 (clicked) | Exit, route to re-onboarding | Continuing the "goodbye" track to a returning user is jarring |
| Completed flow, no engagement | Mark permanently_dormant | Keep mailing and you train the mailbox provider to junk you |

## Suppression & Frequency Capping

- **Consent is the hard gate.** Reactivation must obey transactional/lifecycle/marketing consent absolutely - pinging explicit unsubscribers is a legal liability and a spam violation.
- Permanently suppress any address with a prior hard bounce or complaint **before** enrolling - do not "test" dormant addresses.
- Max 4 emails, ~7d apart. No re-entry: once a contact is `permanently_dormant`, they do not re-enter the sequence on a later dormancy tick.
- Send dormant batches at low volume on a warmed-up reputation; never blast the entire dormant list at once.
- Honour the global cap and any active deliverability throttle.

## Metrics & Targets

| Metric | Definition | Target |
|---|---|---|
| Reactivation rate | `user.logged_in` within 14d of any email | >= 5-10% |
| Win-back conversion | Resubscribed / enrolled (for churned cohort) | >= 2-5% |
| Bounce rate | Bounces / sent | < 2% (above this, pause and clean the list) |
| Spam-complaint rate | Complaints / delivered | < 0.1% (above this, stop immediately) |
| Unsubscribe rate | Opt-outs / sent | Expected higher (~1-2%); that is healthy list-cleaning |

Reactivation deliberately surfaces unsubscribes - that is a feature, not a bug. Each opt-out removes an unengaged address that was dragging your sender reputation down. Watch bounce and complaint rates like a hawk; they are the canaries.

## Anti-Patterns

- Reactivation emails that ping **explicit unsubscribers** - legal liability plus spam complaints that damage the whole catalogue's deliverability.
- Enrolling addresses with prior hard bounces or complaints - the fastest way to get an IP/domain blocklisted.
- Blasting the entire dormant list in one send - a reputation cliff; spread it across a warmed schedule.
- Win-back the day after cancellation - desperate, and it ignores the reason they left; wait 60d.
- Ignoring `cancellation_reason` when personalising "what is new" - you re-pitch the exact gap that drove them out.
- No terminal `permanently_dormant` state - the same dead contacts get re-mailed every dormancy cycle, steadily degrading sender reputation.
- Treating reactivation send-volume as free - every dormant send carries deliverability risk that lands on your active, revenue-generating mail.

## Sequence Config

```yaml
sequence: reactivation
version: 3
entry:
  any_of:
    - "days_since_last_login >= 60"
    - "subscription.cancelled_completed AND days_since_cancel >= 60"
  guards:
    - never_hard_bounced == true        # permanent suppress otherwise
    - never_complained == true
    - lifecycle_consent == true
    - NOT in_sequence(behavioral)        # windows must be disjoint
exit:
  any_of:
    - event: user.logged_in              # -> re-onboarding, end
    - event: subscription.restored
    - event: unsubscribe
    - completed_with_no_engagement -> set lifecycle_stage = permanently_dormant
frequency:
  category: lifecycle
  max_touches: 4
  spacing: 7d
  re_entry: never                        # no re-enrol once permanently_dormant
  send_mode: warmed_batch                # low volume, never blast
deliverability_guards:
  pause_if: "batch_bounce_rate > 0.02 OR batch_complaint_rate > 0.001"
messages:
  - { id: rc_miss_you, delay: 0 }        # T+60d, emotional, no discount
  - { id: rc_whats_new, delay: 7d, personalise_on: cancellation_reason }
  - { id: rc_offer, delay: 14d }
  - { id: rc_goodbye, delay: 21d, then: mark_permanently_dormant }
```

## Copy Template - T+0 "We Miss You"

```text
Subject:  Your {product} data is still here, {first_name}
Preheader: Pick up right where you left off

Hi {first_name},

It has been a while. Your {artifacts_summary} are exactly as you
left them - nothing was deleted.

A lot has changed since {last_active_month}. Want to take another look?

[ Open my workspace ]      <- deep-link, restores their actual data

No pressure - if {product} is not for you, this is the last thing
we will send for a while.
```

Reassurance ("your data is still here") outperforms novelty for the first win-back touch. The fear of having lost work is a stronger return motivator than a feature list. Save the feature news for T+7.

## Deliverability Discipline

Reactivation is where reputation goes to die if run carelessly. Treat the dormant list as radioactive:

| Rule | Threshold | Action if breached |
|---|---|---|
| Pre-flight list hygiene | Validate all addresses (e.g. via verification API) before send | Drop invalid/risky before enrolment |
| Batch size | <= 5-10% of your healthy daily volume per dormant batch | Split across days |
| Bounce rate | > 2% on a batch | Pause sequence, clean list, investigate source |
| Complaint rate | > 0.1% on a batch | Stop immediately; the segment is too cold |
| Dedicated IP/subdomain | Send reactivation from a separate subdomain | Isolates risk from transactional/onboarding mail |

Sending dormant batches on the same IP as your transactional mail lets one cold batch drag your password-reset and receipt deliverability down with it. Isolate the risk.

## Edge Cases

| Case | Handling |
|---|---|
| User logs in after rc_miss_you but before rc_whats_new | Exit immediately -> re-onboarding flow, not the "goodbye" track |
| Dormant user is on a paid (non-cancelled) plan | Still enrol at 60d inactivity; a paying-but-absent user is a churn risk worth re-engaging |
| Address fails verification at pre-flight | Do not enrol; mark `unmailable`, exclude from all future sends |
| User completed the flow last quarter, dormant again | No re-entry; `permanently_dormant` is terminal - they only receive major broadcasts, if any |
| Cancellation reason was "switched vendor" | Lead rc_whats_new with what changed vs that competitor, if known; otherwise standard copy |
