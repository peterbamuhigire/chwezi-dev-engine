# The SaaS Playbook — Rob Walling — Extraction
**Source:** Rob Walling (with Jessie Kwak; foreword Jason Cohen), *The SaaS Playbook: Build a Multimillion Dollar Startup*. Tier: **Founder/product/GTM playbook.**
**Coverage:** Foreword, Introduction, Market (PMF, competition, moats), Pricing (structure, freemium, trials, raising prices), Marketing (funnels, dual funnels, B2B approaches, demos), Team (structure, hiring, equity), 80/20 SaaS Metrics (3 High/3 Low, virality, churn, net-negative-churn), Mindset.

For an **engineering build engine**, this book's value is on the **product/MVP/pricing/onboarding/trial mechanics** — the decisions the dev team must encode in the product to enable the business to grow.

---

## 1. The Walling Frame: Product, Market, Pricing, Marketing, Team, Metrics, Mindset

Walling argues these are the only seven dimensions that matter at the bootstrapped/early-stage SaaS scale. For engineering, the operative four are **Market (PMF), Pricing, Marketing-funnels (the product's role in them), and Metrics**.

---

## 2. Pricing — The Biggest Lever (Engineering Implications)

Walling: "Pricing is the biggest lever in SaaS, and almost no one gets it right out of the gate."

### 2.1 Tier Structure Recipes
- Segment customers by **size + usage** first, then build tiers.
- Common pattern: 3 tiers (Starter / Pro / Enterprise), with the middle being the visible target and Starter being the trial-on-ramp.
- **Per-seat pricing** is only honest if two seats see different things on login. If both see the same dashboard, they'll share a login — instrument accordingly.

### 2.2 Two Pricing Models (and Their Combination)
- **Value metric pricing** (per call, per record, per MB, per active user, per active project): scales with the customer's value capture.
- **Feature gating** (Starter has 1, Pro has 5, Enterprise unlimited): simpler, lower-friction.
- **Combination** (recommended for most B2B): per-seat × feature tier.

### 2.3 Expansion Revenue Mechanics
Build **expansion** into pricing tiers — the SaaS Cheat Code. Two patterns:
- **Usage-meter expansion** — customer uses more, pays more.
- **Seat expansion** — customer adds seats, pays more.
- **Plan-upgrade expansion** — customer outgrows current tier, upgrades.

**Engineering implication:** the product must **show the customer when they're approaching a limit** (usage bar, seat counter, feature lock with upgrade CTA). The upgrade path must be **in-app** and one-click — not "contact sales" unless that's literally enterprise.

### 2.4 Freemium vs Trial
| Model | When it fits |
|---|---|
| **Freemium** | Low support burden per customer, fast TTV (signature app, link shortener); high virality |
| **Time-bounded trial** (7–30 days) | Higher support burden, slower TTV, B2B mid-market |
| **No trial / 30-day refund** | Higher ACV, enterprise-style, demos as the screening mechanism |

Walling on trial length: **shorter trials = faster cohort feedback**. A 7-day trial gives 4 cohorts to the 30-day's 1. Default to the shortest trial that lets the user reach "aha".

**Engineering implications:**
- Trial-start, trial-end, trial-converted, trial-abandoned all instrumented as events.
- Time-to-value (TTV) is **measured** — the "aha event" is a defined product event, and time-from-signup to first-occurrence is the activation KPI.
- Trial-end behavior: graceful downgrade to free tier, or graceful suspension, or graceful conversion — design and ship the policy.

### 2.5 Credit Card Up Front?
- Yes by default — significantly higher trial-to-paid conversion, lower support burden.
- No if: viral product / large-org buyer can't be asked for the corporate card / experimenting.
- **Engineering implication:** support both flows. Tag the cohort with `cc_required_at_signup` so future analysis can compare.

### 2.6 Raising Prices
- Raise prices every 6–12 months. "It's not technically hard to raise your prices. You change a number on the pricing page and make an API call."
- Grandfather existing customers or migrate them with notice — but make the migration **automated** and **billing-system-aware**.

**Engineering implication:** the system must support **price versioning** — new Stripe Prices for new customers; grandfathered Prices for existing; an admin tool to bulk-migrate cohorts.

---

## 3. PMF Mechanics — Product Decisions

Walling on PMF:
- Talk to your ideal customer. Build for them, not for everyone.
- "Edge-case the design to death" is the trap — Cooper's rule: design for the persona, not for "somebody."
- A product loved by a narrow segment > a product tolerated by a wide one.

**Engineering implication:**
- Ship a **narrow** v1 deeply, not a wide one shallowly.
- Build the **PMF feedback loop**: signups → activated → engaged-7-day → engaged-30-day → paid → expanded → retained. Each transition is an event; the funnel is the product team's compass.

---

## 4. Marketing Funnels — Product's Role

The dual-funnel model (paid acquisition + content/SEO) requires the product to expose:
- **Landing-page parity** — the pricing page is generated from the same plan/price data the billing system uses (single source of truth).
- **UTM capture at signup** — attribute every signup to channel.
- **In-product referral mechanism** — invite/share flows that the marketing channel can amplify.
- **Self-serve demo / sandbox** — if the funnel is content-driven, the user must be able to try without scheduling a call.

---

## 5. The 3-High / 3-Low Metrics Framework (Walling's 80/20)

Walling: track six metrics, and that's enough at most stages.

**3 to keep HIGH:**
1. **MRR** (monthly recurring revenue)
2. **LTV** (lifetime value)
3. **NPS** (net promoter score) or qualitative customer sat

**3 to keep LOW:**
1. **Churn** (logo churn or revenue churn — pick and stick)
2. **CAC** (customer acquisition cost)
3. **Customer support load** (tickets per customer per month)

**Engineering implication:** all six are instrumentable, and the build engine should ship dashboards for them out of the box.

---

## 6. Churn — The Walling Take

- Logo churn vs revenue churn — different things. Track both.
- Net negative churn (expansion MRR > churn MRR) = the unlock at scale.
- Churn signals to instrument:
  - Last-login date per user / per tenant.
  - Feature-usage delta (week-over-week, month-over-month).
  - Support ticket count + sentiment.
  - Plan downgrade.
  - Reduced active-user count.
  - Payment failure / card expired.

**Engineering implication:** a **churn-risk score** per tenant, materialised daily, fed to CS for proactive outreach. Even a simple "tenants with no login in 14 days" view is high-value.

---

## 7. Virality Mechanics

Walling: virality is a SaaS Cheat Code when the product naturally creates it (e-signature, calendar tool, expense splitter).

Mechanisms the product can ship:
- **Invite-to-collaborate** — extending the workspace pulls in new users.
- **Branded artifacts** — emails sent from your product carry a small "Sent with X" footer (opt-out for paid tiers).
- **Referral program** — give-X-get-X (Dropbox model).
- **Embed widgets** — public-facing assets the product generates that link back.

**Engineering implications:**
- Invite flow must be one-click + email + tracked.
- "Powered by" branding must be configurable per plan.
- Referral attribution must persist through signup (cookie + URL param).

---

## 8. Demo Engineering for B2B

Walling on demos: structure them. The product team must support:
- **Demo tenant** seeded with realistic data so the demo doesn't crash on empty state.
- **Reset-demo button** for the sales team.
- **Sandbox tenant** the buyer keeps after the demo (time-bounded, full feature).
- **Demo telemetry** — what features the buyer touched in the sandbox.

---

## 9. Anti-Patterns Surfaced

- **Pricing too low.** "If you're charging $10 instead of $100, you have to find 10 times as many customers — and your channels won't pay back."
- **Free trial that's too long.** Cohort feedback slows; users delay action.
- **No activation tracking.** You don't know which features matter.
- **Treating the pricing page as a marketing artifact disconnected from billing.** Drift creates bugs and lost revenue.
- **Building features for "somebody" who isn't the persona.** Bloat without sales.
- **Building integrations before PMF.** Integrations are a moat after PMF, not before.

---

## 10. Build-Engine Deliverables From This Book

For every greenfield SaaS:

1. **Pricing page generated from billing data** — single source of truth (plan/price catalogue).
2. **Trial flow** — signup → activated → "aha event" → conversion or expiry; all events instrumented.
3. **In-app upgrade prompts** — usage-triggered, dismissible, conversion-tracked.
4. **Referral / invite flow** — one-click invite, attribution preserved, give-X-get-X mechanic optional.
5. **Sandbox / demo-tenant capability** — sales-team can spin up a seeded tenant; buyer can keep it.
6. **3-High / 3-Low dashboard** — MRR / LTV / NPS / Churn / CAC / Support-load — out of the box.
7. **Churn-risk score** — daily per tenant.
8. **Price-versioning support** — old customers keep old Prices; new customers get new Prices; bulk migration tool for ops.
9. **Activation event** — defined per product, instrumented, time-to-activation reported.
10. **UTM / acquisition-channel attribution** — captured at signup, persisted on the tenant.

These ten artifacts plus the multi-tenant readiness pack (from Golding) form the **SaaS v1 minimum product** the engine should ship.
