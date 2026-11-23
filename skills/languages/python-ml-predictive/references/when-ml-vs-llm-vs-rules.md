# Choosing rules, classifiers, and LLMs

Choose from the decision the system must make, the available evidence, and the cost of a wrong action. Text is an input format; it does not by itself make an LLM the right classifier.

## Compare candidates on one task

For a text label, begin with a rule that a reviewer can inspect and a sparse linear or Naive Bayes classifier. Keep the same permitted records, prediction time, held-out examples, and review workflow for every candidate. Add an LLM only when it has a defined advantage to test, such as handling varied instructions or producing a justified extraction. Record the prompt and model revision if you test one.

For numeric features with a stable target, compare a simple statistical or ML baseline with the existing rule. Use retrieval when the answer depends on current authorised documents. Use generation when the required output is new text. These can be combined, but each component needs its own evaluation.

Do not fit vocabulary, thresholds, or other learned preprocessing on held-out rows. Split by the unit that can repeat (for example, customer or ticket thread), and respect time order when the prediction is about a future period. An IID random split is not evidence for a time-ordered or grouped workload. See the scikit-learn guidance on [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) and [cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html), accessed 2026-11-23; apply the split that matches the deployment question.

## K1: support-ticket triage under two review policies

K1 in [the casebook](../../../../docs/plans/ai-engine-kaizen/casebook.md) freezes eight support-ticket outcomes for a text-label task. It supplies expected predictions and labels, not raw ticket messages. The current rule yields TP/FP/FN/TN = 1/1/2/4; the candidate yields 3/2/0/3. With illustrative penalties of five per missed urgent case and one per unnecessary review, their hand-calculated costs are 11 and 2. These penalties are assumptions for this example, not measured business costs.

The candidate sends five of eight tickets to review. Under a two-alert shift limit it is infeasible, despite the lower illustrative error cost; keep the current policy until ranking, threshold, or reviewer workflow is evaluated. If a shift can inspect every alert (CAP-ALL), the candidate is eligible for further evaluation on the strength of its lower fixture cost. The accepted SRS handoff still requires further evidence for release. The text-label task and frozen predictions stay fixed while workload changes the decision.

This policy table is a hand calculation over frozen predictions. It is not the model result from the separate fixture below.

## Run the offline text-label example

The example uses original synthetic ticket messages and the Python standard library. Multinomial Naive Bayes is a conventional sparse bag-of-words classifier; it is a baseline, not a claim that this method wins for every text task. The train and test files are separate. Training writes a JSON model artifact, and scoring reloads it in a separate process.

From `skills/languages/python-ml-predictive/`:

```sh
python examples/ticket-triage/train.py --model ticket-triage-model.json
python examples/ticket-triage/score.py --model ticket-triage-model.json
python -m unittest discover -s examples/ticket-triage -p "test_*.py" -v
```

The scorer reports per-class precision, recall, and F1 alongside the confusion counts. Those observed held-out results are in the E01 receipt. The fixture is small and constructed for a walkthrough; it does not support a production-quality or comparative-performance claim.

One held-out row has ID `QZ-8841` and says, “Not urgent; please do not close this case because the report is delayed.” The tokenizer lowercases and splits on punctuation, preserving `not` and adjacent word pairs such as `not urgent`. Lowercasing can erase meaningful case distinctions, punctuation splitting breaks a compound identifier into pieces, and a rare unseen ID has no learned signal. Keep identifiers in a separate field for exact matching or routing; do not rely on a tiny text model to interpret them. A unigram-only tokenizer would not encode `not urgent` as one feature; whether that changes a prediction is NOT_ASSESSED. The fixture test checks that this bigram is retained.

## Measure the decision, not a generic cost tier

Record the population, time window, action threshold, error counts, review capacity, and the source of each penalty. Do not reuse absolute latency or price ranges across providers, models, deployments, or workloads. If speed or cost affects the choice, measure the actual candidate against the same request mix and include setup, review, retry, and operating costs. Unknown measurements remain unknown.

## Route by output and failure path

- A stable, exhaustive condition belongs in a rule with regression coverage.
- A repeated label task with examples can use a conventional classifier if held-out results and operating constraints support it.
- Variable language understanding, extraction, or generated prose may justify an LLM comparison; retrieval can supply current evidence, but does not prove that an answer is supported.
- When labels, permissions, representative evaluation data, or a safe correction path are missing, keep the decision open and record what must be measured.

For current scikit-learn APIs, check the [official documentation](https://scikit-learn.org/stable/) for the installed version. This example intentionally uses no third-party package and makes no scikit-learn compatibility claim.
