# SaaS Maturity Matrix — Reference

Which engineering capabilities ship at which ARR stage. Drawn from the *How to Run a SaaS Business* (Trio) lessons and *Hacking SaaS* (Mersch). Use this to scope every greenfield SaaS — v1 minimum, v2 graduation, v3 industrialization.

## The Matrix

| Capability | v1 ($0-1M ARR) | v2 ($1-10M ARR) | v3 ($10-100M+ ARR) |
|---|---|---|---|
| Multi-tenant isolation (RLS / per-tenant FK) | Required | Required | Required |
| Tenant context in logs / metrics / traces | Required | Required | Required |
| Automated billing (Stripe Billing or equivalent) | Required | Required | Required |
| Webhook reconciliation job | Required | Required | Required |
| Self-serve onboarding | Recommended | Required | Required |
| Tenant lifecycle state machine + status_history | Recommended | Required | Required |
| Audit log on super-admin actions | Recommended | Required | Required |
| Internal admin / back-office console | Recommended | Required | Required |
| Feature flags + canary deployment | Optional | Required | Required |
| Per-tenant cost attribution | Optional | Required | Required |
| Per-tenant rate limits + quotas | Optional | Required | Required |
| Lifecycle email engine (6 sequences) | Optional | Required | Required |
| Public API + webhooks (for tenants) | Optional | Recommended | Required |
| SSO (SAML 2.0 + OIDC) | Optional | Recommended | Required |
| SCIM 2.0 provisioning | Optional | Optional | Required (enterprise) |
| Custom-domain support | Optional | Optional | Required (enterprise) |
| IP allowlists per tenant | Optional | Optional | Required (enterprise) |
| Audit log API (for tenants) | Optional | Optional | Required (enterprise) |
| Status page (public) | Optional | Required | Required |
| Trust portal (SOC2 + DPA + subprocessors) | Optional | Recommended | Required |
| SOC 2 Type II | Optional | Recommended | Required |
| ISO 27001 | Optional | Optional | Recommended (enterprise) |
| Multi-region (active-passive) | Optional | Optional | Required |
| Per-tenant data residency | — | Optional | Required (enterprise) |
| Sandbox / demo tenants | Optional | Recommended | Required (enterprise) |
| GDPR/POPIA data export + erasure | Required | Required | Required |
| DR drills (quarterly) | Optional | Recommended | Required |
| Observability (logs + metrics + traces, tenant-tagged) | Recommended | Required | Required |
| On-call rotation + runbooks | Optional | Required | Required |
| Cohort retention + NRR dashboard | Optional | Required | Required |
| Reverse-ETL to CRM | Optional | Recommended | Required |
| Customer health score | Optional | Recommended | Required |

## How to Use

For a greenfield SaaS project:
1. Identify the **target ARR band in 12 months**.
2. Highlight every "Required" row in that column.
3. Scope v1 = "Required at this stage + Recommended I won't regret".
4. Schedule v2 graduation as a deliberate program when ARR is forecast to cross the band.
5. v3 industrialization is a 6-12 month program; start when v2 metrics show product-market fit and growth velocity.

## Stage Cliffs

Each transition has a "cliff" — capabilities that **must** be in place before crossing or growth breaks:

- $1M cliff — onboarding automation, reconciliation, support tooling, lifecycle email.
- $10M cliff — multi-region, SSO/SCIM, SOC 2, status page, on-call rotation.
- $100M cliff — per-tenant residency, advanced enterprise feature pack, FinOps practice, capacity planning ritual.

## Anti-Patterns

- "We'll add SSO when we land the first enterprise deal." It's a 6-week build; the deal is 4 weeks long.
- "Reconciliation can wait." Drift compounds; one bad month creates years of finance pain.
- "SOC 2 is for later." 6-month evidence collection window; start at $1M ARR if enterprise is on the roadmap.
- "Status page costs money." Customer trust costs more.

## See Also

- `saas-architecture-strategy` — the umbrella skill.
- `saas-control-plane-engineering` — most v2 capabilities live here.
- `subscription-billing` — billing baseline.
- Mersch *Hacking SaaS*; *How to Run a SaaS Business* (Trio).
