from __future__ import annotations
import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PY = sys.executable
RESULTS = []

def run(args, expected=0):
    result = subprocess.run([PY, *map(str, args)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != expected:
        raise AssertionError(f"exit {result.returncode}, expected {expected}: {' '.join(map(str,args))}\n{result.stdout}\n{result.stderr}")
    RESULTS.append(f"exit={result.returncode} {' '.join(map(str,args))}\n{result.stdout.strip()}" + (f"\nstderr: {result.stderr.strip()}" if result.stderr else ""))
    return result

def fresh_db(path: Path):
    with sqlite3.connect(path) as db:
        db.executescript((ROOT / "skills/sdlc-meta/ai-assisted-development/examples/e05-k3/legacy_fixture.sql").read_text(encoding="utf-8"))
    db.close()

def cli(db, event, status, *extra, expected=0):
    return run(["skills/sdlc-meta/ai-assisted-development/examples/e05-k3/cli.py", "--db", db, "--event", event, "--ticket", "T1", "--status", status, *extra], expected)

with tempfile.TemporaryDirectory(prefix="chwezi-readme-") as temp:
    out = Path(temp)
    model = out / "ticket-triage-model.json"
    run(["skills/languages/python-ml-predictive/examples/ticket-triage/train.py", "--model", model])
    run(["skills/languages/python-ml-predictive/examples/ticket-triage/score.py", "--model", model])
    run(["-B", "skills/ai/ai-rag-patterns/examples/curated-retrieval/evaluate.py"])
    run(["-B", "skills/ai/ai-rag-patterns/examples/curated-retrieval/evaluate.py", "--drop-negation"])
    run(["-B", "skills/ai/ai-evaluation/examples/adaptation-review/review.py"])
    run(["-B", "skills/languages/python-ml-predictive/examples/release-diagnostics/diagnose.py"])

    ex = ROOT / "skills/sdlc-meta/ai-assisted-development/examples/e05-k3"
    fixed = out / "fixed.sqlite"; fresh_db(fixed)
    cli(fixed, "E7", "review"); cli(fixed, "E7", "review"); cli(fixed, "E8", "closed")
    with sqlite3.connect(fixed) as db:
        history = db.execute("select source_event_id, count(*) from history group by source_event_id order by source_event_id").fetchall()
        events = db.execute("select event_id,ticket_id,status from delivered_events order by event_id").fetchall()
        status = db.execute("select status from tickets where ticket_id='T1'").fetchone()[0]
    db.close()
    assert history == [(None, 1), ("E7", 1), ("E8", 1)] and len(events) == 2 and status == "closed", (history, events, status)
    RESULTS.append(f"fixed persisted state: history={history}; events={events}; ticket_status={status}")
    cli(fixed, "E7", "closed", expected=3)
    with sqlite3.connect(fixed) as db:
        after = (db.execute("select count(*) from history").fetchone()[0], db.execute("select status from tickets where ticket_id='T1'").fetchone()[0])
    db.close()
    assert after == (3, "closed"), after
    RESULTS.append(f"conflict no-effects state: history_count={after[0]}; ticket_status={after[1]}")

    rollback = out / "rollback.sqlite"; fresh_db(rollback)
    cli(rollback, "E7", "review", "--fail-before-history", expected=4)
    with sqlite3.connect(rollback) as db:
        state = (db.execute("select count(*) from delivered_events").fetchone()[0], db.execute("select count(*) from history").fetchone()[0], db.execute("select status from tickets where ticket_id='T1'").fetchone()[0])
    db.close()
    assert state == (0, 1, "open"), state
    RESULTS.append(f"injected failure rollback: delivered_events={state[0]}; history={state[1]}; ticket_status={state[2]}")
    cli(rollback, "E7", "review")
    with sqlite3.connect(rollback) as db:
        state = (db.execute("select count(*) from delivered_events where event_id='E7'").fetchone()[0], db.execute("select count(*) from history where source_event_id='E7'").fetchone()[0])
    db.close()
    assert state == (1, 1), state
    RESULTS.append(f"retry after rollback: E7_event={state[0]}; E7_history={state[1]}")

    baseline = out / "baseline.sqlite"; fresh_db(baseline)
    cli(baseline, "E7", "review", "--implementation", "baseline"); cli(baseline, "E7", "review", "--implementation", "baseline")
    with sqlite3.connect(baseline) as db:
        count = db.execute("select count(*) from history where source_event_id='E7'").fetchone()[0]
    db.close()
    assert count == 2, count
    RESULTS.append(f"baseline negative control: duplicate E7 history rows={count}")

    wrong = out / "wrong.sqlite"; fresh_db(wrong)
    cli(wrong, "E7", "review", "--implementation", "ticket-level-dedupe"); cli(wrong, "E8", "closed", "--implementation", "ticket-level-dedupe")
    with sqlite3.connect(wrong) as db:
        state = (db.execute("select count(*) from history").fetchone()[0], db.execute("select status from tickets where ticket_id='T1'").fetchone()[0])
    db.close()
    assert state == (1, "open"), state
    RESULTS.append(f"ticket-level-dedupe negative control: history_rows={state[0]}; ticket_status={state[1]}")

print("PASS: README example command walkthrough and E05 black-box paths")
for item in RESULTS:
    print("---")
    print(item)
