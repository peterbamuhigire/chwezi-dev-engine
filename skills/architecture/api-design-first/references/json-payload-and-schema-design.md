# JSON Payload and Schema Design

Parent skill: [`api-design-first`](../SKILL.md). Load this reference when
designing or reviewing request/response bodies, event payloads, tool
input/output schemas, or the JSON Schema that governs them; when choosing
error-body format; or when a payload change must be classified as breaking or
non-breaking.

## Inputs

| Input | Source | If missing |
| --- | --- | --- |
| Resource and event list with owners | API action plan / domain model | Stop; do not invent fields |
| Consumer languages (JS, Python, Kotlin, Swift, PHP, SQL/BI tools) | Consumer inventory | Assume JavaScript clients (the strictest number limits) |
| Money, time, identity, and locale rules | Domain + finance engine | Block money fields until currency and precision are decided |
| Existing contract and published versions | OpenAPI / AsyncAPI / schema registry | Treat as greenfield and flag risk |

## Payload rules (house defaults)

### Shape

1. Top-level response is an object, never a bare array, so fields such as
   `meta` or `links` can be added later without a breaking change. (RFC 8259
   permits any top-level value; this is a house evolvability rule, not a
   syntax rule.)
2. Field names: `snake_case`, matching the house envelope already consumed by
   downstream skills (`per_page`, `documentation_url`). Pick one casing per API
   and lint it; mixing is the defect, not either choice.
3. Names carry units when the value is a measure: `duration_seconds`,
   `weight_grams`, `distance_metres`. Unitless `timeout` or `amount` is rejected.
4. Booleans are JSON `true`/`false`, positively phrased (`enabled`, not
   `disabled`; `is_`/`has_` prefixes are acceptable if applied consistently).
   Never `"yes"`, `1`, or `"Y"`. If a third state is plausible, use an enum.
5. Enums are lower-case strings from a documented closed set. Consumers must be
   told whether new values can appear; if they can, clients must handle an
   unknown value without crashing (document the fallback).
6. Polymorphic objects carry an explicit discriminator (`type`) with a closed
   set of values; never infer the variant from which fields happen to exist.
7. Separate business data from metadata: `data`, `meta`, `links`. Do not
   sprinkle `_created_by` style fields through business objects.
8. Bound everything: every string has `maxLength`, every array `maxItems`,
   every number a range. Unbounded fields are an availability and cost defect.

### Values that JSON does not model

| Value | Rule | Failure prevented |
| --- | --- | --- |
| Money | `{"amount": "150000", "currency": "UGX"}` with amount as a decimal string or integer minor units, currency as ISO 4217; state which, per API. ISO 4217 lists UGX with 0 minor units, so fractional UGX amounts are rejected | Float rounding, double-counting cents, mixed currencies |
| Integers above 2^53 - 1 (IDs, counters, ledger sequence numbers) | Serialise as strings | JavaScript silently rounds `9007199254740993` |
| Instants | RFC 3339 / ISO 8601 with offset, UTC `Z` preferred: `2026-09-24T07:30:00Z` | Local-time ambiguity across EAT and client zones |
| Calendar dates | `YYYY-MM-DD` with no time | Birthdays shifting a day across time zones |
| Durations | Integer with unit in the name, or ISO 8601 duration if humans read it | Seconds vs milliseconds mix-ups |
| Identifiers | Opaque strings. For new keys prefer UUIDv7 (time-ordered) or a prefixed opaque ID (`inv_01J...`); never sequential integers on public APIs | Enumeration/scraping, BOLA probing, index fragmentation |
| Binary | Out-of-band URL (pre-signed) for anything over a few KB; base64 only for small blobs, documented | 33 percent inflation, memory spikes |
| Geolocation | GeoJSON (`[longitude, latitude]` order stated) | Swapped coordinates |
| NaN / Infinity | Not representable; model the condition explicitly (`"reading_status": "sensor_fault"`) | Parser failure or silent null |
| Text | UTF-8 only; normalise to NFC before storing or comparing | Duplicate accounts from visually identical names |

### Absent vs null vs empty

Decide per field and write it in the schema description:

| State | Meaning (house default) | Schema expression |
| --- | --- | --- |
| Key absent in a response | Not applicable or not requested (sparse fieldsets) | Not in `required` |
| `null` | Known to be empty / deliberately cleared | `"type": ["string", "null"]` |
| `""` | Rejected for identifiers and codes; allowed only for free text where empty is meaningful | `minLength: 1` otherwise |
| Key absent in a PATCH body | Leave unchanged | JSON Merge Patch semantics (RFC 7396) |
| `null` in a PATCH body | Clear the field | Only for fields declared nullable |

## JSON Schema rules

1. Author schemas in JSON Schema 2020-12 and declare it (`"$schema":
   "https://json-schema.org/draft/2020-12/schema"`). OpenAPI 3.1 and 3.2 use a
   2020-12-based dialect, so the same schema serves the HTTP contract, the
   validator, and code generation.
2. Use `$defs` for local reuse and `$ref` for shared components; give shared
   schemas a stable `$id`.
3. Request schemas are closed: `"additionalProperties": false` (or
   `"unevaluatedProperties": false` when composing with `allOf`). Response
   schemas are documented as open to additions so clients learn to ignore
   unknown fields.
4. Nullability is `"type": [..., "null"]` in 2020-12/OpenAPI 3.1+. `nullable:
   true` is OpenAPI 3.0 only; flag it during migrations.
5. Use `oneOf` with a `const` discriminator for variants; avoid wide `anyOf`
   combinations that validators evaluate exponentially.
6. `format` (e.g. `date-time`, `email`, `uuid`) is an annotation by default in
   2020-12. Enable format assertion in the validator explicitly or add
   `pattern` constraints; do not assume `format` rejects bad input.
7. Every property has a `description` written for the consumer (and, for agent
   tools, for the model). Include one realistic `examples` entry.
8. Mark retiring fields `"deprecated": true` and state the removal date in the
   description; emit the `Deprecation` (RFC 9745) and `Sunset` (RFC 8594)
   response headers on endpoints being retired.
9. Validate at the edge before business logic; validate outbound payloads in
   tests (contract tests), not only inbound.

## Error bodies: RFC 9457 problem details

Public, partner, and agent-facing APIs return errors as
`application/problem+json` (RFC 9457, which obsoletes RFC 7807). The house
envelope in `rest-conventions.md` maps onto it without losing fields:

```json
{
  "type": "https://api.example.ug/problems/validation-error",
  "title": "Request body failed validation",
  "status": 422,
  "detail": "amount must be a positive whole number of UGX.",
  "instance": "/v1/fee-payments/req_7Q2",
  "code": "VALIDATION_ERROR",
  "errors": [
    { "pointer": "/amount", "detail": "Must be greater than 0." }
  ],
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

Rules: `type` is a stable, documented URI (it is the machine key; `title` is
for humans and must not vary per occurrence); extension members (`code`,
`errors`, `trace_id`) are allowed; field errors use JSON Pointer; never put
stack traces, SQL, or internal hostnames in `detail`. Internal first-party
APIs may keep the house envelope, but one API must not mix both formats.

## Classifying a change

| Change | Classification | Required action |
| --- | --- | --- |
| Add optional response field | Non-breaking (if clients ignore unknowns) | Document; add to changelog |
| Add optional request field with a default | Non-breaking | Document default |
| Add enum value to a response | Potentially breaking | Only if the contract promised an open enum; otherwise new version |
| Make an optional request field required | Breaking | New major version |
| Remove or rename a field; change a type (`5` to `"5"`) | Breaking | New major version, `Deprecation` + `Sunset` on the old one |
| Tighten a constraint (`maxLength` 200 to 100) | Breaking for requests | New version or accept-and-truncate policy stated |
| Change meaning without changing shape (amount now includes VAT) | Breaking and silent | New field name; never reuse the old one |

Automate the check: diff the OpenAPI/JSON Schema in CI with a breaking-change
detector and fail the build on unapproved breaks. For events, the schema
registry enforces backward or full compatibility per topic.

## Parsing, size, and performance

- Set a request body limit per endpoint (for example 64 KB for forms, 1 MB for
  batch import pages) and a maximum nesting depth (for example 32). Reject with
  `413` / `422` before full parsing.
- Stream large collections as NDJSON or JSON Text Sequences (and describe them
  with OpenAPI 3.2 sequential media types where tooling allows), or paginate.
- Compress responses (`gzip`/`br`) above a threshold; measure CPU cost.
- Reject duplicate object keys (RFC 7493 I-JSON forbids them); parsers differ
  on which value wins, which is exploitable.
- Switch to a binary format (Protocol Buffers, Avro, CBOR) only with evidence:
  a measured payload or CPU cost that JSON cannot meet, and consumers that can
  handle the tooling.

## Security rules for JSON handling

- Parse with the platform's standard parser only; never `eval` or template
  string assembly of JSON.
- Reject or strip `__proto__`, `constructor`, and `prototype` keys in
  JavaScript runtimes (prototype pollution).
- Bind validated fields explicitly into domain objects (allow-list); never mass
  assign a request body onto a model (OWASP API3:2023).
- Build responses from a response schema, not by serialising the ORM entity,
  so new internal columns cannot leak.
- Redact secrets and personal data (NIN, phone, MoMo numbers) in logs by field
  path; log the `trace_id`, not the body.
- When embedding JSON into HTML, escape `<`, `>` and `&` or use a data
  attribute with `textContent`.

## Original worked example: EFRIS-style invoice line

Rejected draft: `{"qty": 2.5, "price": 11800.00, "tax": true, "date": "24/09/2026"}`
(unitless quantity, float money, boolean tax, locale date).

Accepted design:

```json
{
  "line_id": "ln_01JAX3Q9ZK",
  "item_code": "MATOOKE-BUNCH-L",
  "quantity": { "value": "2.5", "unit": "bunch" },
  "unit_price": { "amount": "11800", "currency": "UGX" },
  "tax_category": "standard",
  "supplied_on": "2026-09-24"
}
```

## Premium vs generic output

| Generic AI output | Senior-grade output |
| --- | --- |
| `"price": 11800.00` | Decimal string + ISO 4217 currency, precision rule per currency |
| Every field optional, no bounds | Closed request schemas, bounded strings/arrays, explicit nullability |
| Invented error JSON per endpoint | One RFC 9457 problem type catalogue with stable `type` URIs |
| "Backward compatible" asserted | CI breaking-change diff result attached |

## Quality gate

- [ ] Every money, time, identifier, and large-integer field follows the table above.
- [ ] Request schemas closed; every string/array/number bounded.
- [ ] Absent/null semantics stated in each nullable or optional field's description.
- [ ] Error responses conform to RFC 9457 (or the documented internal envelope) consistently.
- [ ] Breaking-change diff run in CI; result recorded.
- [ ] Body size and depth limits configured and tested with an oversize payload.

## Evidence and currentness

Accessed 2026-09-24:

- json-schema.org/specification: current version 2020-12 (previous 2019-09); a newer version is in development and unreleased, so do not adopt it for contracts.
- spec.openapis.org: OpenAPI 3.1.2 and 3.2.1 are the latest patches; 3.1+ lets you set the dialect through `jsonSchemaDialect`/`$schema`.
- RFC 9457 *Problem Details for HTTP APIs* (July 2023, Proposed Standard) obsoletes RFC 7807. Correction: older guidance citing RFC 7807 is stale.
- ISO 4217 List One (SIX Group, maintenance agency): UGX, numeric 800, minor units 0.
- RFC 9745 *The Deprecation HTTP Response Header Field* (March 2025); Sunset must not be earlier than Deprecation.
- RFC 9562 (May 2024) obsoletes RFC 4122 and defines UUIDv7, which it recommends over v1/v6. Correction: sources citing "RFC 4122 format" for UUIDs are stale.
- AsyncAPI 3.1.0 default Schema Object is a JSON Schema Draft 07 superset; set `schemaFormat` explicitly when you need 2020-12 features in event payloads (tool support `NOT_ASSESSED`).
- Book corrections applied: RFC 8259 allows any JSON value at the top level (the object-first rule here is a house evolvability choice); formatting a float to 17 significant digits does not produce `"0.3"` from `0.1 + 0.2`, so money must never originate as a binary float; `required` fields were removed from proto3, so do not copy proto2 `required` into new `.proto` files.

Sources: Johnson (2025) *Practical JSON Design and Usage*; Dynowski and Dulak (2025) *Learning API Styles*; IETF RFC 8259, 7493, 7396, 9457, 9562, 9745; engine references `rest-conventions.md`, `api-error-handling.md`.
