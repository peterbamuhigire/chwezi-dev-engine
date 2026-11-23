import importlib.util
import json
from pathlib import Path
import unittest

EXAMPLE = Path(__file__).resolve().parents[1] / "skills/languages/python-ml-predictive/examples/release-diagnostics"
spec = importlib.util.spec_from_file_location("release_diagnostics", EXAMPLE / "diagnose.py")
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class ReleaseDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.f = json.loads((EXAMPLE / "fixture.json").read_bytes())

    def test_delayed_labels_and_frozen_feature_vectors(self):
        diag = demo.diagnose(self.f)["diagnoses"]
        self.assertEqual(diag["data"]["accuracy"], "NOT_ASSESSED")
        self.assertEqual(diag["data"]["class"], "input_distribution_shift")
        self.assertEqual(diag["serving"]["class"], "training_serving_skew")
        self.f["events"][1]["serving_features"] = self.f["events"][1]["training_features"]
        self.f["events"][0]["input_length_recent"] = self.f["events"][0]["input_length_reference"]
        control = demo.diagnose(self.f)["diagnoses"]
        self.assertEqual(control["serving"]["class"], "features_match")
        self.assertEqual(control["data"]["class"], "threshold_not_crossed")

    def test_rejection_and_atomic_restore(self):
        result = demo.diagnose(self.f)
        self.assertEqual(result["diagnoses"]["release"], {"mismatched_components":["transform.vocabulary","adapter.base"],"candidate_outcome":"incompatible"})
        self.assertEqual(result["interruption"], "interrupted_before_index_promotion")
        self.assertEqual(result["bundle_after_interruption"], self.f["bundles"]["G1"])
        self.assertEqual(result["active_bundle"], self.f["bundles"]["G1"])
        self.assertEqual((result["restoration"],result["retry"],result["effect_count"]),("published","replay",1))

    def test_reused_operation_id_cannot_select_another_bundle(self):
        good=self.f["bundles"]["G1"]
        s, _ = demo.promote({"active":good,"receipts":{}},"P",good)
        with self.assertRaisesRegex(ValueError,"reused"):
            demo.promote(s,"P",{**good,"id":"changed"})
