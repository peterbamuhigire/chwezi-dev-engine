"""F06 checker: behaviour-preserving refactor (stdlib only, no model call).

The golden corpus is produced at run time from this fixture's unmodified ``starter/`` and
compared, case by case, with the workspace: return values, exception types and messages, and
the full audit-event sequence (order included) over every branch combination. It also checks
that duplication actually fell and flags a speculative plugin or registry framework.

    python checker.py <workspace> [--withheld <dir>]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE = "F06"
STARTER = Path(__file__).resolve().parent / "starter"

CORPUS = r'''
import itertools, json, sys
sys.path.insert(0, sys.argv[1])
from eligibility import check_grant_eligibility, check_loan_eligibility, check_membership_eligibility
from eligibility.audit import AuditLog
from eligibility.models import Actor, Applicant

ages = [15, 16, 17, 18, 24, 25, 35, 36, 65, "18", True, None]
countries = ["UG", "KE", "US"]
sanctioned = [False, True]
incomes = [499_999, 500_000, 1_999_999, 2_000_000]
regions = ["central", "west"]
actors = [
    Actor("nobody"),
    Actor("central-officer", frozenset({"eligibility.evaluate"}), frozenset({"central"})),
    Actor("undelegated", frozenset({"eligibility.evaluate"})),
    Actor("delegate-only", frozenset(), frozenset({"central", "west"})),
]
out = []
for fn in (check_loan_eligibility, check_grant_eligibility, check_membership_eligibility):
    for n, (age, country, sanc, income, region, actor) in enumerate(itertools.product(ages, countries, sanctioned, incomes, regions, actors)):
        applicant = Applicant(f"app-{n}", age, country, sanc, income, region)
        audit = AuditLog()
        try:
            outcome = ["ok", fn(applicant, actor, audit)]
        except Exception as exc:
            outcome = ["raise", type(exc).__name__, [c.__name__ for c in type(exc).__mro__], str(exc)]
        out.append({"case": [fn.__name__, repr(age), country, sanc, income, region, actor.id], "outcome": outcome, "audit": [list(e) for e in audit.events]})
print(json.dumps(out))
'''

FRAMEWORK = re.compile(r"\bimportlib\b|entry_points|__subclasses__|metaclass\s*=|\bREGISTRY\b|_registry\b|\bregister\s*\(|\bplugins?\b|__import__", re.IGNORECASE)


def corpus(root: Path, timeout: int = 120) -> tuple[list | None, str]:
    with tempfile.TemporaryDirectory(prefix="f06-probe-") as tmp:
        script = Path(tmp) / "corpus.py"
        script.write_text(CORPUS, encoding="utf-8")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        env.pop("PYTHONPATH", None)
        try:
            proc = subprocess.run([sys.executable, str(script), str(root)], cwd=tmp, env=env, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, "corpus run timed out"
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-400:]
    return json.loads(proc.stdout), "ok"


def first_difference(golden: list, produced: list, key: str) -> str | None:
    if len(golden) != len(produced):
        return f"case count {len(produced)} != {len(golden)}"
    for want, got in zip(golden, produced):
        if want[key] != got[key]:
            return f"{want['case']}: expected {want[key]!r}, got {got[key]!r}"
    return None


def source_text(workspace: Path) -> str:
    package = workspace / "eligibility"
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sorted(package.rglob("*.py"))) if package.is_dir() else ""


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
    checks: list[dict] = []

    def add(cid: str, passed: bool, detail: str) -> None:
        checks.append({"id": cid, "passed": bool(passed), "detail": detail[:400]})

    golden, why = corpus(STARTER)
    if golden is None:
        add("golden_corpus", False, f"starter corpus failed: {why}")
    produced, why = corpus(workspace)
    if golden is not None:
        if produced is None:
            add("workspace_runs", False, why)
        else:
            diff = first_difference(golden, produced, "outcome")
            add("golden_outputs_and_errors_preserved", diff is None, diff or f"{len(golden)} cases identical")
            diff = first_difference(golden, produced, "audit")
            add("audit_event_sequence_identical", diff is None, diff or "every audit sequence identical")
    text = source_text(workspace)
    starter_text = source_text(STARTER)
    permission_calls = len(re.findall(r"\.has_permission\(", text)) - len(re.findall(r"\.has_permission\(", (STARTER / "eligibility" / "models.py").read_text(encoding="utf-8")))
    age_checks = sum(1 for line in text.splitlines() if re.search(r"isinstance\(\s*applicant\.age", line))
    add("duplication_reduced", permission_calls <= 2 and age_checks <= 1 and len(text) < len(starter_text) * 1.5,
        f"evaluate-permission call sites={permission_calls} (starter 4), integer-age check lines={age_checks} (starter 3)")
    hits = sorted({m.group(0) for m in FRAMEWORK.finditer(text)})
    add("no_speculative_framework", not hits, f"framework markers: {hits}" if hits else "none")
    if args.withheld:
        ok, detail = run_withheld(workspace, args.withheld)
        add("withheld_tests", ok, detail)
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
