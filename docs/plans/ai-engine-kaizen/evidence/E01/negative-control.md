# E01 negative-control record

**Acceptance:** AC-E01 · **Control:** report R-squared as MSE.

From `skills/languages/python-ml-predictive/examples/ticket-triage/`, run:

```sh
python -c "from regression_metrics import validate_metric_record; validate_metric_record({'metric_id': 'mse', 'display_label': 'R-squared', 'optimisation_direction': 'maximise'})"
```

Observed exit code: `1`.

```text
ValueError: metric identifier and display label do not agree
```

The same malformed record is covered by `test_negative_control_rejects_a_mislabeled_scorer`, which asserts that the validator rejects it. After the fixture oracle was corrected, the repaired targeted suite completed with `Ran 4 tests` and `OK`. Correct metric results remain MSE `1/3` and R-squared `7/8` on observed `[0, 2, 4]` and predicted `[0, 2, 3]`.
