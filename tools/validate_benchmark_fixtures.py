"""Validate the frozen solution-selection fixture specification."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_IDS = {f"F{index:02d}" for index in range(1, 17)}
REQUIRED_FIELDS = {"id", "title", "stack", "initial_state", "public_task", "positive_oracles", "negative_oracles", "withheld_family", "materialisation_status", "owner_role", "time_limit_minutes"}

# Pressure scenarios (M10-04-T05): an optional case type for discipline-skill
# RED/GREEN testing. They may sit in the ``pressure_scenarios`` array of
# fixtures.json or in a sibling ``pressure-scenarios.json`` file with the same
# array; IDs must be unique across both. The F01-F16 rule above is unchanged.
PRESSURE_FILE = "pressure-scenarios.json"
PRESSURE_ID = re.compile(r"^PS\d{2}$")
PRESSURE_TYPES = {"time", "sunk_cost", "authority", "economic", "exhaustion", "social", "pragmatic"}
PRESSURE_FIELDS = {"id", "title", "target_skill", "discipline_gate", "pressures", "scenario", "forced_choice", "expected_disposition", "baseline_outcome", "with_skill_outcome", "materialisation_status"}
CHOICES = {"A", "B", "C"}


def _outcome_errors(sid: str, field: str, value) -> list[str]:
    if value == "NOT_ASSESSED":
        return []
    if not isinstance(value, dict):
        return [f"{sid} {field} must be NOT_ASSESSED or an object"]
    errors = []
    if value.get("choice") not in CHOICES:
        errors.append(f"{sid} {field}.choice must be A, B or C")
    quotes = value.get("rationalisations_verbatim")
    if not isinstance(quotes, list) or not all(isinstance(item, str) for item in quotes):
        errors.append(f"{sid} {field}.rationalisations_verbatim must be a list of strings")
    if not isinstance(value.get("run_ref"), str) or not value["run_ref"].strip():
        errors.append(f"{sid} {field}.run_ref must name the run record")
    return errors


def validate_pressure_scenarios(scenarios, errors: list[str], warnings: list[str]) -> int:
    if not isinstance(scenarios, list):
        errors.append("pressure_scenarios must be a list")
        return 0
    seen: set[str] = set()
    for index, item in enumerate(scenarios):
        if not isinstance(item, dict):
            errors.append(f"pressure scenario {index} must be an object")
            continue
        sid = str(item.get("id", f"pressure[{index}]"))
        if not PRESSURE_ID.match(sid):
            errors.append(f"{sid} id must match PS<two digits>")
        if sid in seen:
            errors.append(f"{sid} duplicate pressure scenario id")
        seen.add(sid)
        errors.extend(f"{sid} missing {field}" for field in sorted(PRESSURE_FIELDS - set(item)))
        target = item.get("target_skill")
        if not isinstance(target, str) or target.count("/") < 1 or not all(target.split("/")):
            errors.append(f"{sid} target_skill must be <engine>/<skill>")
        pressures = item.get("pressures")
        if not isinstance(pressures, list) or len(set(pressures)) < 3:
            errors.append(f"{sid} needs at least three distinct combined pressures")
        elif set(pressures) - PRESSURE_TYPES:
            errors.append(f"{sid} has unknown pressures {sorted(set(pressures) - PRESSURE_TYPES)}")
        choice = item.get("forced_choice")
        options = choice.get("options") if isinstance(choice, dict) else None
        if not isinstance(options, dict) or set(options) != CHOICES or not all(isinstance(v, str) and v.strip() for v in options.values()):
            errors.append(f"{sid} forced_choice.options must be exactly A, B and C")
        if not isinstance(choice, dict) or choice.get("compliant") not in CHOICES:
            errors.append(f"{sid} forced_choice.compliant must be A, B or C")
        for field in ("baseline_outcome", "with_skill_outcome"):
            if field in item:
                errors.extend(_outcome_errors(sid, field, item[field]))
        if item.get("materialisation_status") not in {"NOT_ASSESSED", "MATERIALISED"}:
            errors.append(f"{sid} has unsupported materialisation_status")
        if "short_prompt" in item and (not isinstance(item["short_prompt"], str) or not item["short_prompt"].strip()):
            errors.append(f"{sid} short_prompt must be a non-empty string when present")
        if "NOT_ASSESSED" in (item.get("baseline_outcome"), item.get("with_skill_outcome")) and not item.get("not_assessed_reason"):
            warnings.append(f"{sid} records NOT_ASSESSED outcomes without not_assessed_reason")
    return len(scenarios)


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
    warnings: list[str] = []
    scenarios = payload.get("pressure_scenarios", [])
    if isinstance(scenarios, list):
        scenarios = list(scenarios)
    sibling = path.parent / PRESSURE_FILE
    sources = ["fixtures.json"] if payload.get("pressure_scenarios") else []
    if sibling.is_file() and sibling.resolve() != path.resolve():
        try:
            extra = json.loads(sibling.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{PRESSURE_FILE}: {exc}")
        else:
            extra = extra.get("pressure_scenarios") if isinstance(extra, dict) else None
            if not isinstance(extra, list):
                errors.append(f"{PRESSURE_FILE} must hold a pressure_scenarios list")
            elif isinstance(scenarios, list):
                scenarios.extend(extra)
                sources.append(PRESSURE_FILE)
    pressure_count = validate_pressure_scenarios(scenarios, errors, warnings)
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "warnings": warnings, "fixture_count": len(fixtures), "pressure_scenario_count": pressure_count, "pressure_scenario_sources": sources, "execution_status": payload.get("status")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path("benchmarks/solution-selection/fixtures.json"))
    args = parser.parse_args()
    result = validate(args.path)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
