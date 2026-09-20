import hashlib
import json
from pathlib import Path

from tools.solution_decision import compute_scope_hash, validate_record


def _record(root: Path, *, evidence_status="verified"):
    source = root / "src.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    files = ["src.py"]
    return {
        "schema_version": 1,
        "decision_id": "SD-EXAMPLE-001",
        "scope": {"root": ".", "files": files, "sha256": compute_scope_hash(root, files)},
        "context": {
            "problem": "The current path repeats validation and makes recovery unclear.",
            "requirements": ["Preserve the public result"],
            "invariants": ["Permission checks remain enforced"],
        },
        "options": [
            {"kind": "no_change", "description": "Keep current path", "reason": "No change is acceptable only if evidence is sufficient."},
            {"kind": "existing_capability", "description": "Reuse the existing helper", "reason": "It already owns the boundary."},
        ],
        "selected_option": "existing_capability",
        "evidence": [{"kind": "test", "status": evidence_status, "path": "src.py", "note": "Synthetic contract check."}],
        "risk": {"tier": "medium", "security_boundary": True, "data_mutation": False, "money_or_ledger": False},
        "exception": None,
        "tests": {"required": ["normal result"], "negative_cases": ["permission denied"]},
    }


def test_valid_record_passes(tmp_path):
    assert validate_record(_record(tmp_path), tmp_path)["status"] == "PASS"


def test_scope_mutation_fails_closed(tmp_path):
    record = _record(tmp_path)
    (tmp_path / "src.py").write_text("VALUE = 2\n", encoding="utf-8")
    result = validate_record(record, tmp_path)
    assert result["status"] == "FAIL"
    assert any("scope.sha256" in error for error in result["errors"])


def test_traversal_and_missing_evidence_fail(tmp_path):
    record = _record(tmp_path)
    record["evidence"][0]["path"] = "../secret.txt"
    result = validate_record(record, tmp_path)
    assert result["status"] == "FAIL"
    assert any("escapes" in error for error in result["errors"])


def test_unassessed_evidence_is_explicit(tmp_path):
    result = validate_record(_record(tmp_path, evidence_status="not_assessed"), tmp_path)
    assert result["status"] == "NOT_ASSESSED"
    assert result["unassessed"] == ["evidence[0]"]


def test_high_risk_requires_verified_test_or_review(tmp_path):
    record = _record(tmp_path, evidence_status="not_assessed")
    record["risk"]["tier"] = "high"
    result = validate_record(record, tmp_path)
    assert result["status"] == "FAIL"
    assert any("high or critical" in error for error in result["errors"])
