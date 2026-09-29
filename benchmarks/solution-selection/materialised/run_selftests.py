"""Checker self-tests for the materialised solution-selection fixtures (no model call).

For every materialised fixture the checker must:

1. PASS ``starter + reference_good`` (with the withheld tests too, when they are present locally);
2. FAIL ``starter + reference_bad`` - the plausible, lazy solution. This proves the checker can
   fail, which is the point of the self-test (discipline adapted from DietrichGebert/ponytail
   ``benchmarks/agentic`` checker good/bad references; MIT, https://github.com/DietrichGebert/ponytail,
   commit e3ba2aa; paraphrased, no code copied).

Informational (never gating): whether the unmodified starter fails the checker, and whether
``reference_bad`` still passes the public tests (a lazy solution that passes the happy path is the
intended shape). A fixture whose checker reports NOT_ASSESSED (a required runtime is missing) is
reported as NOT_ASSESSED, never as a pass.

    python -X utf8 benchmarks/solution-selection/materialised/run_selftests.py [--only F07 F12] [--json out.json]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixture_kit as kit  # noqa: E402


def _public_tests_pass(fixture_id: str, workspace: Path) -> bool | None:
    manifest = json.loads((kit.fixture_dir(fixture_id) / "fixture.json").read_text(encoding="utf-8"))
    command = manifest.get("public_test_command")
    if not isinstance(command, list) or not command:
        return None
    command = [sys.executable if part == "python" else part for part in command]
    if shutil.which(command[0]) is None and not Path(command[0]).exists():
        return None
    try:
        proc = subprocess.run(command, cwd=workspace, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def selftest(fixture_id: str) -> dict:
    record: dict = {"fixture": fixture_id, "missing": kit.missing_parts(fixture_id)}
    if record["missing"]:
        record["status"] = "FAIL"
        return record
    withheld = kit.private_dir(fixture_id)
    withheld = withheld if withheld.is_dir() else None
    record["withheld_present"] = withheld is not None
    with tempfile.TemporaryDirectory(prefix=f"selftest-{fixture_id}-") as tmp:
        root = Path(tmp)
        good = kit.run_checker(fixture_id, kit.compose(fixture_id, root / "good", "good"), withheld)
        bad_ws = kit.compose(fixture_id, root / "bad", "bad")
        bad = kit.run_checker(fixture_id, bad_ws, withheld)
        starter = kit.run_checker(fixture_id, kit.compose(fixture_id, root / "starter"), withheld)
        record["bad_passes_public_tests"] = _public_tests_pass(fixture_id, bad_ws)
    record["good"] = good.get("status")
    record["bad"] = bad.get("status")
    record["starter"] = starter.get("status")
    record["bad_failed_checks"] = [c.get("id") for c in bad.get("checks", []) if not c.get("passed")]
    record["good_failed_checks"] = [c.get("id") for c in good.get("checks", []) if not c.get("passed")]
    for label, result in (("good", good), ("bad", bad)):
        if result.get("error"):
            record[f"{label}_error"] = result["error"]
    if "NOT_ASSESSED" in (record["good"], record["bad"]):
        record["status"] = "NOT_ASSESSED"
    elif record["good"] == "PASS" and record["bad"] == "FAIL":
        record["status"] = "PASS"
    else:
        record["status"] = "FAIL"
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--json", type=Path)
    args = parser.parse_args(argv)
    ids = args.only or kit.materialised_ids()
    results = [selftest(fid) for fid in ids]
    statuses = {r["status"] for r in results}
    overall = "FAIL" if "FAIL" in statuses or not results else ("NOT_ASSESSED" if "NOT_ASSESSED" in statuses else "PASS")
    summary = {"status": overall, "model_calls": 0, "fixtures": len(results),
               "passed": sum(r["status"] == "PASS" for r in results), "results": results}
    text = json.dumps(summary, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
