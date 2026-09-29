"""F01 checker: existing-code reuse (stdlib only, no model call).

Runs the produced report against adversarial Unicode vectors in a subprocess and checks that the
shared identifier contract is reused rather than re-implemented.

    python checker.py <workspace> [--withheld <dir>]

Exit 0 PASS, 1 FAIL, 2 NOT_ASSESSED. Prints one JSON object.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE = "F01"
HERE = Path(__file__).resolve().parent
CALLER_FILES = ("core/identifiers.py", "billing/invoices.py", "crm/lookup.py")

DRIVER = r'''
import json
results = []

def check(cid):
    def wrap(fn):
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        results.append({"id": cid, "passed": bool(ok), "detail": str(detail)[:400]})
        return fn
    return wrap

from reports.customer_report import build_report

def report_id(raw):
    return build_report([{"customer_id": raw, "name": "Synthetic", "balance_minor": 1}])[0].split("\t")[0]

VECTORS = [
    ("straße 7", "STRAßE-7"),
    ("café 9", "CAFé-9"),
    ("ﬁle-1", "ﬁLE-1"),
    ("①-kla", "①-KLA"),
    ("  ab　cd\t", "AB-CD"),
]

@check("unicode_vectors_match_contract")
def _():
    bad = [(raw, report_id(raw), want) for raw, want in VECTORS if report_id(raw) != want]
    return not bad, (f"mismatches: {bad!r}" if bad else "all vectors canonical")

@check("distinct_ids_not_collapsed")
def _():
    pairs = [("ﬁle-1", "file-1"), ("straße", "strasse"), ("①", "1")]
    collapsed = [p for p in pairs if report_id(p[0]) == report_id(p[1])]
    return not collapsed, (f"collapsed: {collapsed!r}" if collapsed else "distinct IDs stay distinct")

@check("empty_identifier_error_contract")
def _():
    for raw in ("", "   ", " 　"):
        try:
            got = build_report([{"customer_id": raw, "name": "x", "balance_minor": 0}])
        except ValueError as exc:
            if type(exc).__name__ != "EmptyIdentifierError":
                return False, f"{raw!r} raised {type(exc).__name__}; the contract is EmptyIdentifierError"
            continue
        return False, f"{raw!r} produced {got!r} instead of EmptyIdentifierError"
    return True, "empty identifiers raise EmptyIdentifierError"

@check("report_matches_directory_keys")
def _():
    from crm.lookup import CustomerDirectory
    directory = CustomerDirectory()
    key = directory.add("café  9", "Synthetic")
    got = report_id("café 9")
    return got == key, f"report {got!r} vs directory key {key!r}"

print("@@RESULTS@@" + json.dumps(results))
'''


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def run(cmd, cwd, timeout=60):
    env = dict(os.environ, PYTHONPATH=str(cwd), PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return None, "", f"timed out after {timeout}s"


def driver_checks(ws: Path) -> list[dict]:
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "driver.py"
        script.write_text(DRIVER, encoding="utf-8")
        rc, out, err = run([sys.executable, str(script)], ws)
    if "@@RESULTS@@" not in out:
        return [{"id": "driver", "passed": False, "detail": (err or out)[-600:] or f"exit {rc}"}]
    return json.loads(out.split("@@RESULTS@@", 1)[1].strip())


def static_checks(ws: Path) -> list[dict]:
    checks = []
    changed = [rel for rel in CALLER_FILES if not (ws / rel).is_file() or _sha(ws / rel) != _sha(HERE / "starter" / rel)]
    checks.append({"id": "existing_callers_unchanged", "passed": not changed,
                   "detail": f"changed: {changed}" if changed else "contract and callers byte-identical"})
    report = ws / "reports" / "customer_report.py"
    try:
        tree = ast.parse(report.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        checks.append({"id": "no_parallel_normaliser", "passed": False, "detail": str(exc)})
        return checks
    imports_contract = any(
        (isinstance(n, ast.ImportFrom) and n.module == "core.identifiers" and any(a.name == "canonical_id" for a in n.names))
        or (isinstance(n, ast.Import) and any(a.name == "core.identifiers" for a in n.names))
        for n in ast.walk(tree))
    local = sorted({n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr in {"upper", "lower", "casefold", "normalize", "split", "strip", "translate"}})
    checks.append({"id": "no_parallel_normaliser", "passed": imports_contract and not local,
                   "detail": f"imports canonical_id={imports_contract}; local normalising calls={local}"})
    return checks


def public_tests(ws: Path) -> dict:
    rc, out, err = run([sys.executable, "-m", "unittest", "discover", "-s", "public_tests", "-t", "."], ws, 120)
    return {"id": "public_tests", "passed": rc == 0, "detail": (err or out)[-400:]}


def withheld_tests(ws: Path, withheld: Path) -> dict:
    dest = ws / "_withheld_tests"
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(withheld, dest, ignore=shutil.ignore_patterns(".gitignore", "__pycache__"))
    try:
        rc, out, err = run([sys.executable, "-m", "unittest", "discover", "-s", "_withheld_tests", "-t", "."], ws, 180)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    return {"id": "withheld_tests", "passed": rc == 0, "detail": (err or out)[-400:]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    ws = args.workspace.resolve()
    checks = [public_tests(ws), *driver_checks(ws), *static_checks(ws)]
    if args.withheld and args.withheld.is_dir():
        checks.append(withheld_tests(ws, args.withheld))
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
