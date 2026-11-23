"""Small regression metric fixture used to catch mislabeled score output."""


def mse(observed, predicted):
    if len(observed) != len(predicted) or not observed:
        raise ValueError("observed and predicted must have the same non-zero length")
    return sum((actual - estimate) ** 2 for actual, estimate in zip(observed, predicted)) / len(observed)


def r_squared(observed, predicted):
    if len(observed) != len(predicted) or not observed:
        raise ValueError("observed and predicted must have the same non-zero length")
    mean = sum(observed) / len(observed)
    total = sum((actual - mean) ** 2 for actual in observed)
    residual = sum((actual - estimate) ** 2 for actual, estimate in zip(observed, predicted))
    if total == 0:
        raise ValueError("R-squared is undefined when observed values have zero variance")
    return 1 - residual / total


def validate_metric_record(record):
    expected_labels = {"mse": "Mean squared error", "r_squared": "R-squared"}
    metric_id = record.get("metric_id")
    if metric_id not in expected_labels or record.get("display_label") != expected_labels[metric_id]:
        raise ValueError("metric identifier and display label do not agree")
    if record.get("optimisation_direction") != ("minimise" if metric_id == "mse" else "maximise"):
        raise ValueError("metric identifier and optimisation direction do not agree")
    return record
