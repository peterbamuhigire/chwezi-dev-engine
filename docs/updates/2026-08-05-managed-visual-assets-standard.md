# Managed Visual Assets Standard Update — 2026-08-05

## Outcome

The engineering catalogue now has a dedicated owner for SaaS-managed authentication backgrounds,
surface-aware logos, and favicons: `skills/saas/saas-managed-visual-assets`.

The skill standardises:

- platform and tenant scope derived from authenticated server context;
- a hard 20-background limit per scope, including inactive items;
- one light-surface logo, one dark-surface logo, and one favicon slot;
- RBAC, CSRF, idempotency, concurrency-safe ordering/quota, audit, and fallback;
- private quarantine, bounded decode, metadata stripping, canonical re-encode, immutable random
  storage keys, controlled delivery, replacement safety, cleanup, and rollback;
- admin/API contracts and a release test matrix.

`skills/frontend-ux/image-compression` was tightened at the same time. Client Squoosh/Canvas
preflight remains useful for speed but is no longer described as security authority. The server
contract now requires detected-content validation, decoder and pixel/resource limits,
profile-aware alpha preservation, canonical re-encoding, final output limits, and private storage.

## Cross-engine boundary

The engineering catalogue owns implementation and lifecycle. The separate
`design-system-skills/webapp-gui-design` contract owns the glass auth composition, immediate-
surface logo selection, visual admin experience, typography, responsive behaviour, and design QA.
Consumers load both engines for a full implementation.

## Release evidence

Run the two strict skill contracts, catalogue guardrails, normal/collision routing, source
ingestion guardrail, engine compliance, routing unit tests, and `git diff --check`. Record any
unavailable deployment scanner or browser/assistive checks as conditional external gates rather
than claiming production readiness.
