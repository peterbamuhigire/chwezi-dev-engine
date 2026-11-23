# E01 evidence receipt

- **Acceptance ID:** AC-E01
- **Input:** K1 in `docs/plans/ai-engine-kaizen/casebook.md`, plus original synthetic train/test CSV fixtures in the public ML skill.
- **Source revision:** `d5075d93cdb9fad66782d5957c98ab84dca8434d` (implementation and checks were run in the worktree based on this revision).
- **Receipt digest:** SHA-256 is recorded in `build.contract.json` after finalising this receipt.
- **Scope:** the public ML decision reference and parent routes in `python-ml-predictive` and `ai-opportunity-canvas`, with an offline example and regression fixture.

## Reproduction

From the repository root, run these commands in order:

```sh
python skills/languages/python-ml-predictive/examples/ticket-triage/train.py --model skills/languages/python-ml-predictive/examples/ticket-triage/ticket-triage-model.json
python skills/languages/python-ml-predictive/examples/ticket-triage/score.py --model skills/languages/python-ml-predictive/examples/ticket-triage/ticket-triage-model.json
python -m unittest discover -s skills/languages/python-ml-predictive/examples/ticket-triage -p "test_*.py" -v
```

Training read only `train.csv` (18 rows) and wrote a reloadable JSON model with 203 observed features. The generated artifact SHA-256 was `FC5427F8575FF7BCFF134727E5BAADB0E0987B8588BF50AF0B57B56D14F2A7DB`. Scoring ran separately, loaded that artifact, and read the frozen six-row `test.csv` fixture. The held-out confusion matrix (actual rows, predicted columns) was:

| Actual | Routine | Urgent |
|---|---:|---:|
| Routine | 3 | 0 |
| Urgent | 1 | 2 |

Class-wise precision, recall, and F1:

| Class | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Routine | 3 | 0.750 | 1.000 | 0.857 |
| Urgent | 3 | 1.000 | 0.667 | 0.800 |

This tiny synthetic fixture demonstrates reproducibility only. The missed urgent case is retained in the result; these figures do not estimate production quality or prove an improvement over a rule or LLM.

## K1 policy table and metric identity control

K1 is hand-calculated separately from the learned fixture. The casebook provides frozen predictions and labels for a support-ticket text-label task, but no raw ticket messages. On the same frozen eight-ticket predictions, the current rule has TP/FP/FN/TN = 1/1/2/4 and cost `2 misses × 5 + 1 unnecessary review × 1 = 11`. The candidate has 3/2/0/3 and cost `0 misses × 5 + 2 unnecessary reviews × 1 = 2`, but it sends five alerts and exceeds the two-alert review capacity. Under CAP-ALL the candidate has the lower fixture cost and fits the shift. Release still requires further evidence under the accepted SRS handoff. No model result is substituted into these K1 calculations.

The regression fixture uses observed `[0, 2, 4]` and predicted `[0, 2, 3]`: MSE is `1/3`; R-squared is `7/8`. The negative control passed a record with `metric_id=mse`, `display_label=R-squared`, and direction `maximise` to `validate_metric_record`. The rejection assertion raised `ValueError: metric identifier and display label do not agree` (command exit 1), so the scorer cannot silently display R-squared as MSE. On the repaired fixture, the targeted suite passed all four tests.

## Currentness and source record

| Source | Scope and locator | Publication/version | Access and verification | Freshness/review | Support and uncertainty |
|---|---|---|---|---|---|
| [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), R03 | Official guidance: fit learned transforms using training data; apply the learned transform to held-out data. Sections 12.1-12.2. | Stable documentation identifies version 1.9.1; accessed 2026-11-23. | 2026-11-23 | Context-bound to the documented version; review by 2027-02-23 or earlier if the version changes. | Verified for the stated preprocessing guidance. This example uses standard-library code and makes no scikit-learn API claim. |
| [scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html), R04 | Official guidance: keep groups separate for unseen-group evaluation and use future observations for time-series evaluation. Sections 3.1.2.4 and 3.1.2.6. | Stable documentation identifies version 1.9.1; accessed 2026-11-23. | 2026-11-23 | Context-bound to the documented version; review by 2027-02-23 or earlier if the version changes. | Verified for grouped/time split selection. The six-row demonstration is not a grouped or time-series performance study. |

The existing source register scope and dates were rechecked at the official pages above. The implementation uses no newly introduced third-party package, current product API, model version, benchmark, or vendor performance claim.

## Model-currentness check required for Kaizen

Official [OpenAI model release notes](https://help.openai.com/en/articles/9624314-model-release-notes) and [ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) were checked on 2026-11-23. The latest model release entry located was GPT-6.2 Astra (`gpt-6.2-astra`) and GPT-6.2 Sol (`gpt-6.2-sol`), dated 2026-11-17; the Work/Codex release entry is also dated 2026-11-17. Actual availability in this running account/runtime catalogue was not exposed to this task and remains **NOT_ASSESSED**. This E01 slice makes no model-policy change, so no task-fit, cost, latency, or quality comparison is proposed. No release claim is used in the public ML guidance.

## Negative control and refinement record

- **Negative control:** mislabeled MSE record (`mse` identifier displayed as `R-squared`, with maximise direction). The identity check rejected it as above.
- **Repair:** corrected the fixture oracle to the actual six frozen held-out rows, then reran separate training, reload-and-score, and the targeted suite. The corrected suite passed 4/4 tests.
- **Initial exploratory failures:** first run exposed a non-adjacent negation assertion and an incorrect expected urgent count. The fixture text and expected matrix were corrected; neither failure was hidden or treated as a passing check.
- **Anti-slop audit:** qualitative manual verdict A for the changed prose and code. The changed artefacts contain K1-specific counts, reproducible synthetic rows, the observed false negative, qualified cost assumptions, and no unscoped speed/price claims in the decision reference. No blocking fabrication, placeholder, or generic section was found. A numeric genericness score was not computed because no structural detector was run. No independent human reviewer or production workload was assessed.

## Limitations and remaining evidence

- No production dataset, reviewer workload, real business penalty, LLM comparison, or latency/cost measurement was supplied or claimed.
- The example is a deliberately small synthetic demonstration. It does not address repeated threads, time ordering, a robust split design, or subpopulation claims; those require task-specific data and a separate evaluation.
- Model runtime/account catalogue availability remains NOT_ASSESSED as recorded above.
- E02-E06 remain pending; E06 depends on the evidence from the preceding tasks.
