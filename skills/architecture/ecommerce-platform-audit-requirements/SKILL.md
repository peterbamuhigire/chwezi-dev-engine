---
name: ecommerce-platform-audit-requirements
description: Use when scoping or specifying an e-commerce platform, payment, API, security, AI, data protection, integration, and remediation audit for SMEs or cross-border digital trade programmes.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# E-Commerce Platform Audit Requirements
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Overview

Use this skill to define a requirements-level audit protocol for e-commerce platforms. It gives the audit a standard, scope, evidence model, legal table, payment scope, integration review, AI review, and remediation backlog so the output is actionable and defensible.

## Use When

- Auditing or scoping an audit of an e-commerce website, app, marketplace presence, payment integration, logistics integration, API, data flow, or AI feature.
- Producing remediation requirements for SMEs in a donor or technical assistance programme.
- Reviewing cross-border readiness involving payment, data protection, consent, consumer trust, and platform security.

## Do Not Use When

- The task is only visual UX feedback or marketing copy.
- You cannot access enough system, process, or owner interview evidence to support findings.
- Legal advice is required. This skill identifies compliance issues and escalation needs; it does not replace counsel.

## Required Inputs

- Platform URLs/apps, architecture notes, payment/logistics providers, data flows, user journeys, admin roles, and support workflows.
- Countries where customers, operations, data processing, or partners are located.
- Known AI/recommendation/fraud/personalisation tools.
- Existing policies: privacy notice, terms, returns, consent, security, incident handling.

## Workflow

1. Define audit scope and evidence access.
2. Set standards baseline: OWASP Top 10, OWASP API Security Top 10, OWASP ASVS, CVSS, PCI-DSS where payment card scope exists, and NIST AI RMF for AI use.
3. Map architecture, integrations, data flows, roles, permissions, and third-party dependencies.
4. Scope payment security. Identify hosted redirect, embedded checkout, card data exposure, mobile money/gateway flows, reconciliation, settlement, refunds, and chargebacks.
5. Map privacy and consumer-protection obligations by jurisdiction using the verified EAC data-protection table and escalate uncertain legal questions.
6. Review AI use for data provenance, human oversight, bias, explainability, security, and EU AI Act exposure where relevant.
7. Produce a remediation backlog with severity, business impact, owner, effort, dependency, and acceptance criteria.
8. Write a founder-readable executive summary and a technical appendix.

## Quality Standards

- Every finding maps to a named standard, law/regime, policy, or observed evidence.
- PCI scope matches the real payment architecture.
- Country legal statuses use the verified table and are dated.
- AI review states whether AI exists, what data it uses, and what risk class/escalation applies.
- The remediation backlog is prioritised, owned, and testable.

## Anti-Patterns

- Vibes-based security review with no standard.
- Over-scoping PCI for a company that never touches card data.
- Using stale data-protection-law status.
- Proposing a payment rail without country coverage and reconciliation checks.
- Findings with no severity, owner, or acceptance criteria.

## Outputs

- Audit scope and evidence request list.
- Security, API, payment, integration, privacy, AI, and data-flow audit checklist.
- Verified EAC data-protection table reference.
- Remediation backlog.
- Founder executive summary and technical appendix requirements.

## References

- `references/audit-scope-and-standards.md`: Scope, standards, evidence, and payment/AI review.
- `references/eac-data-protection-table.md`: Verified EAC data-protection status table and legal-use rules.
- `references/remediation-backlog-template.md`: Backlog fields, severity, business impact, and acceptance criteria.
<!-- dual-compat-end -->
