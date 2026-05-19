# Sales-Assist Product Capabilities — Reference

What the product team must build so the sales team can sell. Distilled from *The SaaS Sales Method for AEs* (Winning By Design) + *The SaaS Sales Method Fundamentals*.

## The Sales-Assist Stack

```
Lead capture → CRM (enriched) → AE routing → Demo tenant → Sandbox tenant
   → Trust portal → Quote generator → Order form → Provisioning → CS handoff → Expansion telemetry
```

Every arrow is engineering work.

## Capabilities Checklist

| Capability | Required for | Detail |
|---|---|---|
| Lead capture form | All AE motions | UTM, firmographics, enriched via Clearbit/6sense, routed to CRM |
| CRM with reverse-ETL | All AE motions | Bidirectional sync of accounts, contacts, opportunities, usage signals |
| AE telemetry (account intent) | Mid-market+ | AE sees: visited pricing page? Tried trial? Read security page? |
| Demo tenant | All B2B | Persona-seeded data; reset button; recordable |
| Demo recorder integration | All B2B | Gong / Chorus / Otter for call playback + AE training |
| Sandbox tenant (pilot) | Mid-market+ | Full-feature, time-bounded; AE-provisioned without engineering tickets |
| Pilot success-metrics dashboard | Mid-market+ | Both AE and buyer see usage, adoption, ROI |
| Trust portal | Mid-market+ | SOC 2, DPA, subprocessors, security questionnaire pack |
| Custom-quote generator | Mid-market+ | Sales-led pricing, line items, discounts, custom limits |
| Order-form integration | Mid-market+ | DocuSign / PandaDoc, signed PDF stored on customer record |
| Procurement integrations | Enterprise | Coupa / Ariba / SAP Concur |
| Custom contract enforcement | Enterprise | Per-tenant entitlement + price overrides without forking code |
| Welcome handoff | All B2B | Won deal → tenant provisioned with contract terms → CS notified |
| Usage telemetry → AE / CSM | Mid-market+ | Approaching-limit accounts, feature-adoption depth, expansion candidates |
| QBR data export | Enterprise | Per-tenant value-realized package each quarter |
| Renewal alerting | Mid-market+ | 90/60/30/14 day notices to CS + AE |
| Enterprise auth pack | Enterprise | SSO, SCIM, audit log API, IP allowlist, custom domain |
| ROI calculator on the website | Mid-market+ | Helps marketing + early discovery |
| Activation funnel telemetry | All B2B | Trial → activated → adopted → expanded |

## Demo Tenant Design

- Persona-keyed seeds (healthcare-demo, restaurant-demo, fintech-demo).
- Realistic data volumes (not 3 sample rows).
- Reset button: clears state for next call.
- Optional read-only mode for screen-share.
- Sandbox / demo tenants are tagged `is_sandbox=true` so they're excluded from MRR / cohort math.

## Sandbox / Pilot Tenant Design

- Full-feature, time-bounded (default 30 days; configurable to 90 for enterprise).
- AE provisions via back-office console.
- Auto-expires; emails AE 7d / 1d before expiry; auto-converts to paid or archives.
- Includes "Convert to paid" CTA inside the workspace.
- Pilot metrics dashboard accessible to AE + buyer.

## Order Form → Provisioning

```
AE marks deal Closed-Won in CRM
    → Webhook to platform: "Provision tenant with contract X"
    → Platform reads contract terms (plan_override, limits, features, billing terms)
    → Onboarding orchestrator runs with custom config
    → Stripe Customer created with metadata.contract_id
    → Stripe Subscription created with negotiated Prices
    → CSM notified; onboarding tracker initialised
    → Welcome email sent to deal stakeholders
```

The contract must be **data**, not code:
```sql
CREATE TABLE customer_contracts (
    id              VARCHAR(64) PRIMARY KEY,
    tenant_id       BIGINT UNSIGNED,
    plan_override   VARCHAR(64),
    feature_overrides JSON,
    limit_overrides JSON,
    pricing_overrides JSON,
    starts_at       DATETIME,
    ends_at         DATETIME,
    auto_renew      BOOLEAN,
    signed_pdf_url  VARCHAR(512),
    signed_at       DATETIME,
    docusign_envelope_id VARCHAR(128)
);
```

## Trust Portal

Single page at `trust.yoursaas.com` exposing:
- SOC 2 report (gated by NDA / authenticated).
- ISO 27001 cert.
- Penetration test summary (annual).
- DPA template.
- Subprocessors list (kept current).
- Security questionnaire pack (SIG / CAIQ pre-filled).
- Status page link.
- Privacy policy + Terms of Service.
- Vulnerability disclosure policy / responsible disclosure email.

## Anti-Patterns

- Demo tenant is the founder's personal tenant — risk + bad data.
- Sandbox tenants in MRR — distorts metrics.
- AE has no telemetry — selling blind.
- No trust portal — security questionnaire takes 4 weeks per deal.
- Contract terms baked into application code — bugs and forks.
- No CSM handoff workflow — won deals fall through cracks.
- Renewal alerts go to AE only, not CS — churn risk uncovered.

## See Also

- `saas-sales-organization` — sales org design.
- `saas-control-plane-engineering` — back-office tools that AE / CSM use.
- `saas-sso-scim-enterprise-auth` — enterprise auth feature pack.
- `subscription-billing` — custom-contract enforcement.
- `saas-entitlements-and-plan-gating` — per-tenant overrides.
