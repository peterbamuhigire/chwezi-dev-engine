import json
import unittest
from pathlib import Path

from evaluate import answer_grade, rank, run, span_for, tokens


HERE = Path(__file__).resolve().parent


class CuratedRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = json.loads((HERE / "corpus.json").read_text(encoding="utf-8"))
        cls.cases = json.loads((HERE / "eval.json").read_text(encoding="utf-8"))

    def test_retrieval_and_answer_support_are_separate(self):
        result = run(self.corpus, self.cases)[0]
        self.assertEqual(result["ranked_ids"][0], "P2")
        self.assertEqual(result["reciprocal_rank"], 1)
        self.assertEqual(result["response_claim"], "five days")
        self.assertFalse(result["answer_supported"])
        self.assertEqual(result["reviewer_grade"], "UNSUPPORTED")
        self.assertFalse(answer_grade("five days", self.corpus[1]))

    def test_no_eligible_document_abstains_without_leaking_ids(self):
        results = run(self.corpus, self.cases)
        for result in (results[2], results[3]):
            self.assertEqual(result["status"], "ABSTAIN")
            self.assertEqual(result["ranked_ids"], [])
        self.assertNotIn("P3", [rid for result in results for rid in result["ranked_ids"]])

    def test_withdrawn_revision_is_excluded_and_identifiers_preserved(self):
        results = run(self.corpus, self.cases)
        all_ids = [rid for result in results for rid in result["ranked_ids"]]
        self.assertNotIn("P1", all_ids)
        self.assertIn("Atlas", self.corpus[1]["text"])
        self.assertIn("P2", results[0]["ranked_ids"])
        self.assertIn("not", tokens(self.corpus[1]["text"]))
        self.assertEqual(tokens("P2"), ["P2"])
        self.assertEqual(tokens("p2"), ["p2"])
        self.assertEqual([row["id"] for row in rank(self.corpus, "P2", "tenant-a")], ["P2"])

    def test_negation_ablation_is_rejected_and_source_span_is_recoverable(self):
        case = self.cases[1]
        correct = rank(self.corpus, case["query"], case["tenant"])
        ablated = rank(self.corpus, case["query"], case["tenant"], drop_negation=True)
        self.assertEqual(correct[0]["id"], "P2")
        self.assertFalse(answer_grade("seven days", correct[0]))
        normalized_without_negation = " ".join(tokens(ablated[0]["text"], drop_negation=True))
        self.assertTrue(answer_grade("seven days", {"text": normalized_without_negation}))
        self.assertTrue(answer_grade("not seven days", correct[0]))
        span = span_for(correct[0], "not seven days")
        self.assertEqual(span["text"], "not seven days")
        self.assertEqual(correct[0]["text"][span["start"]:span["end"]], "not seven days")
        rerun = rank(self.corpus, case["query"], case["tenant"])
        self.assertEqual(rerun[0]["text"][span["start"]:span["end"]], "not seven days")


if __name__ == "__main__":
    unittest.main()
