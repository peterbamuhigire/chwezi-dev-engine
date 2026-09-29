#!/usr/bin/env python3
"""
Repository-grade validator for portable skills.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


def _find_repo_root() -> Path:
    """Return the engine root that holds this skill, whatever its depth.

    Engine copies of this script are byte-identical mirrors of the canonical
    chwezi-dev-engine file, so the root is found by walking up to the first
    directory with a ``.git`` entry or an ``AGENTS.md`` router instead of a
    fixed ``parents[n]`` depth.
    """
    here = Path(__file__).resolve()
    for parent in here.parents[1:]:
        if (parent / ".git").exists() or (parent / "AGENTS.md").is_file():
            return parent
    return here.parents[min(4, len(here.parents) - 1)]


REPO_ROOT = _find_repo_root()
ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
REQUIRED_SECTIONS = [
    "Use When",
    "Do Not Use When",
    "Required Inputs",
    "Workflow",
    "Quality Standards",
    "Anti-Patterns",
    "Outputs",
    "References",
]
MAX_MARKDOWN_LINES = 500
DUAL_COMPAT_START = "<!-- dual-compat-start -->"
DUAL_COMPAT_END = "<!-- dual-compat-end -->"
NONPORTABLE_SNIPPETS = {
    ".github/copilot-instructions.md": "Do not reference unavailable repo-local Copilot instructions.",
    "chat.customAgentInSubagent.enabled": "Do not require VS Code-specific settings in portable skills.",
    "latest VS Code Insiders build": "Do not require a specific editor build in portable skills.",
}

# Tier-1 lint refinements (M10-03-T12). The four rules are adapted from
# addyosmani/agent-skills (MIT, https://github.com/addyosmani/agent-skills,
# commit 2686b62), scripts/lib/skill-lint.js; paraphrased, not copied.
#
# Exemptions live HERE, in the validator, never in skill frontmatter, so a
# contributor cannot switch a rule off by editing their own skill. Each entry
# maps a skill name to {rule: written reason}. Rules: "sections",
# "use-when", "host-yaml", "narration".
EXEMPTIONS: dict[str, dict[str, str]] = {}
# Frontmatter keys that would let a skill exempt itself; always an error.
SELF_EXEMPTION_KEYS = {"exempt", "exemptions", "lint_exempt", "lint-exempt", "skip_validation", "skip-validation", "validator_exemptions"}
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
NEGATED_TRIGGER_RE = re.compile(
    r"\b(?:do\s+not|don't|never|not)\s+(?:use|load|invoke|apply)\s+(?:this(?:\s+skill)?\s+)?(?:when|for|if|to)\b[^.;]*[.;]?",
    re.IGNORECASE,
)
# SP-14: a description that narrates the workflow (step counts, sequencing,
# "runs ...") invites an agent to follow the description instead of reading
# the body. Adapted from obra/superpowers (MIT, https://github.com/obra/superpowers,
# commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d); paraphrased, not copied.
NARRATION_PATTERNS = (
    (re.compile(r"\b(?:\d+|two|three|four|five|six|seven|eight|nine|ten)[- ](?:step|phase|stage|pass)s?\b", re.IGNORECASE), "step or phase count"),
    (re.compile(r"\bstep\s+\d+\b", re.IGNORECASE), "numbered step"),
    (re.compile(r"\bthen\b", re.IGNORECASE), "sequencing word 'then'"),
    (re.compile(r"\bruns\b", re.IGNORECASE), "'runs ...' narration"),
)


def is_exempt(skill_name: str, rule: str) -> bool:
    return rule in EXEMPTIONS.get(skill_name, {})


def strip_fenced_code(text: str) -> str:
    """Remove CommonMark fenced code blocks (``` or ~~~, closing fence of the same
    character and at least the opening length; an unclosed fence runs to the end)."""
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        if fence is None:
            match = FENCE_OPEN_RE.match(line)
            if match and not (match.group(1)[0] == "`" and "`" in match.group(2)):
                fence = match.group(1)
                continue
            kept.append(line)
        else:
            stripped = line.strip()
            if (
                len(line) - len(line.lstrip(" ")) <= 3
                and stripped
                and set(stripped) == {fence[0]}
                and len(stripped) >= len(fence)
            ):
                fence = None
    return "\n".join(kept)


def strip_negated_triggers(description: str) -> str:
    return " ".join(NEGATED_TRIGGER_RE.sub(" ", description).split())


def frontmatter_block(content: str) -> str | None:
    match = re.match(r"^﻿?---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    return match.group(1) if match else None


def host_yaml_errors(frontmatter_text: str) -> list[str]:
    """Reject frontmatter a strict YAML host would refuse even if PyYAML accepts it:
    tab indentation, an unclosed quote, or an unquoted ': ' inside a plain scalar."""
    errors: list[str] = []
    lines = frontmatter_text.splitlines()
    for number, line in enumerate(lines, start=1):
        indent = line[: len(line) - len(line.lstrip(" \t"))]
        if "\t" in indent:
            errors.append(f"Frontmatter line {number} is indented with a tab; strict YAML hosts reject it.")
        match = re.match(r"^\s*(?:-\s+)?[A-Za-z0-9_-]+:\s+(.*)$", line)
        if not match:
            continue
        value = match.group(1).rstrip()
        if not value or value[0] in "|>[{&*!#":
            continue
        if value[0] in "\"'":
            quote = value[0]
            body = value[1:].replace(quote * 2, "") if quote == "'" else re.sub(r"\\.", "", value[1:])
            if quote not in body:
                closed = any(quote in later for later in lines[number:])
                if not closed:
                    errors.append(f"Frontmatter line {number} opens a {quote} quote that is never closed.")
            continue
        if re.search(r":\s", value) and not value.lstrip().startswith("#"):
            errors.append(f"Frontmatter line {number} has an unquoted ': ' in a plain value; quote the value for strict YAML hosts.")
    return errors


def narration_warnings(description: str) -> list[str]:
    found = [label for pattern, label in NARRATION_PATTERNS if pattern.search(description)]
    if not found:
        return []
    return [
        "Description narrates the workflow (" + ", ".join(found) + "). An agent may follow the "
        "description instead of reading the body; keep the description to when to use the skill "
        "and move the procedure into the body (SP-14)."
    ]


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path.name} is not valid UTF-8: {exc}") from exc


def parse_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter found")

    match = re.match(r"^---\n(.*?)\n---\n?", content, re.DOTALL)
    if not match:
        raise ValueError("Invalid frontmatter format")

    frontmatter_text = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in frontmatter: {exc}") from exc

    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must be a YAML dictionary")

    body = content[match.end() :]
    return frontmatter, body


def line_count(text: str) -> int:
    return len(text.splitlines())


def iter_markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def is_external_link(target: str) -> bool:
    return (
        "://" in target
        or target.startswith("mailto:")
        or target.startswith("#")
    )


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0].strip()


def validate_frontmatter(frontmatter: dict, skill_dir: Path, errors: list[str]) -> None:
    unexpected = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        errors.append(
            "Unexpected key(s) in SKILL.md frontmatter: "
            + ", ".join(sorted(unexpected))
        )

    name = frontmatter.get("name")
    if name is None:
        errors.append("Missing `name` in frontmatter.")
    elif not isinstance(name, str):
        errors.append(f"`name` must be a string, got {type(name).__name__}.")
    else:
        stripped = name.strip()
        if stripped != skill_dir.name:
            errors.append(f"`name` must match the directory name `{skill_dir.name}`.")
        if not re.fullmatch(r"[a-z0-9-]+", stripped or ""):
            errors.append("`name` must use hyphen-case.")
        if stripped.startswith("-") or stripped.endswith("-") or "--" in stripped:
            errors.append("`name` cannot start/end with `-` or contain `--`.")
        if len(stripped) > 64:
            errors.append("`name` exceeds 64 characters.")

    description = frontmatter.get("description")
    if description is None:
        errors.append("Missing `description` in frontmatter.")
    elif not isinstance(description, str):
        errors.append(f"`description` must be a string, got {type(description).__name__}.")
    else:
        stripped = description.strip()
        if not stripped:
            errors.append("`description` must not be empty.")
        if "<" in stripped or ">" in stripped:
            errors.append("`description` cannot contain angle brackets.")
        if len(stripped) > 350:
            errors.append("`description` exceeds the repository limit of 350 characters.")
        skill_name = name.strip() if isinstance(name, str) else ""
        if not is_exempt(skill_name, "use-when"):
            if not stripped.lower().startswith("use when"):
                errors.append("`description` must start with 'Use when'.")
            else:
                # Negated clauses ("do not use when ...") are stripped globally
                # first, so they can never supply the positive trigger.
                positive = strip_negated_triggers(stripped)
                trigger = re.match(r"(?i)use when\w*\b[\s:,-]*(.*)", positive)
                if not trigger or not re.search(r"[A-Za-z0-9]", trigger.group(1)):
                    errors.append("`description` has no positive 'Use when' trigger once negated clauses are removed.")

    self_exempt = SELF_EXEMPTION_KEYS & set(frontmatter.keys())
    metadata_for_keys = frontmatter.get("metadata")
    if isinstance(metadata_for_keys, dict):
        self_exempt |= SELF_EXEMPTION_KEYS & set(metadata_for_keys.keys())
    if self_exempt:
        errors.append(
            "Validator exemptions cannot be declared in skill frontmatter ("
            + ", ".join(sorted(self_exempt))
            + "); they live in quick_validate.py EXEMPTIONS with a written reason."
        )

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("`metadata` must exist and be a mapping for portable skills.")
        return

    if metadata.get("portable") is not True:
        errors.append("`metadata.portable` must be `true`.")

    compatible = metadata.get("compatible_with")
    if not (
        isinstance(compatible, list)
        and all(isinstance(item, str) and item.strip() for item in compatible)
        and len(compatible) == len(set(compatible))
        and {"claude-code", "codex"} <= set(compatible)
    ):
        errors.append("`metadata.compatible_with` must list unique runtime names including 'claude-code' and 'codex'.")

    invocation = metadata.get("invocation", "implicit")
    if invocation not in {"implicit", "explicit", "both"}:
        errors.append("`metadata.invocation` must be one of: implicit, explicit, both.")

    if invocation == "explicit":
        description = str(frontmatter.get("description", "")).lower()
        if "explicit" not in description and "direct user" not in description:
            errors.append("Explicit-invocation skills must state the direct/explicit user trigger in `description`.")


def validate_portable_sections(frontmatter: dict, body: str, errors: list[str]) -> None:
    if DUAL_COMPAT_START not in body or DUAL_COMPAT_END not in body:
        errors.append("Portable contract markers are missing.")
        return

    if not re.search(
        rf"{re.escape(DUAL_COMPAT_START)}.*?{re.escape(DUAL_COMPAT_END)}",
        body,
        re.DOTALL,
    ):
        errors.append("Portable contract markers are malformed.")
        return
    metadata = frontmatter.get("metadata")
    metadata = metadata if isinstance(metadata, dict) else {}
    name = frontmatter.get("name")
    if isinstance(name, str) and is_exempt(name.strip(), "sections"):
        return
    # Headings inside fenced code are examples, not sections (CommonMark fences).
    body = strip_fenced_code(body)
    groups = {
        "Use When": (["Use When"], "use_when"),
        "Do Not Use When": (["Do Not Use When", "Degraded mode"], "do_not_use_when"),
        "Required Inputs": (["Required Inputs", "Inputs"], "required_inputs"),
        "Workflow": (["Workflow", "Operating contract", "Decision rules"], "workflow"),
        "Quality Standards": (["Quality Standards", "Capability contract", "Capability and permission boundaries", "Non-negotiables"], "quality_standards"),
        "Anti-Patterns": (["Anti-Patterns", "Domain anti-patterns"], "anti_patterns"),
        "Outputs": (["Outputs"], "outputs"),
        "References": (["References", "Read next", "Companion Skills", "Companion skills"], "references"),
    }
    for section, (aliases, metadata_key) in groups.items():
        heading_exists = any(
            re.search(rf"^##\s+{re.escape(alias)}\s*$", body, re.MULTILINE | re.IGNORECASE)
            for alias in aliases
        )
        if not heading_exists and not metadata.get(metadata_key):
            errors.append(f"Portable contract element missing: `{section}`.")


def validate_markdown_file(path: Path, errors: list[str]) -> None:
    text = read_utf8(path)
    count = line_count(text)
    if path.name == "SKILL.md" and count > MAX_MARKDOWN_LINES:
        errors.append(
            f"{path.relative_to(REPO_ROOT)} exceeds {MAX_MARKDOWN_LINES} lines ({count})."
        )

    if "\ufffd" in text:
        errors.append(
            f"{path.relative_to(REPO_ROOT)} contains replacement characters."
        )


def validate_local_links(skill_dir: Path, skill_md: Path, body: str, errors: list[str]) -> None:
    for target in iter_markdown_links(body):
        clean = strip_anchor(target)
        if not clean or is_external_link(clean):
            continue

        resolved = (skill_md.parent / clean).resolve()
        try:
            resolved.relative_to(REPO_ROOT.resolve())
        except ValueError:
            if not resolved.exists():
                errors.append(f"External local link does not exist: `{target}`.")
            continue

        if not resolved.exists():
            errors.append(f"Broken local link: `{target}`.")

    for snippet, reason in NONPORTABLE_SNIPPETS.items():
        if snippet in body:
            errors.append(f"Nonportable content `{snippet}` found. {reason}")


def validate_skill(skill_path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    skill_path = skill_path.resolve()
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return False, ["SKILL.md not found."]

    try:
        raw = read_utf8(skill_md)
    except ValueError as exc:
        return False, [str(exc)]

    try:
        frontmatter, body = parse_frontmatter(raw)
    except ValueError as exc:
        return False, [str(exc)]

    validate_frontmatter(frontmatter, skill_path, errors)
    skill_name = str(frontmatter.get("name") or "").strip()
    block = frontmatter_block(raw)
    if block is not None and not is_exempt(skill_name, "host-yaml"):
        errors.extend(host_yaml_errors(block))
    validate_portable_sections(frontmatter, body, errors)
    validate_local_links(skill_path, skill_md, body, errors)

    for md_file in sorted(skill_path.rglob("*.md")):
        try:
            validate_markdown_file(md_file, errors)
        except ValueError as exc:
            errors.append(str(exc))

    return not errors, errors


def collect_warnings(skill_path: Path) -> list[str]:
    """Advisory findings that never change the exit status (SP-14 narration lint)."""
    skill_md = Path(skill_path).resolve() / "SKILL.md"
    try:
        frontmatter, _body = parse_frontmatter(read_utf8(skill_md))
    except (OSError, ValueError):
        return []
    description = frontmatter.get("description")
    name = str(frontmatter.get("name") or "").strip()
    if not isinstance(description, str) or is_exempt(name, "narration"):
        return []
    return narration_warnings(description)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -X utf8 quick_validate.py <skill_directory>")
        return 1

    skill_dir = Path(sys.argv[1])
    valid, errors = validate_skill(skill_dir)
    for warning in collect_warnings(skill_dir):
        print(f"WARNING: {warning}")
    if valid:
        print("Skill is valid.")
        return 0

    print("Skill validation failed:")
    for error in errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
