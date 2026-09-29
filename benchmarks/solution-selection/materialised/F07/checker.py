"""F07 API boundary validation - deterministic checker (stdlib only, no model call).

Runs the produced service code in a subprocess against adversarial payloads on BOTH untrusted
entry points (HTTP handler and queue consumer): malformed and oversized bodies, boolean-as-integer,
null, unknown and nested unknown fields, type-confused nested values, out-of-range quantities,
path traversal in the order identifier, and a payload that would leave a partial write.

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

FIXTURE = "F07"

PROBE = r'''
import json, tempfile, traceback
from pathlib import Path
from service.http_api import handle_create
from service.queue_consumer import consume
from service.store import Store

results = {}
def record(cid, passed, detail=""):
    results[cid] = [bool(passed), str(detail)[:300]]

VALID = {"id": "ord-1", "customer": "Kato Traders", "items": [{"sku": "AB12", "qty": 3}]}

def fresh():
    tmp = tempfile.mkdtemp()
    root = Path(tmp) / "a" / "store"
    return Path(tmp), Store(root)

def stray_files(base):
    orders = base / "a" / "store" / "orders"
    return [p for p in base.rglob("*") if p.is_file() and orders not in p.parents]

def http(body):
    base, store = fresh()
    try:
        status, payload = handle_create(body, store)
    except Exception as exc:
        return base, store, None, {"exception": repr(exc)}
    return base, store, status, payload

def code_of(payload):
    try:
        return payload["error"]["code"]
    except Exception:
        return None

def expect_http(cid, body, status, code):
    base, store, got, payload = http(body)
    written = store.count() if got is not None else len(list((base / "a" / "store" / "orders").glob("*")))
    stray = stray_files(base)
    ok = got == status and code_of(payload) == code and written == 0 and not stray
    record(cid, ok, f"status={got} code={code_of(payload)} written={written} stray={[str(p.name) for p in stray]} payload={payload}")

def with_(**changes):
    order = json.loads(json.dumps(VALID))
    order.update(changes)
    return order

def enc(value):
    return json.dumps(value).encode()

try:
    base, store, status, payload = http(enc(VALID))
    record("http_valid_created", status == 201 and store.count() == 1, f"status={status}")
    expect_http("http_malformed_json", b'{"id": "ord-1", "customer":', 400, "malformed_json")
    big = with_(note="x" * 20000)
    expect_http("http_oversize_body", enc(big), 413, "body_too_large")
    expect_http("http_bool_as_int", enc(with_(items=[{"sku": "AB12", "qty": True}])), 422, "validation_failed")
    expect_http("http_null_customer", enc(with_(customer=None)), 422, "validation_failed")
    expect_http("http_unknown_field", enc(with_(is_admin=True)), 422, "validation_failed")
    expect_http("http_nested_unknown_field", enc(with_(items=[{"sku": "AB12", "qty": 1, "price_override": 0}])), 422, "validation_failed")
    expect_http("http_nested_type_confusion", enc(with_(items=[{"sku": {"$ne": ""}, "qty": 1}])), 422, "validation_failed")
    expect_http("http_qty_out_of_range", enc(with_(items=[{"sku": "AB12", "qty": 1000}])), 422, "validation_failed")
    expect_http("http_float_qty", enc(with_(items=[{"sku": "AB12", "qty": 1.5}])), 422, "validation_failed")
    expect_http("http_path_traversal_id", enc(with_(id="../../escaped")), 422, "validation_failed")
    expect_http("http_no_partial_write", enc(with_(items=[{"sku": "AB12", "qty": 1}, {"qty": 2}])), 422, "validation_failed")
    expect_http("http_top_level_array", enc([VALID]), 422, "validation_failed")

    queue_cases = {
        "bool_as_int": with_(items=[{"sku": "AB12", "qty": True}]),
        "null_customer": with_(customer=None),
        "unknown_field": with_(is_admin=True),
        "nested_unknown": with_(items=[{"sku": "AB12", "qty": 1, "price_override": 0}]),
        "traversal_id": with_(id="..\\..\\escaped"),
    }
    failures = []
    for name, message in queue_cases.items():
        base, store = fresh()
        try:
            out = consume(message, store)
        except Exception as exc:
            failures.append(f"{name}: exception {exc!r}")
            continue
        if not (isinstance(out, dict) and out.get("status") == "rejected" and code_of(out) == "validation_failed" and store.count() == 0 and not stray_files(base)):
            failures.append(f"{name}: {out}")
    record("queue_applies_same_contract", not failures, "; ".join(failures))
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
