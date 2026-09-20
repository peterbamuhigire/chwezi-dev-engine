---
name: hospitality-hotel-restaurant-systems
description: Use when architecting, specifying, implementing, or auditing PMS, POS, restaurant, hotel, resort, lodge, guest-house, venue, catering, or food-service software.
metadata:
  portable: true
  compatible_with: [claude-code, codex]
---

# Hospitality Hotel And Restaurant Systems
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->

Use with requirements, modular SaaS, PHP/API/database, security, finance,
offline-first, observability, testing, UX and professional documentation skills.
This is an implementation contract, not a certification that any existing
product is complete.

## Product boundary

Model one operational platform with bounded domains: tenant/property/outlet,
rooms and rates, guests, reservations, stays and folios, housekeeping,
maintenance, events, restaurant tables/orders/KOT/KDS, menus/recipes/inventory,
payments, shifts/day close, finance integration, reporting and administration.
Keep PMS and POS workflows independently usable but share only explicit,
reconciled contracts.

## Core engineering rules

- Every tenant/property/outlet query is scoped and negative-tested; role and
  capability checks occur server-side.
- State machines are explicit for room status, reservation, stay, folio,
  housekeeping task, order, KOT, payment, shift and night audit. Invalid
  transitions fail safely and create an audit event.
- Posted charges, payments, refunds, inventory movements, KOTs and audit events
  are append-only or reversal-based. Use idempotency keys and an outbox/queue
  for notifications, fiscal calls and integrations.
- Money, tax, discounts, tips/service charge, deposits, room charges, city
  ledger, recipe yield, wastage and reconciliation have an account/dimension
  owner. Route journal logic through the canonical finance posting service.
- Offline/staged operation must declare what is safe to queue, how conflicts are
  resolved, how a user sees stale state, and how duplicate orders/payments are
  prevented. Never silently overwrite.
- Provider boundaries isolate payment, SMS/WhatsApp, fiscal, channel manager,
  maps, identity and analytics. Contracts include timeout, retry, signature,
  idempotency, reconciliation and degraded-mode behaviour.
- Prefer a modular monolith plus durable queue for current scale. Introduce
  services only when measured load, isolation, team ownership or failure domain
  justifies them.

## Hotel implementation slices

1. Property/room types/rooms/capacity/amenities and room-status board.
2. Availability, reservation overlap protection, rate plans, restrictions,
   deposits, cancellation/no-show, group blocks and booking sources.
3. Guest profile/identity consent, check-in/walk-in, stay, folio, room charges,
   split/transfer, payment/refund and checkout.
4. Housekeeping assignment/inspection, maintenance work order and out-of-order.
5. Night audit/business date, city ledger, reconciliation, operational reports
   and event/meeting charges.

## Restaurant implementation slices

1. Outlets/areas/tables/reservations/waitlist and table status.
2. Menu/category/item/modifier/availability, price history, recipe/BOM/yield.
3. Order/seat/course/notes/allergy flag, KOT routing, station/KDS timers,
   reprint/void and manager override.
4. Bill, service charge/tips, discounts, split/transfer, room charge,
   payments/refunds, shift open/close and cash reconciliation.
5. Receiving, stock, wastage/spoilage, menu engineering, delivery/events,
   food-safety logs, finance posting and reports.

## Test and release contract

Each slice needs normal, validation, permission, tenant-isolation, concurrency,
retry/idempotency, rollback/reversal, offline/reconnect, device/browser,
accessibility, performance and rendered/UAT evidence where applicable. Test
room overlap, stale availability, duplicate payment, partial KOT failure,
negative stock, void-after-posting, tax/fiscal outage, lost connection, night
audit rerun, cross-property access and backup restore. Code or a screen is only
`observed`; release status requires executable evidence and owner sign-off.

## Evidence Produced

| Category | Artifact | Format | Example |
|---|---|---|---|
| Correctness | Scenario and state-transition evidence | Markdown table plus test output | Reservation overlap, folio posting, night-audit rerun and KOT state tests with expected outcomes |
| Security | Tenant, role and provider-boundary findings | JSON or Markdown finding record | Cross-property access denial, server-side capability check and webhook signature result |
| Data safety | Ledger, inventory and idempotency trace | JSON/YAML trace with stable IDs | Duplicate payment key, reversal lineage, stock movement and reconciliation evidence |
| Performance | Workload and latency result | Versioned benchmark record | Availability search, KDS timer and report query measured with data volume and environment |
| Operability | Recovery and owner runbook | Markdown runbook plus incident evidence | Fiscal outage, queue retry, backup restore and night-audit recovery steps |
| UX quality | Accessibility and device-state evidence | Test matrix plus rendered/UAT record | Keyboard flow, focus/error/loading states, narrow-screen and offline/reconnect results |
| Release evidence | Signed readiness and rollback record | Markdown/JSON manifest | Migration, feature flag, rollback, approver and unresolved-risk status |

## Deliberate exclusions until proven

No raw card storage, biometric guest ID, blockchain ledger, metaverse/VR as core,
robots, unexplainable AI pricing, broad OTA/channel manager, social feed,
microservice fleet, or feature with no actor, state, business outcome, control,
oracle, dependency and owner.

## Anti-patterns

- Treating a route, migration or screen as proof. Fix: execute the acceptance slice.
- Sharing a database without tenant/property/outlet lineage. Fix: enforce scope
  at repository, API, job, report and export boundaries.
- Retrying money, orders or fiscal calls without idempotency. Fix: persist keys
  and reconcile provider responses.
- Making offline mode silently overwrite state. Fix: show staleness, conflict and
  recovery, and queue only safe events.
- Adding AI or integrations before operational controls. Fix: gate them behind
  data, privacy, security, explainability and support evidence.

## Worked example

For a last-room booking, model the reservation command with a property-scoped
transaction, unique inventory constraint, idempotency key and audit event;
concurrently attempt a second booking, force a retry and restore a backup. The
slice passes only when one booking wins, the other receives a safe result, the
folio/report state reconciles and the event trail is complete.

## References

- `C:\wamp64\www\chwezi-dev-engine\docs\skill-routing-index.md`
- `C:\wamp64\www\chwezi-dev-engine\docs\source-registers\hospitality-currentness-2026-09.json`

<!-- dual-compat-end -->
