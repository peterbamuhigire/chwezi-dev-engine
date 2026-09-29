"""Doctrine guard for the per-lane report shapes in parallel-execution-lanes.md.

The lane report lines are a machine contract (R2 register): a controller parses them.
These tests pin the three line shapes with good and bad samples, and check that the
reference still lists the five status tokens verbatim, so a silent edit to the
doctrine fails CI. (Doctrine-as-tests idea adapted from tt-a1i/archify, MIT,
commit 0e4949f910a8e390bd3b4933883a4dcabad571be.)
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCE = REPO_ROOT / "skills" / "ai" / "coding-agent-optimization" / "references" / "parallel-execution-lanes.md"

LOCATE_RE = re.compile(r"^[^\s:]+:\d+ — .+$")
EDIT_RE = re.compile(r"^[^\s:]+:\d+-\d+ — .+$")
REVIEW_RE = re.compile(r"^[^\s:]+:\d+(-\d+)?: (critical|high|medium|low): .+\. .+\.$")
STATUS_TOKENS = ("blocked.", "too-big.", "needs-confirm.", "ambiguous.", "regressed.")
STATUS_RE = re.compile(r"^(blocked|too-big|needs-confirm|ambiguous|regressed)\. \S.*$")


@pytest.mark.parametrize(
    "line",
    [
        "app/Services/InvoiceService.php:142 — credit note posts without period check",
        "src/lib/money.ts:7 — rounding uses float arithmetic",
    ],
)
def test_locate_good(line: str) -> None:
    assert LOCATE_RE.match(line)


@pytest.mark.parametrize(
    "line",
    [
        "InvoiceService.php line 142: credit note posts without period check",
        "app/Services/InvoiceService.php — no line number",
        "app/Services/InvoiceService.php:142 - hyphen instead of dash separator",
    ],
)
def test_locate_bad(line: str) -> None:
    assert not LOCATE_RE.match(line)


@pytest.mark.parametrize(
    "line",
    [
        "app/Services/InvoiceService.php:140-155 — added period lock guard before post",
        "database/migrations/2026_09_29_add_lock.php:1-40 — new periods.locked_at column",
    ],
)
def test_edit_good(line: str) -> None:
    assert EDIT_RE.match(line)


@pytest.mark.parametrize(
    "line",
    [
        "app/Services/InvoiceService.php:140 — single line is a locate shape, not an edit range",
        "app/Services/InvoiceService.php:140-155 changed the guard",
    ],
)
def test_edit_bad(line: str) -> None:
    assert not EDIT_RE.match(line)


@pytest.mark.parametrize(
    "line",
    [
        "app/Http/Controllers/PosController.php:88: high: tenant id read from request body. Take it from the session.",
        "src/api/refunds.ts:12-30: critical: refund skips idempotency key. Require the key before the provider call.",
    ],
)
def test_review_good(line: str) -> None:
    assert REVIEW_RE.match(line)


@pytest.mark.parametrize(
    "line",
    [
        "app/Http/Controllers/PosController.php:88: severe: tenant id read from request body. Take it from the session.",
        "app/Http/Controllers/PosController.php:88: high: tenant id read from request body",
        "PosController line 88 is risky, please fix.",
    ],
)
def test_review_bad(line: str) -> None:
    assert not REVIEW_RE.match(line)


@pytest.mark.parametrize(
    "line",
    [
        "blocked. The staging database credential is not available to this lane.",
        "needs-confirm. The next step drops the legacy_invoices table.",
        "regressed. PeriodLockTest passed before this lane and now fails.",
    ],
)
def test_status_good(line: str) -> None:
    assert STATUS_RE.match(line)


@pytest.mark.parametrize(
    "line",
    [
        "BLOCKED: no credential",
        "blocked no credential",
        "done. everything worked",
    ],
)
def test_status_bad(line: str) -> None:
    assert not STATUS_RE.match(line)


def test_reference_lists_status_tokens_and_shapes_verbatim() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    for token in STATUS_TOKENS:
        assert f"`{token}`" in text, f"status token {token!r} missing from {REFERENCE.name}"
    for shape in ("`path:line — finding`", "`path:start-end — change`", "`path:line: severity: problem. fix.`"):
        assert shape in text, f"line shape {shape} missing from {REFERENCE.name}"
    assert "R1" in text, "the rewrite-into-R1 rule is missing"


def test_reference_examples_match_their_shapes() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    examples = re.findall(r"^\| (Locate|Edit|Review) \| `[^`]+` \| `([^`]+)` \|$", text, re.MULTILINE)
    assert len(examples) == 3
    patterns = {"Locate": LOCATE_RE, "Edit": EDIT_RE, "Review": REVIEW_RE}
    for lane, example in examples:
        assert patterns[lane].match(example), f"{lane} example does not match its own shape: {example}"
