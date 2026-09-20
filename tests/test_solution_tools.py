import json
import subprocess

from tools.solution_debt import scan
from tools.solution_evidence import validate
from tools.solution_mode import get_mode, reset_mode, set_mode
from tools.solution_review import repo_audit


def test_mode_is_repository_and_session_scoped(tmp_path):
    assert get_mode(tmp_path, "one")["mode"] == "advisory"
    assert set_mode(tmp_path, "enforced-review", "one")["mode"] == "enforced-review"
    assert get_mode(tmp_path, "two")["mode"] == "advisory"
    assert reset_mode(tmp_path, "one")["mode"] == "advisory"


def test_corrupt_mode_state_is_not_assessed(tmp_path):
    state = tmp_path / ".kaizen"
    state.mkdir()
    (state / "solution-mode.json").write_text("{broken", encoding="utf-8")
    assert get_mode(tmp_path, "one")["status"] == "NOT_ASSESSED"


def test_debt_scan_detects_missing_fields_and_ignores_vendor(tmp_path):
    (tmp_path / "src.py").write_text("# SOLUTION_DEBT: reason=temporary owner=team\n", encoding="utf-8")
    vendor = tmp_path / "vendor"
    vendor.mkdir()
    (vendor / "third.py").write_text("# SOLUTION_DEBT: reason=x\n", encoding="utf-8")
    records = scan(tmp_path)
    assert len(records) == 1
    assert "trigger" in records[0]["missing"]


def test_review_is_read_only_and_reports_duplicates(tmp_path):
    source = "alpha = 1\nbeta = 2\ngamma = 3\n\nalpha = 1\nbeta = 2\ngamma = 3\n"
    (tmp_path / "src.py").write_text(source, encoding="utf-8")
    before = (tmp_path / "src.py").read_bytes()
    findings = repo_audit(tmp_path)
    assert any(item.code == "duplicated-block" for item in findings)
    assert (tmp_path / "src.py").read_bytes() == before


def test_evidence_rejects_mixed_models_and_zero_cost(tmp_path):
    (tmp_path / "raw-a.json").write_text("{}", encoding="utf-8")
    (tmp_path / "raw-b.json").write_text("{}", encoding="utf-8")
    payload = {
        "schema_version": 1,
        "baseline_id": "B1",
        "runs": [
            {"run_id": "a", "arm": "A", "fixture": "F01", "status": "PASS", "model_id": "m1", "raw_path": "raw-a.json", "tokens": 10, "cost_usd": 0},
            {"run_id": "b", "arm": "B", "fixture": "F01", "status": "PASS", "model_id": "m2", "raw_path": "raw-b.json", "tokens": 10, "cost_usd": 1},
        ],
    }
    result = validate(payload, tmp_path)
    assert result["status"] == "FAIL"
    assert any("mixed model" in error for error in result["errors"])
    assert any("zero cost" in error for error in result["errors"])
