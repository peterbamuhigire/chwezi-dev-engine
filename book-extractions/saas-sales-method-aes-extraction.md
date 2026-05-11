# The SaaS Sales Method for Account Executives — Extraction
**Source:** *The SaaS Sales Method for Account Executives: How to Win Customers* (Winning By Design). Tier: **Sales motion + AE workflow.**
**Coverage:** Discovery, demos, pilots, negotiation, closing, expansion — for AEs working with mid-market and enterprise SaaS deals.

For a build engine, the value of this book is **what the product must do to support a sales-led motion** — the features sales reps need from the product, the artifacts the product must generate, and the operational hooks the AE workflow depends on.

---

## 1. The Sales Motion's Product Dependencies

For an AE motion to work, the product must support:

### 1.1 Discovery Phase
- **Public marketing site** with case studies, pricing transparency at the entry tier, ROI calculator.
- **Demo request form** wired to CRM (HubSpot / Salesforce) with UTM capture, firmographics enrichment (Clearbit / 6sense), routing to the right AE.
- **Sales-team telemetry** — the AE needs to know: did the prospect visit the pricing page? Try the trial? Read the security page? (Marketing tools: Segment + reverse-ETL to Salesforce; or Mutiny / 6sense / Demandbase.)

### 1.2 Demo Phase
- **Demo tenant** — seeded with realistic data so empty-state doesn't undermine the pitch.
- **Reset-demo capability** — AE clears state between calls.
- **Persona-specific demo seeds** — healthcare demo data, fintech demo data, restaurant demo data.
- **Screen-share-friendly UI** — large text, high-contrast, no clutter.
- **Demo recorder integration** — Gong / Chorus / built-in.

### 1.3 Pilot / Trial Phase
- **Sandbox tenant** — full-feature, time-bounded (typically 14-30 days for SMB pilots; 60-90 days for enterprise PoCs).
- **AE-controlled provisioning** — AE can spin up a sandbox without engineering tickets.
- **Pilot success metrics dashboard** — both AE and buyer see usage, adoption, ROI per the pilot's success criteria.
- **Pilot expiration handling** — automated reminder emails, automated conversion-to-paid flow, automated archive-on-expiry with data retention for win-back.

### 1.4 Negotiation Phase
- **Custom-quote generation** — sales-led pricing that doesn't appear on the public pricing page; line-item pricing with discounts, custom limits, custom features.
- **Order-form / contract generation** — DocuSign / PandaDoc integration; legal-approved templates; signed PDF stored alongside the customer record.
- **Security questionnaire automation** — answers to SIG / CAIQ / SOC2 questions exposed via a trust portal.
- **Procurement integrations** — Coupa / Ariba / SAP Concur where the buyer requires.

### 1.5 Closing Phase
- **Order-form-driven provisioning** — sales-marked-won deal triggers tenant provisioning with the negotiated terms (custom plan, custom limits, custom price).
- **Custom contract enforcement** — the billing system must support per-tenant overrides (custom Prices, custom entitlements, custom limits) without forking the codebase.
- **Welcome handoff** — to CS or onboarding-specialist with full deal context (negotiated terms, success criteria, stakeholders).

### 1.6 Expansion Phase
- **Usage telemetry to AE** — AE can see which accounts are approaching limits, adopting new features, or candidate-for-upsell.
- **In-product expansion CTAs** — coordinated with AE outreach (avoid double-asking).
- **NRR dashboard** per AE / per book of business.

---

## 2. The MEDDIC / MEDDPICC Pattern (Sales Qualification → Product Capability)

The AE method uses MEDDPICC for qualification: **Metrics, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Identify Pain, Champion, Competition.**

Each translates to product capabilities the AE needs:

| MEDDPICC element | Product capability that supports it |
|---|---|
| **Metrics** | ROI calculator on the website + per-pilot success-metrics dashboard |
| **Economic Buyer** | Multi-stakeholder demo support (different personas see different value) |
| **Decision Criteria** | Side-by-side feature comparison vs competitors (built into the sales kit) |
| **Decision Process** | Procurement-friendly artifacts (SOC2 report, DPA, MSA template) |
| **Paper Process** | Order form generator, DocuSign integration, custom legal terms |
| **Identify Pain** | Discovery questionnaire embedded in trial signup; AE telemetry |
| **Champion** | Champion enablement materials (internal-business-case template) |
| **Competition** | Win/loss CRM tracking; product comp matrix |

---

## 3. The Sales-Assist Engineering Stack

What the product team must build to support an AE motion (typical mid-market $5K–$50K ACV deal):

```
Lead capture form
    ↓
CRM (Salesforce / HubSpot) with firmographic enrichment
    ↓
Routing engine → AE
    ↓
Demo tenant + recorded demo
    ↓
Trial / Sandbox tenant (AE-provisioned, time-bounded)
    ↓
Trust portal (SOC2, DPA, security questionnaire pack)
    ↓
Quote generator → DocuSign → Order form
    ↓
Won deal → Automated provisioning with custom contract terms
    ↓
Handoff to CS + onboarding tracker
    ↓
Usage telemetry → AE / CSM expansion dashboards
```

Every step is **engineering work**. A product without these is selling itself one deal at a time at the founder's energy level.

---

## 4. Enterprise-Specific Product Capabilities

Larger deals demand more from the product:

- **SSO** (SAML 2.0 minimum, OIDC preferred).
- **SCIM** for user lifecycle management from the buyer's IdP.
- **Per-tenant data residency**.
- **Audit log API** exportable to the buyer's SIEM.
- **Custom domain** (`app.customer.com` CNAMEd to the SaaS).
- **IP allowlist** per tenant.
- **DLP integration** (data-loss prevention hooks).
- **Private cloud / dedicated VPC deployment** for the largest accounts (silo'd tenant on the SaaS's infra, billed at premium tier).

These are not edge-case features; they are **the price of entry** to the enterprise segment.

---

## 5. The Build-Engine Deliverables From This Book

For every SaaS the engine ships with a sales motion:

1. **Demo tenant** seeded per persona; reset button for the AE.
2. **Sandbox / pilot tenant** — full-feature, time-bounded, AE-provisioned.
3. **Trust portal** — SOC2 (when achieved), DPA, sub-processor list, security questionnaire pack.
4. **Custom-quote support** — admin-side pricing overrides, order-form-driven plan.
5. **Order-form integration** — DocuSign / PandaDoc; signed PDF stored.
6. **CRM integration** — bidirectional sync of accounts, contacts, opportunities, usage signals.
7. **AE telemetry dashboards** — pipeline + portfolio usage + expansion candidates.
8. **Enterprise feature pack** (when targeting enterprise) — SSO, SCIM, audit log API, data residency, IP allowlist.
9. **Procurement-friendly artifacts** — MSA / DPA / SOC2 / order-form templates, accessible from a single page.
10. **Handoff automation** — won deal → tenant provisioned → CS notified → onboarding tracker initialized.

A SaaS that ships these enables a 5-rep AE team to close mid-market deals without the founder in every meeting. The cost is real engineering investment, and the return is a sales motion that scales.
