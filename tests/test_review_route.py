"""The review route must connect a mixed-defect diff to every owning check, and the links must resolve."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "skills/sdlc-meta/ai-assisted-development/references/ai-generated-code-review-gate.md"
EXERCISE = ROOT / "examples/tenant-invoice-listing/review-exercise.md"
HEADING = "Domain-owned checks to load for a mixed-defect diff"
LINK = re.compile(r"\[[^\]]+\]\(([^)#\s]+)(?:#([^)\s]+))?\)")

# defect class -> (keyword the table row must carry, keyword the linked file must carry)
EXPECTED = {
    "sql injection": ("SQL built from request input", "bound"),
    "tenant predicate": ("Tenant predicate missing", "tenant"),
    "n+1": ("N+1", "N+1"),
    "output escaping": ("Unescaped output", "escap"),
    "ledger write": ("Ledger or journal write", "journal_lines"),
}


def section(text: str, heading: str) -> str:
    start = text.index(f"## {heading}")
    rest = text[start + 3 :]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


def slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")


def test_root_router_has_a_review_row_pointing_at_the_gate():
    router = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    rows = [line for line in router.splitlines() if line.startswith("|") and "pull request" in line.lower()]
    assert rows, "root router has no pull-request review row"
    assert "ai-generated-code-review-gate.md" in rows[0]
    index = (ROOT / "docs/skill-routing-index.md").read_text(encoding="utf-8")
    assert "accounting-engine" in section(index, "Reviewing a change before merge")


def test_gate_table_covers_each_defect_class_and_every_link_resolves():
    body = section(GATE.read_text(encoding="utf-8"), HEADING)
    rows = [line for line in body.splitlines() if line.startswith("|") and "---" not in line][1:]
    assert len(rows) == len(EXPECTED)
    for defect, (row_key, file_key) in EXPECTED.items():
        row = next((line for line in rows if row_key in line), None)
        assert row is not None, f"no row for {defect}"
        match = LINK.search(row)
        assert match, f"{defect}: row has no link"
        target = (GATE.parent / match.group(1)).resolve()
        assert target.is_file(), f"{defect}: {match.group(1)} does not exist"
        assert file_key.lower() in target.read_text(encoding="utf-8").lower(), f"{defect}: linked file does not mention {file_key!r}"


def test_ledger_row_requires_the_accounting_owner_and_review_record_names_it():
    text = GATE.read_text(encoding="utf-8")
    assert "A diff with a ledger write and no accounting owner named is incomplete" in text
    assert "Domain-owned checks loaded:" in text


def test_exercise_links_the_gate_anchor_and_uses_the_owning_skill_name():
    text = EXERCISE.read_text(encoding="utf-8")
    anchors = [m for m in LINK.finditer(text) if m.group(1).endswith("ai-generated-code-review-gate.md")]
    assert anchors, "exercise does not link the review gate"
    target = (EXERCISE.parent / anchors[0].group(1)).resolve()
    assert target == GATE
    headings = [slug(line[3:]) for line in GATE.read_text(encoding="utf-8").splitlines() if line.startswith("## ")]
    assert anchors[0].group(2) in headings
    assert "LedgerPostingService" in text
    assert "doctrine-controlled `JournalPostingService`" not in text
