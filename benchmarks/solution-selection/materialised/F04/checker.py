"""F04 checker: persistent per-user saved filters (stdlib only, no model call).

Runs the produced code in separate Python processes against adversarial input:
restart persistence, cross-user reads and deletes, malformed specs, deterministic duplicate
keys and an injected failure inside the create transaction.

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

FIXTURE = "F04"

PREAMBLE = r'''
import json, sys
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
from catalogue import db, users
from catalogue.query import QueryLayer
DB = sys.argv[1]
def open_q(path=DB):
    conn = db.connect(path)
    db.init_schema(conn)
    return QueryLayer(conn)
def raises(exc_name, fn):
    from catalogue import saved_filters as sf
    exc = getattr(sf, exc_name)
    try:
        fn()
    except exc:
        return True
    except Exception as other:
        return False
    return False
'''

EPILOGUE = r'''
print("RESULT:" + json.dumps(results))
'''

PHASE_WRITE = r'''
@check("persist_restart_write")
def _():
    from catalogue import saved_filters as sf
    q = open_q()
    uid = users.create_user(q, "restart@example.invalid")
    created = sf.create_filter(q, uid, "kept", {"category": "books", "min_price": 100})
    q._conn.close()
    with open(sys.argv[2], "w", encoding="utf-8") as handle:
        json.dump({"user": uid, "id": created["id"]}, handle)
    return True, "written"
'''

PHASE_READ = r'''
@check("persist_restart")
def _():
    from catalogue import saved_filters as sf
    saved = json.load(open(sys.argv[2], encoding="utf-8"))
    q = open_q()
    listed = sf.list_filters(q, saved["user"])
    ok = [(f["id"], f["name"], f["spec"]) for f in listed] == [(saved["id"], "kept", {"category": "books", "min_price": 100})]
    return ok, f"after restart list_filters returned {listed!r}"
'''

PHASE_MAIN = r'''
from catalogue import saved_filters as sf
q = open_q()
a = users.create_user(q, "a@example.invalid")
b = users.create_user(q, "b@example.invalid")

def count_rows(name=None):
    fresh = db.connect(DB)
    try:
        if name is None:
            return fresh.execute("SELECT COUNT(*) FROM saved_filters").fetchone()[0]
        return fresh.execute("SELECT COUNT(*) FROM saved_filters WHERE name = ?", (name,)).fetchone()[0]
    finally:
        fresh.close()

@check("table_in_database")
def _():
    sf.create_filter(q, a, "probe", {"text": "probe"})
    return count_rows("probe") == 1, "saved_filters table must hold the created row (read by a fresh connection)"

@check("list_isolated_per_user")
def _():
    sf.create_filter(q, a, "a-one", {"category": "lamps"})
    sf.create_filter(q, a, "a-two", {"max_price": 5000})
    sf.create_filter(q, b, "b-one", {"category": "rugs"})
    names_a = [f["name"] for f in sf.list_filters(q, a)]
    names_b = [f["name"] for f in sf.list_filters(q, b)]
    return names_a == ["probe", "a-one", "a-two"] and names_b == ["b-one"], f"a={names_a} b={names_b}"

@check("get_other_user_denied")
def _():
    target = [f for f in sf.list_filters(q, a) if f["name"] == "a-one"][0]
    return raises("FilterNotFound", lambda: sf.get_filter(q, b, target["id"])), "user b read user a's filter by id"

@check("delete_other_user_denied")
def _():
    target = [f for f in sf.list_filters(q, a) if f["name"] == "a-two"][0]
    denied = raises("FilterNotFound", lambda: sf.delete_filter(q, b, target["id"]))
    survived = count_rows("a-two") == 1
    return denied and survived, f"denied={denied} row_survived={survived}"

@check("guessed_ids_fail_closed")
def _():
    ok = all(raises("FilterNotFound", lambda i=i: sf.get_filter(q, b, i)) for i in (0, -1, 10**9))
    return ok, "absent ids must raise FilterNotFound"

@check("invalid_specs_rejected")
def _():
    bad_specs = [[], "category=books", {}, None, {"colour": "red"}, {"min_price": "10"}, {"min_price": True},
                 {"min_price": -1}, {"min_price": 10, "max_price": 5}, {"category": 5}, {"max_price": 1.5},
                 {"category": "books", "__proto__": "x"}]
    before = count_rows()
    failures = [repr(s) for s in bad_specs if not raises("InvalidFilter", lambda s=s: sf.create_filter(q, a, "bad", s))]
    for name in ("", "x" * 81, None):
        if not raises("InvalidFilter", lambda n=name: sf.create_filter(q, a, n, {"text": "ok"})):
            failures.append(f"name={name!r}")
    after = count_rows()
    return not failures and before == after, f"accepted: {failures}; rows {before}->{after}"

@check("duplicate_same_spec_returns_original")
def _():
    first = sf.create_filter(q, a, "dup", {"category": "books", "max_price": 900})
    second = sf.create_filter(q, a, "dup", {"max_price": 900, "category": "books"})
    return first["id"] == second["id"] and count_rows("dup") == 1, f"{first['id']} vs {second['id']}, rows={count_rows('dup')}"

@check("duplicate_different_spec_rejected")
def _():
    rejected = raises("DuplicateFilter", lambda: sf.create_filter(q, a, "dup", {"category": "toys"}))
    kept = [f for f in sf.list_filters(q, a) if f["name"] == "dup"]
    return rejected and len(kept) == 1 and kept[0]["spec"] == {"category": "books", "max_price": 900}, f"rejected={rejected} kept={kept}"

@check("same_name_other_user_independent")
def _():
    other = sf.create_filter(q, b, "dup", {"category": "toys"})
    return other["user_id"] == b and len([f for f in sf.list_filters(q, a) if f["name"] == "dup"]) == 1, "names are per user"

@check("rollback_leaves_no_partial_filter")
def _():
    original = QueryLayer.execute
    fired = []
    def failing(self, sql, params=()):
        cursor = original(self, sql, params)
        text = " ".join(sql.lower().split())
        if "insert" in text and "saved_filters" in text:
            fired.append(sql)
            raise RuntimeError("injected failure after the insert")
        return cursor
    QueryLayer.execute = failing
    try:
        try:
            sf.create_filter(q, a, "atomic", {"text": "lamp"})
        except RuntimeError:
            pass
    finally:
        QueryLayer.execute = original
    if not fired:
        return False, "create_filter did not write saved_filters through QueryLayer.execute"
    return count_rows("atomic") == 0, f"rows after injected failure: {count_rows('atomic')}"
'''


def run_probe(workspace: Path, body: str, *args: str, timeout: int = 60) -> dict:
    with tempfile.TemporaryDirectory(prefix="f04-probe-") as tmp:
        script = Path(tmp) / "probe.py"
        script.write_text(PREAMBLE + body + EPILOGUE, encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
        try:
            proc = subprocess.run([sys.executable, str(script), *args], cwd=workspace, env=env, capture_output=True, text=True, timeout=timeout)
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
    results: dict[str, list] = {}
    with tempfile.TemporaryDirectory(prefix="f04-db-") as tmp:
        restart_db = str(Path(tmp) / "restart.sqlite3")
        handoff = str(Path(tmp) / "handoff.json")
        write = run_probe(workspace, PHASE_WRITE, restart_db, handoff)
        if write.get("persist_restart_write", [False])[0]:
            results.update(run_probe(workspace, PHASE_READ, restart_db, handoff))
        else:
            results["persist_restart"] = [False, f"write phase failed: {write}"]
        results.update(run_probe(workspace, PHASE_MAIN, str(Path(tmp) / "main.sqlite3")))
    if args.withheld:
        results["withheld_tests"] = list(run_withheld(workspace, args.withheld))
    checks = [{"id": cid, "passed": bool(value[0]), "detail": value[1]} for cid, value in results.items()]
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
