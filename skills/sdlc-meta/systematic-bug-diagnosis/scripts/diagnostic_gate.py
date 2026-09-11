#!/usr/bin/env python3
"""Gate causal diagnosis and mutation on reproduction evidence and authority."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

REQUIRED = {"symptom", "environment", "red_capable", "red_observed", "case", "cause_claimed", "fix_authority"}
CASES = {"normal", "intermittent", "performance", "production-only"}


def evaluate(data: object) -> tuple[list[str], str]:
    if not isinstance(data, dict):
        return ["record must be a mapping"], "stop"
    missing = REQUIRED - set(data)
    if missing:
        return [f"missing: {', '.join(sorted(missing))}"], "stop"
    findings: list[str] = []
    if not isinstance(data["symptom"], str) or not data["symptom"].strip():
        findings.append("symptom must be non-empty text")
    if not isinstance(data["environment"], str) or not data["environment"].strip():
        findings.append("environment must be non-empty text")
    for field in ("red_capable", "red_observed", "cause_claimed", "fix_authority"):
        if not isinstance(data[field], bool):
            findings.append(f"{field} must be boolean")
    if data["case"] not in CASES:
        findings.append(f"unsupported case: {data['case']!r}")
    if data["cause_claimed"] is True and not (data["red_capable"] is True and data["red_observed"] is True):
        findings.append("causal claim requires a red-capable loop with observed red evidence")
    if data["case"] == "intermittent" and data.get("reproduction_rate") is None:
        findings.append("intermittent case requires a measured reproduction_rate")
    if data["case"] == "performance" and not data.get("comparison_boundary"):
        findings.append("performance case requires a fixed comparison_boundary")
    if data["case"] == "production-only" and data.get("telemetry_authority") is not True:
        findings.append("production-only case requires telemetry_authority before instrumentation")
    if findings:
        return findings, "stop"
    if data["red_capable"] is not True or data["red_observed"] is not True:
        return [], "instrument-or-report-not-assessed"
    if data["cause_claimed"] is True and data["fix_authority"] is True:
        return [], "handoff-for-fix"
    if data["cause_claimed"] is True:
        return [], "report-cause-read-only"
    return [], "run-discriminating-experiment"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        data = yaml.safe_load(args.record.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"[FAIL] cannot read record: {exc}")
        return 1
    findings, action = evaluate(data)
    for finding in findings:
        print(f"[FAIL] {finding}")
    print(f"diagnostic-gate: findings={len(findings)} action={action}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
