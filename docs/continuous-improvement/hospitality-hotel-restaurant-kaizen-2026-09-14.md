# Hospitality, hotel and restaurant Kaizen - 2026-09-14

## Change

Added an engineering-catalog skill for PMS/POS and hospitality systems. It
defines modular domains, room/order/folio/KOT/KDS state machines, tenant and
capability isolation, append-only financial/audit events, idempotency, outbox
integration, offline safeguards, observability and release evidence. It keeps
Maduuka's target lean: core operations first, speculative automation later.

## Evidence discipline

The five hotel and seven restaurant books informed workflows and decision
criteria. Maduuka source/docs establish evidence surfaces and known gaps, not
certification. Current security, accessibility, privacy, fiscal and provider
claims must be verified by primary sources and executable tests.

## Experiment and gate

Hypothesis: vertical slices plus failure/concurrency/tenant/reconciliation tests
will reveal more product risk than feature-count tracking. Measure escaped
defects, unresolved `NOT_ASSESSED` items, recovery time and audit completeness
on the next Maduuka slice. Rollback by removing the route; retain existing
engineering skills. Next review: 2026-10-14.
