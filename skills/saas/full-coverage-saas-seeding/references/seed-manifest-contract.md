# Seed manifest contract

The manifest is a versioned plan, not a database dump. It contains no SQL, direct
table names, numeric foreign keys, passwords, tokens, real identifiers, or posted
journal lines.

## Required top-level fields

| Field | Requirement |
|---|---|
| `manifest_id`, `version`, `checksum`, `product`, `environment_class` | Stable identity and non-production target classification |
| `reference_catalogue_expectations` | Source/version/status and preservation assertions for default data |
| `tenants` and `facilities` | Stable natural keys, ownership, locale, timezone, configuration, and reset scope |
| `actors` | Fixture key, role, department, facility grants, status, supervisor, and separation-of-duties tags; credentials are external references only |
| `entities` | Stable fixture key, classification, prerequisites, actor, input, boundary, and expected state |
| `scenarios` | Journey key, module, ordered steps, actor, source keys, expected events/reports/invariants, negative cases, and rollback |
| `fault_probes` | Isolated probe key, target scenario, injected condition, expected refusal/recovery, and evidence requirement |
| `reset_policy` and `verification` | Owned cleanup boundary, preservation checks, counts, isolation, reconciliation, and evidence destinations |

## Classification rule

Use `reference`, `tenant_configuration`, `demo_activity`, or `fault_probe` on every
entity. Global categories, status vocabularies, currencies, units, countries,
permissions, coding lists, and medicine catalogue entries are `reference`;
hospital examples:
fictional facility policy is `tenant_configuration`; patients and encounters are
`demo_activity`; a cross-tenant patient-ID attempt is a `fault_probe`.

## Entity and scenario rules

- Prefer natural fixture keys such as `DEMO-HOSP-A-PATIENT-001`; resolve server IDs from application responses and store them in the entity ledger.
- Every write carries tenant, actor, scenario, idempotency, correlation, and manifest checksum metadata where the application supports it.
- Every dependency is a fixture key or scenario key, never a guessed database ID.
- Expected state and invariant assertions must be independently verifiable.
- A missing supported boundary is `BLOCKED`, not an alternate SQL implementation.
