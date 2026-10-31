"""Tests for scripts/content_hygiene.py: machine paths, duplicate headings, broken links."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import content_hygiene as ch  # noqa: E402


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- machine paths -----------------------------------------------------------------

@pytest.mark.parametrize("line", [
    "Use the engine at `C:\\wamp64\\www\\digital-research-engine`.",
    "Use the engine at `d:/wamp64/www/x`.",
    "Profile `C:\\Users\\Peter\\AppData` is hard-coded.",
    "Copy from /home/peter/work/notes",
    "See [log](/tmp/run/output.log) for detail.",
])
def test_host_specific_paths_are_flagged(tmp_path, line):
    write(tmp_path, "skills/a/SKILL.md", line + "\n")
    findings = ch.check_machine_paths(tmp_path, allowlist=[])
    assert [f[0] for f in findings] == ["machine-path"], line
    assert findings[0][1] == "skills/a/SKILL.md"


@pytest.mark.parametrize("line", [
    "Home folder example /home/you/project and /home/username/app.",
    "Windows example C:\\Users\\username\\Documents.",
    "Teaching path /Users/alice/Desktop/report.pdf.",
    "Relative <project>/public/api/ is fine and so is engine-name/skills/x.",
    "Link to [site](https://example.org/tmp/x) and [local](references/a.md).",
])
def test_examples_and_relative_paths_are_not_flagged(tmp_path, line):
    write(tmp_path, "skills/a/SKILL.md", line + "\n")
    assert ch.check_machine_paths(tmp_path, allowlist=[]) == []


def test_dated_records_fixtures_and_changelog_are_out_of_scope(tmp_path):
    bad = "C:\\wamp64\\www\\x\n"
    for rel in ("docs/audits/2026/a.md", "docs/updates/a.md", "tests/fixtures/a.md", "CHANGELOG.md", "benchmarks/a.md"):
        write(tmp_path, rel, bad)
    assert ch.check_machine_paths(tmp_path, allowlist=[]) == []
    write(tmp_path, "docs/kaizen/2026-10-engine-kaizen-pass-2/a.md", bad)
    assert len(ch.check_machine_paths(tmp_path, allowlist=[])) == 1


def test_allowlist_needs_path_contains_and_reason(tmp_path):
    write(tmp_path, "skills/a/SKILL.md", "Layout C:\\wamp64\\www\\{project}\\\n")
    entry = {"path": "skills/a/SKILL.md", "contains": "{project}", "reason": "documented WAMP layout"}
    assert ch.check_machine_paths(tmp_path, allowlist=[entry]) == []
    gates = tmp_path / "docs/quality-gates"
    gates.mkdir(parents=True)
    (gates / "machine-path-allowlist.yml").write_text("allow:\n  - path: skills/a/SKILL.md\n    contains: x\n", encoding="utf-8")
    with pytest.raises(ValueError):
        ch.check_machine_paths(tmp_path)


def test_repository_has_no_machine_specific_paths_in_active_content():
    assert ch.check_machine_paths(ROOT) == []
