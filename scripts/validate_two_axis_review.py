#!/usr/bin/env python3
"""Validate that a review reports specification and standards verdicts independently."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

VERDICTS = {"PASS", "FAIL", "NOT ASSESSED"}
AXIS = re.compile(r"^- Axis ([AB]):\s*(PASS|FAIL|NOT ASSESSED)\s*$", re.MULTILINE)


def validate(text: str) -> tuple[list[str], str]:
    findings: list[str] = []
    matches = AXIS.findall(text)
    found = {axis: verdict for axis, verdict in matches}
    for axis in ("A", "B"):
        if sum(1 for matched_axis, _ in matches if matched_axis == axis) > 1:
            findings.append(f"Axis {axis} verdict appears more than once")
        if axis not in found:
            findings.append(f"Axis {axis} verdict is missing or invalid")
    if findings:
        return findings, "NOT ASSESSED"
    overall = "PASS" if found["A"] == found["B"] == "PASS" else "FAIL"
    return [], overall


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    try:
        text = args.review.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"[FAIL] cannot read review: {exc}")
        return 1
    findings, overall = validate(text)
    for finding in findings:
        print(f"[FAIL] {finding}")
    print(f"two-axis-review: findings={len(findings)} overall={overall}")
    return 1 if findings or overall != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
