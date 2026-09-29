"""F13 counterexample: native date input insufficient - deterministic checker (stdlib only).

The requirements need range semantics, per-day blackout explanations reachable by keyboard and
assistive technology, and display in the account locale. Two bare native date inputs cannot meet
them, so this checker fails that shape while still requiring server-side range validation
(including a range that spans a blackout without starting or ending in it) and a recorded,
evidence-based decision. Rendering is parsed with html.parser; the server validator is executed.

    python checker.py <workspace> [--withheld <dir>]

Prints one JSON object and exits 0 (PASS), 1 (FAIL) or 2 (NOT_ASSESSED).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

FIXTURE = "F13"

PROBE = r'''
import json, traceback
from datetime import date
from html.parser import HTMLParser

results = {}
def record(cid, passed, detail=""):
    results[cid] = [bool(passed), str(detail)[:300]]

VOID = {"input", "br", "img", "meta", "link", "hr"}
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements, self.stack, self.text, self.all_text = [], [], {}, ""
    def handle_starttag(self, tag, attrs):
        attrs = {k: (v if v is not None else "") for k, v in attrs}
        self.elements.append((tag, attrs))
        if tag not in VOID:
            self.stack.append(attrs.get("id"))
    def handle_endtag(self, tag):
        if tag not in VOID and self.stack:
            self.stack.pop()
    def handle_data(self, data):
        self.all_text += data
        for ident in self.stack:
            if ident:
                self.text[ident] = self.text.get(ident, "") + data

def parse(markup):
    page = Page(); page.feed(markup); return page

try:
    from scheduling.booking import validate_booking
    from scheduling.page import render_schedule_page

    def check(form):
        try:
            return validate_booking(form)
        except Exception as exc:
            return (["exception " + type(exc).__name__], None)

    errors, booking = check({"start": "2026-03-02", "end": "2026-03-05"})
    record("server_accepts_free_range", not errors and booking and booking.get("start") == date(2026, 3, 2) and booking.get("end") == date(2026, 3, 5), f"{errors} {booking}")
    errors, booking = check({"start": "2026-03-13", "end": "2026-03-19"})
    record("server_accepts_range_between_blackouts", not errors and booking, f"{errors}")
    errors, booking = check({"start": "2026-03-05", "end": "2026-03-02"})
    record("server_rejects_reversed_range", errors and booking is None, errors)
    errors, booking = check({"start": "2026-03-08", "end": "2026-03-14"})
    record("server_rejects_range_spanning_blackout", errors and booking is None, errors)
    record("spanning_error_explains_reason", any("staff training" in str(e).lower() for e in (errors or [])), errors)
    errors, booking = check({"start": "2026-03-20", "end": "2026-03-20"})
    record("server_rejects_single_blackout_day", errors and booking is None, errors)
    bad = [f for f in ({"start": "2026-02-30", "end": "2026-03-02"}, {"start": "", "end": "2026-03-02"}, {"end": "2026-03-02"},
                       {"start": ["2026-03-02"], "end": "2026-03-03"}, {"start": "20260302", "end": "20260303"}, {"start": "2026-03-02T00:00", "end": "2026-03-03"})
           if not (check(f)[0] and check(f)[1] is None)]
    record("server_rejects_invalid_or_missing_dates", not bad, bad)

    page = parse(render_schedule_page("en-GB", date(2026, 3, 2), date(2026, 3, 5)))
    days = {a.get("data-date"): a for t, a in page.elements if a.get("data-date")}
    blackout_days = ["2026-03-10", "2026-03-11", "2026-03-12", "2026-03-20"]
    problems = []
    for d in blackout_days:
        a = days.get(d)
        if a is None:
            problems.append(f"{d} not rendered as an explorable day"); continue
        if a.get("aria-disabled") != "true":
            problems.append(f"{d} not marked aria-disabled")
        ids = a.get("aria-describedby", "").split()
        if not any(("training" in page.text.get(i, "").lower() or "holiday" in page.text.get(i, "").lower()) for i in ids):
            problems.append(f"{d} has no associated reason")
        if "disabled" in a:
            problems.append(f"{d} uses disabled (not focusable for exploration)")
    record("blackout_reasons_exposed_per_day", not problems, problems)
    grids = [a for t, a in page.elements if a.get("role") == "grid"]
    selected = sorted(a.get("data-date") for t, a in page.elements if a.get("aria-selected") == "true" and a.get("data-date"))
    cells_selected = [a for t, a in page.elements if a.get("aria-selected") == "true"]
    record("range_semantics", bool(grids) and any(g.get("aria-multiselectable") == "true" for g in grids) and len(cells_selected) >= 4, f"grids={len(grids)} selected={len(cells_selected)}")
    focusable = [a.get("data-date") for t, a in page.elements if a.get("data-date") and a.get("tabindex") == "0"]
    record("keyboard_exploration_roving_focus", len(days) >= 28 and len(focusable) == 1, f"days={len(days)} tabindex0={focusable}")
    names = {a.get("name") for t, a in page.elements if t == "input"}
    record("submits_start_and_end", {"start", "end"} <= names, names)
    unlabelled = []
    labels_for = {a.get("for") for t, a in page.elements if t == "label"}
    for t, a in page.elements:
        if t == "input" and a.get("type") != "hidden" and not (a.get("id") in labels_for or a.get("aria-label") or a.get("aria-labelledby")):
            unlabelled.append(a.get("name"))
    record("controls_labelled", not unlabelled, unlabelled)

    fr = parse(render_schedule_page("fr-FR", date(2026, 3, 2), date(2026, 3, 5))).all_text
    us = parse(render_schedule_page("en-US", date(2026, 3, 2), date(2026, 3, 5))).all_text
    record("account_locale_display", "2 mars 2026" in fr and "5 mars 2026" in fr and "March 2, 2026" in us, f"fr={'2 mars 2026' in fr} us={'March 2, 2026' in us}")
except Exception:
    record("probe_crashed", False, traceback.format_exc())
print(json.dumps(results))
'''


def decision_recorded(workspace: Path) -> tuple[bool, str]:
    folder = workspace / "docs" / "decisions"
    notes = sorted(folder.glob("*.md")) if folder.is_dir() else []
    for note in notes:
        text = note.read_text(encoding="utf-8", errors="replace").lower()
        if "native" in text and re.search(r"range[_ ]calendar", text) and ("blackout" in text or "unavailable" in text):
            return True, note.name
    return False, f"no decision note in docs/decisions weighing native input against range_calendar ({[n.name for n in notes]})"


def run_probe(workspace: Path) -> tuple[dict, str]:
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-X", "utf8", "-c", PROBE], cwd=workspace, env=env,
                              capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return {}, "probe timed out"
    lines = [line for line in proc.stdout.splitlines() if line.startswith("{")]
    if not lines:
        return {}, (proc.stderr or proc.stdout)[-1500:]
    return json.loads(lines[-1]), ""


def run_unittests(workspace: Path, start: Path, top: Path) -> tuple[bool, str]:
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", str(start), "-t", str(top)],
                              cwd=workspace, env=env, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return False, "tests timed out"
    return proc.returncode == 0, proc.stderr[-800:]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    checks = []
    ok, tail = run_unittests(workspace, workspace / "public_tests", workspace)
    checks.append({"id": "public_tests", "passed": ok, "detail": "" if ok else tail})
    results, error = run_probe(workspace)
    if error:
        checks.append({"id": "probe", "passed": False, "detail": error})
    for cid, (passed, detail) in results.items():
        checks.append({"id": cid, "passed": passed, "detail": detail})
    ok, detail = decision_recorded(workspace)
    checks.append({"id": "component_reuse_justified_by_evidence", "passed": ok, "detail": detail})
    if args.withheld and args.withheld.is_dir():
        withheld = args.withheld.resolve()
        ok, tail = run_unittests(workspace, withheld, withheld)
        checks.append({"id": "withheld_tests", "passed": ok, "detail": "" if ok else tail})
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
