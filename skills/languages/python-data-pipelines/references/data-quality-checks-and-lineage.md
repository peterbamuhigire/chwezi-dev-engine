# Data Quality Checks and Lineage for Contract-Backed Pipelines

Parent skill: [python-data-pipelines](../SKILL.md).

Load when a pipeline publishes to, or reads from, an interface governed by a data
contract and you must decide where each quality check runs, how service-level
objectives are measured, and how lineage is emitted so impact analysis and
deprecation are evidence-based.

Neighbours: record-level validation and dead-letter handling stay in
`validation-and-deadletter.md`; run tracking, Prometheus metrics, and alert rules
stay in `observability-pipelines.md`. Contract authoring and change classification
live in `../../../backend-databases/database-design-engineering/references/data-contracts-and-schema-evolution.md`.

## 1. Two kinds of quality failure

| Kind | Examples | Primary defence | Secondary defence |
|---|---|---|---|
| Predicted: the contract names it | Wrong type, missing required field, value outside enum, negative amount, duplicate key | Schema plus declared checks, enforced before data reaches consumers | Post-publish checks for rules that need the whole table |
| Unpredicted: nobody wrote a rule | A timestamp in the future, a sudden 40% drop in daily volume, one branch's records all zero | Resilient consumers that quarantine bad records and keep processing good ones | Profiling and anomaly detection on the published interface, alerting the producer |

Decision rule: every incident caused by an unpredicted failure produces a new
predicted check in the contract within the incident's corrective actions. Track
the ratio; a mature feed shifts failures from the second row to the first.

## 2. Where each check runs

| Placement | Blast radius when it fires | Use for | Implementation |
|---|---|---|---|
| Publish time, in the producer | Contained at source; no consumer sees the record | Row-level rules: type, required, pattern, range, enum, referential shape | Validate each record against a schema generated from the contract (JSON Schema 2020-12 or Pydantic model); failing records go to the producer's dead-letter queue and page the producer |
| Infrastructure | Contained; the write is rejected | Structural type conformance | Table schema generated from the contract; topic schema enforcement where the broker supports it |
| After publish | Consumers may already have read it | Set-level rules: uniqueness across the table, row counts, cross-table reconciliation, distribution drift | Scheduled SQL or a checks tool reading the contract's `quality` block; results attached to lineage (Section 5) |

Prefer the earliest placement that can evaluate the rule. A uniqueness rule
cannot be proven per record; a pattern rule should never wait for a nightly job.

## 3. Mapping contract quality rules to executable checks

ODCS v3.2.0 library metrics and how to implement them without inventing semantics:

| Metric | Meaning to implement | Typical operator |
|---|---|---|
| `nullValues` | Count of nulls in the column | `mustBe: 0` for required fields |
| `missingValues` | Count of values treated as absent: null plus declared sentinels such as `''`, `'N/A'`, `'0000'` passed in `arguments` | `mustBeLessOrEqualTo` a count or percent |
| `invalidValues` | Count failing declared valid values or pattern in `arguments` | `mustBe: 0` |
| `duplicateValues` | Duplicates in one column or a column combination | `mustBe: 0` for keys |
| `rowCount` | Rows in the object for the check window | `mustBeBetween` a volume band |

Rules:

1. Read thresholds from the contract at run time; never hard-code a second copy.
2. Evaluate over a stated window (for example, the business day in `Africa/Kampala`
   converted to UTC boundaries) and record the window with the result.
3. `severity: error` blocks promotion or pages; lower severities report only.
4. Use `type: sql` for rules the library cannot express, and keep the query
   dialect-specific to the declared server.
5. Record `unit` (`rows` or `percent`) with every result; a bare number is not evidence.

## 4. Measuring service-level objectives

A contract SLO is only credible if a machine measures it continuously.

| SLO | Measurement | Where the timestamps come from |
|---|---|---|
| Latency or timeliness | Publish time minus business-event time, p95 over the window | Event time set by the producer (`received_at`); publish time set by the broker or loader, never by the consumer |
| Freshness | Now minus the latest business-event time available to consumers | Max event time in the interface |
| Completeness | Records published divided by records the source says it produced, per window | Producer-side count emitted with the run (output statistics) |
| Availability | Proportion of probe queries against the interface that succeed | Synthetic probe from outside the producer's network |

Alert the producer when the burn rate threatens the SLO, not when a consumer
notices a stale dashboard.

## 5. Emitting lineage with OpenLineage

Lineage is how you find every reader before a breaking change, every affected
report during an incident, and every downstream copy during an erasure request.
Draw it from runtime events; hand-drawn lineage diagrams are stale on the day they are drawn.

Model:

- A **job** is the recurring process (`publish_loan_repayment_received`).
- A **run** is one execution, identified by a UUID (UUIDv7 preferred by the spec).
- **Datasets** are named by `namespace` (where the data lives) and `name`.
- Each run emits one `START` and exactly one terminal event (`COMPLETE`, `FAIL`,
  or `ABORT`); `RUNNING` and `OTHER` are optional additions.
- Facets carry extras: `schema`, `ownership`, `columnLineage`, `outputStatistics`,
  and data-quality facets (`dataQualityAssertions`, `dataQualityMetrics`), which
  attach to the dataset being checked as an input facet.
- `JobEvent` and `DatasetEvent` declare static lineage and metadata outside a run;
  use them to register a contract-backed dataset before the first run.

Verified minimal pattern (openlineage-python 1.53.0; executed with the console
transport on 2026-09-24):

```python
from datetime import datetime, timezone
from uuid import uuid4  # use a UUIDv7 generator where available; the spec prefers v7

from openlineage.client import OpenLineageClient
from openlineage.client.event_v2 import (
    InputDataset, Job, OutputDataset, Run, RunEvent, RunState,
)
from openlineage.client.facet_v2 import data_quality_assertions_dataset as dqa

PRODUCER = "https://git.example.ug/lending/repayment-publisher"
client = OpenLineageClient()  # reads openlineage.yml or OPENLINEAGE_URL

SOURCE = ("postgres://lending-db:5432", "lending.public.repayments")
TARGET = ("bigquery", "lending.loan_repayment_received_v2")


def emit(job_name, run, state, inputs=(), outputs=()):
    client.emit(RunEvent(
        eventType=state,
        eventTime=datetime.now(timezone.utc).isoformat(),
        run=run, job=Job(namespace="lending", name=job_name),
        producer=PRODUCER, inputs=list(inputs), outputs=list(outputs),
    ))


# 1. Publish job: lineage edge source -> contract interface.
publish = Run(runId=str(uuid4()))
emit("publish_loan_repayment_received", publish, RunState.START,
     inputs=[InputDataset(*SOURCE)])
# ... extract, validate against the contract, load ...
emit("publish_loan_repayment_received", publish, RunState.COMPLETE,
     inputs=[InputDataset(*SOURCE)], outputs=[OutputDataset(*TARGET)])

# 2. Verify job: contract checks reported as input facets of the checked dataset.
verify = Run(runId=str(uuid4()))
results = [
    dqa.Assertion(assertion="amount_ugx_positive", success=True, column="amount_ugx"),
    dqa.Assertion(assertion="repayment_id_unique", success=True, column="repayment_id"),
]
checked = InputDataset(
    *TARGET,
    inputFacets={"dataQualityAssertions": dqa.DataQualityAssertionsDatasetFacet(assertions=results)},
)
emit("verify_loan_repayment_received", verify, RunState.START, inputs=[InputDataset(*TARGET)])
emit("verify_loan_repayment_received", verify, RunState.COMPLETE, inputs=[checked])
```

Operational rules:

1. Emit `FAIL` from the exception handler; a run with `START` and no terminal
   event is an incident signal, not noise.
2. Lineage emission must never fail the pipeline: send asynchronously or with a
   short timeout, and count dropped events as a metric.
3. Namespaces follow the OpenLineage naming conventions for each platform so that
   lineage from dbt, Spark, Airflow, and custom jobs joins on the same dataset identity.
4. Never put personal data in facets. Dataset names, column names, and assertion
   names only; no sample values.
5. Keep the lineage backend's retention at least as long as the longest
   deprecation window you run, or retirement checks become guesswork.

## 6. Acceptance checklist

- [ ] Every contract `quality` rule maps to one executable check, placed at the earliest point that can evaluate it.
- [ ] Check thresholds are read from the contract, not duplicated.
- [ ] Each result records rule id, window, unit, observed value, pass or fail.
- [ ] Latency, freshness, completeness, and availability SLOs are measured by machines, with producer-side timestamps.
- [ ] Every run emits `START` plus exactly one terminal event; failures emit `FAIL`.
- [ ] Data-quality results are attached to the checked dataset in lineage.
- [ ] No personal data appears in lineage facets or check outputs.

## 7. Anti-patterns

- Consumers each re-validating raw data with private rules. Fix: move the rule
  into the contract and enforce it once at the producer.
- Nightly checks for row-level rules. Fix: enforce at publish time; keep nightly
  runs for set-level rules.
- Timeliness measured from the consumer's load time. Fix: use producer event time
  and broker publish time.
- Lineage maintained as a diagram in a slide deck. Fix: emit OpenLineage events
  from every job and query the backend.
- Letting lineage outages fail data delivery. Fix: fire-and-forget with a dropped-event metric.

## Evidence/currentness

Access date: 2026-09-24.

- OpenLineage: core spec schema `https://openlineage.io/spec/2-0-2/OpenLineage.json`
  (raw spec on GitHub `main`), event types `START`, `RUNNING`, `COMPLETE`,
  `ABORT`, `FAIL`, `OTHER`; latest release 1.53.0 published 2026-09-01 (GitHub
  releases API). Python import paths (`event_v2`, `facet_v2`) and the
  `Assertion` signature checked against the installed 1.53.0 wheel; the example
  above was executed with `OPENLINEAGE__TRANSPORT__TYPE=console`.
- ODCS v3.2.0 library metrics and operators: `schema/odcs-json-schema-v3.2.0.json`.
- JSON Schema current version 2020-12 (json-schema.org/specification).
- Specific check tools (Great Expectations, Soda, dbt tests) and lineage
  backends: current versions and ODCS import support `NOT_ASSESSED`.

Sources: Jones (2023) *Driving Data Quality with Data Contracts*; OpenLineage
project specification and Python client 1.53.0 (2026); Bitol project, Open Data
Contract Standard v3.2.0 (2026).
