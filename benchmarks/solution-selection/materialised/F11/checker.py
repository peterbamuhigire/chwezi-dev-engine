"""F11 checker: asynchronous failure and retries (stdlib only, no model call).

Runs the produced ``notify.job.NotificationJob`` in separate processes (10 s timeout each, so an
unbounded retry loop fails rather than hangs) against adversarial fake transports.

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

FIXTURE = "F11"
TIMEOUT = 10

PRELUDE = textwrap.dedent('''
    import json, random
    from notify.clock import FakeClock
    from notify.errors import TransientError, PermanentError, RetryAfter
    from notify.job import NotificationJob
    from notify.store import InMemoryStore

    class Transport:
        def __init__(self, script, accepted_on_timeout=False):
            self.script = list(script)
            self.keys = []
            self.accepted = set()
            self.accepted_on_timeout = accepted_on_timeout
        def send(self, message, idempotency_key):
            self.keys.append(idempotency_key)
            step = self.script.pop(0) if self.script else "ok"
            if step == "ok":
                self.accepted.add(idempotency_key)
                return "prov-" + str(len(self.keys))
            if step == "timeout_after_accept":
                self.accepted.add(idempotency_key)
                raise TimeoutError("read timed out after provider accepted")
            if step == "timeout":
                raise TimeoutError("connect timed out")
            if step == "permanent":
                raise PermanentError("invalid recipient")
            raise TransientError("provider busy")
        def status(self, idempotency_key):
            return "accepted" if idempotency_key in self.accepted else "unknown"

    def emit(passed, detail):
        print(json.dumps({"passed": bool(passed), "detail": detail}))
''')

SCENARIOS = {
    "bounded-retries-dead-letter": '''
        t = Transport(["transient"] * 50)
        clock = FakeClock()
        job = NotificationJob(t, InMemoryStore(), clock, rng=random.Random(7))
        rec = job.process({"id": "n-100", "body": "x"})
        ok = rec["state"] == "dead_letter" and len(t.keys) == 5 and rec["attempts"] == 5 and bool(rec["last_error"])
        emit(ok, {"state": rec["state"], "sends": len(t.keys), "attempts": rec["attempts"], "last_error": rec["last_error"]})
    ''',
    "backoff-within-jitter-bounds": '''
        t = Transport(["transient"] * 4)
        clock = FakeClock()
        job = NotificationJob(t, InMemoryStore(), clock, rng=random.Random(3))
        rec = job.process({"id": "n-101", "body": "x"})
        bounds = [min(30.0, 1.0 * 2 ** (n - 1)) for n in range(1, 5)]
        within = len(clock.sleeps) == 4 and all(d / 2 - 1e-9 <= s <= d + 1e-9 for s, d in zip(clock.sleeps, bounds))
        emit(within and rec["state"] == "sent", {"sleeps": clock.sleeps, "bounds": bounds, "state": rec["state"]})
    ''',
    "delay-capped": '''
        t = Transport(["transient"] * 50)
        clock = FakeClock()
        job = NotificationJob(t, InMemoryStore(), clock, rng=random.Random(5), max_attempts=6, base_delay=10.0, max_delay=15.0)
        job.process({"id": "n-102", "body": "x"})
        emit(bool(clock.sleeps) and max(clock.sleeps) <= 15.0 + 1e-9, {"sleeps": clock.sleeps})
    ''',
    "permanent-not-retried": '''
        t = Transport(["permanent", "ok"])
        clock = FakeClock()
        job = NotificationJob(t, InMemoryStore(), clock, rng=random.Random(1))
        rec = job.process({"id": "n-103", "body": "x"})
        emit(len(t.keys) == 1 and rec["state"] == "dead_letter" and bool(rec["last_error"]) and not clock.sleeps,
             {"sends": len(t.keys), "state": rec["state"], "sleeps": clock.sleeps})
    ''',
    "timeout-after-acceptance-not-duplicated": '''
        t = Transport(["timeout_after_accept", "ok", "ok"])
        job = NotificationJob(t, InMemoryStore(), FakeClock(), rng=random.Random(1))
        rec = job.process({"id": "n-104", "body": "x"})
        emit(len(t.keys) == 1 and rec["state"] == "sent", {"sends": len(t.keys), "state": rec["state"]})
    ''',
    "genuine-timeout-retried": '''
        t = Transport(["timeout", "ok"])
        job = NotificationJob(t, InMemoryStore(), FakeClock(), rng=random.Random(1))
        rec = job.process({"id": "n-105", "body": "x"})
        emit(len(t.keys) == 2 and rec["state"] == "sent", {"sends": len(t.keys), "state": rec["state"]})
    ''',
    "stable-idempotency-key": '''
        t = Transport(["transient", "timeout", "ok"])
        job = NotificationJob(t, InMemoryStore(), FakeClock(), rng=random.Random(1))
        rec = job.process({"id": "n-106", "body": "x"})
        emit(set(t.keys) == {"n-106"} and rec["state"] == "sent", {"keys": t.keys})
    ''',
    "shutdown-preserves-pending": '''
        t = Transport(["transient"] * 10)
        holder = {}
        clock = FakeClock(on_sleep=lambda s: holder["job"].request_shutdown())
        store = InMemoryStore()
        job = NotificationJob(t, store, clock, rng=random.Random(1))
        holder["job"] = job
        rec = job.process({"id": "n-107", "body": "x"})
        stored = store.get("n-107")
        ok = rec["state"] == "pending" and stored["state"] == "pending" and stored["attempts"] == 1 and len(t.keys) == 1
        emit(ok, {"state": rec["state"], "stored": stored, "sends": len(t.keys)})
    ''',
    "terminal-failure-observable-in-store": '''
        t = Transport(["permanent"])
        store = InMemoryStore()
        job = NotificationJob(t, store, FakeClock(), rng=random.Random(1))
        job.process({"id": "n-108", "body": "x"})
        stored = store.get("n-108")
        emit(stored is not None and stored["state"] == "dead_letter" and bool(stored["last_error"]), {"stored": stored})
    ''',
}


def run_python(workspace: Path, source: str) -> dict:
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-X", "utf8", "-c", source], cwd=workspace, env=env,
                              capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"passed": False, "detail": f"timed out after {TIMEOUT}s (unbounded retry?)"}
    lines = [line for line in proc.stdout.splitlines() if line.startswith("{")]
    if proc.returncode != 0 or not lines:
        return {"passed": False, "detail": (proc.stderr or proc.stdout)[-800:]}
    return json.loads(lines[-1])


def run_withheld(workspace: Path, withheld: Path) -> dict:
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", str(withheld), "-t", str(withheld)],
                              cwd=workspace, env=env, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return {"passed": False, "detail": "withheld tests timed out"}
    return {"passed": proc.returncode == 0, "detail": proc.stderr[-800:]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    checks = []
    for check_id, body in SCENARIOS.items():
        result = run_python(workspace, PRELUDE + textwrap.dedent(body))
        checks.append({"id": check_id, "passed": bool(result.get("passed")), "detail": result.get("detail")})
    if args.withheld and args.withheld.is_dir():
        result = run_withheld(workspace, args.withheld.resolve())
        checks.append({"id": "withheld-tests", "passed": result["passed"], "detail": result["detail"]})
    status = "PASS" if all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, default=str))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
