# Hacking SaaS — Eric Mersch — Extraction
**Source:** Eric Mersch, *Hacking SaaS: An Insider's Guide to Managing Software Business Success*. Tier: **Operational metrics & GTM-financial.**
**Coverage:** Three parts — Part 1: SaaS 101 (Ch.1–6, perpetual-vs-SaaS, financial reporting, top-line metrics, unit economics, financial metrics, using metrics). Part 2: Customer-Centric SaaS Model (Ch.7–14, Enterprise / SMB / B2C financial profiles, GTM, metrics). Part 3: Industry-Centric Models (Ch.15–16, horizontal vs vertical).

This book is a **CFO's framing** — its engineering value is in the **specific metrics, definitions, and instrumentation requirements** that every SaaS product must surface to the business. For a build engine, this becomes the **dashboard/event/aggregation contract** that the application must produce.

---

## 1. Why a Build Engine Should Care

Engineering decisions cascade into the books of a SaaS:
- **What you instrument** determines whether the business can compute its top-line metrics.
- **What you bill** (and how granularly) determines whether the unit economics are visible.
- **What signals you capture** determines whether the GTM team can run cohorts, segment, and forecast.
- **What the system records as state** determines whether revenue recognition is even possible.

The engineering output of this book is: **a SaaS metrics event contract** the build engine ships with every product.

---

## 2. Customer-Type Determines Backend Shape

Mersch's most useful framing for engineers is that **the customer type fundamentally changes what the system must expose**:

| Segment | ACV range | Sales motion | Engineering implications |
|---|---|---|---|
| **Enterprise** | $50K – millions ARR | Direct sales, AE+SE, 6-12 mo cycle, ROI-driven | SSO, SCIM, audit logs, per-tenant data residency, custom contracts/quotes, security questionnaire support, signed data-export, sandbox tenant for the buyer, IP allowlists |
| **SMB / Mid-market** | $500 – $50K ARR | Hybrid (PLG + AE), self-serve + assisted, 1-3 mo cycle | Self-service signup, automated trial, in-app upgrade prompts, light SSO, automated billing, in-product analytics for usage-led conversion |
| **B2C** | $5 – $500 ARR | Pure self-serve, viral / paid acquisition, instant | Frictionless signup, App Store / Play Store IAP, social auth, mobile-first paywall, payment retries, lightweight tenant model |

A product that says it's "B2B SaaS" but ships an enterprise-only feature set with no self-serve is silently choosing enterprise economics. The engineering team should explicitly choose, and instrument for, the segment.

---

## 3. The Top-Line Metric Contract (Ch.3)

Every SaaS must compute, in real time or daily:

| Metric | Definition | What engineering must record |
|---|---|---|
| **MRR** (Monthly Recurring Revenue) | Sum of monthly-equivalent recurring contract value across all active subscriptions | `subscription_active`, `monthly_amount`, `currency` events |
| **ARR** | MRR × 12 | Derived |
| **New MRR** | MRR added from new logos in period | `subscription_created` with `is_new_customer=true` |
| **Expansion MRR** | MRR added from upgrades, seat adds, usage growth on existing customers | `subscription_updated` with delta |
| **Contraction MRR** | MRR lost from downgrades/seat reductions | `subscription_updated` with negative delta |
| **Churned MRR** | MRR lost from full cancellations | `subscription_cancelled` |
| **Net New MRR** | New + Expansion − Contraction − Churn | Derived |
| **Gross / Net Revenue Retention** | (Starting MRR − Churn − Contraction [± Expansion]) / Starting MRR | Cohort math on MRR events |

**Engineering implication:** every billing state change must produce a typed event with `tenant_id`, `customer_id`, `event_type`, `mrr_delta_usd`, `currency`, `effective_date`, `reason_code`, idempotency_key. These flow to the warehouse where the metrics are computed. Without this contract, finance reconstructs the data from Stripe by hand every month.

---

## 4. Unit Economics (Ch.4)

| Metric | Definition |
|---|---|
| **CAC** | (Sales + Marketing spend in period) / (new customers acquired in period) |
| **LTV** | ARPU × Gross Margin / Churn Rate |
| **LTV:CAC** | Target ≥ 3x for healthy SaaS |
| **CAC Payback** | CAC / (ARPU × Gross Margin); target < 12 months SMB, < 18 enterprise |
| **Magic Number** | (Net New ARR in quarter × 4) / S&M spend in prior quarter |
| **Gross Margin** | (Revenue − COGS) / Revenue; SaaS target 70-85% |

**Engineering implication:** to compute these correctly, the system must surface:
- New-customer flag on every billing event.
- Cost-per-tenant (infra + support cost attributed to each tenant — see Multi-Tenant extraction §11).
- COGS attribution: which infra spend is COGS (hosting, third-party APIs called for the customer) vs OPEX (eng salaries).

A SaaS that doesn't surface cost-per-tenant cannot compute gross margin correctly. **Cost-per-tenant telemetry is a hard requirement from day one.**

---

## 5. Cohort Retention Engineering

Mersch is emphatic: **retention is the engine of SaaS.** Engineering must support cohort analysis.

Required event log per tenant:
```
tenant_id, plan, signup_date, mrr_each_month, status_each_month, churn_date, expansion_events
```

Common cohort cuts:
- Signup cohort by month → MRR retention curve at 3/6/12 months.
- Plan cohort → which plans churn fastest.
- Acquisition channel cohort → which channels yield lasting customers (requires `acquisition_channel` attribute on tenant).
- Geography / industry / company-size cohort → tied to firmographic data captured at signup or enriched (Clearbit-style).

**Engineering implication:** the signup form must capture firmographic data (or enrich it asynchronously); the tenant record must have `acquisition_channel`, `company_size`, `industry`; the billing event stream must allow grouping by these fields.

---

## 6. Enterprise vs. SMB vs. B2C — Feature Sets That Must Exist

### 6.1 Enterprise SaaS (Ch.7–9)
Must-have engineering features for enterprise GTM to function:
- **SSO** (SAML 2.0 minimum, OIDC preferred) + per-tenant IdP configuration.
- **SCIM** for user provisioning/deprovisioning from the buyer's IdP.
- **Audit log API** the customer can pull and feed into their SIEM.
- **Data residency** — at least region-level pinning; ideally per-tenant region selection.
- **Security questionnaire pack** — automated answers to SIG/CAIQ/SOC2 questions, exposed via a trust portal.
- **Custom contracts** — order-form-driven plan creation rather than self-serve plans.
- **Sandbox tenant** for the buyer (proof-of-concept tenant, full-feature, time-bound).
- **IP allowlists** per tenant.
- **SLA & status page** with per-customer SLA reporting.

### 6.2 SMB SaaS (Ch.10–11)
- **Self-serve signup** with credit card or invoice.
- **14-30 day trial** with optional credit-card-up-front.
- **Activation flow** with measurable time-to-value (the "aha moment" event).
- **In-app upgrade prompts** triggered by usage signals (PQL).
- **Light SSO** (Google/Microsoft).
- **Automated billing recovery** (Smart Retries dunning).

### 6.3 B2C SaaS (Ch.12–14)
- **One-click signup** (social auth, magic link).
- **Mobile-native paywall** if there's an app — StoreKit2 / Play Billing.
- **Viral hooks** (share, invite, referral).
- **Receipt validation server-side**.
- **Server-side entitlement sync** between app-store subscription and platform.

The build engine should default to the SMB feature pack, lift to enterprise on demand, and add B2C primitives only when the segment matches.

---

## 7. Magic Number, Burn Multiple, Rule of 40

Mersch uses these as the headline business-health metrics. To compute them the system must produce:

| Metric | Engineering data dependency |
|---|---|
| **Magic Number** | Net new ARR per quarter; S&M spend per quarter (from finance) |
| **Burn Multiple** | Net burn / Net new ARR (from finance + billing events) |
| **Rule of 40** | YoY revenue growth % + EBITDA margin % (≥ 40 for healthy SaaS) |

The signal for engineering: surface **net new ARR per period** as a first-class number from the billing event stream. Finance should not be reconstructing this from Stripe exports.

---

## 8. Pricing Implications That Engineering Must Support

From Mersch's discussion of perpetual-vs-SaaS and per-segment GTM:

- **Per-seat pricing** requires a robust users-per-tenant model with active-user signal (seat = active in last 30 days, or seat = invited, etc. — decide and instrument).
- **Usage-based pricing** requires real-time metering — see `saas-engineering-skills-audit-2026.md` (new `saas-metering-and-usage-billing` skill).
- **Tiered pricing** requires entitlements engineering: features-per-plan, limits-per-plan, gate enforcement.
- **Custom contracts (enterprise)** require the billing system to support overrides per tenant (price overrides, custom features, custom limits) without forking the codebase.

---

## 9. Horizontal vs Vertical SaaS (Ch.15–16)

| Type | Build implications |
|---|---|
| **Horizontal** (e.g., generic CRM, billing tool) | Generic feature surface; deep integrations marketplace; broad SSO list; multi-vertical reporting |
| **Vertical** (e.g., dental practice software, restaurant POS) | Domain workflows pre-built; industry-specific compliance (HIPAA, PCI, EHR integrations); fewer customers, higher ACV typically; deep vertical data model |

Vertical SaaS often justifies **mixed-mode** deployment (silo for the compliance-sensitive data, pool for the catalog).

---

## 10. Anti-Patterns From This Book (engineering-flavored)

- **Billing events live only in Stripe.** Finance has to scrape monthly. Fix: mirror every billing event into the warehouse with a typed contract.
- **No cost-per-tenant.** Cannot compute gross margin. Fix: per-tenant cost attribution from day one.
- **No new-customer flag on signup.** Finance cannot separate New MRR from Expansion. Fix: tag every subscription creation with `is_new_customer`.
- **No `acquisition_channel` on tenant.** Marketing cannot do channel cohort analysis. Fix: capture at signup; default to UTM; allow override.
- **Building enterprise SSO/SCIM only when the first enterprise deal closes.** It's a 4-6 week delay that kills the deal. Fix: ship SSO/SCIM at the beginning of any B2B SaaS.
- **Treating mobile IAP and Stripe Billing as the same code path.** They are not. Fix: separate entitlement service; reconcile from both sources.

---

## 11. The Mersch Build-Engine Deliverables

For every SaaS the engine ships, produce:

1. **SaaS metrics event contract** — every billing/usage/lifecycle event typed, with `tenant_id`, `is_new_customer`, `mrr_delta`, `currency`, `effective_date`, `reason_code`, idempotency key.
2. **Cohort-ready tenant model** — captures `signup_date`, `plan`, `acquisition_channel`, `company_size`, `industry`, `geography`.
3. **Per-tenant cost telemetry** — surfaces COGS-relevant resource usage per tenant.
4. **MRR/ARR/Net New MRR/NRR daily aggregates** — materialised in the warehouse.
5. **Net Revenue Retention dashboard** — cohort × month, MRR retained.
6. **Magic Number / Burn Multiple / Rule of 40 inputs** — exported daily for the finance dashboard.
7. **Segment-appropriate feature pack** — enterprise/SMB/B2C decided up front; pack shipped.

These deliverables are the difference between a SaaS that can scale GTM and one that has to rebuild instrumentation when revenue hits $1M.
