"""Check that a fresh operator can discover the solution-selection commands."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED = {
    "solution_decision": "tools/solution_decision.py",
    "solution_review": "tools/solution_review.py",
    "solution_debt": "tools/solution_debt.py",
    "solution_mode": "tools/solution_mode.py",
    "solution_evidence": "tools/solution_evidence.py",
    "adapter_lifecycle": "tools/adapter_lifecycle.py",
}


def check(root: Path) -> dict:
    missing = [path for path in EXPECTED.values() if not (root / path).is_file()]
    docs = root / "docs" / "engine-control-plane.md"
    if not docs.is_file():
        missing.append("docs/engine-control-plane.md")
    else:
        text = docs.read_text(encoding="utf-8")
        for command in EXPECTED:
            if command not in text:
                missing.append(f"docs/engine-control-plane.md:{command}")
    return {"status": "PASS" if not missing else "FAIL", "missing": missing, "command_count": len(EXPECTED), "read_only": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = check(args.root.resolve())
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
