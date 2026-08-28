# Electronic Fiscal Taxing Skill — 2026-08-28

Added the jurisdiction-neutral `electronic-fiscal-taxing` engineering skill
under `skills/finance-accounting/`, with a detailed Uganda EFRIS reference pack.
The skill covers fiscal-provider adapters, tenant/TIN isolation, API contracts,
cryptographic boundaries, outbox/queue reliability, offline/manual states,
reconciliation, observability, and Android read-only projections.

The reference pack was independently distilled from the eight supplied EFRIS
Markdown books and checked against URA public EFRIS pages on 2026-08-28. Older
or conflicting technical details remain explicitly versioned and blocked until
the authenticated current URA technical pack is promoted in the consuming
project's source register.

The routing fixture was added before the skill and failed as expected; the
post-authoring routing, catalog, safety, and engine-control validations are the
release evidence for this change.
