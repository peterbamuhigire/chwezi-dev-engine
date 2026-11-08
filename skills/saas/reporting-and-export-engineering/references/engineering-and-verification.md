Parent skill: [reporting-and-export-engineering](../SKILL.md)

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

# Engineering and verification

Use this reference when a reporting surface is built or tested, so the work can be delivered and
proved with this engine alone. It covers the build architecture, the records a report leaves
behind, test fixtures, performance, observability and tenant isolation. Rule IDs:
[rules-and-gates.md](rules-and-gates.md).

## Task 1: build on five layers

| Layer | Holds | Rule |
|---|---|---|
| Metrics layer | Versioned metric catalogue; measures computed once on the server from facts and dimensions with declared grain | RPT-METRIC-001/002/004 |
| Report definition registry | One entry per report: ID, title, owner, domain, privacy class, parameter schema, formats, default sort, allowed roles, metric versions, retention | RPT-EXPORT-007 |
| Generation service | Immutable generation records; background jobs for large output | RPT-EXPORT-004/005 |
| Presentation | Screen components and separate print templates; formatting only, no arithmetic; both read the same canonical dataset | RPT-VIEW-007, RPT-RECON-003 |
| Delivery and archive | Downloads, scheduled delivery, share links, retention; every exit authorised and logged | RPT-SEC-001/003 |

Calculations stay server-authoritative. An offline client may show cached figures only with their
snapshot time and never presents a locally computed total as reconciled.

## Task 2: write the generation record

```yaml
generation:
  id: gen_01JC8Z3K4Q            # opaque; not a document number
  report_id: sales.daily_close
  report_version: 3
  parameters: {tenant: t_118, branch: kampala_road, business_day: 2026-11-03, timezone: Africa/Kampala, currency: UGX}
  metric_versions: {sales.net_sales: 1.2.0, cash.collections: 1.0.0, cash.variance: 1.0.0}
  source_watermark: "ledger posting 88412; sync complete except branch kireka (last 11:40)"
  requested_by: user_442        # or service identity for schedules
  kind: download                # download | scheduled | share
  status: ready                 # queued | running | ready | failed | expired
  outputs: [{format: pdf, pages: 4, sha256: "..."}, {format: xlsx, sha256: "..."}]
  created_at: 2026-11-03T19:02:11+03:00
  expires_at: 2026-11-10T19:02:11+03:00
```

The record is written once and never edited; a re-run creates a new record. Machine timestamps
use ISO form inside records and files; every screen shows the readable form (`3 Nov 2026, 19:02`).

## Task 3: run export jobs

States: queued, running, ready, failed, expired, cancelled. An identical request (same report,
parameters and requester) while one is queued or running returns the existing job instead of a
second one. Transient failures retry with back-off a bounded number of times, then fail visibly
with a reason. Ready files expire; links to expired files say so. File names are deterministic and
contain no personal data (RPT-EXPORT-004).

## Task 4: test with four fixtures per component and five per reconciliation

| Fixture | Purpose |
|---|---|
| Normal | Representative values at production scale |
| Extreme value | Very large amounts, long names, many rows, 200% text |
| Missing data | Unsynced branch, missing period, absent source |
| Permission-restricted | A role that may see only part of the scope |

Reconciliation adds positive, zero, negative, reversed and missing-data cases across headline,
detail, ledger, PDF and spreadsheet (RPT-RECON-001/003). Formatter tests cover ISO 4217 minor
units, percentage versus percentage-point wording and "New this period". Export tests open the
CSV and XLSX output and include an injection fixture and leading-zero identifiers
(RPT-EXPORT-002/003). Print tests render every page (RPT-PRINT-008).

Fixture data is synthetic, reconciled and labelled synthetic; it never ships in a production build.

## Task 5: budget and measure performance

- Record a budget per surface for query time, payload size and render time on the declared
  baseline device and dataset, then measure it (RPT-PERF-002). Never promise a universal
  millisecond figure.
- Aggregate on the server; paginate or virtualise detail; bound the points a chart draws; run
  large exports as jobs (RPT-PERF-001).
- Caches carry their snapshot time and are invalidated explicitly when source data changes
  (RPT-PERF-003); a refresh keeps the last valid figures on screen.

## Task 6: observe in production

Track query duration, cache hit rate, export queue time, job failure rate, reconciliation
mismatches, permission denials, report adoption and task completion. Alert on any mismatch and on
repeated job failures. Never log raw sensitive payloads; log identifiers and counts.

## Task 7: prove tenant and role isolation

- Call the report, export and schedule endpoints directly with a lower-role session and with
  another tenant's session; both must return only authorised rows and fields (RPT-SEC-001,
  RPT-GATE-04).
- Check that a scheduled report re-checks the recipient's rights at each run, not only when the
  schedule was created.
- Check masked fields in previews, emails, file names and logs (RPT-SEC-003).

## Task 8: review before release

Independent verifier for every reporting change; a human domain reviewer as well for financial,
clinical or regulatory reports (RPT-QA-002). Record the gate table with evidence classes; any
applicable gate without `MEASURED` evidence keeps the verdict at BLOCKED.

## Evidence/currentness

No external fact is cited here. Retry counts, budgets and expiry periods are product decisions
recorded in the report contract.
