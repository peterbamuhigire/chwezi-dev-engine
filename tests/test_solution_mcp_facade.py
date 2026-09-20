import json

from tools.solution_mcp_facade import dispatch


def test_facade_is_read_only_and_bounded(tmp_path):
    (tmp_path / "record.json").write_text(json.dumps({"decision_id": "SD-001", "selected_option": "stdlib", "evidence": []}), encoding="utf-8")
    before = (tmp_path / "record.json").read_bytes()
    assert dispatch({"method": "list_tools"}, tmp_path)["ok"]
    result = dispatch({"method": "inspect_decision", "path": "record.json"}, tmp_path)
    assert result["decision_id"] == "SD-001"
    assert (tmp_path / "record.json").read_bytes() == before
    assert dispatch({"method": "inspect_decision", "path": "../secret"}, tmp_path)["ok"] is False


def test_facade_unknown_method_fails(tmp_path):
    assert dispatch({"method": "write", "path": "record.json"}, tmp_path)["ok"] is False
