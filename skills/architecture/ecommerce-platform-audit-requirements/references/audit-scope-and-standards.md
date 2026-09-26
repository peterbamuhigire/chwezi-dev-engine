# Audit Scope and Standards

## Evidence Request

- Public storefront/app links.
- Admin role list and access model.
- Architecture/integration diagram if available.
- Payment providers and flow description.
- Logistics and fulfilment integrations.
- Privacy notice, terms, returns/refunds, consent forms.
- Analytics and tracking tools.
- AI/recommendation/fraud/personalisation tools.
- Incident, backup, and support process.

## Standards Baseline

| Area | Baseline |
|---|---|
| Web application risk | OWASP Top 10. |
| API risk | OWASP API Security Top 10. |
| Verification | OWASP ASVS. Record the exact stable release in the scope and qualify each cited requirement ID by version (for example, `v5.0.0-1.2.5`). As checked on 2026-09-26, v5.0.0 is the latest stable release; recheck the [official ASVS project](https://owasp.org/projects/asvs) before each engagement. Do not use bleeding-edge content as a production baseline. |
| Severity | CVSS plus business impact. |
| Payment card scope | PCI-DSS and appropriate SAQ logic. |
| AI risk | NIST AI RMF; EU AI Act exposure where selling into or processing for EU markets. |

## Payment Review

- Does the company collect, transmit, process, or store card data?
- Is checkout hosted/redirected or embedded?
- Which mobile money/gateway rails are used in each country?
- How are failed payments, refunds, settlement, chargebacks, and reconciliation handled?
- Are payment logs protected and minimised?

## AI Review

- What AI feature exists and why?
- What data trains or prompts it?
- Is personal data used?
- Is output shown to customers or used in eligibility/credit/fraud decisions?
- Is there human review for consequential decisions?
- Is there a documented fallback when AI fails?
