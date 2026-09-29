"""Crafted fixtures for the Tier-1 lint refinements (M10-03-T12) and the SP-14
description-narration warning (M10-03-T13) in skill-writing/scripts/quick_validate.py."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "sdlc-meta" / "skill-writing" / "scripts" / "quick_validate.py"
SPEC = importlib.util.spec_from_file_location("quick_validate_lint", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
qv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qv)

SECTIONS = ["Use When", "Do Not Use When", "Required Inputs", "Workflow", "Quality Standards", "Anti-Patterns", "Outputs", "References"]


def meta(description: str) -> dict:
    return {"name": "example", "description": description, "metadata": {"portable": True, "compatible_with": ["claude-code", "codex"]}}


def body(sections: list[str]) -> str:
    return "<!-- dual-compat-start -->\n<!-- dual-compat-end -->\n" + "".join(f"## {name}\n\nText.\n\n" for name in sections)


def test_headings_inside_a_fence_do_not_count_as_sections():
    fenced = body(SECTIONS[:-1]) + "```markdown\n## References\n```\n"
    errors: list[str] = []
    qv.validate_portable_sections(meta("Use when testing."), fenced, errors)
    assert "Portable contract element missing: `References`." in errors
    errors = []
    qv.validate_portable_sections(meta("Use when testing."), body(SECTIONS), errors)
    assert errors == []


def test_tilde_and_longer_fences_are_stripped():
    text = "a\n~~~~\n## Hidden\n~~~\nstill hidden\n~~~~\nb\n````\n```\n## Also hidden\n````\n## Shown"
    stripped = qv.strip_fenced_code(text)
    assert "Hidden" not in stripped and "Also hidden" not in stripped and "## Shown" in stripped


def test_negated_trigger_cannot_supply_the_positive_trigger():
    errors: list[str] = []
    qv.validate_frontmatter(meta("Use when: do not use when drafting prose."), Path("example"), errors)
    assert any("no positive 'Use when' trigger" in error for error in errors)
    errors = []
    qv.validate_frontmatter(meta("Use when reviewing pull requests; do not use when drafting prose."), Path("example"), errors)
    assert errors == []


def test_self_exemption_in_frontmatter_is_rejected():
    data = meta("Use when testing fixtures.")
    data["metadata"]["lint_exempt"] = ["sections"]
    errors: list[str] = []
    qv.validate_frontmatter(data, Path("example"), errors)
    assert any("cannot be declared in skill frontmatter" in error for error in errors)


def test_validator_owned_exemption_is_honoured(monkeypatch):
    monkeypatch.setitem(qv.EXEMPTIONS, "example", {"sections": "fixture reason"})
    errors: list[str] = []
    qv.validate_portable_sections(meta("Use when testing."), body([]), errors)
    assert errors == []


def test_host_strict_yaml_subset():
    assert any("tab" in e for e in qv.host_yaml_errors("name: x\nmetadata:\n\tportable: true"))
    assert any("never closed" in e for e in qv.host_yaml_errors('name: x\ndescription: "Use when testing'))
    assert any("unquoted ': '" in e for e in qv.host_yaml_errors("name: x\ndescription: Use when testing: a fixture"))
    assert qv.host_yaml_errors('name: x\ndescription: "Use when testing: a fixture"\nmetadata:\n  portable: true') == []


def test_narration_warning_and_clean_description():
    assert qv.narration_warnings("Use when shipping; runs the six-phase gate then reports.")
    assert qv.narration_warnings("Use when reviewing pull requests before merge.") == []


def test_narration_warning_does_not_change_exit_status(tmp_path):
    skill = tmp_path / "example"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: Use when shipping a release; runs the six-phase gate then reports.\n"
        "metadata:\n  portable: true\n  compatible_with: [claude-code, codex]\n---\n" + body(SECTIONS),
        encoding="utf-8",
    )
    result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(skill)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
    assert "WARNING: Description narrates the workflow" in result.stdout
    assert "instead of reading the body" in result.stdout


def test_clean_use_when_fixture_passes_without_warning(tmp_path):
    skill = tmp_path / "example"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: Use when reviewing pull requests before merge.\n"
        "metadata:\n  portable: true\n  compatible_with: [claude-code, codex]\n---\n" + body(SECTIONS),
        encoding="utf-8",
    )
    result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(skill)], capture_output=True, text=True)
    assert result.returncode == 0
    assert "WARNING" not in result.stdout
