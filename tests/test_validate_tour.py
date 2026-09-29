"""Tests for skills/sdlc-meta/doc-architect/scripts/validate_tour.py."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "sdlc-meta" / "doc-architect" / "scripts" / "validate_tour.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "tours"
PROJECT_REL = Path("tests") / "fixtures" / "tours" / "project"

SPEC = importlib.util.spec_from_file_location("validate_tour", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE  # dataclasses resolve annotations through sys.modules
SPEC.loader.exec_module(MODULE)


def codes(tour: Path, root: Path) -> list[str]:
    findings, _notes = MODULE.validate(tour, root)
    return [f.code for f in findings]


def git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "-C", str(root), *args],
        check=True,
        capture_output=True,
    )


def test_valid_fixture_passes_on_disk() -> None:
    assert codes(FIXTURES / "valid.tour", REPO_ROOT) == []
    assert MODULE.main([str(FIXTURES / "valid.tour"), "--repo-root", str(REPO_ROOT)]) == 0


@pytest.mark.parametrize(
    ("fixture", "expected"),
    [
        ("missing-file.tour", "tour/missing-file"),
        ("line-out-of-range.tour", "tour/line-out-of-range"),
        ("unanchored-first-step.tour", "tour/unanchored-first-step"),
    ],
)
def test_failing_fixtures_report_their_distinct_code(fixture: str, expected: str) -> None:
    assert codes(FIXTURES / fixture, REPO_ROOT) == [expected]
    assert MODULE.main([str(FIXTURES / fixture), "--repo-root", str(REPO_ROOT)]) == 1


@pytest.fixture()
def fixture_repo(tmp_path: Path) -> Path:
    """A throwaway repository: tag fixture-base predates LatePoster.php."""
    root = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / PROJECT_REL, root / PROJECT_REL)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    git(root, "tag", "fixture-base")
    late = root / PROJECT_REL / "app" / "Services" / "LatePoster.php"
    late.write_text("<?php\n// added after fixture-base\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "late")
    return root


def test_absent_at_ref_fixture(fixture_repo: Path) -> None:
    assert codes(FIXTURES / "absent-at-ref.tour", fixture_repo) == ["tour/absent-at-ref"]
    assert MODULE.main([str(FIXTURES / "absent-at-ref.tour"), "--repo-root", str(fixture_repo)]) == 1


def test_ref_reads_line_counts_from_the_revision_not_disk(fixture_repo: Path, tmp_path: Path) -> None:
    index = fixture_repo / PROJECT_REL / "public" / "index.php"
    index.write_text(index.read_text(encoding="utf-8") + "\n" * 50, encoding="utf-8")
    tour = json.loads((FIXTURES / "valid.tour").read_text(encoding="utf-8"))
    tour["ref"] = "fixture-base"
    tour["steps"][2]["line"] = 40  # in range on disk, out of range at the ref
    path = tmp_path / "vibecoder-ref.tour"
    path.write_text(json.dumps(tour), encoding="utf-8")
    assert codes(path, fixture_repo) == ["tour/line-out-of-range"]


def test_unknown_ref_is_reported(tmp_path: Path, fixture_repo: Path) -> None:
    tour = json.loads((FIXTURES / "valid.tour").read_text(encoding="utf-8"))
    tour["ref"] = "no-such-ref"
    path = tmp_path / "t.tour"
    path.write_text(json.dumps(tour), encoding="utf-8")
    assert codes(path, fixture_repo) == ["tour/bad-ref"]


def test_step_budget_from_file_name(tmp_path: Path) -> None:
    tour = json.loads((FIXTURES / "valid.tour").read_text(encoding="utf-8"))
    del tour["persona"]
    path = tmp_path / "architect-invoicing.tour"
    path.write_text(json.dumps(tour), encoding="utf-8")
    assert codes(path, REPO_ROOT) == ["tour/step-count-out-of-budget"]


def test_no_persona_marks_budget_not_assessed(tmp_path: Path) -> None:
    tour = json.loads((FIXTURES / "valid.tour").read_text(encoding="utf-8"))
    del tour["persona"]
    path = tmp_path / "t.tour"
    path.write_text(json.dumps(tour), encoding="utf-8")
    findings, notes = MODULE.validate(path, REPO_ROOT)
    assert findings == []
    assert any("NOT_ASSESSED" in n for n in notes)


def test_path_escape_is_rejected(tmp_path: Path) -> None:
    tour = json.loads((FIXTURES / "valid.tour").read_text(encoding="utf-8"))
    tour["steps"][1]["file"] = "../outside.md"
    path = tmp_path / "t.tour"
    path.write_text(json.dumps(tour), encoding="utf-8")
    assert codes(path, REPO_ROOT) == ["tour/missing-file"]


def test_budgets_match_code_tour_reference() -> None:
    text = (REPO_ROOT / "skills" / "sdlc-meta" / "doc-architect" / "references" / "code-tour.md").read_text(encoding="utf-8")
    for persona, (low, high) in MODULE.PERSONA_BUDGETS.items():
        assert f"| `{persona}` | {low}-{high} |" in text, f"budget for {persona} drifted from code-tour.md"
