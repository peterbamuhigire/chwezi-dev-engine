"""F05 checker: half-open window bug across components (stdlib only, no model call).

Exercises the shared helper and every advertised caller (API, worker, export) with boundary,
empty, reversed and mixed naive/aware inputs in a separate process.

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

FIXTURE = "F05"

PROBE = r'''
import json
from datetime import datetime, timedelta, timezone
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

def raises(fn):
    try:
        fn()
    except (TypeError, ValueError):
        return True
    return False

T = lambda h, m=0, s=0, us=0: datetime(2026, 9, 29, h, m, s, us)
UTC = timezone.utc
EAT = timezone(timedelta(hours=3))

@check("helper_upper_excluded")
def _():
    from core.time_windows import in_window
    return in_window(T(10), T(9), T(10)) is False, "the end instant must be outside [start, end)"

@check("helper_lower_included")
def _():
    from core.time_windows import in_window
    return in_window(T(9), T(9), T(10)) is True and in_window(T(9, 59, 59, 999999), T(9), T(10)) is True, "start and last microsecond inside"

@check("helper_before_start_excluded")
def _():
    from core.time_windows import in_window
    return in_window(T(8, 59, 59, 999999), T(9), T(10)) is False, "a microsecond before start is outside"

@check("empty_window_contains_nothing")
def _():
    from core.time_windows import in_window
    from api.report import count_events
    return in_window(T(9), T(9), T(9)) is False and count_events([{"at": T(9)}], T(9), T(9)) == 0, "start == end contains nothing"

@check("reversed_window_raises")
def _():
    from core.time_windows import in_window, InvalidWindow
    try:
        in_window(T(9, 30), T(10), T(9))
    except InvalidWindow:
        return True, "raised InvalidWindow"
    except Exception as exc:
        return False, f"raised {type(exc).__name__} instead of InvalidWindow"
    return False, "reversed window accepted"

@check("aware_and_naive_never_compared_silently")
def _():
    from core.time_windows import in_window
    naive_ts_aware_window = raises(lambda: in_window(T(9, 30), T(9).replace(tzinfo=UTC), T(10).replace(tzinfo=UTC)))
    aware_ts_naive_window = raises(lambda: in_window(T(9, 30).replace(tzinfo=UTC), T(9), T(10)))
    on_bound = raises(lambda: in_window(T(9), T(9).replace(tzinfo=UTC), T(10).replace(tzinfo=UTC)))
    return naive_ts_aware_window and aware_ts_naive_window and on_bound, f"{naive_ts_aware_window}/{aware_ts_naive_window}/{on_bound}"

@check("aware_offsets_compare_by_instant")
def _():
    from core.time_windows import in_window
    start, end = T(6).replace(tzinfo=UTC), T(7).replace(tzinfo=UTC)
    at_end = T(10).replace(tzinfo=EAT)      # 07:00 UTC
    at_start = T(9).replace(tzinfo=EAT)     # 06:00 UTC
    return in_window(at_end, start, end) is False and in_window(at_start, start, end) is True, "EAT 10:00 equals the UTC end"

@check("api_upper_excluded")
def _():
    from api.report import count_events
    events = [{"at": T(9)}, {"at": T(9, 30)}, {"at": T(10)}, {"at": T(11)}]
    return count_events(events, T(9), T(10)) == 2 and count_events(events, T(10), T(11)) == 1, "API counts per half-open window"

@check("worker_counts_each_event_once")
def _():
    from workers.rollup import bucket_events
    bounds = [T(9), T(10), T(11), T(12)]
    events = [{"at": T(9)}, {"at": T(10)}, {"at": T(10, 30)}, {"at": T(11)}, {"at": T(11, 59)}, {"at": T(12)}]
    counts = bucket_events(events, bounds)
    return counts == [1, 2, 2], f"buckets {counts}; boundary events must land only in the later bucket"

@check("export_upper_excluded")
def _():
    from exports.csv_export import export_rows
    text = export_rows([{"id": "a", "at": T(9)}, {"id": "b", "at": T(10)}], T(9), T(10))
    return text.splitlines() == ["id,at", "a,2026-09-29T09:00:00"], repr(text)

@check("callers_share_the_helper")
def _():
    from core.time_windows import in_window
    from api.report import count_events
    from exports.csv_export import export_rows
    from workers.rollup import bucket_events
    events = [{"id": str(i), "at": T(9) + timedelta(minutes=15 * i)} for i in range(9)]
    helper = sum(in_window(e["at"], T(9), T(10)) for e in events)
    api = count_events(events, T(9), T(10))
    worker = bucket_events(events, [T(9), T(10)])[0]
    export = len(export_rows(events, T(9), T(10)).splitlines()) - 1
    return helper == api == worker == export == 4, f"helper={helper} api={api} worker={worker} export={export}"

print("RESULT:" + json.dumps(results))
'''


def run_probe(workspace: Path, timeout: int = 60) -> dict:
    with tempfile.TemporaryDirectory(prefix="f05-probe-") as tmp:
        script = Path(tmp) / "probe.py"
        script.write_text(PROBE, encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
        try:
            proc = subprocess.run([sys.executable, str(script)], cwd=workspace, env=env, capture_output=True, text=True, timeout=timeout)
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
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
