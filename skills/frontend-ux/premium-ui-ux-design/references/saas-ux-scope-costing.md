# SaaS UX Scope And Costing

This reference is self-contained. It distills the user's supplied Design Studio UI/UX
articles into reusable scope, costing, and SRS rules without depending on the source
pages remaining available.

Sources used:

- https://www.designstudiouiux.com/blog/saas-ux-design-cost/
- https://www.designstudiouiux.com/blog/how-to-design-and-build-saas-product/
- Bank of Uganda May 2026 macro indicators for USD/UGX calibration.

## Core Rule

Price UX by product risk, buyer value, evidence required, and delivery responsibility,
not by screens alone. Screen count is a workload input; it is not the commercial model.

## Discovery Questions

Capture these before recommending UI/UX approach or fee band:

| Question | Why It Changes Scope |
|---|---|
| Who must activate in the first session? | Defines onboarding, time-to-value, and first-run UX. |
| What 3-5 core capabilities prove the MVP? | Prevents feature bloat and false enterprise scope. |
| How many user roles and permission levels exist? | Drives IA, navigation, states, and testing matrix. |
| What data surfaces are decision-critical? | Drives dashboards, tables, filters, exports, and chart QA. |
| What integrations or compliance duties exist? | Raises design, copy, error, audit, and handoff effort. |
| What business value is at stake in 12-24 months? | Sets value-based pricing ceiling and project priority. |
| What proof is needed before engineering starts? | Determines wireframes, prototype fidelity, usability tests, and SRS traceability. |

## Scope Bands

| Band | Best Fit | UX Deliverables | Typical Duration |
|---|---|---|---|
| Lean MVP | Founder-led validation, one primary role, 3-5 capabilities | UX brief, IA, core flows, low/mid fidelity wireframes, basic design tokens, dev handoff | 3-6 weeks |
| Funded MVP | Multi-role SaaS, dashboards, onboarding, billing/admin surfaces | Research synthesis, IA, clickable prototype, component states, usability testing, SRS-ready UX requirements | 6-10 weeks |
| Growth Product | Existing SaaS with churn, adoption, dashboard, or enterprise-readiness problems | UX audit, role-based IA, design system extension, analytics-backed redesign, workflow QA, adoption metrics | 8-14 weeks |
| Enterprise SaaS | Committees, compliance, data-heavy workflows, integrations, audit needs | Research plan, service blueprint, permission/state matrix, enterprise patterns, evidence pack, formal sign-off gates | 12-24+ weeks |

## Uganda-Calibrated Fee Bands

Use these as starting bands for Ugandan and East African companies, then adjust by value,
risk, urgency, proof burden, and buyer maturity. Convert USD to UGX with the current
Bank of Uganda or bank selling rate at proposal time. In May 2026, public rate sources
cluster around UGX 3,700-3,800 per USD, so do not hard-code a stale exchange rate.

| Band | Local SME / Startup | Established Ugandan Company | Export, Donor, Regional, Or Funded Buyer |
|---|---:|---:|---:|
| UX audit / design diagnosis | $300-$900 | $900-$2,500 | $2,500-$6,000 |
| Lean MVP UX package | $1,200-$3,500 | $3,500-$8,000 | $8,000-$18,000 |
| Funded MVP / full UX spec | $3,500-$9,000 | $9,000-$20,000 | $20,000-$45,000 |
| Growth redesign / dashboard UX | $5,000-$15,000 | $15,000-$35,000 | $35,000-$75,000 |
| Enterprise SaaS UX programme | Rarely a fit | $25,000-$60,000 | $60,000-$150,000+ |
| Monthly UX/product retainer | $500-$2,000 | $2,000-$6,000 | $6,000-$12,000+ |

Do not treat a low Ugandan market budget as permission to reduce quality. Reduce scope,
fidelity, number of flows, research depth, or support window while preserving the quality
gate for what remains.

## Cost Drivers

Score each 0-2 and use the total to move within or above the selected band.

| Driver | 0 | 1 | 2 |
|---|---|---|---|
| User roles | 1 role | 2-3 roles | 4+ roles or permission tiers |
| Workflow complexity | CRUD/basic | Multi-step business process | Regulated, irreversible, or cross-team |
| Data complexity | Simple lists | Dashboards/tables | Analytics, exports, reconciliation, audit |
| Research depth | Stakeholder interview only | User interviews + prototype test | Field study, usability lab, longitudinal validation |
| Design system maturity | Existing system | Partial tokens/components | New system from scratch |
| Engineering handoff risk | Internal team known | Mixed team | Vendor handoff, legacy stack, strict QA |
| Commercial urgency | Flexible | Dated launch | Funding, board, procurement, compliance deadline |

0-4 points: floor of band. 5-8: mid-band. 9-14: upper band or next band.

## SRS And Handoff Requirements

Every formal UX package must produce:

- UX assumptions and excluded flows.
- Role and permission matrix.
- IA and navigation model.
- First-run onboarding and time-to-value requirement.
- Component state matrix for loading, empty, error, success, disabled, offline, and permissions denied.
- Pattern register for cards, tables, filters, modals, tabs, notifications, AI surfaces, and pagination.
- Acceptance criteria tied to SRS IDs, with verification method.
- Design handoff checklist: tokens, assets, responsive rules, accessibility notes, prototype links, and unresolved decisions.

## Pricing Guardrails

- Always present a paid diagnosis option when the brief is unclear.
- Never quote a full product UX fee from "number of screens" alone.
- Offer three options only when each option has a real scope difference.
- Protect the low option by reducing scope, not by skipping accessibility, states, or handoff quality.
- For Ugandan clients, state UGX and USD equivalents where helpful, but define which rate and date were used.
