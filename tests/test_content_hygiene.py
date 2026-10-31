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


# --- duplicate headings --------------------------------------------------------------

SKILL = "---\nname: x\ndescription: d\n---\n\n# X\n\n## Use When\n\n- a\n\n## References\n\n- one\n\n```md\n## References\n```\n"


def test_duplicate_h2_outside_code_fences_is_found(tmp_path):
    write(tmp_path, "skills/a/SKILL.md", SKILL)
    assert ch.duplicate_headings(tmp_path) == {}
    write(tmp_path, "skills/b/SKILL.md", SKILL + "\n## references\n\n- two\n")
    assert ch.duplicate_headings(tmp_path) == {"skills/b/SKILL.md": ["references"]}


def test_new_duplicate_fails_and_fixed_baseline_entry_must_be_removed(tmp_path):
    write(tmp_path, "skills/b/SKILL.md", SKILL + "\n## References\n\n- two\n")
    baseline = tmp_path / "docs/quality-gates/duplicate-heading-baseline.json"
    write(tmp_path, "docs/quality-gates/duplicate-heading-baseline.json", json.dumps({"skills": {}}))
    findings = ch.check_duplicate_headings(tmp_path, baseline)
    assert [f[0] for f in findings] == ["duplicate-heading"]
    baseline.write_text(json.dumps({"skills": {"skills/b/SKILL.md": ["references"]}}), encoding="utf-8")
    assert ch.check_duplicate_headings(tmp_path, baseline) == []
    write(tmp_path, "skills/b/SKILL.md", SKILL)  # the duplicate is fixed
    findings = ch.check_duplicate_headings(tmp_path, baseline)
    assert [f[0] for f in findings] == ["duplicate-heading-baseline"]


def test_repository_duplicate_headings_match_the_recorded_baseline():
    assert ch.check_duplicate_headings(ROOT) == []
    recorded = json.loads((ROOT / "docs/quality-gates/duplicate-heading-baseline.json").read_text(encoding="utf-8"))["skills"]
    assert recorded == ch.duplicate_headings(ROOT)


# --- broken links --------------------------------------------------------------------

def test_broken_relative_links_are_found_and_placeholders_and_urls_are_ignored(tmp_path):
    write(tmp_path, "skills/a/SKILL.md", "---\nname: a\ndescription: d\n---\n[ok](references/r.md) [gone](references/missing.md#x) [web](https://e.org/x) [tpl](references/<topic>.md) [anchor](#top)\n")
    write(tmp_path, "skills/a/references/r.md", "[parent](../SKILL.md) [bad](../nothing.md)\n```md\n[fenced](ignored.md)\n```\n")
    found = ch.broken_links(tmp_path)
    assert found == {"skills/a/SKILL.md": ["references/missing.md#x"], "skills/a/references/r.md": ["../nothing.md"]}


def test_new_broken_link_fails_and_repaired_baseline_entry_must_be_removed(tmp_path):
    write(tmp_path, "skills/a/SKILL.md", "[gone](missing.md)\n")
    baseline = tmp_path / "docs/quality-gates/broken-link-baseline.json"
    write(tmp_path, "docs/quality-gates/broken-link-baseline.json", json.dumps({"files": {}}))
    assert [f[0] for f in ch.check_broken_links(tmp_path, baseline)] == ["broken-link"]
    baseline.write_text(json.dumps({"files": {"skills/a/SKILL.md": ["missing.md"]}}), encoding="utf-8")
    assert ch.check_broken_links(tmp_path, baseline) == []
    write(tmp_path, "skills/a/missing.md", "now present\n")
    assert [f[0] for f in ch.check_broken_links(tmp_path, baseline)] == ["broken-link-baseline"]


def test_repository_broken_links_match_the_recorded_baseline():
    assert ch.check_broken_links(ROOT) == []
    recorded = json.loads((ROOT / "docs/quality-gates/broken-link-baseline.json").read_text(encoding="utf-8"))["files"]
    assert recorded == ch.broken_links(ROOT)
