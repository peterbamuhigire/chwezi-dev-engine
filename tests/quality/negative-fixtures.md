# Negative Quality Fixtures

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 negative-fixture pack

These fixtures prove release gates fail for the right reasons. Use them when reviewing `docs/quality-gates/release-blocking-gates.md` and `docs/quality-gates/anti-slop-governance.md`.

## Fixture 1: Generic Architecture Claim

Bad artifact:

> The platform will use a secure and scalable microservices architecture with modern cloud-native best practices.

Expected verdict: fail.

Reason: no service boundary, data owner, threat, SLO, deployment evidence, or trade-off. The fix is not better wording; the fix is an ADR with named capabilities and evidence.

## Fixture 2: API Without Idempotency

Bad artifact:

```http
POST /payments
```

Description: "Creates a payment."

Expected verdict: fail.

Reason: mutating payment-like operation has no idempotency key, duplicate-work behavior, retry guidance, or error model.

## Fixture 3: Security Checklist Without Tests

Bad artifact:

> We follow OWASP and use RBAC to keep users safe.

Expected verdict: fail.

Reason: OWASP is named without risk mapping; RBAC is asserted without role matrix, negative authorization tests, tenant isolation evidence, or audit trail.

## Fixture 4: SLO Without Release Consequence

Bad artifact:

> The service target is 99.9% uptime.

Expected verdict: fail.

Reason: no measurement window, critical journey, query, dashboard, alert, error-budget policy, or release-freeze rule.

## Fixture 5: Current Vendor Claim Without Source

Bad artifact:

> The latest model supports this tool natively and is the recommended production choice.

Expected verdict: fail.

Reason: "latest" and "recommended" are volatile claims without source register entry, verification date, or vendor documentation.
