"""F02 native form control - deterministic checker (stdlib only, no model call).

Renders the produced form and parses it with html.parser: the renewal date must use the native
date control with no picker dependency, keep keyboard entry, and associate label, help and error
text with the control. Then it executes the server-side handler against adversarial values
(impossible and leap dates, lax formats, timestamps, whitespace, huge and non-string input) and
checks that a valid civil date round-trips unchanged for users at extreme UTC offsets (no
conversion through UTC midnight) and that an empty optional value is kept as an absence.

    python checker.py <workspace> [--withheld <dir>]

Prints one JSON object and exits 0 (PASS), 1 (FAIL) or 2 (NOT_ASSESSED).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

FIXTURE = "F02"

PROBE = r'''
import json, re, traceback
from html.parser import HTMLParser

results = {}
def record(cid, passed, detail=""):
    results[cid] = [bool(passed), str(detail)[:300]]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements, self.stack, self.text = [], [], {}
    def handle_starttag(self, tag, attrs):
        attrs = {k: (v if v is not None else "") for k, v in attrs}
        self.elements.append((tag, attrs))
        if tag not in ("input", "br", "img", "meta", "link"):
            self.stack.append(attrs.get("id"))
    def handle_endtag(self, tag):
        if tag not in ("input", "br", "img", "meta", "link") and self.stack:
            self.stack.pop()
    def handle_data(self, data):
        for ident in self.stack:
            if ident:
                self.text[ident] = self.text.get(ident, "") + data

def parse(markup):
    page = Page(); page.feed(markup); return page

def field(page):
    for tag, attrs in page.elements:
        if tag == "input" and attrs.get("name") == "renewal_date":
            return attrs
    return None

try:
    from app.settings import display_value, handle_submit, render_form
    plain = parse(render_form("2026-03-01"))
    ctrl = field(plain) or {}
    record("native_date_control", ctrl.get("type", "").lower() == "date", f"input attrs={ctrl}")
    scripts = [a.get("src", "") for t, a in plain.elements if t == "script"]
    links = [a.get("href", "") for t, a in plain.elements if t == "link"]
    picker = [s for s in scripts + links if re.search(r"pick|date|calendar|flatpickr|jquery", s, re.I)]
    record("no_picker_dependency", not picker, f"scripts={scripts} links={links}")
    keyboard_ok = ctrl and "readonly" not in ctrl and "disabled" not in ctrl and ctrl.get("inputmode") != "none" \
        and not str(ctrl.get("tabindex", "0")).startswith("-") and not any(k.startswith("onkey") for k in ctrl)
    record("keyboard_entry_preserved", keyboard_ok, ctrl)
    ident = ctrl.get("id")
    labels = [a for t, a in plain.elements if t == "label" and a.get("for") == ident]
    record("label_associated", bool(ident) and len(labels) == 1, f"id={ident}")
    described = (ctrl.get("aria-describedby") or "").split()
    record("help_text_associated", any("Optional" in plain.text.get(d, "") for d in described), described)
    record("optional_not_required", ctrl and "required" not in ctrl and ctrl.get("aria-required") != "true", ctrl)
    message = "Enter a real date."
    bad = parse(render_form("", message))
    bctrl = field(bad) or {}
    bdesc = (bctrl.get("aria-describedby") or "").split()
    err_ids = [d for d in bdesc if message in bad.text.get(d, "")]
    record("error_associated_and_invalid", bool(err_ids) and bctrl.get("aria-invalid") == "true", f"describedby={bdesc} aria-invalid={bctrl.get('aria-invalid')}")
    esc = render_form('"><script>alert(1)</script>')
    record("value_escaped", "<script>alert(1)" not in esc, "")

    failures = []
    for raw in ("2024-02-29", "2026-01-01", "2025-12-31", "2026-03-01"):
        errors, stored = handle_submit({"renewal_date": raw})
        if errors:
            failures.append(f"{raw} rejected: {errors}")
            continue
        for offset in (-720, -600, -300, 0, 330, 780, 840):
            shown = display_value(stored, offset)
            if shown != raw:
                failures.append(f"{raw} at {offset:+}min shown as {shown}")
    record("civil_date_round_trips_all_offsets", not failures, "; ".join(failures[:6]))

    errors, stored = handle_submit({"renewal_date": ""})
    record("empty_optional_retained", not errors and stored.get("renewal_date") in (None, "") and display_value(stored, -300) == "", f"{errors} {stored}")
    errors, stored = handle_submit({})
    record("absent_field_retained", not errors and stored.get("renewal_date") in (None, ""), f"{errors} {stored}")

    accepted = []
    for raw in ("2023-02-29", "2024-02-30", "2024-13-01", "2024-00-10", "2024-1-5", "2024-01-05T00:00",
                "2024-01-05T00:00:00Z", "20240105", " 2024-01-05", "2024-01-05 ", "2024-01-05\n", "05/01/2024",
                "tomorrow", "+2024-01-05", "2024-W01-5", "x" * 5000, ["2024-01-05"], 20240105):
        try:
            errors, stored = handle_submit({"renewal_date": raw})
        except Exception as exc:
            accepted.append(f"{str(raw)[:20]!r} raised {type(exc).__name__}")
            continue
        if "renewal_date" not in errors or stored.get("renewal_date"):
            accepted.append(repr(raw)[:24])
    record("server_rejects_invalid_even_if_client_bypassed", not accepted, accepted)
except Exception:
    record("probe_crashed", False, traceback.format_exc())
print(json.dumps(results))
'''


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
    if args.withheld and args.withheld.is_dir():
        withheld = args.withheld.resolve()
        ok, tail = run_unittests(workspace, withheld, withheld)
        checks.append({"id": "withheld_tests", "passed": ok, "detail": "" if ok else tail})
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
