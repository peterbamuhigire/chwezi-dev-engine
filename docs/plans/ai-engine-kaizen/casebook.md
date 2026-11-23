# Acceptance cases for the AI engine Kaizen

These are original, synthetic examples for implementation. The expected outcomes below are the oracle for a future test. The examples use no private project data, downloaded model, hosted API or production service. An engine may express the same case as a specification, executable fixture or handoff. Keep the case ID and expected result consistent.

## K1 · Dispatch support tickets under a fixed review capacity

A shift lead can inspect two alerts in a shift. Missing an urgent case is costly. A second operating profile can inspect every alert. A prior triage rule and a candidate text classifier produced the following frozen predictions. They are fixture inputs, not measured model predictions. Flagged means dispatch to review.

| Ticket | Urgent truth | Existing rule | Candidate |
|---|---:|---:|---:|
| A | 1 | 1 | 1 |
| B | 0 | 1 | 1 |
| C | 1 | 0 | 1 |
| D | 0 | 0 | 1 |
| E | 0 | 0 | 0 |
| F | 1 | 0 | 1 |
| G | 0 | 0 | 0 |
| H | 0 | 0 | 0 |

**Expected result.** In TP, FP, FN, TN order the current rule yields (1,1,2,4) and the candidate yields (3,2,0,3). Precision and recall are 1/2 and 1/3 for the rule, 3/5 and 1 for the candidate. At a predeclared penalty of five per miss and one per unnecessary review, costs are 11 and 2. The candidate emits five alerts and breaches the two-review profile. Reject deployment under that profile pending an evaluated ranking, threshold or workflow change. The more permissive profile can accept a different decision using the same counts. The penalties belong only to this example.

**Challenge the experiment.** Construct distinct development rows with two messages from the same ticket thread, a near duplicate, a future closure code, a training-only word and a test-only word. Group threads before splitting, sort by information available at prediction time, and fit learned vocabulary only on training rows. Show exactly which rows were quarantined. Preserve original ticket IDs and negation when normalizing text. If all predictions are negative, precision has a zero denominator. Report the convention and count. If labels are pending, report label coverage independently. Include a subpopulation whose small sample prevents a defensible performance claim. Freeze the test set before choosing a threshold.

**Metric identity control.** On a separate regression fixture use observed values [0, 2, 4] and predictions [0, 2, 3]. The mean squared error is 1/3 and the coefficient of determination is 7/8. Require the metric identifier, optimization direction, unit and displayed label to agree. A result labeled MSE that actually reports the estimator’s default R-squared fails. R19/R20 document the relevant API behavior.

## K2 · Find the right maintenance instruction and prove the answer

Use a synthetic index of work instructions. Entry P1, revision 1, said that *Atlas* retained jobs for seven days and has been withdrawn. P2, revision 2, is active and permits the statement “Atlas retains jobs for three days.” P3 belongs to a different tenant. P4 describes an unrelated product. The synthetic query asks how long Atlas retains jobs. Store corpus revision, eligibility checks, ranked IDs, selected span, response claim and reviewer grade.

| Input variation | Retrieval oracle | Answer oracle |
|---|---|---|
| Active authorized corpus | P2 is eligible and relevant | Three days, source P2 at revision 2 |
| P2 ranks first and response says five days | Retrieval hit | Unsupported answer fails |
| P1 was withdrawn and the index rebuilt | P1 absent from eligible results and caches | Neither old claim nor stale citation appears |
| Only P3 would answer | No eligible supporting document | Abstain or escalate. No title, snippet or ID from P3 appears |
| Query contains a meaningful identifier or negation | Preserve differentiating token and source identity | Do not claim equivalence to a different identifier or reverse polarity |
| Authorized documents disagree with no effective revision | Return conflicting evidence if allowed | State uncertainty and route to a resolving owner |

Compute retrieval rank and answer support separately. If only the second-ranked document is relevant, reciprocal rank is 1/2. Record no-answer cases separately from answerable-query rank aggregates. A lexical or retrieval-only solution remains acceptable when it meets the task.

## K3 · Fix duplicate delivery in an existing software feature

A public ticket-import function accepts an event ID, ticket ID and requested status. A retry of a successful event currently adds a second status-history entry. Existing tickets may predate event IDs. Give the implementing assistant a minimal repository map, the intended public behavior, a migration constraint and an original test owned by the reviewer. Keep tests local to a fixture store.

1. Deliver E7 for ticket T1 with status *review*, then retry E7 with identical data. Expect one history entry and a consistent success response on retry.
2. Deliver E8 for T1 with status *closed*. Expect a second, distinct entry. A patch that suppresses all events for a ticket fails this test.
3. Reuse E7 with a different payload. Expect the specified conflict and no new history. Exercise a failure between recording the idempotency key and committing the history record. Retry must produce one complete event. Use a transaction or equivalent recoverable mechanism appropriate to the fixture.
4. Open a legacy record without an event ID. Preserve its old history and accept a new, explicitly identified event. Concurrent delivery of the same event must leave one committed effect.
5. Record the public entry point, before revision with failing oracle, after revision with passing oracle, review findings and remaining risks. A helper-only green test, a weakened assertion or a self-reported success cannot discharge the acceptance criterion.

## K4 · Roll back an AI pipeline as a compatible unit

Represent a release by code, input schema, transform/vocabulary, model, tokenizer, adapter, prompt and index revisions where relevant. A known good bundle G1 serves a fixture request. Candidate G2 expects a different vocabulary order. Present a G2 adapter paired to G1 weights, an interrupted index promotion, and a replay with the same promotion ID. Assert rejection before serving incompatible parts, recovery to one complete bundle, and identical eligible results after replay. Record which component caused the mismatch.

Use a second trace where the distribution of input length shifts but labels arrive next week. A data shift alert can open an investigation. Quality loss remains unknown until labels arrive. Use a third trace where online and training transforms produce different features for the same frozen record. This is direct evidence of training-serving skew. Show pilot owner, user correction path, decision time and restoration receipt. Compare query-to-first-output time separately from complete-response time. Include timeouts and retries in denominators. Unknown charge is a missing observation.

## K5 · Review generated media and model changes

Use an original, locally constructed collection of simple images with stable IDs and rights metadata. Provide a repeated output, one low-fidelity result, one item with unknown rights and one candidate with a different scheduler or tokenizer revision. Record conditioning, model family, revision, seed, sampling settings and reviewer rubric.

A byte-identical duplicate flags a diversity problem. A near-duplicate review may require a perceptual check. Missing permission excludes the item from training or publication until resolved. Same seed across changed software is insufficient for a reproducibility claim. Record fidelity and diversity independently. A fake generator tests metadata, rejection and routing. A real inference trial and an independent review set are needed to claim observed generation quality or performance. Compare adaptation or training to a simpler baseline, including use of an existing permitted asset.

## K6 · Measure AI-assisted software delivery

Choose a bug fix and a small feature in a non-sensitive fixture repository. Match tasks by difficulty and prior familiarity. Compare existing practice with the candidate skill on fresh task variants. Keep runner/model/settings, task scope, verification and review rubric fixed. Counterbalance order across matched variants. Give the person judging the diff the same independently held acceptance tests. Separate route discovery from implementation quality. Document opt-outs, failures and changed conditions.

| Observation | Definition and use |
|---|---|
| First-pass accepted | Independent behavior and compatibility gates pass without repair. Report count over attempted tasks. |
| Total effort | Elapsed and active human minutes separately, including setup, waiting, review and repair. Keep interrupted assignments in the record. |
| Rework | Count correction cycles, reviewer findings still open, reverted changes and time spent diagnosing them. |
| Quality | Record correctness through the public path, legacy behavior, recovery, scope adherence and residual failures. |
| Cost and latency | Use recorded consumption where available, with units, completion status and billing basis. Report unknowns. |
| Adoption | Record route availability, whether it was used and the resulting outcome. Count false routes and abstentions. |

Pair outcomes within comparable tasks. One successful run establishes a demonstration. A claim of relative productivity requires adequate representative comparisons, uncertainty and no material loss of quality. If sample size or selection prevents inference, record that fact and keep both useful qualitative findings and the planned repeat.
