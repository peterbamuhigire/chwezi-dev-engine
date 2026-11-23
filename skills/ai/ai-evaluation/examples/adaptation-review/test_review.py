import json
import unittest
from pathlib import Path

from review import review


HERE = Path(__file__).resolve().parent


class AdaptationReviewTests(unittest.TestCase):
    def load(self, name):
        return json.loads((HERE / name).read_text(encoding="utf-8"))

    def test_wrong_base_is_rejected_and_inference_stays_unassessed(self):
        report = review(self.load("fixture.json"))
        self.assertFalse(report["adapter_accepted"])
        self.assertIn("adapter_base_revision_mismatch", report["compatibility_failures"])
        self.assertEqual(report["inference_claim"], "NOT_ASSESSED")
        self.assertEqual(report["quality_claim"], "NOT_ASSESSED")
        self.assertEqual(report["decision"]["runtime_model_status"], "MISSING")
        self.assertEqual(report["decision"]["license_status"], "UNRESOLVED")
        self.assertEqual(report["decision"]["training_status"], "NOT_RUN")
        self.assertEqual(report["decision"]["fixed_comparator_id"], "prompt-baseline-P0")
        self.assertEqual(report["decision"]["fixed_comparator"]["template_revision"], "template-p0")
        self.assertEqual(report["decision"]["held_out_set_revision"], "K5-review-v1")
        self.assertEqual(report["decision"]["comparison_status"], "NOT_RUN")

    def test_matching_base_and_tokenizer_pass_compatibility_gate(self):
        report = review(self.load("compatible-fixture.json"))
        self.assertTrue(report["adapter_accepted"])
        self.assertEqual(report["compatibility_failures"], [])

    def test_duplicate_low_fidelity_unknown_rights_and_changed_sampler_are_separate(self):
        report = review(self.load("fixture.json"))
        self.assertEqual(report["duplicate_output_groups"], [["img-a", "img-b"]])
        self.assertEqual(report["low_fidelity_for_reviewer"], ["img-c"])
        self.assertEqual(report["exclude_from_training_or_publication"], ["img-d"])
        self.assertEqual(report["sampler_revision_changed"], ["img-d"])

    def test_tokenizer_mismatch_is_rejected_even_when_base_matches(self):
        fixture = self.load("compatible-fixture.json")
        fixture["candidate"]["adapter_tokenizer_revision"] = "tokenizer-old"
        report = review(fixture)
        self.assertFalse(report["adapter_accepted"])
        self.assertEqual(report["compatibility_failures"], ["adapter_tokenizer_revision_mismatch"])


if __name__ == "__main__":
    unittest.main()
