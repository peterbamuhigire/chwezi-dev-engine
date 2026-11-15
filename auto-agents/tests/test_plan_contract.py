import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import plan_contract


class PlanContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Plan Contract Test"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "plan-contract@example.invalid"], check=True)
        (self.root / "src").mkdir()
        (self.root / "src" / "output.py").write_text("# output\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "src/output.py"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture"], check=True)

    def tearDown(self):
        self.temp.cleanup()

    def contract(self):
        return {
            "schema_version": 1,
            "tasks": [
                {
                    "id": "TASK-01",
                    "title": "Implement bounded output",
                    "depends_on": [],
                    "scope": ["src/output.py"],
                    "acceptance": [
                        {
                            "id": "AC-001",
                            "description": "Output matches the documented result",
                            "commands": [["python", "-m", "unittest"]],
                            "cwd": ".",
                        }
                    ],
                    "state": "pending",
                    "evidence": [],
                }
            ],
        }

    def add_evidence(self, contract, result="PASS"):
        evidence = self.root / "src" / "evidence.txt"
        evidence.write_text("criterion AC-001 passed\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "src/evidence.txt"], check=True)
        head = subprocess.check_output(["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True).strip()
        contract["tasks"][0]["state"] = "complete"
        contract["tasks"][0]["evidence"] = [
            {
                "criterion_id": "AC-001",
                "path": "src/evidence.txt",
                "tested_revision": head,
                "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
                "command": ["python", "-m", "unittest"],
                "result": result,
            }
        ]

    def test_incomplete_valid_contract_is_not_completion_ready(self):
        result = plan_contract.completion_readiness(self.contract(), self.root)
        self.assertTrue(result["valid"])
        self.assertFalse(result["completion_ready"])
        self.assertFalse(result["independent_commit_verified"])

    def test_complete_contract_with_digest_bound_tracked_evidence(self):
        contract = self.contract()
        self.add_evidence(contract)
        result = plan_contract.completion_readiness(contract, self.root)
        self.assertTrue(result["valid"], result["errors"])
        self.assertTrue(result["completion_ready"])
        self.assertTrue(result["ready_for_independent_verification"])
        self.assertFalse(result["semantic_acceptance_verified"])
        self.assertEqual(result["task_states"]["complete"], 1)

    def test_complete_without_evidence_is_rejected(self):
        contract = self.contract()
        contract["tasks"][0]["state"] = "complete"
        result = plan_contract.validate_contract(contract, self.root)
        self.assertFalse(result["valid"])
        self.assertIn("complete without evidence", result["errors"][0])

    def test_unknown_dependency_is_rejected(self):
        contract = self.contract()
        contract["tasks"][0]["depends_on"] = ["TASK-99"]
        self.assertIn("unknown dependencies", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_dependency_cycle_is_rejected(self):
        contract = self.contract()
        first = contract["tasks"][0]
        second = {**first, "id": "TASK-02", "depends_on": ["TASK-01"], "acceptance": [{**first["acceptance"][0], "id": "AC-002"}]}
        first["depends_on"] = ["TASK-02"]
        contract["tasks"].append(second)
        self.assertIn("dependency cycle", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_duplicate_task_or_criterion_id_is_rejected(self):
        contract = self.contract()
        contract["tasks"].append(dict(contract["tasks"][0]))
        self.assertIn("duplicate task ID", plan_contract.validate_contract(contract, self.root)["errors"][0])

        contract = self.contract()
        second = {**contract["tasks"][0], "id": "TASK-02", "acceptance": [dict(contract["tasks"][0]["acceptance"][0])]}
        contract["tasks"].append(second)
        self.assertIn("duplicate criterion ID", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_empty_acceptance_is_rejected(self):
        contract = self.contract()
        contract["tasks"][0]["acceptance"] = []
        self.assertIn("at least one criterion", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_unsafe_scope_and_evidence_paths_are_rejected(self):
        contract = self.contract()
        contract["tasks"][0]["scope"] = ["../outside.py"]
        self.assertIn("stay within", plan_contract.validate_contract(contract, self.root)["errors"][0])
        contract = self.contract()
        self.add_evidence(contract)
        contract["tasks"][0]["evidence"][0]["path"] = "../outside.txt"
        self.assertIn("stay within", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_untracked_evidence_and_digest_mismatch_are_rejected(self):
        contract = self.contract()
        self.add_evidence(contract)
        evidence = self.root / "src" / "evidence.txt"
        subprocess.run(["git", "-C", str(self.root), "reset", "-q", "HEAD", "--", "src/evidence.txt"], check=True)
        self.assertIn("tracked worktree file", plan_contract.validate_contract(contract, self.root)["errors"][0])
        subprocess.run(["git", "-C", str(self.root), "add", "src/evidence.txt"], check=True)
        contract["tasks"][0]["evidence"][0]["sha256"] = "0" * 64
        self.assertIn("does not match", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_complete_with_not_assessed_evidence_is_rejected(self):
        contract = self.contract()
        self.add_evidence(contract, result="NOT_ASSESSED")
        self.assertIn("not PASS", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_complete_task_must_wait_for_dependency(self):
        contract = self.contract()
        first = contract["tasks"][0]
        second = {**first, "id": "TASK-02", "depends_on": ["TASK-01"], "state": "running", "acceptance": [{**first["acceptance"][0], "id": "AC-002"}]}
        contract["tasks"].append(second)
        self.assertIn("before dependencies complete", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_evidence_command_must_match_declared_command(self):
        contract = self.contract()
        self.add_evidence(contract)
        contract["tasks"][0]["evidence"][0]["command"] = ["python", "-m", "unittest", "extra"]
        self.assertIn("must match a command declared", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_unknown_keys_are_rejected(self):
        contract = self.contract()
        contract["extra"] = True
        self.assertIn("unknown keys", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_criterion_must_declare_exactly_one_command(self):
        contract = self.contract()
        contract["tasks"][0]["acceptance"][0]["commands"].append(["python", "-m", "compileall"])
        self.assertIn("exactly one command", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_tested_revision_must_be_available_ancestor_of_head(self):
        contract = self.contract()
        self.add_evidence(contract)
        tree = subprocess.check_output(["git", "-C", str(self.root), "write-tree"], text=True).strip()
        detached_commit = subprocess.check_output(
            ["git", "-C", str(self.root), "commit-tree", tree, "-m", "unrelated commit"],
            text=True,
        ).strip()
        contract["tasks"][0]["evidence"][0]["tested_revision"] = detached_commit
        self.assertIn("not an ancestor", plan_contract.validate_contract(contract, self.root)["errors"][0])

    def test_duplicate_json_keys_are_rejected(self):
        contract_path = self.root / "contract.json"
        contract_path.write_text('{"schema_version": 1, "schema_version": 1, "tasks": []}', encoding="utf-8")
        with self.assertRaisesRegex(plan_contract.ContractError, "duplicate JSON key: schema_version"):
            plan_contract.load_contract(contract_path)


if __name__ == "__main__":
    unittest.main()
