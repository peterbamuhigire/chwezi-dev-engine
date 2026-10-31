"""Tests for scripts/engine_roots.py and the validators that use it."""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import engine_roots  # noqa: E402


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTROL = load("validate_engine_control_plane_roots_test", ROOT / "scripts" / "validate_engine_control_plane.py")
APPROVAL = load("validate_approval_adapters_roots_test", ROOT / "scripts" / "validate_approval_adapters.py")


def clear_overrides(monkeypatch):
    for engine_id in engine_roots.ENGINE_DIR_ALIASES:
        monkeypatch.delenv(engine_roots.env_name(engine_id), raising=False)
    monkeypatch.delenv(engine_roots.ENV_ROOTS, raising=False)


def test_current_name_comes_first_and_former_names_follow(monkeypatch):
    clear_overrides(monkeypatch)
    names = [p.name for p in engine_roots.candidates("digital-research", Path("parent"))]
    assert names == ["digital-research-engine", "chwezi-research-engine", "digital-research-skills"]
    assert [p.name for p in engine_roots.candidates("chwezi-dev-engine", Path("parent"))] == ["chwezi-dev-engine", "skills-web-dev"]


def test_every_registered_engine_has_an_alias_entry():
    registry = json.loads((ROOT / "docs" / "engine-control-plane.json").read_text(encoding="utf-8"))
    assert {engine["id"] for engine in registry["engines"]} == set(engine_roots.ENGINE_DIR_ALIASES)


def test_parents_are_searched_in_order_and_duplicates_dropped(monkeypatch):
    clear_overrides(monkeypatch)
    found = engine_roots.candidates("linux", [Path("a"), Path("b"), Path("a")])
    assert found == [Path("a/linux-skills"), Path("b/linux-skills")]
    assert engine_roots.candidates("not-an-engine", Path("a")) == []


def test_environment_override_is_sole_and_final(monkeypatch, tmp_path):
    clear_overrides(monkeypatch)
    monkeypatch.setenv(engine_roots.env_name("linux"), str(tmp_path / "elsewhere"))
    assert engine_roots.candidates("linux", [tmp_path]) == [tmp_path / "elsewhere"]


def test_roots_from_environment_use_the_platform_separator(monkeypatch, tmp_path):
    clear_overrides(monkeypatch)
    monkeypatch.setenv(engine_roots.ENV_ROOTS, os.pathsep.join([str(tmp_path / "one"), "", str(tmp_path / "two")]))
    assert engine_roots.roots_from_env() == [tmp_path / "one", tmp_path / "two"]


def test_first_existing_does_not_fall_back_past_a_broken_checkout(tmp_path):
    (tmp_path / "second").mkdir()
    assert engine_roots.first_existing([tmp_path / "first", tmp_path / "second"]) == tmp_path / "second"
    (tmp_path / "first").mkdir()
    assert engine_roots.first_existing([tmp_path / "first", tmp_path / "second"]) == tmp_path / "first"
    assert engine_roots.first_existing([tmp_path / "none"]) is None


def make_checkout(parent: Path, name: str, engine: dict) -> None:
    for key in ("router", "adoption_doc"):
        target = parent / name / engine[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("Fixture contract\n", encoding="utf-8")


def test_validator_finds_former_directory_names_across_two_parents(tmp_path, monkeypatch):
    clear_overrides(monkeypatch)
    registry = json.loads(CONTROL.REGISTRY.read_text(encoding="utf-8"))
    first, second = tmp_path / "first", tmp_path / "second"
    for engine in registry["engines"]:
        if engine["id"] == "political":
            continue
        names = engine_roots.ENGINE_DIR_ALIASES[engine["id"]]
        # Use the LAST (former) name and split the engines between two parents.
        parent = first if len(names) % 2 == 0 else second
        make_checkout(parent, names[-1], engine)
    public = CONTROL.EXPECTED_ENGINES - {"political"}
    assert CONTROL.validate_registry([first, second], public) == []
    # One parent alone cannot satisfy every engine: the check must fail closed.
    assert CONTROL.validate_registry([first], public)


def test_dev_engine_resolves_to_the_running_checkout_only_when_no_parent_has_one(tmp_path, monkeypatch):
    clear_overrides(monkeypatch)
    assert CONTROL.engine_candidates(tmp_path, "chwezi-dev-engine")[-1] == CONTROL.ROOT
    monkeypatch.setenv(engine_roots.env_name("chwezi-dev-engine"), str(tmp_path / "chosen"))
    assert CONTROL.engine_candidates(tmp_path, "chwezi-dev-engine") == [tmp_path / "chosen"]


def test_no_drive_letter_or_home_path_is_built_in():
    for module in ("engine_roots.py", "validate_engine_control_plane.py", "validate_approval_adapters.py"):
        text = (ROOT / "scripts" / module).read_text(encoding="utf-8")
        assert "wamp64" not in text and ":/political" not in text and "D:\\" not in text, module


def test_approval_locate_prefers_override_then_self_then_parents(tmp_path, monkeypatch):
    clear_overrides(monkeypatch)
    parent = tmp_path / "parent"
    (parent / "srs-skills").mkdir(parents=True)
    found, tried = APPROVAL.locate("srs", [parent], {})
    assert found == parent / "srs-skills" and [p.name for p in tried] == ["chwezi-sdlc-documentation", "srs-skills"]
    override = {"srs": tmp_path / "direct"}
    assert APPROVAL.locate("srs", [parent], override)[0] == tmp_path / "direct"
    assert APPROVAL.locate("chwezi-dev-engine", [parent], {})[0] == APPROVAL.ROOT
    assert APPROVAL.locate("website", [parent], {})[0] is None


def test_approval_command_line_reports_missing_checkout(tmp_path):
    script = str(ROOT / "scripts" / "validate_approval_adapters.py")
    env = {k: v for k, v in os.environ.items() if not k.startswith("SKILL_ENGINE_ROOT_") and k != engine_roots.ENV_ROOTS}
    result = subprocess.run([sys.executable, script, "--workspace-root", str(tmp_path)], capture_output=True, text=True, env=env)
    assert result.returncode == 1
    assert "no checkout found" in result.stdout
    assert "chwezi-dev-engine: " not in result.stdout  # the running checkout is found
