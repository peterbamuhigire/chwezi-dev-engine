# The SaaS Sales Method Fundamentals — Extraction
**Source:** *The SaaS Sales Method Fundamentals* (Winning By Design). Tier: **Sales fundamentals — common language between sales, CS, and product.**
**Coverage:** The bowtie funnel (lead → prospect → customer → expansion), pipeline mechanics, qualification, discovery, lifecycle motions.

For an engineering build engine, this book reinforces and complements the AE book: the **funnel stages map to product events**, and the product must instrument every transition so sales/CS/product share the same source of truth.

---

## 1. The Bowtie — The Lifecycle Model

The Winning By Design bowtie funnel:

```
              IMPRESSION  ENGAGED  EXPLORE  EVALUATE  COMMIT   ONBOARD  ADOPT  EXPAND  RENEW
   (Marketing)             (Sales/SDR)        (AE)              (CS)               (CS/AE)
                                  ←  ACQUISITION  →                ←  RETENTION & GROWTH →
```

Each stage in the bowtie has:
- An **entry event** (marketing-qualified lead, sales-qualified opportunity, signed contract, completed onboarding, etc.)
- A **stage duration** (how long the typical prospect / customer stays in this stage).
- A **conversion rate** to the next stage.
- A **leakage rate** (where prospects / customers fall out).

**Engineering implication:** every transition is a product event. The product must emit:
- `lead.captured` (marketing form)
- `lead.qualified` (BANT/MEDDIC met)
- `opportunity.created` (CRM)
- `opportunity.demo_completed`
- `opportunity.trial_started`
- `opportunity.trial_activated` (TTV achieved)
- `opportunity.won` / `opportunity.lost`
- `customer.onboarded` (success criteria met within first 30/60/90 days)
- `customer.adopted` (repeat-use threshold met)
- `customer.expanded` (additional MRR added)
- `customer.renewed` / `customer.churned`

These events live in the warehouse + push to CRM. The bowtie dashboard is just SQL.

---

## 2. Common Language — Shared Definitions

The book hammers shared definitions across functions. Engineering must encode these:

| Term | Definition (engineering-instrumentable) |
|---|---|
| **MQL** (marketing-qualified lead) | Submitted form + fits ICP scoring criteria |
| **SQL** (sales-qualified lead) | MQL + accepted by SDR + first meeting booked |
| **Opportunity** | SQL + CRM record with stage > "Discovery" |
| **Customer** | Opportunity won + first invoice paid + provisioned tenant active |
| **Activated** | Tenant has triggered the "aha event" (product-defined) within trial window |
| **Adopted** | Tenant has crossed engagement threshold (e.g., 3 active users, 5 weekly sessions) |
| **Expanded** | Tenant MRR has increased > 0% since contract start |
| **Churned** | Subscription cancelled OR no activity in 90 days (define per product) |
| **Reactivated** | Previously churned, new subscription within 12 months |

These definitions become **filter predicates** in the warehouse. They must be **consistent** — sales/CS/product all read the same view.

---

## 3. Discovery Engineering — The Buyer's Hidden Data

A great AE asks questions; a great product **captures the answers**. Discovery questions that should be encoded in the trial-signup flow or progressive profiling:

- Industry / vertical
- Company size (employees, revenue band)
- Current solution (what they're replacing — competitor name)
- Use-case primary (e.g., "billing for SaaS", "billing for marketplaces")
- Decision timeframe
- Decision-maker role
- Budget band (optional, often pre-qualifying)

**Engineering implication:** ship a **progressive profiling** mechanism — don't ask everything at signup; ask one question per session for the first 5 sessions, store on the tenant record. Feeds segmentation, AE prep, and lifecycle email.

---

## 4. Activation — The Most Important Number

Activation = first achievement of value. Every product has one:
- For a billing SaaS: "first invoice sent".
- For a project tool: "first project created + first task assigned".
- For an email tool: "first list imported + first campaign sent".

**Engineering implication:** the build engine must:
1. **Define activation per product** (PRD-level decision).
2. **Instrument activation event**.
3. **Measure time-to-activation** distribution (median, p75, p90).
4. **Surface activation rate** by cohort (signup-week × plan × channel).
5. **Fire activation event** to email engine (triggers next sequence) and to CS (kicks off onboarding milestones tracking).

---

## 5. Pipeline Hygiene — What Engineering Owes the Sales Team

Sales depends on clean pipeline data. Engineering must ensure:
- **Source-of-truth for every CRM field** is the product where possible (usage signals, tenant plan, MRR, last_login).
- **Reverse-ETL** keeps CRM in sync nightly.
- **Auto-create opportunities** for high-PQL accounts (PLG-to-SLG bridge).
- **Lead/opportunity decay rules** — opportunities with no activity in N days auto-flag stale; auto-close after M days.

---

## 6. Customer Success — The Other Side of the Bowtie

Once a customer is signed, CS owns onboarding → adoption → expansion → renewal. Product must surface:

- **Onboarding tracker** — defined milestones per customer; CS sees completion %.
- **Health score** — daily-materialized per tenant (engagement, support load, NPS, churn risk).
- **Adoption depth** — feature usage breadth per tenant.
- **Expansion candidate score** — usage approaching limits, repeat hits on gated features.
- **Renewal alerting** — 90/60/30/14 days before renewal date.
- **QBR (quarterly business review) data export** — per-tenant value-realized + ROI metrics for the buyer's executive review.

---

## 7. Common Anti-Patterns Engineering Causes

- **Product events don't match CRM definitions.** Sales calls a "trial" something different from product. Fix: shared definitions table; product is source-of-truth where applicable.
- **No bowtie dashboard.** Sales/CS/product each look at different numbers and argue. Fix: warehouse-based shared dashboard.
- **No reverse-ETL to CRM.** AE/CSM doesn't see usage. Fix: nightly sync of tenant.* signals to CRM account.
- **No QBR data exporter.** CSM rebuilds the deck by hand each quarter. Fix: per-tenant QBR data export.
- **No PQL → SQL bridge.** PLG signups never become enterprise opportunities. Fix: PQL scoring → auto-create opportunity when threshold hit.

---

## 8. Build-Engine Deliverables

For every SaaS the engine ships with a sales motion (mid-market or above):

1. **Bowtie event contract** — every stage transition is an event in the warehouse.
2. **Shared definitions** — MQL / SQL / Opportunity / Customer / Activated / Adopted / Churned encoded as warehouse views, used by all teams.
3. **Activation metric** — defined, instrumented, dashboard'd.
4. **Reverse-ETL to CRM** — tenant signals propagate nightly.
5. **PQL → SQL bridge** — auto-create opportunities for PLG accounts hitting thresholds.
6. **Health score** — per tenant, daily materialized.
7. **Onboarding tracker** — milestones defined; CS sees completion %.
8. **QBR data export** — per-tenant value-realized package, generated for CS each quarter.
9. **Progressive profiling** — capture firmographics + use-case data over the first sessions.
10. **Renewal alerting** — 90/60/30/14 day notices to CS + AE.

These ten artifacts close the loop between product instrumentation and sales/CS productivity — turning a product into a revenue engine.
