# Kaizen Wave — Electronic Fiscal Taxing Engineering Skill

**Date:** 2026-08-28
**Engine:** skills-web-dev
**Baseline:** 63/100 capped portfolio baseline; no reusable fiscal-taxing
implementation route and no EFRIS-specific tenant/queue/mobile contract.
**Target:** 95/100; the portfolio reporting cap remains `min(raw, 65)`.

## Observe

BIRDC's ERP contains an EFRIS queue foundation and a fake client, while the
Android app correctly syncs only to the ERP. The missing reusable route was the
implementation contract connecting source documents, tenant-scoped profiles,
provider adapters, offline state, evidence, and mobile projections.

## Select and experiment

**Hypothesis:** one focused engineering skill with progressive Uganda references
will improve routing and reduce unsafe direct-provider/mobile implementations.

**Change:** add `skills/finance-accounting/electronic-fiscal-taxing/`, a Uganda
reference tree, a worked ERP mapping example, and a routing fixture. The fixture
was created first and the routing test failed because the route was absent.

**Owner/review:** web-dev engine owner with ERP, security, finance, and mobile
reviewers; re-audit after sandbox/UAT evidence.

**Rollback:** remove the route, fixture, and references while leaving unrelated
catalogue knowledge untouched; no production data mutation is part of this wave.

## Check and standardise

Run catalog guardrails, routing smoke/collision report, source-ingestion guard,
skill contract/quick validation, engine-control validation, and human safety
review. Promote the route only if it remains distinct from generic API,
distributed-systems, SaaS, and Android skills.

## Teach and re-measure

Update README, overview, plan index, next-feature tracker, routing fixture, and
this record. Re-measure routing precision, source currency, skill depth,
security, and applied proof after the current URA contract and BIRDC UAT results
exist. Current provider activation remains explicitly `NOT ASSESSED`.
