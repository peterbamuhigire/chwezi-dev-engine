import unittest

from regression_metrics import mse, r_squared, validate_metric_record
from score import evaluate, predict
from train import read_rows, tokens, train


class TicketTriageExampleTests(unittest.TestCase):
    def test_training_vocabulary_and_held_out_class_results(self):
        from pathlib import Path

        folder = Path(__file__).parent
        artifact = train(read_rows(folder / "train.csv"))
        rows = read_rows(folder / "test.csv")
        predictions = [predict(artifact, row["text"]) for row in rows]
        confusion, report = evaluate(rows, predictions, artifact["labels"])
        self.assertEqual(artifact["document_counts"], {"urgent": 9, "routine": 9})
        self.assertEqual(confusion["urgent"]["urgent"], 2)
        self.assertEqual(confusion["urgent"]["routine"], 1)
        self.assertEqual(confusion["routine"]["routine"], 3)
        self.assertEqual(report["urgent"]["support"], 3)
        self.assertEqual(report["routine"]["support"], 3)
        self.assertNotIn("qz", artifact["vocabulary"])
        self.assertNotIn("8841", artifact["vocabulary"])

    def test_negation_bigrams_are_not_removed(self):
        self.assertIn("not urgent", tokens("QZ-8841: not urgent; please do not close this case"))

    def test_metric_identity_and_correct_values(self):
        observed = [0, 2, 4]
        predicted = [0, 2, 3]
        self.assertAlmostEqual(mse(observed, predicted), 1 / 3)
        self.assertAlmostEqual(r_squared(observed, predicted), 7 / 8)
        validate_metric_record({
            "metric_id": "mse",
            "display_label": "Mean squared error",
            "optimisation_direction": "minimise",
        })

    def test_negative_control_rejects_a_mislabeled_scorer(self):
        with self.assertRaisesRegex(ValueError, "identifier and display label"):
            validate_metric_record({
                "metric_id": "mse",
                "display_label": "R-squared",
                "optimisation_direction": "maximise",
            })


if __name__ == "__main__":
    unittest.main()
