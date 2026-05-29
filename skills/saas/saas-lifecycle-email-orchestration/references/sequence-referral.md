# Sequence 6 - Referral

NPS-promoter and active-user referral. This sequence converts happy, sticky customers into an acquisition channel. The discipline that makes it work: only ask people who are demonstrably getting value **right now**. Ask too early, ask the wrong people, or ask too often, and the referral request reads as needy and the goodwill evaporates.

## When It Fires

| Entry trigger | Enrol? | Why it qualifies |
|---|---|---|
| `nps_score >= 9` recorded within last 14d | Yes | Active promoter, freshest possible signal |
| `active_user >= 30d sustained AND tenant_plan = paid` | Yes | Proven, retained value |
| Milestone reached (e.g. "100th project", "1 year") | Yes, one-off | Natural celebratory moment to ask |
| `nps_score <= 6` (detractor) | No - route to Retention | Asking a detractor to refer is tone-deaf and surfaces their complaint publicly |
| `churn_risk_score >= 0.5` | No | Do not ask someone wavering to vouch for you |
| Trial / free / unactivated | No | They have nothing to vouch for yet |

The promoter signal is the strongest. Strike while the NPS response is fresh - a 9/10 from three months ago is stale; the person may feel differently now.

## Entry / Exit Conditions

- **Entry:** promoter score OR sustained-active-paid OR milestone, AND not a detractor, AND not churn-risk.
- **Exit:** the user submits a referral / invite (route to a thank-you + reward-tracking flow), OR explicit opt-out, OR `churn_risk_score` rises above 0.5 mid-sequence (stop asking).
- **Cooldown:** a user who completes (or ignores) the sequence does not re-enter for 90d, even on a fresh trigger. Referral fatigue is real.

## The Messages

```text
T+0   "You are getting value -- would you tell a friend?"
      Goal: the ask, framed around their success. Link to the in-app invite flow (not a raw mailto).
      Copy: "You have shipped 40 projects this quarter. Know a team who would benefit?"
      Branch: if referral submitted -> thank-you flow, exit.

T+5   "Give X, get X" (only if no referral yet)
      Goal: introduce the two-sided incentive.
      Copy: clear value on both sides -- "Give a friend $50 credit, get $50 when they subscribe."
      Branch: if referral submitted -> thank-you flow, exit.

T+12  "One-click invite" (only if still no referral)
      Goal: remove all friction. Pre-filled invite link, share-to-Slack/LinkedIn buttons.
      Branch: if no action -> exit, set 90d cooldown.
```

For enterprise / high-MRR accounts, replace the self-serve flow with a **champion-program invite**: a personal note from CS offering case-study collaboration, advisory-board membership, or co-marketing - referral by relationship, not by coupon.

## Decision Table - Who and How to Ask

| Customer profile | Referral mechanism | Failure mode of the wrong choice |
|---|---|---|
| Self-serve promoter (NPS 9-10) | Two-sided incentive, in-app invite | A formal champion ask overwhelms a small customer |
| Enterprise / high MRR | Champion program, CS-led, case study | A "$50 credit" coupon is beneath them and cheapens the brand |
| Active but neutral (NPS 7-8) | Soft milestone celebration, light ask | A hard incentive push to a lukewarm user falls flat |
| Detractor (NPS <= 6) | No referral ask -> Retention | Asking them to advocate amplifies their dissatisfaction |
| Wavering (churn-risk rising) | No ask | Asking a leaving customer to vouch is incoherent |

## Coordination with Other Sequences

- Referral **never** overlaps Retention or Upgrade for the same user - a happy promoter being simultaneously upsold and asked to refer feels transactional. Sequence the asks: value first, then at most one ask per window.
- The in-app invite flow and the email ask share `prompt_dispatcher` state so the user is not asked to refer in two channels the same day.
- Honour the global cap (1 lifecycle email / 24h); referral is the lowest priority and yields to Onboarding, Retention, and Upgrade.

## Suppression & Frequency Capping

- Never enrol detractors, churn-risk, trial, or unactivated users.
- 90d cooldown after completion or exit; no rapid re-asking.
- Max 3 touches per enrolment.
- Honour `marketing`/`lifecycle` opt-out - a referral ask is not transactional.
- Suppress the email touch on any day the in-app referral prompt fired.

## Metrics & Targets

| Metric | Definition | Target |
|---|---|---|
| Referral participation | Invites sent / enrolled | >= 5-10% |
| Referral conversion | New paid signups / invites sent | >= 1-3% |
| Viral coefficient (k) | New users generated per existing user via referrals | track; >0.1 is meaningful |
| Promoter ask response | Invite-flow opens / sent | >= 20% (these are happy users) |
| CAC vs other channels | Cost per referred acquisition | Should be lowest of all channels |

Attribute referred signups back to the referring `user_id` and `send_id` so you can measure referral-channel CAC and reward correctly. Referral is usually your cheapest acquisition channel when it works - but only when targeted at genuine promoters.

## Anti-Patterns

- Asking **detractors or churn-risk users** to refer - amplifies dissatisfaction and produces nothing.
- Asking trial or unactivated users - they have no value experience to vouch for.
- A generic "$50 credit" coupon sent to enterprise accounts - cheapens the relationship; those need a CS-led champion program.
- No cooldown - re-asking every quarter on each fresh NPS response breeds referral fatigue and opt-outs.
- Stale promoter signal - asking on a 3-month-old NPS 9 that no longer reflects the user's sentiment.
- Overlapping the referral ask with an active upsell - the user feels squeezed from two directions.
- A raw `mailto:` instead of a tracked in-app invite flow - you cannot attribute the referral, reward the referrer, or measure the channel.

## Sequence Config

```yaml
sequence: referral
version: 2
priority: 4                              # lowest; yields to all others
entry:
  any_of:
    - "nps_score >= 9 AND days_since_nps <= 14"
    - "active_days_30d_sustained AND tenant_plan == paid"
    - "milestone_reached"
  guards:
    - nps_score > 6 OR nps_score == null   # never ask a detractor
    - churn_risk_score < 0.50
    - lifecycle_stage in [paid, activated]
    - marketing_consent == true
exit:
  any_of:
    - event: referral.submitted          # -> thank_you + reward tracking
    - event: unsubscribe
    - churn_risk_score >= 0.50
    - touches_sent >= 3 -> set cooldown 90d
routing:
  if: "tenant_mrr >= enterprise_threshold"
  then: champion_program                 # CS-led, not self-serve coupon
  else: self_serve_two_sided
coordination:
  prompt_dispatcher: { context: referral }   # in-app + email share state
messages:
  - { id: rf_ask, delay: 0 }
  - { id: rf_incentive, delay: 5d, skip_if: referral.submitted }
  - { id: rf_one_click, delay: 12d, skip_if: referral.submitted }
```

## Copy Template - T+0 Promoter Ask

```text
Subject:  You gave us a 9 - know someone who would love {product}?
Preheader: Takes 30 seconds, helps a friend

Hi {first_name},

Thanks for the great score last week. Since you are getting value
from {product} ({personal_proof_point, e.g. "40 projects this quarter"}),
you might know a team facing the same problem you solved.

[ Invite a colleague ]     <- in-app invite flow, NOT a mailto link

We will give them {referee_reward} to get started, and you get
{referrer_reward} when they subscribe.
```

The `{personal_proof_point}` is what separates a referral ask from spam. Naming the user's own success ("40 projects this quarter") earns the ask; a generic "love us? refer us!" does not. The CTA must open the tracked in-app invite flow so the referral attributes back to this `send_id` and `user_id`.

## Two-Sided Incentive Design

| Lever | Self-serve default | Why |
|---|---|---|
| Referee reward | Account credit or extended trial | Lowers the friend's barrier to signing up |
| Referrer reward | Credit, paid only on referee's first payment | Aligns reward with real revenue, not vanity signups |
| Reward trigger | `referral.subscribed`, not `referral.signed_up` | Paying on signup invites fraud and low-quality leads |
| Cap | Limit rewards per referrer per quarter | Caps abuse and runaway cost |

Pay on conversion, never on signup. Rewarding raw signups is the fastest route to referral fraud (self-referrals, throwaway accounts) and a channel whose CAC looks great until you measure retention of referred users.

## Champion Program (enterprise track)

For accounts above the enterprise MRR threshold, replace the coupon flow with a relationship-led ask owned by CS:

```text
- Personal note from the account's CS owner (not automated send).
- Offer: case-study collaboration, advisory board, beta access, co-marketing.
- Ask: a warm intro to a peer company, or a public reference/quote.
- Reward: recognition and partnership, not account credit.
```

A "$50 credit" to a six-figure account is faintly insulting and converts poorly; status and partnership convert.

## Edge Cases

| Case | Handling |
|---|---|
| Promoter score lapses below 7 mid-flow | Exit; do not keep asking someone whose sentiment cooled |
| User already referred this quarter | Honour 90d cooldown; do not re-ask even on a fresh NPS 9 |
| Referee signs up then churns in trial | No referrer reward (reward is gated on subscription); flag for fraud review if a pattern emerges |
| Enterprise account triggers self-serve criteria | Routing override sends them to champion_program, not the coupon flow |
| Referral submitted via in-app, not email | `prompt_dispatcher` records it; the email flow exits and skips remaining touches |
