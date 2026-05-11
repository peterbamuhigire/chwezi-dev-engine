# The SaaS Email Marketing Playbook — Étienne Garbugli — Extraction
**Source:** Étienne Garbugli, *The SaaS Email Marketing Playbook: Convert Leads, Increase Customer Retention, and Close More Recurring Revenue With Email*. Tier: **Lifecycle email + transactional infra.**
**Coverage:** Strategy (key milestones, 6 sequences, segmentation, custom fields, data implementation plan), Execution (automations, deliverability, testing, reporting, list hygiene), Optimization (deliverability, opens, body, landing), Deep Dives (cold, welcome/onboarding, behavioral/lifecycle, upgrade/upsell, retention, referral, reactivation).

For an **engineering build engine**, the value is in **what the email system has to know about each user/tenant** — the data model, the event triggers, and the deliverability infrastructure that make lifecycle marketing possible. This is the **email-infra and event-router contract** the SaaS app must produce.

---

## 1. The Six Email Sequences Every SaaS Needs

Garbugli's central organizing principle. Every SaaS lifecycle needs these six:

| # | Sequence | Trigger | Goal |
|---|---|---|---|
| 1 | **Cold / acquisition** | Outbound list addition | Get qualified prospects to engage |
| 2 | **Welcome & onboarding** | Signup event | Get user to first value (activation) |
| 3 | **Behavioral & lifecycle** | Usage events (or absence) | Drive feature discovery, prevent stall |
| 4 | **Upgrade, upsell, expansion** | Tier/usage signals | Expand revenue |
| 5 | **Retention / churn prevention** | Churn-risk signals | Save accounts |
| 6 | **Reactivation** | Long inactivity | Win back dormants |
| (7) | **Referral** | Activated user, NPS promoter | Drive viral acquisition |

Each sequence has a **trigger contract** — the product must emit the trigger event reliably.

---

## 2. Data Foundation — What the Email System Must Receive

Garbugli's Ch.11-12 ("Defining Necessary Custom Fields" + "Creating a Data Implementation Plan") is, for engineering, the most important section. The email system (Customer.io / Klaviyo / Braze / MailerLite / in-house) must receive a continuous stream of:

### 2.1 User-level attributes (sticky on the contact record)
- `email`, `name`, `signup_date`, `first_login_date`, `last_login_date`
- `tenant_id`, `tenant_name`, `tenant_plan`, `tenant_mrr`
- `role` (owner / admin / member / billing)
- `lifecycle_stage` (visitor → signup → trial → paid → churned → reactivated)
- `acquisition_channel`, `utm_source`, `utm_medium`, `utm_campaign`
- `firmographics` (industry, company_size, country, language)
- `activation_state` (activated / not activated; date)
- `churn_risk_score`
- `nps_score`, `last_nps_date`
- `unsubscribed_categories` (transactional / product / marketing / digest)

### 2.2 Event stream (firehose)
Every event the user triggers in the product becomes available to email automation:
- `user.signed_up`, `user.activated`, `user.logged_in`, `user.invited_teammate`
- `feature.X.used_first_time`, `feature.X.used_repeat`
- `trial.started`, `trial.day_3`, `trial.day_7`, `trial.ended`, `trial.converted`
- `subscription.upgraded`, `subscription.downgraded`, `subscription.cancelled`
- `payment.failed`, `payment.succeeded`
- `support.ticket.created`, `support.csat_low`
- `usage.approaching_limit`, `usage.limit_hit`

### 2.3 Engineering pattern — the event bridge
Build an **event router** between the product event bus and the email tool. Pattern:
```
Product app  -> emits event ->  Event bus (Kafka/SQS/Webhook)
                                  -> Email Service (Customer.io / Braze / in-house)
                                  -> Warehouse (mirror for analytics)
                                  -> Other tools (analytics, CRM)
```
Events are typed, idempotent, replayable, schema-versioned.

---

## 3. Deliverability Engineering

Garbugli's Ch.33 ("Optimizing Email Deliverability") combined with industry baseline gives the build engine a deliverability spec:

### 3.1 Domain & DNS Setup
- **SPF** record — authorize sending IPs / ESP.
- **DKIM** — signed key per sending domain; rotate annually.
- **DMARC** — policy `p=quarantine` minimum, `p=reject` once aligned.
- **BIMI** — once DMARC is enforced, optional but trust-boosting.
- **Subdomain strategy** — `mail.yourdomain.com` for marketing, `app.yourdomain.com` or `notify.yourdomain.com` for transactional; never mix the reputations.

### 3.2 Sender Reputation
- **Warm up** new IPs/domains — start at low volume, ramp.
- **Bounce handling** — hard bounces auto-suppressed; soft bounces retried then suppressed.
- **Complaint feedback loops** (FBL) — all major mailbox providers; auto-suppress.
- **Unsubscribe** — one-click (List-Unsubscribe header), honored within minutes.
- **Engagement-based pruning** — drop addresses with no opens in 90 days from broadcasts; keep them eligible for transactional only.

### 3.3 ESP Selection
| ESP | Strength |
|---|---|
| **SendGrid / Mailgun / Amazon SES** | High-volume transactional, low cost, raw API |
| **Postmark** | Transactional, best deliverability + speed for receipts/auth |
| **Customer.io / Braze / Iterable** | Event-driven lifecycle automation |
| **MailerLite / ConvertKit / Drip** | Marketing broadcasts, simpler |
| **Resend** | Developer-friendly transactional |

**Default stack:** Postmark (transactional) + Customer.io (lifecycle) + a marketing tool if needed. Or AWS SES + a thin automation layer if cost matters at scale.

### 3.4 Suppression Management
- Centralized suppression list across all senders.
- Tenant-aware suppression — a user can unsubscribe from one tenant's notifications without losing all email.
- GDPR/CCPA/POPIA-aware — deletion requests cascade through suppression list.

---

## 4. Transactional vs Lifecycle vs Marketing — The Separation Engineers Must Honor

| Type | Examples | Sending domain | Consent model |
|---|---|---|---|
| **Transactional** | Password reset, receipt, invitation, 2FA code, security alert, MFA, payment failure | `notify.domain.com` | Required, always sent |
| **Lifecycle / product** | Welcome, onboarding nudges, feature announcements, churn-prevention | `notify.domain.com` or `mail.domain.com` | Implicit on signup; granular opt-out |
| **Marketing** | Newsletter, promotions, webinars | `mail.domain.com` | Explicit opt-in (GDPR/CASL/POPIA in regulated regions) |

**Engineering implication:** the email system must support **categories** at send time, and the suppression list must be category-aware. Never send marketing on the transactional reputation domain.

---

## 5. Onboarding Sequence (Ch.41) — Detailed Build Spec

Garbugli's onboarding sequence is the most engineering-actionable. Typical 5–7 emails:

1. **Welcome (T+0)** — confirm signup, deliver core CTA ("complete setup"), set expectations.
2. **Getting Started (T+1)** — concrete first step, links into product at the right place.
3. **Feature Discovery (T+3)** — surface a high-value feature the user hasn't touched.
4. **Social Proof / Case Study (T+5)** — show what users like them achieve.
5. **Activation Check (T+7)** — branch: if activated, congratulate + next feature; if not, troubleshoot + offer help.
6. **Trial-End Warning (T+trial_length - 3)** — soft, value-led.
7. **Trial-End Conversion (T+trial_length)** — paywall + offer.

**Branches** are critical — these are not linear drips. Engineering must support:
- **Conditional sending** based on event presence/absence ("send only if user has not yet completed setup_step_2").
- **Wait-until** logic ("wait up to 24h for activation event; if it happens, branch A; else branch B").
- **Skip logic** ("if user is already on paid plan, skip the trial-end series").

---

## 6. Behavioral & Lifecycle Emails (Ch.42) — Event-Driven Patterns

Examples and the events that drive them:

| Email | Trigger event | Suppression |
|---|---|---|
| "You haven't used X yet — here's why it matters" | `feature.X.never_used AND user.activated AND days_since_signup >= 7` | If user dismisses 2x |
| "You're approaching your limit" | `usage.approaching_limit (80% threshold)` | After upgrade |
| "Your team is collaborating!" | `collaboration_event_count >= 5 in last 7 days` | Once per month |
| "You haven't logged in for X days" | `last_login_date < now - 14d` | After login |
| "Your invoice is ready" | `invoice.created` | Never (transactional) |
| "Card expiring soon" | `payment_method.expires_in < 30 days` | After update (transactional) |

---

## 7. Upgrade / Upsell / Expansion (Ch.43)

Triggered by **usage signals** (PQL — Product-Qualified Leads):
- Approaching plan limit (seats / API calls / storage / projects).
- Repeat use of a feature gated behind a higher tier.
- Hit the limit (paywall moment).
- Crossed an engagement threshold ("active 5+ days/week for last 4 weeks").

**Engineering implications:**
- PQL scoring — a daily-materialized number per user/tenant.
- In-app prompts coordinated with email (don't spam both).
- Upgrade CTA links go straight to in-app one-click upgrade, not "contact sales" unless enterprise.

---

## 8. Retention & Churn Prevention (Ch.44)

Triggers:
- Churn-risk score crosses threshold.
- Plan downgrade.
- Cancellation initiated.
- Long stretch without login.

Sequences:
- **At-risk** — value reinforcement, support offer, "what would make this work?" survey.
- **Cancellation attempted** — offer pause / discount / direct CS contact; capture cancellation reason.
- **Post-cancellation** — exit survey, mark for win-back queue.

**Engineering:** the cancellation flow must capture **reason code** (dropdown + free text), feed it back to the email engine for branched win-back later.

---

## 9. Reactivation (Ch.46)

Trigger: `last_login_date < now - 60d` (or 90d depending on use frequency).

Sequences:
- "We miss you" — emotional reconnect.
- "What's new" — features added since departure.
- "Special offer" — discount or extended free use.
- "Final goodbye" — last chance + permission to fully unsubscribe.

**Engineering:** suppression list must allow reactivation sequence to override marketing-unsubscribe **only if** legally permitted (transactional-adjacent borderline; check region).

---

## 10. Reporting (Ch.26-27)

Required dashboards:
- **Per-sequence performance** — open / click / unsubscribe / complaint / convert.
- **Cohort impact** — does the welcome sequence move 30-day activation rate?
- **Deliverability** — bounce rate (< 2%), complaint rate (< 0.1%), inbox placement rate.
- **List hygiene** — % engaged in last 30/90 days; auto-prune unengaged.
- **Revenue attribution** — MRR attributed to email-touched conversions vs control.

**Engineering:** every email send/open/click writes to the warehouse, with `user_id`, `tenant_id`, `sequence_id`, `email_id`, `event_type`, `timestamp`.

---

## 11. Build-Engine Deliverables From This Book

For every SaaS the engine ships:

1. **Event bridge** — product event bus → email automation tool (Customer.io / Braze / in-house).
2. **Contact data model** — every contact has the attributes listed in §2.1, kept in sync.
3. **Deliverability setup** — SPF / DKIM / DMARC, separate transactional vs marketing subdomains, FBL configured, suppression list centralized.
4. **Six core sequences** — cold (if applicable), welcome/onboarding, behavioral, upgrade, retention, reactivation; defined branches per trigger.
5. **PQL scoring** — daily materialized signal per user/tenant; drives upgrade emails + in-app prompts.
6. **Churn-risk scoring** — daily materialized signal per tenant; drives retention sequence.
7. **Cancellation-reason capture** — structured + free-text; feeds branched win-back.
8. **Email analytics warehouse** — every send/open/click/convert event mirrored; cohort-able.
9. **Email-revenue attribution** — control-vs-treatment cohorts measured per sequence.
10. **Compliance** — granular consent, one-click unsubscribe, suppression list cascade on GDPR delete.
