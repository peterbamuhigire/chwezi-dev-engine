#!/usr/bin/env python3
"""
Repository-level guardrails for the active skills catalog.

This script intentionally does not move, delete, or rewrite skills. It scans the
active catalog roots and reports loader risks that matter during consolidation.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACTIVE_ROOTS = (
    "skills",
    "00-meta-initialization",
)
DEFAULT_REFERENCE_ROOTS = (
    "doctrine/skills",
)
DEFAULT_EXTERNAL_ENGINE_ROOTS: tuple[str, ...] = ()
DEFAULT_MAX_ACTIVE_SKILLS = 200
MAX_DESCRIPTION_CHARS = 1024
MAX_SKILL_MD_LINES = 500
FRONTMATTER_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
ALIASES_YML = REPO_ROOT / "docs" / "skill-aliases.yml"

# Relative resource references a SKILL.md may point at (deep-dive material the
# skill tells the agent to load on demand). A broken one means the skill
# promises depth it cannot deliver.
RESOURCE_REF_RE = re.compile(
    r"(?:\]\(|`)((?:\./)?(?:references|templates|scripts|assets|examples)/[^)`\s]+)"
)
# Template/illustrative references (e.g. references/*.md, references/<topic>.md)
# are documentation examples inside meta-skills, not real targets.
PLACEHOLDER_REF_RE = re.compile(r"[*<>]")


@dataclass(frozen=True)
class SkillRecord:
    path: Path
    relpath: Path
    line_count: int
    frontmatter: dict | None

    @property
    def name(self) -> str | None:
        if not isinstance(self.frontmatter, dict):
            return None
        value = self.frontmatter.get("name")
        return value.strip() if isinstance(value, str) else None

    @property
    def description(self) -> str | None:
        if not isinstance(self.frontmatter, dict):
            return None
        value = self.frontmatter.get("description")
        return value if isinstance(value, str) else None


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: Path | None
    message: str

    def format(self) -> str:
        location = f" {self.path}" if self.path is not None else ""
        return f"[{self.severity.upper()}] {self.code}:{location} {self.message}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check repository-level skill catalog guardrails."
    )
    parser.add_argument(
        "--root",
        action="append",
        dest="roots",
        help=(
            "Active catalog root relative to the repository root. "
            "May be supplied more than once. Defaults to skills and "
            "00-meta-initialization. doctrine/skills is retained reference "
            "material, not part of this engine's active catalog."
        ),
    )
    parser.add_argument(
        "--max-active",
        type=int,
        default=DEFAULT_MAX_ACTIVE_SKILLS,
        help=f"Maximum active SKILL.md files allowed. Default: {DEFAULT_MAX_ACTIVE_SKILLS}.",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Print findings but exit 0. Useful before the catalog is below the cap.",
    )
    return parser.parse_args()


def active_roots(root_args: list[str] | None) -> list[Path]:
    roots = root_args if root_args else list(DEFAULT_ACTIVE_ROOTS)
    resolved: list[Path] = []
    for raw in roots:
        path = (REPO_ROOT / raw).resolve()
        if path.exists():
            resolved.append(path)
    return resolved


def reference_roots() -> list[Path]:
    resolved: list[Path] = []
    for raw in DEFAULT_REFERENCE_ROOTS + DEFAULT_EXTERNAL_ENGINE_ROOTS:
        candidate = Path(raw)
        path = candidate.resolve() if candidate.is_absolute() else (REPO_ROOT / candidate).resolve()
        if path.exists():
            resolved.append(path)
    return resolved


def iter_skill_files(roots: Iterable[Path]) -> list[Path]:
    paths: dict[Path, None] = {}
    for root in roots:
        for skill_md in root.rglob("SKILL.md"):
            if any(part.startswith(".") for part in skill_md.relative_to(root).parts):
                continue
            paths[skill_md.resolve()] = None
    return sorted(paths)


def relpath(path: Path) -> Path:
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        return path


def read_skill(path: Path) -> tuple[str | None, Finding | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError as exc:
        return None, Finding(
            "error",
            "utf8",
            relpath(path),
            f"SKILL.md is not valid UTF-8: {exc}",
        )


def parse_frontmatter(path: Path, content: str) -> tuple[dict | None, Finding | None]:
    match = FRONTMATTER_RE.match(content)
    if match is None:
        return None, Finding(
            "error",
            "frontmatter",
            relpath(path),
            "missing or malformed YAML frontmatter",
        )

    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, Finding(
            "error",
            "frontmatter-yaml",
            relpath(path),
            f"invalid YAML frontmatter: {exc}",
        )

    if not isinstance(parsed, dict):
        return None, Finding(
            "error",
            "frontmatter",
            relpath(path),
            "frontmatter must be a YAML mapping",
        )

    return parsed, None


def collect_records(paths: list[Path]) -> tuple[list[SkillRecord], list[Finding]]:
    records: list[SkillRecord] = []
    findings: list[Finding] = []

    for path in paths:
        content, read_error = read_skill(path)
        if read_error is not None:
            findings.append(read_error)
            continue
        assert content is not None

        frontmatter, fm_error = parse_frontmatter(path, content)
        if fm_error is not None:
            findings.append(fm_error)

        record = SkillRecord(
            path=path,
            relpath=relpath(path),
            line_count=len(content.splitlines()),
            frontmatter=frontmatter,
        )
        records.append(record)

    return records, findings


def check_count(records: list[SkillRecord], max_active: int) -> list[Finding]:
    if len(records) <= max_active:
        return []
    return [
        Finding(
            "error",
            "active-count",
            None,
            f"{len(records)} active SKILL.md files exceeds cap {max_active}",
        )
    ]


def check_duplicate_names(records: list[SkillRecord]) -> list[Finding]:
    by_name: dict[str, list[SkillRecord]] = defaultdict(list)
    for record in records:
        if record.name:
            by_name[record.name].append(record)

    findings: list[Finding] = []
    for name, duplicates in sorted(by_name.items()):
        if len(duplicates) < 2:
            continue
        paths = ", ".join(str(record.relpath) for record in duplicates)
        findings.append(
            Finding(
                "error",
                "duplicate-name",
                None,
                f"frontmatter name `{name}` appears in {paths}",
            )
        )
    return findings


def check_descriptions(records: list[SkillRecord]) -> list[Finding]:
    findings: list[Finding] = []
    for record in records:
        description = record.description
        if description is None:
            continue
        length = len(description.strip())
        if length > MAX_DESCRIPTION_CHARS:
            findings.append(
                Finding(
                    "error",
                    "description-length",
                    record.relpath,
                    f"description is {length} characters; max is {MAX_DESCRIPTION_CHARS}",
                )
            )
    return findings


def check_line_counts(records: list[SkillRecord]) -> list[Finding]:
    findings: list[Finding] = []
    for record in records:
        if record.line_count > MAX_SKILL_MD_LINES:
            findings.append(
                Finding(
                    "error",
                    "skill-lines",
                    record.relpath,
                    f"SKILL.md has {record.line_count} lines; max is {MAX_SKILL_MD_LINES}",
                )
            )
    return findings


def check_broken_references(roots: list[Path]) -> list[Finding]:
    """Flag SKILL.md links to references/templates/scripts that do not exist.

    A skill that tells the agent to load `references/foo.md` when that file is
    absent is a silent dead end: the agent loads nothing and the promised depth
    never arrives. This is the decay that catalog reorganisations introduce.
    """
    findings: list[Finding] = []
    for root in roots:
        for skill_md in root.rglob("SKILL.md"):
            if any(part.startswith(".") for part in skill_md.relative_to(root).parts):
                continue
            try:
                text = skill_md.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue  # reported by check via read_skill elsewhere
            seen: set[str] = set()
            for match in RESOURCE_REF_RE.finditer(text):
                ref = match.group(1).lstrip("./")
                if ref in seen or PLACEHOLDER_REF_RE.search(ref):
                    continue
                seen.add(ref)
                if not (skill_md.parent / ref).exists():
                    findings.append(
                        Finding(
                            "error",
                            "broken-reference",
                            relpath(skill_md),
                            f"references `{ref}` which does not exist",
                        )
                    )
    return findings


def check_alias_integrity(records: list[SkillRecord]) -> list[Finding]:
    """Keep ALIAS.md files and the alias registry in lockstep.

    Three failure modes: an ALIAS.md on disk with no registry route, a registry
    route with no ALIAS.md on disk (stale alias), and a route whose target skill
    no longer exists (dangling redirect).
    """
    findings: list[Finding] = []
    if not ALIASES_YML.exists():
        return [
            Finding("error", "alias-registry", relpath(ALIASES_YML), "alias registry is missing")
        ]
    try:
        registry = yaml.safe_load(ALIASES_YML.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [Finding("error", "alias-registry-yaml", relpath(ALIASES_YML), f"invalid YAML: {exc}")]

    routes: dict[str, str] = registry.get("inactive_skill_aliases", {}) or {}
    external_prefixes: dict[str, str] = registry.get("external_target_prefixes", {}) or {}
    on_disk = {p.parent.relative_to(REPO_ROOT).as_posix() for p in REPO_ROOT.rglob("ALIAS.md")}
    in_registry = set(routes)

    for orphan in sorted(on_disk - in_registry):
        findings.append(
            Finding("error", "alias-unrouted", Path(orphan), "ALIAS.md exists but has no route in skill-aliases.yml")
        )
    for stale in sorted(in_registry - on_disk):
        findings.append(
            Finding("error", "alias-stale", Path(stale), "registry route has no ALIAS.md on disk")
        )

    skill_dir_names = {r.path.parent.name for r in records}
    skill_dir_paths = {r.path.parent.relative_to(REPO_ROOT).as_posix() for r in records}
    retained_dir_names: set[str] = set()
    retained_dir_paths: set[str] = set()
    for root in reference_roots():
        for skill_md in root.rglob("SKILL.md"):
            retained_dir_names.add(skill_md.parent.name)
            try:
                retained_dir_paths.add(skill_md.parent.relative_to(REPO_ROOT).as_posix())
            except ValueError:
                retained_dir_paths.add(skill_md.parent.as_posix())

    for src, target in sorted(routes.items()):
        target = str(target).strip()
        target_slug = Path(target.replace("\\", "/")).name
        resolves = (
            target in skill_dir_paths
            or target in retained_dir_paths
            or (REPO_ROOT / target / "SKILL.md").exists()
            or (("/" not in target) and target in skill_dir_names)
            or target_slug in retained_dir_names
            or any(
                target == prefix.rstrip("/") or target.startswith(prefix.rstrip("/") + "/")
                for prefix in external_prefixes
            )
        )
        if not resolves:
            findings.append(
                Finding(
                    "error",
                    "alias-dangling",
                    Path(src),
                    f"routes to `{target}` which is not an active or retained reference skill",
                )
            )
    return findings


def main() -> int:
    args = parse_args()
    roots = active_roots(args.roots)
    paths = iter_skill_files(roots)
    records, findings = collect_records(paths)

    findings.extend(check_count(records, args.max_active))
    findings.extend(check_duplicate_names(records))
    findings.extend(check_descriptions(records))
    findings.extend(check_line_counts(records))
    findings.extend(check_broken_references(roots))
    findings.extend(check_alias_integrity(records))

    print("skill-catalog-guardrails:")
    print(f"- repo: {REPO_ROOT}")
    print("- active roots:")
    for root in roots:
        print(f"  - {relpath(root)}")
    print("- retained reference roots:")
    for root in reference_roots():
        print(f"  - {relpath(root)}")
    print(f"- active SKILL.md files: {len(records)}")
    print(f"- max active SKILL.md files: {args.max_active}")
    print(f"- findings: {len(findings)}")

    for finding in findings:
        print(finding.format())

    if findings and not args.report_only:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
