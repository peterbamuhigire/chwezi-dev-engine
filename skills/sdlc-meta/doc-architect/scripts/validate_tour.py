#!/usr/bin/env python3
"""Validate a CodeTour `.tour` file against the repository it describes.

Checks (each failure has a stable code):

  tour/invalid-json           the file is not a JSON object with a `steps` list
  tour/unanchored-first-step  step 1 has no `file` or `directory` anchor
  tour/missing-file           a step's file or directory does not exist on disk (no `ref`)
  tour/absent-at-ref          a step's file or directory is absent at the tour's `ref`
  tour/bad-ref                the tour's `ref` does not resolve in the repository
  tour/line-out-of-range      a `line` or `selection` is outside the file, or reversed
  tour/pattern-not-found      a `pattern` anchor matches nothing in the file
  tour/step-count-out-of-budget  the step count is outside the persona budget

Standard library only; `git` is called for `ref` checks with --no-replace-objects.
Exit status: 0 valid, 1 findings, 2 usage or environment error.

Usage:
  python -X utf8 validate_tour.py <tour> [--repo-root DIR] [--persona NAME] [--json]

The persona budget comes from --persona, else a top-level "persona" key in the tour,
else the file-name prefix (`<persona>-<focus>.tour`). With none, the budget check is
skipped and reported as NOT_ASSESSED. Budgets mirror the Workflow table in
`doc-architect/references/code-tour.md`.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

PERSONA_BUDGETS: dict[str, tuple[int, int]] = {
    "new-joiner": (9, 13),
    "vibecoder": (5, 8),
    "architect": (14, 18),
    "pr-reviewer": (7, 11),
    "rca-investigator": (7, 11),
    "security-reviewer": (7, 11),
    "feature-explainer": (7, 11),
    "bug-fixer": (7, 11),
}


@dataclass
class Finding:
    code: str
    step: int | None
    message: str

    def render(self) -> str:
        where = f"step {self.step}" if self.step is not None else "tour"
        return f"{self.code}: {where}: {self.message}"


class Source:
    """Reads files either from disk or from a git revision."""

    def __init__(self, root: Path, ref: str | None):
        self.root = root
        self.ref = ref

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "--no-replace-objects", "-C", str(self.root), *args],
            capture_output=True,
        )

    def ref_resolves(self) -> bool:
        if self.ref is None:
            return True
        return self._git("rev-parse", "--verify", "--quiet", f"{self.ref}^{{commit}}").returncode == 0

    def kind(self, rel: str) -> str | None:
        """Return 'file', 'dir' or None."""
        if self.ref is None:
            p = self.root / rel
            if p.is_file():
                return "file"
            if p.is_dir():
                return "dir"
            return None
        res = self._git("cat-file", "-t", f"{self.ref}:{rel}")
        if res.returncode != 0:
            return None
        t = res.stdout.decode().strip()
        return {"blob": "file", "tree": "dir"}.get(t)

    def text(self, rel: str) -> str:
        if self.ref is None:
            return (self.root / rel).read_text(encoding="utf-8", errors="replace")
        res = self._git("cat-file", "-p", f"{self.ref}:{rel}")
        return res.stdout.decode("utf-8", errors="replace")


def line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def safe_rel(path: str) -> str | None:
    p = path.replace("\\", "/")
    if p.startswith("/") or re.match(r"^[A-Za-z]:", p):
        return None
    parts = PurePosixPath(p).parts
    if any(part == ".." for part in parts):
        return None
    return str(PurePosixPath(*parts)) if parts else None


def persona_for(tour: dict, tour_path: Path, override: str | None) -> str | None:
    if override:
        return override
    if isinstance(tour.get("persona"), str):
        return tour["persona"]
    stem = tour_path.stem
    for name in sorted(PERSONA_BUDGETS, key=len, reverse=True):
        if stem == name or stem.startswith(name + "-"):
            return name
    return None


def validate(tour_path: Path, repo_root: Path, persona: str | None = None) -> tuple[list[Finding], list[str]]:
    notes: list[str] = []
    try:
        tour = json.loads(tour_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [Finding("tour/invalid-json", None, str(exc))], notes
    if not isinstance(tour, dict) or not isinstance(tour.get("steps"), list) or not tour["steps"]:
        return [Finding("tour/invalid-json", None, "expected an object with a non-empty 'steps' list")], notes

    ref = tour.get("ref") if isinstance(tour.get("ref"), str) and tour.get("ref").strip() else None
    source = Source(repo_root, ref)
    findings: list[Finding] = []
    if not source.ref_resolves():
        return [Finding("tour/bad-ref", None, f"ref {ref!r} does not resolve in {repo_root}")], notes

    steps = tour["steps"]
    first = steps[0] if isinstance(steps[0], dict) else {}
    if not (first.get("file") or first.get("directory")):
        findings.append(Finding("tour/unanchored-first-step", 1, "the first step must be anchored to a file or directory"))

    missing_code = "tour/absent-at-ref" if ref else "tour/missing-file"
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            findings.append(Finding("tour/invalid-json", index, "step must be an object"))
            continue
        target = step.get("file") or step.get("directory")
        if not target:
            continue
        rel = safe_rel(str(target))
        if rel is None:
            findings.append(Finding(missing_code, index, f"path {target!r} is absolute or escapes the repository"))
            continue
        kind = source.kind(rel)
        wanted = "file" if step.get("file") else "dir"
        if kind != wanted:
            where = f"at ref {ref!r}" if ref else "on disk"
            findings.append(Finding(missing_code, index, f"{wanted} {rel!r} not found {where}"))
            continue
        if wanted != "file":
            continue
        text = source.text(rel)
        total = line_count(text)
        if "line" in step:
            line = step["line"]
            if not isinstance(line, int) or line < 1 or line > total:
                findings.append(Finding("tour/line-out-of-range", index, f"line {line!r} outside 1..{total} in {rel}"))
        sel = step.get("selection")
        if isinstance(sel, dict):
            try:
                start = int(sel["start"]["line"])
                end = int(sel["end"]["line"])
            except (KeyError, TypeError, ValueError):
                findings.append(Finding("tour/line-out-of-range", index, f"malformed selection in {rel}"))
            else:
                if start < 1 or end > total or start > end:
                    findings.append(Finding("tour/line-out-of-range", index, f"selection {start}-{end} outside 1..{total} in {rel}"))
        if isinstance(step.get("pattern"), str):
            try:
                if not re.search(step["pattern"], text, re.MULTILINE):
                    findings.append(Finding("tour/pattern-not-found", index, f"pattern {step['pattern']!r} not found in {rel}"))
            except re.error as exc:
                findings.append(Finding("tour/pattern-not-found", index, f"invalid pattern: {exc}"))

    name = persona_for(tour, tour_path, persona)
    if name is None:
        notes.append("budget: NOT_ASSESSED (no persona declared)")
    elif name not in PERSONA_BUDGETS:
        notes.append(f"budget: NOT_ASSESSED (unknown persona {name!r})")
    else:
        low, high = PERSONA_BUDGETS[name]
        if not low <= len(steps) <= high:
            findings.append(Finding("tour/step-count-out-of-budget", None, f"{len(steps)} steps; persona {name} allows {low}-{high}"))
        else:
            notes.append(f"budget: {len(steps)} steps within {name} {low}-{high}")
    return findings, notes


def default_root() -> Path:
    res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(res.stdout.strip()) if res.returncode == 0 and res.stdout.strip() else Path.cwd()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate a CodeTour .tour file.")
    ap.add_argument("tour", type=Path)
    ap.add_argument("--repo-root", type=Path, default=None, help="Repository the tour describes (default: git top level of the current directory).")
    ap.add_argument("--persona", default=None, help="Persona whose step budget applies.")
    ap.add_argument("--json", action="store_true", help="Print a JSON report.")
    args = ap.parse_args(argv)
    if not args.tour.is_file():
        print(f"usage error: tour file not found: {args.tour}", file=sys.stderr)
        return 2
    root = (args.repo_root or default_root()).resolve()
    if not root.is_dir():
        print(f"usage error: repo root not found: {root}", file=sys.stderr)
        return 2
    findings, notes = validate(args.tour, root, args.persona)
    if args.json:
        print(json.dumps({
            "tour": str(args.tour),
            "status": "FAIL" if findings else "PASS",
            "findings": [{"code": f.code, "step": f.step, "message": f.message} for f in findings],
            "notes": notes,
        }, indent=2))
    else:
        for f in findings:
            print(f.render())
        for n in notes:
            print(n)
        print(f"validate-tour: {'FAIL' if findings else 'PASS'} ({len(findings)} finding(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
