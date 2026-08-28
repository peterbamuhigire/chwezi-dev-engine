# Fiscal Taxing Testing, Observability, and Release

## Required test matrix

- canonical mapping: seller, buyer, lines, UOM, tax categories, totals, payment;
- source hash and idempotency replay, changed-payload conflict, and concurrency;
- provider acceptance/rejection/timeout/duplicate/invalid response;
- tenant/profile/device wrong-owner and cross-tenant query tests;
- queue lease, retry backoff, dead-letter, permissioned replay, and recovery;
- online/offline/manual deadline and clock-skew behavior;
- FDN/verification/QR atomic persistence and print/read-model gating;
- credit/debit/cancel linkage and accounting reconciliation;
- migration backfill, rollback, retention, redaction, and load behavior;
- Android API projection, Room migration, sync retry, and user-visible states.

## Telemetry

Every attempt carries correlation ID, tenant/profile ID (non-secret), source ID,
document class, provider version, exchange ID, attempt, latency, state, error
class, queue age, and release version. Never emit payload secrets or full
personal/tax data into general logs. Alert on queue age/depth, rejection rate,
unknown results, missing evidence, cross-tenant attempts, dead letters, and
dictionary/key expiry.

## Release gates

1. Current URA source/register and onboarding evidence is approved.
2. Contract, security, isolation, accounting, and failure tests pass.
3. Sandbox/recorded official fixtures prove parser and idempotency behavior.
4. Rollback leaves commercial and fiscal evidence coherent; no duplicate replay.
5. Operators have dashboards, runbooks, replay permissions, and support owners.
6. Android builds pass min/current device checks and do not contain fiscal
   credentials.

If any legal, tax, security, privacy, or provider gate is unavailable, release
is `NOT ASSESSED` or `blocked`, not production-ready.
