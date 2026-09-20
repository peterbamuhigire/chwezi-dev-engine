"""Validate quality-gated solution-selection experiment evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def validate(payload: Any, root: Path) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        return {"status": "FAIL", "errors": ["schema_version 1 evidence object is required"]}
    baseline = payload.get("baseline_id")
    runs = payload.get("runs")
    if not isinstance(baseline, str) or not baseline:
        errors.append("baseline_id is required")
    if not isinstance(runs, list) or not runs:
        errors.append("runs must contain at least one raw run")
        runs = []
    models: set[str] = set()
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            errors.append(f"runs[{index}] must be an object")
            continue
        for field in ("run_id", "arm", "fixture", "status", "model_id", "raw_path"):
            if not run.get(field):
                errors.append(f"runs[{index}] missing {field}")
        if run.get("status") not in {"PASS", "FAIL", "NOT_ASSESSED"}:
            errors.append(f"runs[{index}] has unsupported status")
        models.add(str(run.get("model_id")))
        raw_path = run.get("raw_path")
        if isinstance(raw_path, str):
            path = Path(raw_path)
            if path.is_absolute() or ".." in path.parts or not (root / path).is_file():
                errors.append(f"runs[{index}] raw_path is not a repository-local existing file")
        if "cost_usd" in run and run["cost_usd"] is None:
            errors.append(f"runs[{index}] unknown cost must remain null and cannot be aggregated")
        if run.get("cost_usd") == 0 and run.get("tokens", 0):
            errors.append(f"runs[{index}] non-empty run cannot claim zero cost")
    if len(models) > 1:
        errors.append("mixed model IDs cannot be compared as one evidence set")
    statuses = {run.get("status") for run in runs if isinstance(run, dict)}
    if "NOT_ASSESSED" in statuses:
        status = "NOT_ASSESSED" if not errors else "FAIL"
    else:
        status = "FAIL" if errors else "PASS"
    return {"status": status, "errors": errors, "run_count": len(runs), "models": sorted(models)}


def report(payload: dict[str, Any]) -> dict[str, Any]:
    runs = payload.get("runs", [])
    usable = [run for run in runs if run.get("status") == "PASS" and isinstance(run.get("quality"), dict)]
    quality_failures = [run.get("run_id") for run in runs if run.get("status") == "FAIL"]
    return {"status": "PASS" if usable and not quality_failures else "NOT_ASSESSED", "usable_runs": len(usable), "failed_runs": quality_failures, "cost_status": "NOT_ASSESSED" if any(run.get("cost_usd") is None for run in runs) else "MEASURED"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "report"))
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.evidence.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, indent=2))
        return 1
    result = validate(payload, args.root.resolve()) if args.command == "validate" else report(payload)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
