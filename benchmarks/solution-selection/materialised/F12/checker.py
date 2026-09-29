"""F12 checker: money workflow, synthetic receipt (stdlib only, no model call).

Drives the produced receipt handler against a fresh SQLite ledger per check, with adversarial
callbacks: tampered signatures, idempotency-key reuse with a different payload, rounding at the
half-minor-unit boundary in USD (2 decimals) and UGX (0 decimals), injected failure between
header, lines and audit, closed period, unauthorised actor, absent evidence, reversal and edits
to posted journals. The ERP "never simplify away" list (idempotency, audit trail, balanced
journal, period lock, reversal-not-delete) is the negative oracle.

    python checker.py <workspace> [--withheld <dir>]

Exit 0 PASS, 1 FAIL, 2 NOT_ASSESSED. Prints one JSON object.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE = "F12"

DRIVER = r'''
import hashlib, hmac, json, os, sqlite3, sys, tempfile
results = []
TMP = tempfile.mkdtemp(prefix="f12-")

def check(cid):
    def wrap(fn):
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        results.append({"id": cid, "passed": bool(ok), "detail": str(detail)[:400]})
        return fn
    return wrap

from ledger import db
from receipts import handler

SECRET = b"synthetic-shared-secret-K"
_n = [0]

def fresh():
    _n[0] += 1
    conn = db.connect(os.path.join(TMP, f"ledger-{_n[0]}.sqlite"))
    db.init_schema(conn)
    db.seed_fixture(conn)
    return conn

def body(**over):
    p = {"idempotency_key": "rcpt-0001", "entity": "K", "book": "MAIN", "value_date": "2026-09-15",
         "currency": "USD", "amount": "125.50", "receivable_ref": "AR-1001",
         "evidence_ref": "bank-line-5531", "version": 1}
    p.update(over)
    return json.dumps(p, sort_keys=True).encode("utf-8")

def sign(raw):
    return hmac.new(SECRET, raw, hashlib.sha256).hexdigest()

def post(conn, raw, actor="cashier-1", signature=None):
    return handler.process_receipt(conn, raw, sign(raw) if signature is None else signature, secret=SECRET, actor=actor)

def count(conn, table, where="1=1", args=()):
    return conn.execute(f"SELECT COUNT(*) FROM {table} WHERE {where}", args).fetchone()[0]

def rejected(fn):
    try:
        fn()
    except Exception as exc:
        return True, type(exc).__name__
    return False, "accepted"

def lines(conn, jid):
    return conn.execute("SELECT account, debit_minor, credit_minor FROM journal_lines WHERE journal_id = ? ORDER BY line_no", (jid,)).fetchall()

@check("balanced_and_clears_receivable")
def _():
    conn = fresh()
    jid = post(conn, body())
    got = lines(conn, jid)
    dr = sum(l[1] for l in got); cr = sum(l[2] for l in got)
    revenue = [l for l in got if l[0] == "4000"]
    ok = dr == cr == 12550 and ("1000", 12550, 0) in got and ("1100", 0, 12550) in got and not revenue
    return ok, f"lines={got}"

@check("same_key_same_payload_returns_original")
def _():
    conn = fresh()
    raw = body()
    a = post(conn, raw); b = post(conn, raw)
    return a == b and count(conn, "journals") == 1 and count(conn, "journal_lines") == 2, f"ids {a},{b}; journals={count(conn, 'journals')}"

@check("same_key_different_payload_rejected_and_audited")
def _():
    conn = fresh()
    jid = post(conn, body())
    ok_reject, how = rejected(lambda: post(conn, body(amount="999.00")))
    audit = conn.execute("SELECT event FROM audit WHERE event LIKE '%conflict%' OR event LIKE '%idempot%'").fetchall()
    amount = conn.execute("SELECT SUM(debit_minor) FROM journal_lines").fetchone()[0]
    ok = ok_reject and bool(audit) and count(conn, "journals") == 1 and amount == 12550
    return ok, f"rejected={ok_reject} ({how}); audit={audit}; journals={count(conn, 'journals')}; debit total={amount}"

@check("signature_verified_over_raw_body")
def _():
    conn = fresh()
    raw = body()
    tampered = raw.replace(b"125.50", b"925.50")
    r1 = rejected(lambda: post(conn, tampered, signature=sign(raw)))[0]
    r2 = rejected(lambda: post(conn, raw, signature="0" * 64))[0]
    r3 = rejected(lambda: post(conn, raw, signature=""))[0]
    return r1 and r2 and r3 and count(conn, "journals") == 0, f"tampered={r1} zero-sig={r2} empty-sig={r3} journals={count(conn, 'journals')}"

@check("rounding_half_even_usd_ugx")
def _():
    conn = fresh()
    cases = [("USD", "2.675", 268), ("USD", "1.015", 102), ("USD", "10.005", 1000), ("USD", "10.015", 1002),
             ("UGX", "1500.5", 1500), ("UGX", "1501.5", 1502), ("UGX", "250000", 250000)]
    wrong = []
    for i, (cur, amount, want) in enumerate(cases):
        jid = post(conn, body(idempotency_key=f"round-{i}", currency=cur, amount=amount))
        got = conn.execute("SELECT debit_minor FROM journal_lines WHERE journal_id = ? AND account = '1000'", (jid,)).fetchone()[0]
        if got != want:
            wrong.append((cur, amount, got, want))
    return not wrong, f"wrong={wrong}" if wrong else "house rule ROUND_HALF_EVEN applied"

@check("failure_between_writes_rolls_back_all")
def _():
    conn = fresh()
    conn.execute("CREATE TEMP TRIGGER inject_fault BEFORE INSERT ON audit BEGIN SELECT RAISE(ABORT, 'injected fault'); END")
    raised = rejected(lambda: post(conn, body()))[0]
    conn.execute("DROP TRIGGER inject_fault")
    j, l = count(conn, "journals"), count(conn, "journal_lines")
    return raised and j == 0 and l == 0, f"raised={raised}; journals={j}; lines={l}"

@check("closed_period_rejected")
def _():
    conn = fresh()
    r = rejected(lambda: post(conn, body(value_date="2026-08-20")))
    return r[0] and count(conn, "journals") == 0, f"{r}; journals={count(conn, 'journals')}"

@check("unauthorised_actor_rejected")
def _():
    conn = fresh()
    r1 = rejected(lambda: post(conn, body(), actor="visitor-3"))
    r2 = rejected(lambda: post(conn, body(idempotency_key="k2"), actor="unknown-actor"))
    return r1[0] and r2[0] and count(conn, "journals") == 0, f"{r1} {r2}"

@check("absent_evidence_rejected")
def _():
    conn = fresh()
    r = rejected(lambda: post(conn, body(evidence_ref="")))
    return r[0] and count(conn, "journals") == 0, f"{r}; journals={count(conn, 'journals')}"

@check("invalid_amount_rejected_without_write")
def _():
    conn = fresh()
    outcomes = [rejected(lambda a=a, i=i: post(conn, body(idempotency_key=f"bad-{i}", amount=a)))[0]
                for i, a in enumerate(("-5.00", "0.00", "abc", "NaN", "1e400"))]
    j, l = count(conn, "journals"), count(conn, "journal_lines")
    return all(outcomes) and j == 0 and l == 0, f"rejected={outcomes}; journals={j}; lines={l}"

@check("lineage_retained")
def _():
    conn = fresh()
    jid = post(conn, body())
    row = conn.execute("SELECT actor, source, request_key, version, evidence_ref, payload_hash FROM journals WHERE id = ?", (jid,)).fetchone()
    audit = count(conn, "audit", "journal_id = ?", (jid,))
    ok = row[0] == "cashier-1" and bool(row[1]) and row[2] == "rcpt-0001" and row[3] == 1 and row[4] == "bank-line-5531" and bool(row[5]) and audit >= 1
    return ok, f"row={row}; audit rows={audit}"

@check("correction_is_linked_reversal")
def _():
    conn = fresh()
    jid = post(conn, body())
    audit_before = count(conn, "audit", "journal_id = ?", (jid,))
    rid = handler.reverse_receipt(conn, jid, actor="controller-1", reason="posted to wrong customer", evidence_ref="memo-77")
    orig_exists = count(conn, "journals", "id = ?", (jid,)) == 1 and len(lines(conn, jid)) == 2
    link = conn.execute("SELECT reversal_of FROM journals WHERE id = ?", (rid,)).fetchone()
    net = conn.execute("SELECT SUM(credit_minor - debit_minor) FROM journal_lines WHERE account = '1100'").fetchone()[0]
    audit_after = count(conn, "audit", "journal_id = ?", (jid,))
    twice = rejected(lambda: handler.reverse_receipt(conn, jid, actor="controller-1", reason="again", evidence_ref="memo-78"))[0]
    ok = rid != jid and orig_exists and link is not None and link[0] == jid and net == 0 and audit_after >= audit_before and twice
    return ok, f"reversal={rid} original kept={orig_exists} link={link} net AR={net} audit {audit_before}->{audit_after} second reversal rejected={twice}"

@check("posted_journal_immutable")
def _():
    conn = fresh()
    jid = post(conn, body())
    attempts = {
        "update_journal": lambda: conn.execute("UPDATE journals SET actor = 'someone' WHERE id = ?", (jid,)),
        "delete_journal": lambda: conn.execute("DELETE FROM journals WHERE id = ?", (jid,)),
        "update_line": lambda: conn.execute("UPDATE journal_lines SET debit_minor = 1 WHERE journal_id = ?", (jid,)),
        "delete_lines": lambda: conn.execute("DELETE FROM journal_lines WHERE journal_id = ?", (jid,)),
    }
    allowed = []
    for name, fn in attempts.items():
        if not rejected(fn)[0]:
            allowed.append(name)
    return not allowed, f"edits allowed: {allowed}" if allowed else "posted journals and lines refuse edits"

import gc, shutil
gc.collect()
shutil.rmtree(TMP, ignore_errors=True)
print("@@RESULTS@@" + json.dumps(results))
'''


def run(cmd, cwd, timeout=120):
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


def public_tests(ws: Path) -> dict:
    rc, out, err = run([sys.executable, "-m", "unittest", "discover", "-s", "public_tests", "-t", "."], ws)
    return {"id": "public_tests", "passed": rc == 0, "detail": (err or out)[-400:]}


def withheld_tests(ws: Path, withheld: Path) -> dict:
    dest = ws / "_withheld_tests"
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(withheld, dest, ignore=shutil.ignore_patterns(".gitignore", "__pycache__"))
    try:
        rc, out, err = run([sys.executable, "-m", "unittest", "discover", "-s", "_withheld_tests", "-t", "."], ws, 240)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    return {"id": "withheld_tests", "passed": rc == 0, "detail": (err or out)[-400:]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    ws = args.workspace.resolve()
    checks = [public_tests(ws), *driver_checks(ws)]
    if args.withheld and args.withheld.is_dir():
        checks.append(withheld_tests(ws, args.withheld))
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
