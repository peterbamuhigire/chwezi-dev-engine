"""Content hygiene checks for the active engine tree.

Used by ``skill_catalog_guardrails.py`` and runnable on its own:

    python scripts/content_hygiene.py machine-paths
    python scripts/content_hygiene.py duplicate-headings
    python scripts/content_hygiene.py broken-links

Each check returns ``(code, relative_path, message)`` tuples so the caller decides
how to report them. Duplicate headings and broken links use a recorded baseline
that may only shrink: a new problem fails, an old problem that was fixed must be
removed from the baseline so the ratchet tightens.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
QUALITY_GATES = REPO_ROOT / "docs" / "quality-gates"
MACHINE_PATH_ALLOWLIST = QUALITY_GATES / "machine-path-allowlist.yml"
HEADING_BASELINE = QUALITY_GATES / "duplicate-heading-baseline.json"
LINK_BASELINE = QUALITY_GATES / "broken-link-baseline.json"

Finding = tuple[str, str, str]

TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".json", ".js", ".sh", ".ps1", ".toml"}
# Dated records of past work keep the paths they were written with.
HISTORICAL_DOCS = (
    "docs/audits", "docs/superpowers", "docs/plans", "docs/updates", "docs/continuous-improvement",
    "docs/engine-upgrade-july-2026", "docs/sept-matt-pocock", "docs/analysis", "docs/game-dev-analysis",
    "docs/engine-status",
)
HISTORICAL_FILES = ("CHANGELOG.md",)
# Folders whose files the machine-path check never reads: test fixtures hold hostile or
# negative-case paths on purpose, and git history is not content.
SKIPPED_DIRS = {".git", "node_modules", "__pycache__", "tests", "benchmarks", ".claude"}

# A host layout, not a teaching example: a drive-rooted WAMP checkout, a real user profile,
# or a markdown link whose target is an absolute local path.
PLACEHOLDER_USERS = r"(?:alice|bob|you|your|user|users|username|youruser|yourname|name|example|jdoe|attacker|arcgis|ubuntu|deploy|www-data|root|runner|public|default|appuser|app)"
MACHINE_PATTERNS = {
    "wamp-path": re.compile(r"[A-Za-z]:[\\/]+wamp64", re.IGNORECASE),
    "windows-profile": re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+(?!" + PLACEHOLDER_USERS + r"\b)[A-Za-z][\w.-]*", re.IGNORECASE),
    "unix-profile": re.compile(r"(?<![\w.])/(?:home|Users)/(?!" + PLACEHOLDER_USERS + r"\b)[A-Za-z][\w.-]*/"),
    "absolute-link": re.compile(r"\]\(((?:/(?:tmp|home|Users|var|mnt|opt)/|[A-Za-z]:[\\/])[^)\s]*)\)"),
}
FENCE = re.compile(r"^\s*(```|~~~)")


def _is_historical(rel: str) -> bool:
    return rel in HISTORICAL_FILES or any(rel == h.rstrip("/") or rel.startswith(h if h.endswith("/") else h + "/") for h in HISTORICAL_DOCS)


def iter_text_files(root: Path = REPO_ROOT, include_historical: bool = False) -> Iterable[Path]:
    """Yield text files in the active tree, skipping caches, fixtures and dated records."""
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root)
        if any(part in SKIPPED_DIRS for part in rel.parts):
            continue
        if not include_historical and _is_historical(rel.as_posix()):
            continue
        yield path


def load_allowlist(path: Path = MACHINE_PATH_ALLOWLIST) -> list[dict]:
    if not path.exists():
        return []
    entries = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("allow") or []
    for entry in entries:
        if not all(str(entry.get(key) or "").strip() for key in ("path", "contains", "reason")):
            raise ValueError(f"allow-list entry needs path, contains and reason: {entry!r}")
    return entries


def check_machine_paths(root: Path = REPO_ROOT, allowlist: list[dict] | None = None) -> list[Finding]:
    """Flag host-specific paths in active content. Allow-listed lines must name a reason."""
    allowed = load_allowlist(root / "docs" / "quality-gates" / "machine-path-allowlist.yml") if allowlist is None else allowlist
    findings: list[Finding] = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            for code, pattern in MACHINE_PATTERNS.items():
                match = pattern.search(line)
                if not match:
                    continue
                if any(entry["path"] == rel and entry["contains"] in line for entry in allowed):
                    continue
                findings.append(("machine-path", rel, f"line {number}: {code} `{match.group(0)[:60]}`; resolve per device or use a placeholder"))
                break
    return findings


def _headings(text: str) -> list[str]:
    """Level-2 headings outside the frontmatter and fenced code, lower-cased."""
    text = re.sub(r"^﻿?---\r?\n.*?\r?\n---\r?\n?", "", text, count=1, flags=re.DOTALL)
    fenced = False
    found: list[str] = []
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = re.match(r"^##\s+(.*?)\s*#*\s*$", line)
        if match:
            found.append(match.group(1).strip().lower())
    return found


def duplicate_headings(root: Path = REPO_ROOT, roots: tuple[str, ...] = ("skills", "00-meta-initialization")) -> dict[str, list[str]]:
    """Map each SKILL.md with an exact duplicate H2 to the sorted duplicated headings."""
    result: dict[str, list[str]] = {}
    for base in roots:
        folder = root / base
        if not folder.exists():
            continue
        for skill in sorted(folder.rglob("SKILL.md")):
            counts: dict[str, int] = {}
            for heading in _headings(skill.read_text(encoding="utf-8", errors="replace")):
                counts[heading] = counts.get(heading, 0) + 1
            dupes = sorted(h for h, n in counts.items() if n > 1)
            if dupes:
                result[skill.relative_to(root).as_posix()] = dupes
    return result


def _load_baseline(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def check_duplicate_headings(root: Path = REPO_ROOT, baseline_path: Path | None = None) -> list[Finding]:
    """Fail on a new duplicate H2 and on a baseline entry that no longer applies (ratchet)."""
    baseline = _load_baseline(baseline_path or root / "docs" / "quality-gates" / "duplicate-heading-baseline.json").get("skills", {})
    current = duplicate_headings(root)
    findings: list[Finding] = []
    for rel, headings in current.items():
        known = set(baseline.get(rel, []))
        new = [h for h in headings if h not in known]
        if new:
            findings.append(("duplicate-heading", rel, "new duplicate H2: " + ", ".join(f"`{h}`" for h in new) + "; merge the sections"))
    for rel, headings in baseline.items():
        gone = [h for h in headings if h not in current.get(rel, [])]
        if gone:
            findings.append(("duplicate-heading-baseline", rel, "fixed or removed, so delete it from the baseline: " + ", ".join(f"`{h}`" for h in gone)))
    return findings


LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def broken_links(root: Path = REPO_ROOT, roots: tuple[str, ...] = ("skills", "00-meta-initialization")) -> dict[str, list[str]]:
    """Map each Markdown file under the active roots to its relative links that do not resolve."""
    result: dict[str, list[str]] = {}
    for base in roots:
        folder = root / base
        if not folder.exists():
            continue
        for md in sorted(folder.rglob("*.md")):
            text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8", errors="replace"), flags=re.DOTALL)
            missing: list[str] = []
            for match in LINK.finditer(text):
                target = match.group(1)
                if re.match(r"^(https?:|mailto:|tel:|#)", target) or PLACEHOLDER.search(target):
                    continue
                file_part = target.split("#", 1)[0].split("?", 1)[0]
                if not file_part or file_part.startswith("/"):
                    continue
                try:
                    destination = (md.parent / file_part).resolve()
                except (OSError, RuntimeError):
                    missing.append(target)
                    continue
                if not destination.exists() and target not in missing:
                    missing.append(target)
            if missing:
                result[md.relative_to(root).as_posix()] = sorted(missing)
    return result


PLACEHOLDER = re.compile(r"[<>{}*$]")


def check_broken_links(root: Path = REPO_ROOT, baseline_path: Path | None = None) -> list[Finding]:
    """Fail on a new broken relative link and on a baseline entry that now resolves (ratchet)."""
    baseline = _load_baseline(baseline_path or root / "docs" / "quality-gates" / "broken-link-baseline.json").get("files", {})
    current = broken_links(root)
    findings: list[Finding] = []
    for rel, targets in current.items():
        new = [t for t in targets if t not in set(baseline.get(rel, []))]
        if new:
            findings.append(("broken-link", rel, "new broken relative link: " + ", ".join(f"`{t}`" for t in new)))
    for rel, targets in baseline.items():
        gone = [t for t in targets if t not in current.get(rel, [])]
        if gone:
            findings.append(("broken-link-baseline", rel, "now resolves or removed, so delete it from the baseline: " + ", ".join(f"`{t}`" for t in gone)))
    return findings


def write_baselines(root: Path = REPO_ROOT) -> None:
    """Record the current duplicate headings and broken links. Run only to shrink the baseline."""
    gates = root / "docs" / "quality-gates"
    (gates / "duplicate-heading-baseline.json").write_text(
        json.dumps({"note": "Exact duplicate H2 headings in active SKILL.md files. This list may only shrink.", "skills": duplicate_headings(root)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (gates / "broken-link-baseline.json").write_text(
        json.dumps({"note": "Relative Markdown links under active skill roots that do not resolve. This list may only shrink.", "files": broken_links(root)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


CHECKS = {
    "machine-paths": check_machine_paths,
    "duplicate-headings": check_duplicate_headings,
    "broken-links": check_broken_links,
}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["write-baselines"]:
        write_baselines()
        print("baselines written")
        return 0
    if len(args) != 1 or args[0] not in CHECKS:
        print(f"usage: content_hygiene.py {{{'|'.join(CHECKS)}|write-baselines}}")
        return 2
    findings = CHECKS[args[0]]()
    for code, rel, message in findings:
        print(f"[FAIL] {code}: {rel}: {message}")
    print(f"- findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
