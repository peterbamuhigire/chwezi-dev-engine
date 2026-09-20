"""Read-only review helpers for solution decisions and changed repositories."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

EXCLUDED_PARTS = {".git", ".venv", "node_modules", "vendor", "dist", "build", "generated", "__pycache__"}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    severity: str
    confidence: str
    message: str


def _files(root: Path) -> Iterable[Path]:
    try:
        result = subprocess.run(["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True)
        names = [item for item in result.stdout.decode("utf-8").split("\0") if item]
        paths = [root / item for item in names]
    except (OSError, subprocess.CalledProcessError):
        paths = list(root.rglob("*"))
    for path in paths:
        if path.is_file() and not any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts):
            yield path


def _duplicate_blocks(path: Path, lines: list[str], size: int = 3) -> list[Finding]:
    locations: dict[tuple[str, ...], list[int]] = {}
    for index in range(0, max(0, len(lines) - size + 1)):
        block = tuple(line.strip() for line in lines[index:index + size])
        if sum(bool(line) for line in block) < size:
            continue
        locations.setdefault(block, []).append(index + 1)
    findings: list[Finding] = []
    for block, starts in locations.items():
        if len(starts) > 1:
            findings.append(Finding(path.as_posix(), starts[0], "duplicated-block", "warning", "medium", f"same three-line block appears at lines {', '.join(map(str, starts))}"))
    return findings


def repo_audit(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _files(root):
        if path.suffix.lower() not in {".py", ".js", ".ts", ".tsx", ".php", ".java", ".go", ".rb", ".rs", ".md"}:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(_duplicate_blocks(path.relative_to(root), lines))
        for line_number, line in enumerate(lines, 1):
            if "SOLUTION_DEBT" in line and not re.search(r"owner=.+trigger=.+expires=", line, re.IGNORECASE):
                findings.append(Finding(path.relative_to(root).as_posix(), line_number, "incomplete-debt-marker", "error", "high", "SOLUTION_DEBT marker lacks owner, trigger, or expires fields"))
            if re.search(r"\bTODO\b", line) and "TODO(" not in line:
                findings.append(Finding(path.relative_to(root).as_posix(), line_number, "unresolved-todo", "warning", "low", "TODO requires an owner and review trigger before release"))
    return findings


def diff_review(root: Path) -> list[Finding]:
    try:
        diff = subprocess.run(["git", "diff", "--no-ext-diff", "--unified=0"], cwd=root, check=True, capture_output=True, text=True, encoding="utf-8").stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        return [Finding(".", 0, "diff-unavailable", "error", "high", str(exc))]
    findings: list[Finding] = []
    current: str | None = None
    for raw in diff.splitlines():
        if raw.startswith("+++ b/"):
            current = raw[6:]
            continue
        match = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
        if match:
            line_number = int(match.group(1))
            continue
        if current is None or not raw.startswith("+") or raw.startswith("+++"):
            continue
        text = raw[1:]
        if re.search(r"^(?:from\s+\S+\s+import|import\s+\S+|require\(|use\s+\S+)", text.strip()):
            findings.append(Finding(current, line_number, "dependency-change", "warning", "medium", "new import or dependency boundary requires solution-decision evidence"))
        if re.search(r"\b(pass|except\s*:\s*pass)\b", text) and not text.lstrip().startswith(("#", "//")):
            findings.append(Finding(current, line_number, "weak-failure-path", "warning", "medium", "new pass or empty failure path needs a negative oracle"))
        line_number += 1
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("repo-audit", "diff-review"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    findings = repo_audit(args.root.resolve()) if args.command == "repo-audit" else diff_review(args.root.resolve())
    payload = {"status": "PASS" if not any(item.severity == "error" for item in findings) else "FAIL", "findings": [asdict(item) for item in findings], "read_only": True}
    if args.as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"solution-review: {payload['status']}")
        for item in findings:
            print(f"{item.severity.upper()} {item.path}:{item.line} {item.code}: {item.message}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
