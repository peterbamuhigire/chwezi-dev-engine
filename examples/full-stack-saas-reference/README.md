# Full-Stack SaaS Reference Evidence Pack

Last verified: 2026-07-08
Benchmark: Stripe-quality API discipline, Thoughtworks evolutionary architecture, Google SRE release evidence, OWASP security review.

This example shows how `skills-web-dev` composes into a complete delivery workflow. The running example is FieldOps Ledger, a Chwezi Core Systems multi-tenant field-service SaaS.

## Pack Contents

| File | Purpose |
|---|---|
| `architecture.md` | Service boundaries, data ownership, integration contracts, and trade-offs |
| `api-contract.md` | Resource-oriented API contract with idempotency, pagination, validation, export, and compatibility notes |
| `security-threat-model.md` | Tenant isolation, identity, secrets, database security, CI/CD, and abuse cases |
| `reliability-and-release.md` | SLOs, error budgets, observability, deployment, rollback, and incident evidence |

## How to Use This Example

1. Start with a user request such as: "Design a production-ready SaaS for field-service contractors."
2. Route through `SKILL.md` to SaaS, architecture, API, database, security, and reliability skills.
3. Use `templates/delivery-dod/evidence-pack.md` as the required release wrapper.
4. Consult `docs/source-registers/ai-platforms.md` before naming current vendor behavior.
5. Route statutory accounting behavior to `chwezi-accounting-doctrine`; do not hardcode tax rules here.

## Completion Standard

The example is complete when a reviewer can answer these questions without asking the author:

- What are the service boundaries and why are they not arbitrary?
- Which API calls are safe to retry and how is duplicate work prevented?
- Where is tenant isolation enforced and tested?
- Which user journeys have SLOs, alerts, rollback steps, and runbooks?
- What evidence blocks release if it is absent?
