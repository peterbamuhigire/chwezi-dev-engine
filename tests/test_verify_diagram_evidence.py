"""Tests for system-architecture-design/scripts/verify_diagram_evidence.py.

Each test builds a throwaway Git repository in tmp_path.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "architecture" / "system-architecture-design" / "scripts" / "verify_diagram_evidence.py"
SPEC = importlib.util.spec_from_file_location("verify_diagram_evidence", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def git(root: Path, *args: str) -> str:
    res = subprocess.run(
        ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return res.stdout.strip()


@pytest.fixture()
def repo(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repo"
    (root / "app" / "Services").mkdir(parents=True)
    (root / "app" / "Services" / "InvoicePoster.php").write_text("\n".join(f"line {n}" for n in range(1, 41)) + "\n", encoding="utf-8")
    (root / "README.md").write_text("# fixture\n", encoding="utf-8")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    sha = git(root, "rev-parse", "HEAD")
    # Move the file after the pinned revision: the old citation must still verify at `sha`.
    git(root, "mv", "app/Services/InvoicePoster.php", "app/Services/Poster.php")
    git(root, "commit", "-q", "-m", "move")
    return root, sha


def model(sha: str, *sources: dict) -> dict:
    return {"meta": {"repository": {"revision": sha}}, "elements": [{"id": "erp.web.posting"}], "sources": list(sources)}


def codes(doc: dict, root: Path) -> list[str]:
    return [f["code"] for f in MODULE.verify(doc, root)]


def test_valid_citations_pass(repo, tmp_path: Path) -> None:
    root, sha = repo
    doc = model(sha, {"path": "app/Services/InvoicePoster.php", "line": 14, "end_line": 38}, {"path": "README.md", "line": 1})
    assert codes(doc, root) == []
    path = tmp_path / "model.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    assert MODULE.main(["--repo-root", str(root), str(path)]) == 0


def test_out_of_range_line(repo) -> None:
    root, sha = repo
    assert codes(model(sha, {"path": "app/Services/InvoicePoster.php", "line": 30, "end_line": 41}), root) == ["evidence/line-out-of-range"]


def test_reversed_range(repo) -> None:
    root, sha = repo
    assert codes(model(sha, {"path": "README.md", "line": 2, "end_line": 1}), root) == ["evidence/line-out-of-range"]


def test_moved_file_is_missing_at_revision(repo) -> None:
    root, sha = repo
    assert codes(model(sha, {"path": "app/Services/Poster.php", "line": 1}), root) == ["evidence/missing-at-revision"]


@pytest.mark.parametrize(
    "path",
    ["../outside.md", "app/../README.md", "./README.md", "app\\Services\\InvoicePoster.php", "/etc/passwd", "C:/Windows/win.ini", ".git/config"],
)
def test_path_escape(repo, path: str) -> None:
    root, sha = repo
    assert codes(model(sha, {"path": path, "line": 1}), root) == ["evidence/path-escape"]


def test_short_sha_is_rejected(repo) -> None:
    root, sha = repo
    assert codes(model(sha[:12], {"path": "README.md", "line": 1}), root) == ["evidence/revision-not-full"]


def test_unknown_revision(repo) -> None:
    root, _sha = repo
    assert codes(model("0" * 40, {"path": "README.md", "line": 1}), root) == ["evidence/revision-unknown"]


def test_repo_root_must_be_toplevel(repo) -> None:
    root, sha = repo
    assert codes(model(sha, {"path": "README.md", "line": 1}), root / "app") == ["evidence/repo-root-not-toplevel"]


def test_missing_fields(repo) -> None:
    root, _sha = repo
    assert codes({"sources": []}, root) == ["evidence/invalid-document"]
