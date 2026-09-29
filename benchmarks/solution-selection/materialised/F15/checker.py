"""F15 checker: compact code must not hide complexity (stdlib only, no model call).

Runs the produced parser and retry machine in separate, time-boxed processes:
- golden parse vectors and the four error codes (classification is part of the contract);
- adversarial inputs that trigger catastrophic regex backtracking (2 s budget) and a large
  record that a linear parser handles well inside the budget;
- the full transition trace for success, permanent failure and exhaustion (every span present,
  retry bounded - an unbounded loop hits the timeout).

    python checker.py <workspace> [--withheld <dir>]
Exit 0 PASS, 1 FAIL, 2 NOT_ASSESSED.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

FIXTURE = "F15"

PARSE_VECTORS = [
    ("order=1042; status=paid; note=", {"order": "1042", "status": "paid", "note": ""}),
    ("  a_1 = x y ;b=", {"a_1": "x y", "b": ""}),
    ("url=https://example.test/a?b=c", {"url": "https://example.test/a?b=c"}),
    ("", ("empty", 0)),
    ("   ", ("empty", 0)),
    ("a=1;b", ("missing_separator", 1)),
    ("a=1;;b=2", ("missing_separator", 1)),
    ("a=1;2b=3", ("bad_key", 1)),
    ("a=1;B=3", ("bad_key", 1)),
    ("a=1;k-y=3", ("bad_key", 1)),
    ("a=1;b=2;a=3", ("duplicate_key", 2)),
]

PARSE_PROGRAM = textwrap.dedent('''
    import json, sys
    from worker.parser import parse_record
    from worker.errors import ParseError
    vectors = json.loads(sys.stdin.read())
    out = []
    for text, _ in vectors:
        try:
            out.append({"ok": parse_record(text)})
        except ParseError as exc:
            out.append({"error": [getattr(exc, "code", None), getattr(exc, "position", None)]})
        except Exception as exc:
            out.append({"crash": repr(exc)})
    print(json.dumps(out))
''')

ADVERSARIAL = {
    "catastrophic-backtracking-keys": "'a' * 34 + '!'",
    "catastrophic-backtracking-spaced": "'a ' * 30 + '#'",
    "large-record-linear": "';'.join(f'k{i}=v{i}' for i in range(200000))",
}

ADVERSARIAL_PROGRAM = textwrap.dedent('''
    import sys
    from worker.parser import parse_record
    from worker.errors import ParseError
    text = eval(sys.argv[1])
    try:
        parse_record(text)
    except ParseError:
        pass
    print("done")
''')

MACHINE_PROGRAM = textwrap.dedent('''
    import json, sys
    from worker.errors import PermanentFailure, TransientFailure
    from worker.retry import RetryMachine
    from worker.tracing import FakeClock, RecordingTracer
    plan = sys.argv[1].split(",")
    calls = []
    def operation():
        step = plan[len(calls)] if len(calls) < len(plan) else plan[-1]
        calls.append(step)
        if step == "t":
            raise TransientFailure("busy")
        if step == "p":
            raise PermanentFailure("rejected")
    tracer, clock = RecordingTracer(), FakeClock()
    state = RetryMachine(tracer, clock, max_attempts=int(sys.argv[2])).run(operation)
    spans = [[a.get("source"), a.get("target"), a.get("attempt")] for name, a in tracer.spans if name == "retry.transition"]
    print(json.dumps({"state": state, "calls": len(calls), "spans": spans, "sleeps": len(clock.sleeps)}))
''')

MACHINE_CASES = {
    "trace-success-after-transient": ("t,ok", 4, {"state": "SUCCEEDED", "calls": 2, "sleeps": 1, "spans": [
        ["IDLE", "SENDING", 1], ["SENDING", "BACKOFF", 1], ["BACKOFF", "SENDING", 2], ["SENDING", "SUCCEEDED", 2]]}),
    "permanent-classified-not-retried": ("p,ok", 4, {"state": "FAILED_PERMANENT", "calls": 1, "sleeps": 0, "spans": [
        ["IDLE", "SENDING", 1], ["SENDING", "FAILED_PERMANENT", 1]]}),
    "retry-bounded-exhausted-traced": ("t", 3, {"state": "EXHAUSTED", "calls": 3, "sleeps": 2, "spans": [
        ["IDLE", "SENDING", 1], ["SENDING", "BACKOFF", 1], ["BACKOFF", "SENDING", 2], ["SENDING", "BACKOFF", 2],
        ["BACKOFF", "SENDING", 3], ["SENDING", "EXHAUSTED", 3]]}),
}


def _run(workspace: Path, args: list[str], timeout: float, stdin: str | None = None):
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-X", "utf8", *args], cwd=workspace, env=env, input=stdin,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, f"timed out after {timeout}s"
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-800:]
    return proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "", None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    checks = []

    out, err = _run(workspace, ["-c", PARSE_PROGRAM], 10, json.dumps(PARSE_VECTORS))
    results = json.loads(out) if out else []
    golden_ok, codes_ok, detail = True, True, []
    for (text, expected), got in zip(PARSE_VECTORS, results or [None] * len(PARSE_VECTORS)):
        if isinstance(expected, dict):
            if not got or got.get("ok") != expected:
                golden_ok = False
                detail.append({"input": text, "got": got})
        elif not got or got.get("error") != list(expected):
            codes_ok = False
            detail.append({"input": text, "expected": list(expected), "got": got})
    if err:
        golden_ok = codes_ok = False
        detail.append(err)
    checks.append({"id": "parse-golden-vectors", "passed": golden_ok, "detail": [d for d in detail if not isinstance(d, dict) or "expected" not in d]})
    checks.append({"id": "error-classification-preserved", "passed": codes_ok, "detail": [d for d in detail if isinstance(d, dict) and "expected" in d]})

    for check_id, expression in ADVERSARIAL.items():
        out, err = _run(workspace, ["-c", ADVERSARIAL_PROGRAM, expression], 2.0)
        checks.append({"id": check_id, "passed": err is None and out == "done", "detail": err or "completed inside 2 s"})

    for check_id, (plan, attempts, expected) in MACHINE_CASES.items():
        out, err = _run(workspace, ["-c", MACHINE_PROGRAM, plan, str(attempts)], 5.0)
        got = json.loads(out) if out and not err else None
        checks.append({"id": check_id, "passed": got == expected, "detail": err or {"got": got, "expected": expected}})

    if args.withheld and args.withheld.is_dir():
        env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
        try:
            proc = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", str(args.withheld.resolve()), "-t", str(args.withheld.resolve())],
                                  cwd=workspace, env=env, capture_output=True, text=True, timeout=60)
            checks.append({"id": "withheld-tests", "passed": proc.returncode == 0, "detail": proc.stderr[-800:]})
        except subprocess.TimeoutExpired:
            checks.append({"id": "withheld-tests", "passed": False, "detail": "withheld tests timed out"})

    status = "PASS" if all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, default=str))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
