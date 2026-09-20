"""Validate the frozen solution-selection fixture specification."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_IDS = {f"F{index:02d}" for index in range(1, 17)}
REQUIRED_FIELDS = {"id", "title", "stack", "initial_state", "public_task", "positive_oracles", "negative_oracles", "withheld_family", "materialisation_status", "owner_role", "time_limit_minutes"}


def validate(path: Path) -> dict:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "errors": [str(exc)]}
    fixtures = payload.get("fixtures") if isinstance(payload, dict) else None
    if not isinstance(fixtures, list):
        return {"status": "FAIL", "errors": ["fixtures must be a list"]}
    ids = {item.get("id") for item in fixtures if isinstance(item, dict)}
    if ids != REQUIRED_IDS:
        errors.append(f"fixture IDs must be exactly F01-F16, got {sorted(ids)}")
    for index, item in enumerate(fixtures):
        if not isinstance(item, dict):
            errors.append(f"fixture {index} must be an object")
            continue
        missing = REQUIRED_FIELDS - set(item)
        errors.extend(f"{item.get('id', index)} missing {field}" for field in sorted(missing))
        if item.get("materialisation_status") not in {"NOT_ASSESSED", "MATERIALISED"}:
            errors.append(f"{item.get('id')} has unsupported materialisation_status")
        if not isinstance(item.get("positive_oracles"), list) or not item["positive_oracles"]:
            errors.append(f"{item.get('id')} needs positive oracles")
        if not isinstance(item.get("negative_oracles"), list) or not item["negative_oracles"]:
            errors.append(f"{item.get('id')} needs negative oracles")
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "fixture_count": len(fixtures), "execution_status": payload.get("status")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path("benchmarks/solution-selection/fixtures.json"))
    args = parser.parse_args()
    result = validate(args.path)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
