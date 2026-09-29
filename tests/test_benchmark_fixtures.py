import copy
import json
from pathlib import Path

from tools.validate_benchmark_fixtures import validate

SPEC = Path("benchmarks/solution-selection/fixtures.json")


def test_solution_fixture_specification_is_complete():
    result = validate(SPEC)
    assert result["status"] == "PASS"
    assert result["fixture_count"] == 16


def _write(tmp_path, payload):
    path = tmp_path / "fixtures.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _payload():
    payload = json.loads(SPEC.read_text(encoding="utf-8"))
    for item in payload["fixtures"]:
        item.update({"materialisation_status": "NOT_ASSESSED", "initial_commit": None, "hidden_manifest_hash": None})
    return payload


def test_fixture_without_short_prompt_fails(tmp_path):
    payload = _payload()
    del payload["fixtures"][0]["short_prompt"]
    result = validate(_write(tmp_path, payload))
    assert result["status"] == "FAIL"
    assert any("short_prompt" in error for error in result["errors"])


def test_pressure_scenario_without_short_prompt_fails(tmp_path):
    payload = _payload()
    scenario = copy.deepcopy(payload["pressure_scenarios"][0])
    del scenario["short_prompt"]
    payload["pressure_scenarios"] = [scenario]
    result = validate(_write(tmp_path, payload))
    assert result["status"] == "FAIL"
    assert any("short_prompt" in error for error in result["errors"])


def test_materialised_fixture_needs_commit_hash_and_folder(tmp_path):
    payload = _payload()
    payload["fixtures"][0]["materialisation_status"] = "MATERIALISED"
    result = validate(_write(tmp_path, payload))
    assert result["status"] == "FAIL"
    joined = " ".join(result["errors"])
    assert "initial_commit" in joined and "hidden_manifest_hash" in joined and "folder" in joined
