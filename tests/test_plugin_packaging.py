from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import check_package_file_budget
from check_package_file_budget import LIMIT, counts


def test_codex_portable_manifest_and_repo_marketplace_are_valid_shapes() -> None:
    plugin = json.loads((REPO / "plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((REPO / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    assert plugin["name"] == "chwezi-dev-engine"
    assert plugin["version"] == "1.1.0"
    assert plugin["author"]["name"] == "Peter Bamuhigire"
    assert "skills" not in plugin  # Portable packages discover root skills/.
    assert marketplace["plugins"][0]["source"]["path"] == "./"
    assert marketplace["plugins"][0]["policy"]["installation"] == "AVAILABLE"


def test_claude_plugin_skill_paths_match_present_skills() -> None:
    manifest = json.loads((REPO / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    paths = manifest["skills"]
    assert len(paths) == 168
    assert all((REPO / path.removeprefix("./") / "SKILL.md").is_file() for path in paths)
    active = list((REPO / "skills").glob("**/SKILL.md"))
    initialisation = list((REPO / "00-meta-initialization").glob("**/SKILL.md"))
    assert len(active) == 168
    assert len(initialisation) == 2


def test_current_checkout_is_under_file_budget() -> None:
    checkout, package = counts(REPO)
    assert 0 < package <= LIMIT
    assert checkout >= package


def test_budget_reports_checkout_and_excludes_git_and_dependency_trees_from_package_count(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "metadata").write_text("x", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "module.js").write_text("x", encoding="utf-8")
    (tmp_path / "skill").mkdir()
    (tmp_path / "skill" / "SKILL.md").write_text("x", encoding="utf-8")
    assert counts(tmp_path) == (3, 1)


def test_large_git_history_is_reported_but_does_not_consume_package_budget(tmp_path: Path) -> None:
    git_objects = tmp_path / ".git" / "objects"
    git_objects.mkdir(parents=True)
    for index in range(LIMIT + 1):
        (git_objects / f"object-{index}").touch()
    skill = tmp_path / "skills" / "example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")

    checkout, package = counts(tmp_path)
    assert checkout > LIMIT
    assert package == 1
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts/check_package_file_budget.py"), str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"checkout entries (including .git): {checkout}" in result.stdout
    assert "package-oriented entries (documented exclusions): 1" in result.stdout
    assert "PASS: package-oriented entries are at most 5000" in result.stdout


def test_budget_command_fails_above_the_hard_cap(tmp_path: Path) -> None:
    package = tmp_path / "skills"
    package.mkdir()
    for index in range(LIMIT + 1):
        (package / f"file-{index}.md").touch()
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts/check_package_file_budget.py"), str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "FAIL: package-oriented entries must be at most 5000" in result.stdout


def test_budget_count_fails_closed_when_walk_skips_a_directory(tmp_path: Path, monkeypatch) -> None:
    def failed_walk(root, *, followlinks, onerror):
        onerror(PermissionError("fixture permission failure"))
        return iter(())

    monkeypatch.setattr(check_package_file_budget.os, "walk", failed_walk)
    try:
        counts(tmp_path)
    except OSError as exc:
        assert "could not count all entries" in str(exc)
    else:
        raise AssertionError("partial file inventory must not be accepted")
