import json

from tools.adapter_lifecycle import apply, plan, revert


def test_plan_is_read_only_and_apply_revert_owns_one_key(tmp_path):
    config = tmp_path / "host.json"
    config.write_text(json.dumps({"unrelated": {"keep": True}}), encoding="utf-8")
    proposal = plan(config, "codex")
    assert proposal["status"] == "PASS"
    assert json.loads(config.read_text(encoding="utf-8")) == {"unrelated": {"keep": True}}
    result = apply(config, "codex", tmp_path / "backups")
    assert result["status"] == "PASS"
    current = json.loads(config.read_text(encoding="utf-8"))
    assert current["unrelated"] == {"keep": True}
    backup = tmp_path / "backups" / result["backup"].split("\\")[-1]
    assert revert(config, backup)["status"] == "PASS"
    assert json.loads(config.read_text(encoding="utf-8")) == {"unrelated": {"keep": True}}


def test_apply_refuses_foreign_owned_entry(tmp_path):
    config = tmp_path / "host.json"
    config.write_text(json.dumps({"chwezi_solution_selection": {"owner": "other"}}), encoding="utf-8")
    assert apply(config, "codex", tmp_path / "backups")["status"] == "FAIL"


def test_malformed_config_is_not_assessed(tmp_path):
    config = tmp_path / "host.json"
    config.write_text("{broken", encoding="utf-8")
    assert plan(config, "codex")["status"] == "NOT_ASSESSED"
