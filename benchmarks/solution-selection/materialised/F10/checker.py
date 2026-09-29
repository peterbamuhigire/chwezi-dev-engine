"""F10 checker: staged customer foreign-key migration on SQLite (stdlib only, no model call).

Builds its own synthetic data set (duplicates by case/space, unknown codes, blanks, NULLs),
then drives expand / backfill / verify / contract / rollback in a separate process: lineage,
exception path, v1 coexistence, interrupted-backfill resumption (SQLite progress-handler
abort, reconnect, re-run), idempotency and source preservation on rollback.
The PostgreSQL integration leg is NOT_ASSESSED (see fixture.json) and is not claimed here.

    python checker.py <workspace> [--withheld <dir>]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE = "F10"

PROBE = r'''
import hashlib, json, sqlite3, sys
from collections import Counter
from pathlib import Path
results = {}
def check(cid):
    def deco(fn):
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        results[cid] = [bool(ok), str(detail)[:300]]
        return fn
    return deco

from shop import app_v1, schema
from migrations import m002_customer_fk as m

WORK = Path(sys.argv[1])
CUSTOMERS = [(1, "ACME", "Acme"), (2, "BETA", "Beta"), (3, "acme ", "Acme duplicate"), (4, "GAMMA", "Gamma"),
             (5, "Delta", "Delta"), (6, "EPSILON", "Epsilon")]
CODES = ["BETA", " beta", "ACME", "ZETA", None, "GAMMA", "", "delta", "  DELTA  ", "Epsilon", "epsilon ", "OMEGA", "acme"]
ORDERS = [(i, CODES[i % len(CODES)], 100 + (i * 37) % 9000) for i in range(1, 181)]

def norm(code):
    return (code or "").strip().upper()
counts = Counter(norm(c) for _, c, _ in CUSTOMERS)
UNIQUE = {norm(c): cid for cid, c, _ in CUSTOMERS if counts[norm(c)] == 1}
EXPECTED_MAP = {oid: UNIQUE.get(norm(code)) if norm(code) else None for oid, code, _ in ORDERS}
EXPECTED_EXC = {oid: ("ambiguous" if norm(code) and counts[norm(code)] > 1 else "unmapped") for oid, code, _ in ORDERS if EXPECTED_MAP[oid] is None}

counter = [0]
def fresh(name, customers=CUSTOMERS, orders=ORDERS):
    path = WORK / f"{name}.sqlite3"
    conn = schema.connect(path)
    schema.create_legacy_schema(conn)
    conn.executemany("INSERT INTO customers (id, code, name) VALUES (?, ?, ?)", customers)
    conn.executemany("INSERT INTO orders (id, legacy_customer_code, amount_minor) VALUES (?, ?, ?)", orders)
    return conn, path

def source(conn):
    return (conn.execute("SELECT id, legacy_customer_code, amount_minor FROM orders ORDER BY id").fetchall(),
            conn.execute("SELECT id, code, name FROM customers ORDER BY id").fetchall())

def mapping(conn):
    return dict(conn.execute("SELECT id, customer_id FROM orders ORDER BY id").fetchall())

def exceptions(conn):
    return dict(conn.execute("SELECT order_id, reason FROM customer_fk_exceptions ORDER BY order_id").fetchall())

def checksum(orders):
    digest = hashlib.sha256()
    for oid, code, _ in sorted(orders):
        digest.update(f"{oid}:{code or ''}\n".encode("utf-8"))
    return digest.hexdigest()

@check("expand_idempotent_and_v1_compatible")
def _():
    conn, _ = fresh("expand")
    before = app_v1.list_orders(conn)
    m.expand(conn)
    m.expand(conn)
    new_id = app_v1.create_order(conn, "BETA", 4200)
    after = app_v1.list_orders(conn)
    ok = after[:-1] == before and after[-1] == (new_id, "BETA", 4200) and app_v1.customer_total(conn, "GAMMA") == sum(a for _, c, a in ORDERS if c == "GAMMA")
    return ok, "v1 reads and writes after a repeated expand"

@check("backfill_lineage_preserved")
def _():
    conn, _ = fresh("lineage")
    src = source(conn)
    m.expand(conn)
    m.backfill(conn, batch_size=7)
    got = mapping(conn)
    wrong = [oid for oid, want in EXPECTED_MAP.items() if got.get(oid) != want]
    return not wrong and source(conn) == src, f"wrong mappings for orders {wrong[:8]}; source unchanged={source(conn) == src}"

@check("no_order_deleted")
def _():
    conn, _ = fresh("nodelete")
    m.expand(conn)
    m.backfill(conn)
    ids = [row[0] for row in conn.execute("SELECT id FROM orders ORDER BY id")]
    return ids == [o[0] for o in ORDERS], f"{len(ids)} of {len(ORDERS)} orders remain"

@check("unmapped_and_ambiguous_enter_exception_path")
def _():
    conn, _ = fresh("exceptions")
    m.expand(conn)
    m.backfill(conn, batch_size=11)
    got = exceptions(conn)
    return got == EXPECTED_EXC, f"{len(got)} exception rows, expected {len(EXPECTED_EXC)}; sample {list(got.items())[:4]}"

@check("verify_reports_reconciliation")
def _():
    conn, _ = fresh("verify")
    m.expand(conn)
    m.backfill(conn)
    v = m.verify(conn)
    want = {"total": len(ORDERS), "mapped": sum(1 for x in EXPECTED_MAP.values() if x is not None),
            "unmapped": sum(1 for r in EXPECTED_EXC.values() if r == "unmapped"),
            "ambiguous": sum(1 for r in EXPECTED_EXC.values() if r == "ambiguous"), "pending": 0, "legacy_checksum": checksum(ORDERS)}
    got = {k: v.get(k) for k in want}
    return got == want, f"verify={got} expected={want}"

@check("contract_blocked_while_unresolved")
def _():
    conn, _ = fresh("blocked")
    m.expand(conn)
    m.backfill(conn)
    try:
        m.contract(conn)
    except m.MigrationBlocked:
        pass
    else:
        return False, "contract succeeded with unresolved exceptions"
    app_v1.create_order(conn, None, 10)
    return True, "blocked, and v1 can still insert"

@check("contract_after_resolution_requires_customer")
def _():
    customers = [(1, "ACME", "Acme"), (2, "BETA", "Beta"), (3, "acme ", "Acme duplicate")]
    orders = [(1, "BETA", 10), (2, "ACME", 20), (3, "ZETA", 30)]
    conn, _ = fresh("resolve", customers, orders)
    m.expand(conn)
    m.backfill(conn)
    conn.execute("UPDATE customers SET code = 'ACME-OLD' WHERE id = 3")
    conn.execute("INSERT INTO customers (id, code, name) VALUES (9, 'ZETA', 'Zeta')")
    m.backfill(conn)
    v = m.verify(conn)
    if (v.get("unmapped"), v.get("ambiguous"), v.get("pending"), v.get("mapped")) != (0, 0, 0, 3):
        return False, f"after fixing data verify={v}"
    m.contract(conn)
    try:
        conn.execute("INSERT INTO orders (legacy_customer_code, amount_minor) VALUES ('BETA', 5)")
    except sqlite3.DatabaseError:
        return mapping(conn) == {1: 2, 2: 1, 3: 9}, f"mapping={mapping(conn)}"
    return False, "an order without customer_id was accepted after contract"

@check("interrupted_backfill_resumes")
def _():
    reference_conn, _ = fresh("reference")
    m.expand(reference_conn)
    m.backfill(reference_conn, batch_size=13)
    want_map, want_exc = mapping(reference_conn), exceptions(reference_conn)
    failures = []
    interrupted = 0
    for limit in (5, 40, 150, 400, 1200):
        conn, path = fresh(f"interrupt{limit}")
        m.expand(conn)
        calls = [0]
        def handler():
            calls[0] += 1
            return 1 if calls[0] > limit else 0
        conn.set_progress_handler(handler, 20)
        try:
            m.backfill(conn, batch_size=13)
        except sqlite3.Error:
            interrupted += 1
        conn.close()
        conn = schema.connect(path)
        m.backfill(conn, batch_size=13)
        if mapping(conn) != want_map or exceptions(conn) != want_exc or conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] != len(ORDERS):
            failures.append(limit)
    return not failures and interrupted >= 3, f"interrupted {interrupted} runs; divergent after resume at limits {failures}"

@check("backfill_idempotent")
def _():
    conn, _ = fresh("twice")
    m.expand(conn)
    m.backfill(conn)
    first = (mapping(conn), exceptions(conn), source(conn))
    m.backfill(conn)
    m.backfill(conn, batch_size=1)
    return (mapping(conn), exceptions(conn), source(conn)) == first, "state after repeated backfills"

@check("rollback_preserves_source")
def _():
    conn, _ = fresh("rollback", CUSTOMERS, [o for o in ORDERS if EXPECTED_MAP[o[0]] is not None][:40])
    src = source(conn)
    m.expand(conn)
    m.backfill(conn)
    m.contract(conn)
    m.rollback(conn)
    after_contract_rollback = source(conn) == src
    app_v1.create_order(conn, None, 77)
    conn2, _ = fresh("rollback2")
    src2 = source(conn2)
    m.expand(conn2)
    m.backfill(conn2, batch_size=9)
    m.rollback(conn2)
    ok2 = source(conn2) == src2
    leftover = [r for r in conn2.execute("PRAGMA table_info(orders)") if r[1] == "customer_id"]
    emptied = not leftover or conn2.execute("SELECT COUNT(*) FROM orders WHERE customer_id IS NOT NULL").fetchone()[0] == 0
    return after_contract_rollback and ok2 and emptied, f"after contract+rollback={after_contract_rollback} after backfill+rollback={ok2} customer_id emptied={emptied}"

print("RESULT:" + json.dumps(results))
'''


def run_probe(workspace: Path, timeout: int = 180) -> dict:
    with tempfile.TemporaryDirectory(prefix="f10-probe-") as tmp:
        script = Path(tmp) / "probe.py"
        script.write_text(PROBE, encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
        try:
            proc = subprocess.run([sys.executable, str(script), tmp], cwd=workspace, env=env, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"probe_timeout": [False, f"probe exceeded {timeout}s"]}
    for line in reversed(proc.stdout.splitlines()):
        if line.startswith("RESULT:"):
            return json.loads(line[len("RESULT:"):])
    return {"probe_crashed": [False, (proc.stderr or proc.stdout)[-400:]]}


def run_withheld(workspace: Path, withheld: Path) -> tuple[bool, str]:
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(withheld), "-t", str(withheld), "-p", "test_*.py"],
                              cwd=workspace, env=env, capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        return False, "withheld tests timed out"
    return proc.returncode == 0, proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "no output"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    results = run_probe(workspace)
    if args.withheld:
        results["withheld_tests"] = list(run_withheld(workspace, args.withheld))
    checks = [{"id": cid, "passed": bool(value[0]), "detail": value[1]} for cid, value in results.items()]
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks,
                      "not_assessed": ["PostgreSQL integration leg (no pinned image)"]}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
