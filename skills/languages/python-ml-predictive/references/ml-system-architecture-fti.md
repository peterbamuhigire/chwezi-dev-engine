# ML System Architecture: Feature, Training and Inference Pipelines

Load when an ML model must run in production beyond a single notebook: designing a batch scoring system, a real-time prediction API, an LLM/RAG feature that uses enterprise data, deciding whether a feature store is warranted, or diagnosing training-serving skew, irreproducible training data or unexplained production degradation. `model-serving.md` covers the serving mechanics; `monitoring-and-drift.md` covers drift; `ai-rag-patterns` covers retrieval quality.

## Inputs

| Input | If absent |
| --- | --- |
| Prediction problem: entity (customer, loan, device), prediction target, decision it drives | Stop; architecture follows the decision |
| Latency need: batch (hours), near-real-time (minutes), online (sub-second) | Default to batch; it is cheaper and easier to get right |
| Feature freshness need: the maximum acceptable age of each feature at prediction time | Ask per feature; freshness drives pipeline technology |
| Label availability: how and how late true outcomes arrive | Mark performance monitoring `NOT_ASSESSED` until known |
| Data sources, owners and change cadence | Record as dependencies with owners |

## The decomposition

Every ML system, batch, real-time or LLM, splits into three independently run and tested programs joined by shared storage:

| Pipeline | Input | Output | Runs |
| --- | --- | --- | --- |
| **Feature** | raw data (DB rows, events, files, APIs, documents) | feature tables (and vector indexes) | on schedule or streaming |
| **Training** | feature tables + labels | versioned model in a registry, with metrics and lineage | on trigger (see retraining in `monitoring-and-drift.md`) |
| **Inference** | model + feature data (+ request data for online) | predictions, logged | batch: on schedule; online: per request |

Why: each pipeline has its own owner, cadence, scaling and tests; teams can change one without redeploying the others; and the shared storage (feature tables, model registry) is the contract. A single script that fetches, trains and predicts in one run cannot be monitored, backfilled or rolled back.

## Where each transformation belongs

| Transformation | Definition | Examples | Runs in |
| --- | --- | --- | --- |
| **Model-independent** | produces a reusable feature any model could use | 30-day transaction count, days since last repayment, rolling mean rainfall | feature pipeline only |
| **Model-dependent** | specific to one model's training data or framework | scaling, one-hot/target encoding, imputation with training means, tokenisation | training *and* inference, from the same fitted object |
| **On-demand** | needs data only available at request time | distance from the customer's usual location to this transaction, time since the previous request | online inference, *and* the feature pipeline when backfilling history, from the same function |

Rules:

- Model-dependent transformations run last, immediately before the model. Store features untransformed so they stay readable for analysis and reusable across models.
- Fit model-dependent transformations inside the training pipeline and ship them with the model (a scikit-learn `Pipeline`, a saved tokenizer at a pinned version). Re-implementing them in the serving code is the main source of training-serving skew.
- On-demand functions live in one importable module used by both the backfill and the online path. Two implementations will diverge.

## Do you need a feature store?

| Situation | Choice |
| --- | --- |
| One or two batch models, features computed in SQL, no online serving | No feature store. Versioned feature tables in the warehouse/Postgres/lakehouse with `entity_id`, `event_time`, `ingested_at` columns and point-in-time queries |
| Online model needing precomputed features in milliseconds | Offline table for training + key-value online copy (Redis, Postgres, or a feature store's online store) kept in sync by the feature pipeline |
| Many models sharing features across teams, time-series features, audit/lineage obligations (credit, health, insurance) | A feature store/platform (managed or open source) earns its cost |
| LLM/RAG over structured enterprise data | Retrieval by entity key from feature tables alongside document/vector retrieval (below) |

Whatever you choose, the data model is the same: rows keyed by entity id(s) plus an event time, written by feature pipelines, read through a declared selection of features per model (a "feature view"), versioned when the schema or meaning changes.

## Point-in-time correct training data

A training row labelled at time *t* may only use feature values known before *t*. Joining "latest features" onto historical labels leaks the future and produces a model that looks excellent offline and fails in production.

```python
import pandas as pd

# labels: loan_id, customer_id, decision_time, defaulted
# features: customer_id, event_time, txn_count_30d, avg_balance_30d
training = pd.merge_asof(
    labels.sort_values("decision_time"),
    features.sort_values("event_time"),
    left_on="decision_time",
    right_on="event_time",
    by="customer_id",
    direction="backward",          # only values at or before decision_time
    allow_exact_matches=False,     # exclude features stamped at the same instant
    tolerance=pd.Timedelta("35D"), # older values are stale; leave NaN, handle explicitly
)
```

Also filter on ingestion time when data can arrive late: a value with `event_time` before *t* but `ingested_at` after *t* was not available at decision time.

## Pipeline properties (acceptance criteria)

**Feature pipeline**
- Idempotent: rerunning a window produces the same rows (upsert on entity id + event time, never blind append).
- Backfillable: the same code computes history from a start/end parameter and runs incrementally in production.
- Validated on write: schema, ranges, nullability and uniqueness checked before commit; failing batches are quarantined, not half-written.
- Freshness SLO stated per feature group and monitored (for example, "mobile-money aggregates no older than 15 minutes at 08:00-20:00 EAT").

**Training pipeline**
- Reproducible training data: create the dataset once, version it (snapshot, commit id or table version plus split seed or cut-off), and have every candidate model read that same version. Re-querying "the same" data later returns different rows once late data arrives.
- Seeds set for the framework, NumPy and data loaders; residual non-determinism (GPU kernels) documented.
- Validation gates before registration: beats the agreed baseline on the held-out set; no protected or business-critical segment (region, gender, product, new vs returning customer) worse than an agreed floor; calibration checked for probability outputs.
- Registered with lineage: dataset version, feature view version, code commit, lockfile hash, metrics, and a model card (intended use, limits, segments evaluated, owner).

**Inference pipeline**
- Batch: reads features for the entities or time window being scored, loads the model version pinned in config (never "latest" implicitly), writes predictions with model version and timestamp.
- Online: defines a **deployment API** (what callers send, usually ids and request fields) separate from the **model signature** (the final feature vector). Callers must never assemble feature vectors.
- Logs the feature vector and prediction for every request or batch row; this log is the input to monitoring and to the next training set.
- Couples versions: a model version is deployed together with the feature view version it was trained on. Upgrading only the model while the online features come from an older, schema-compatible feature version produces a silent accuracy drop.

## Online latency budget and failure handling

Prediction latency is the sum of: request parsing, online feature lookup, on-demand transformations, model-dependent transformations, `predict`, feature/prediction logging and network. Budget each step and measure p95/p99 in the deployed environment, not on a laptop.

Fallbacks, decided and tested in advance:

| Failure | Fallback |
| --- | --- |
| Precomputed feature missing or stale | last known value from a bounded cache (with age limit), else training-set median/mode, and set a `feature_missing` flag |
| Online store unreachable | serve from cache or a simpler model using request data only |
| Third-party enrichment API slow | timeout below the budget; proceed without that feature |
| Model load failure on deploy | keep the previous version serving; fail the deploy |

Every fallback is logged with a reason code and counted; a rising fallback rate is an incident, not a detail.

## LLM and RAG systems in the same frame

LLM features follow the same three pipelines; there is no separate architecture to invent.

- **Feature pipelines** chunk, clean and embed documents into a vector index; they also prepare instruction or evaluation datasets. Embedding model and chunking parameters are versioned; changing either requires re-embedding (see `ai-rag-patterns` for triggers).
- **Training pipelines** fine-tune or align a model when that is justified; the tokenizer is a model-dependent transformation and must match exactly at inference.
- **Inference pipelines** hold the prompt templates (versioned), retrieval, tool calls and the model call. For questions about a specific customer, order or account, retrieve structured rows by entity id from feature tables, filtered by the caller's tenant and permissions, rather than hoping a vector search surfaces them.
- Log retrieved context ids, prompt version, model version and output per request, as for any model.

## Testing the system

| Level | What to test |
| --- | --- |
| Feature functions | unit tests on small frames: each feature's definition is a contract other models depend on |
| Feature pipeline | run end to end on committed sample data into a dev/test table; assert validation rejects a known-bad row and data read back equals data written |
| Training pipeline | performance vs baseline and per-segment floors as automated gates; fails the pipeline, not just a report |
| Deployment | contract test of the deployment API; load test at expected peak with the real feature store in the path; fallback paths exercised |
| Batch inference | compare new model against current on the same batch (shadow) before switching |
| LLM features | evaluation set with graded expected answers (see `ai-evaluation`) |

## Anti-patterns

- Treating MLOps as DevOps: testing code but not the data or the model.
- Versioning the model but not the features and training data it depends on.
- Assuming the model signature is the API, so clients build feature vectors.
- Quoting `predict()` time as prediction latency.
- Building a separate "LLMOps" stack instead of applying the same pipelines, registry and monitoring.
- Adopting an ML-specific orchestrator by default; a general scheduler (cron, Airflow, a CI scheduler, the platform's jobs) is usually enough, and lineage belongs in the data layer (feature tables, registry), not the orchestrator.
- Re-querying training data for each experiment and comparing models trained on different rows.

## Worked example

A Ugandan SACCO wants a loan-default score shown to loan officers when an application is opened, using mobile-money repayment history. Decisions: online inference (officer waits), but features change daily, so a nightly feature pipeline computes per-member aggregates (on-time repayment rate over 90 days, balance volatility, months of membership) into a Postgres table with `member_id`, `event_time`, `ingested_at`, copied to Redis for serving. The only on-demand feature is requested amount relative to the member's average savings, computed by a shared function also used in backfill. Training reads a point-in-time dataset as of each historical application date, versioned as `loan_default_ds_v4`; gates: AUC above the scorecard baseline and no branch more than 0.05 AUC below the overall figure. Serving API accepts `member_id` and `requested_amount_ugx`; missing Redis features fall back to the cached value up to 48 hours old, then to the rules scorecard, with a reason code. Acceptance: offline/online feature parity test on 500 sampled members shows identical vectors; p95 latency under 300 ms at 20 concurrent requests; fallback rate dashboarded.

## Quality gate

- [ ] Three pipelines identified with owner, schedule and storage contract.
- [ ] Every transformation classified; model-dependent ones ship with the model; on-demand ones have one implementation.
- [ ] Training data is point-in-time correct and versioned; late-arriving data handled via ingestion time.
- [ ] Model, feature view and dataset versions linked in the registry; deploy couples model and feature versions.
- [ ] Deployment API documented separately from the model signature.
- [ ] Latency budget per step and fallbacks tested; feature/prediction logging in place.
- [ ] Offline/online parity test exists.

## Senior vs generic output

Generic: "train a model, pickle it, wrap it in FastAPI." Senior: names the three pipelines and their contracts, classifies every transformation, proves training data is point-in-time correct and reproducible, couples model and feature versions, budgets latency end to end, and specifies what happens when a feature is missing.

## Evidence/currentness

Access date 2026-09-24. Concepts are durable; no tool is mandated. Tool activity checked via GitHub releases: Feast v0.66.0 (2026-08), Hopsworks client 5.1.0 (2026-09), MLflow v3.16.1 (2026-09), Great Expectations 1.23.1 (2026-09), pandera v0.33.1 (2026-09). `pd.merge_asof` parameters per pandas 3.0 API reference. Latency and AUC figures in the example are illustrative targets, not benchmarks. Fit of any specific feature store to a client's infrastructure: `NOT_ASSESSED` until evaluated.

Sources: Dowling (2026) *Building Machine Learning Systems with a Feature Store*; Nelson (2024) *Software Engineering for Data Scientists*; pandas documentation.
