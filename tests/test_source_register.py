"""Tests for scripts/check_source_register.py: the checker must fail closed."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_source_register as csr  # noqa: E402

AS_OF = date(2026, 10, 31)


def source(**changes):
    base = {
        "id": "s1", "accessed": "2026-10-31", "verified_at": "2026-10-31", "review_after": "2026-11-30",
        "freshness_class": "platform", "as_of": "2026-10-31", "scope": "Example scope.",
    }
    base.update(changes)
    return base


def register(*sources, claims=None, **extra):
    data = {"sources": list(sources), "claims": claims if claims is not None else []}
    data.update(extra)
    return data


def test_valid_register_passes():
    findings, _ = csr.check_register(register(source(), claims=[{"id": "c1", "requires_currentness": True, "source_ids": ["s1"]}]), AS_OF)
    assert findings == []


def test_overdue_review_fails():
    findings, _ = csr.check_register(register(source(review_after="2026-10-30")), AS_OF)
    assert any("overdue" in item for item in findings)


def test_review_due_today_is_not_overdue():
    findings, _ = csr.check_register(register(source(review_after="2026-10-31")), AS_OF)
    assert findings == []


def test_upcoming_review_warns_without_failing():
    findings, warnings = csr.check_register(register(source(review_after="2026-11-05")), AS_OF, warn_days=14)
    assert findings == [] and any("within 14 days" in item for item in warnings)


@pytest.mark.parametrize("field", ["accessed", "verified_at", "review_after", "freshness_class"])
def test_missing_required_field_fails(field):
    item = source()
    del item[field]
    findings, _ = csr.check_register(register(item), AS_OF)
    assert any(f"missing {field}" in text for text in findings)


def test_bad_iso_date_and_future_date_fail():
    findings, _ = csr.check_register(register(source(accessed="31/10/2026")), AS_OF)
    assert any("not an ISO date" in text for text in findings)
    findings, _ = csr.check_register(register(source(accessed="2026-11-02", verified_at="2026-11-02")), AS_OF)
    assert any("in the future" in text for text in findings)


def test_current_source_needs_a_date_basis_and_context_bound_needs_scope():
    item = source()
    del item["as_of"]
    findings, _ = csr.check_register(register(item), AS_OF)
    assert any("requires publication_date" in text for text in findings)
    findings, _ = csr.check_register(register(source(freshness_class="context-bound", scope="  ")), AS_OF)
    assert any("non-empty scope" in text for text in findings)


def test_claim_may_not_name_unknown_superseded_or_quarantined_source():
    data = register(
        source(),
        claims=[{"id": "c1", "requires_currentness": True, "source_ids": ["gone", "old", "held"]}],
        superseded_sources=[source(id="old", superseded_by="s1")],
        quarantined_sources=[source(id="held", quarantine={"status": "NOT_ASSESSED", "reason": "page blocked", "reverify_by": "2026-11-30"})],
    )
    findings, _ = csr.check_register(data, AS_OF)
    assert any("gone names an unknown source" in text for text in findings)
    assert any("old names a superseded or quarantined source" in text for text in findings)
    assert any("held names a superseded or quarantined source" in text for text in findings)


def test_superseded_and_quarantined_entries_are_validated():
    data = register(
        source(),
        superseded_sources=[source(id="old", superseded_by="missing")],
        quarantined_sources=[source(id="held", quarantine={"status": "verified", "reason": "", "reverify_by": "soon"})],
    )
    findings, _ = csr.check_register(data, AS_OF)
    text = "\n".join(findings)
    assert "superseded_by 'missing' is not an active source" in text
    assert "quarantine.status must be NOT_ASSESSED" in text
    assert "quarantine needs a reason" in text
    assert "quarantine.reverify_by is not an ISO date" in text


def test_duplicate_ids_fail():
    findings, _ = csr.check_register(register(source(), source()), AS_OF)
    assert any("duplicate source id" in text for text in findings)


def test_legacy_schema_is_warned_not_enforced():
    legacy = {"register_id": "old", "review_date": "2026-10-14", "sources": [{"source_id": "x"}]}
    assert "overdue" in (csr.legacy_warning(legacy, AS_OF) or "")
    assert csr.legacy_warning(legacy, date(2026, 10, 1)) is None


def test_command_line_exit_codes(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(json.dumps(register(source())), encoding="utf-8")
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(register(source(review_after="2026-01-01"))), encoding="utf-8")
    script = str(ROOT / "scripts" / "check_source_register.py")
    ok = subprocess.run([sys.executable, script, "--as-of", "2026-10-31", str(good)], capture_output=True, text=True)
    failed = subprocess.run([sys.executable, script, "--as-of", "2026-10-31", str(bad)], capture_output=True, text=True)
    assert ok.returncode == 0 and "PASS" in ok.stdout
    assert failed.returncode == 1 and "overdue" in failed.stdout


def test_repository_registers_pass_on_the_reconciliation_date():
    paths = sorted((ROOT / "docs" / "source-registers").glob("*.json"))
    assert paths
    result = csr.run(paths, AS_OF, 14)
    assert result == 0
