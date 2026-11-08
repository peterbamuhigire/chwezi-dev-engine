Parent skill: [reporting-and-export-engineering](../SKILL.md)

# Verification fixtures, performance budgets and observability

Load this when planning tests, performance work or telemetry for reporting surfaces. It covers
RPT-VIEW-007, RPT-STATE-001..005, RPT-PERF-001..003, RPT-QA-001..003 and the trust gate
RPT-GATE-08 (unknown shown as known).

## 1. Fixture set per component (RPT-VIEW-007)

Every reporting component (KPI tile, variance badge, filter bar, date range, data table,
hierarchy table, chart, reconciliation warning, narrative card, export status, A4 header, A4
financial table, empty state) ships with at least four fixtures:

| Fixture | Contents | Proves |
|---|---|---|
| Normal | Realistic, synthetic, labelled fictional | Layout and formatting |
| Extreme value | 12+ digit UGX total, 80-character names, negative and zero values, 10,000 rows | No overflow, truncation or compact form on totals |
| Missing data | Null cost, unsynced branch, source down | "Not available" with reason; never 0 (RPT-STATE-002) |
| Permission restricted | Lower-role scope, masked fields | Only permitted data; masked fields read "Restricted" |

Components receive values, units, currency, period and status from the server; they contain no
domain arithmetic. Snapshot or screenshot tests cover density and light and dark modes; the
print variant is tested without hover or tap-only content.

## 2. Reporting state matrix (RPT-STATE-001..005)

In addition to the product's usual screen states (loading, empty, error, offline and so on), a
reporting surface models these as distinct values of one state type, never as booleans that can
contradict each other:

```kotlin
sealed interface ReportData {
  data class Ready(val snapshotAt: Instant, val complete: Boolean, val values: ReportValues) : ReportData
  data class Partial(val snapshotAt: Instant, val missingSources: List<SourceRef>, val values: ReportValues) : ReportData
  data class Stale(val lastGood: Instant, val values: ReportValues) : ReportData
  data class ReconciliationFailed(val difference: Money, val cause: String?, val lastGood: Instant) : ReportData
  data class SourceDisconnected(val source: SourceRef, val since: Instant) : ReportData
  data class AccessRestricted(val reason: String) : ReportData
  data class ExportPending(val jobId: String, val progress: Int?) : ReportData
  data class NoData(val reason: NoDataReason) : ReportData   // none recorded, out of scope, not yet synced
}
```

Rules: no data, unknown and restricted never render as zero; the reconciliation warning has no
dismiss action until resolved (test that a dismiss attempt fails); refresh keeps the last valid
figures with a refresh indicator; freshness shows snapshot time, source lag and estimated versus
actual, never a bare "confidence %".

## 3. Verification matrix (RPT-QA-001, RPT-QA-002)

| Layer | What | Evidence |
|---|---|---|
| Data | Reconciliation harness (five fixture classes), fan-out tests, period boundary tests across midnight and month end in the tenant timezone, back-dated postings, currency rounding | RECON, UIT |
| Security | Role x endpoint denial matrix for view, export, print, schedule, share | UIT, NET |
| Interface | State matrix screenshots at each width class, keyboard and screen-reader run, 200% text | SHOT, AT |
| Exports | Injection fixture, leading zeros, totals equal screen | EXPORT, UIT |
| Print | Acceptance cases in [print-pipeline-acceptance.md](print-pipeline-acceptance.md) | PRINT |
| Scale | Production-scale dataset (or a documented synthetic one at the same volume) | TRACE |
| Review | Independent verifier; human domain reviewer for financial, clinical or regulatory reports | REVIEW |

Test data is synthetic and labelled; no figure from a reference mockup or design inspiration
enters a fixture or a production build.

## 4. Performance (RPT-PERF-001..003)

- Aggregate on the server; ship summaries, not row dumps, to dashboards. Detail lists paginate
  with keyset pagination or virtualise on the client.
- Budget per report: query time at p95, payload size and render time, each for a named target
  device class and a named dataset size, recorded in the report's contract. Measure on the
  baseline device the product declares; emulator or developer-laptop numbers alone are not
  evidence. Never publish a universal millisecond promise.
- Index for the report's grain and filters (tenant, branch, business date); check the plan on
  production-sized data.
- Cache: every cached aggregate carries `computed_at` and a freshness target; invalidate
  explicitly on the events that change it (posting, void, back-dated entry, day reopen) as well
  as by time. Test that a void after close changes the cached figure.
- Large exports always run as jobs ([generation-records-and-export-jobs.md](generation-records-and-export-jobs.md)).

## 5. Observability

The standard asks for measurement after release (RPT-QA-003) and for measured budgets
(RPT-PERF-002); the signals below are this engine's engineering practice for meeting them.
Telemetry design follows `observability-monitoring`.

| Signal | Use | Alert |
|---|---|---|
| Report query duration (p50, p95) by report ID and tenant size band | Budget tracking | p95 above budget for a sustained window |
| Cache hit rate and age at read | Freshness and cost | Age above freshness target |
| Export queue latency and job duration | Capacity | Queue latency above target |
| Job failure rate by reason | Reliability | Any rise above baseline |
| Reconciliation mismatches by report and tenant | Data integrity | Every mismatch on a fixed report |
| Role denials on report and export endpoints | Security signal | Spikes per actor |
| Report adoption, task completion and misreading reports | Kaizen input (RPT-QA-003) | Reviewed each cycle |

Log identifiers (report ID, generation ID, tenant key, actor ID, durations, row counts), never
raw payloads, amounts tied to named people, personal data or file contents.

## 6. Multi-tenant isolation checks

- Every reporting query takes tenant and branch scope from the authenticated server context.
- Caches, job payloads, storage paths and share links are keyed by tenant.
- Fixture: two tenants with identical record ids and names; every report, export, schedule and
  share returns only the requester's tenant data.
- Cross-tenant aggregates exist only in platform-owner reports with their own permission and
  never include tenant-identifying details beyond what the platform role is allowed to see.
