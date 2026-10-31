"""Resolve sibling engine checkouts without hard-coded drive letters or one layout.

Engine repositories were renamed upstream while some local checkouts kept the old
directory names, and a host may keep engines in more than one parent directory.
This module turns an engine ID plus a list of parent directories into an ordered
list of candidate checkouts:

1. ``SKILL_ENGINE_ROOT_<ID>`` (for example ``SKILL_ENGINE_ROOT_DIGITAL_RESEARCH``)
   names one checkout. When set it is authoritative and no fallback is tried.
2. Otherwise each parent directory is searched, in the order given, for each known
   directory name of the engine (current name first, then former names).

Parent directories come from the command line or from ``CHWEZI_ENGINES_ROOT``
(separated by the platform path separator). No machine-specific path is built in.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Sequence

ENV_ROOTS = "CHWEZI_ENGINES_ROOT"

# engine id -> directory names, current name first, then former or alternative names.
ENGINE_DIR_ALIASES: dict[str, tuple[str, ...]] = {
    "srs": ("chwezi-sdlc-documentation", "srs-skills"),
    "business-plan": ("business-plan-skills",),
    "website": ("website-skills",),
    "social-media": ("social-media-skills",),
    "linux": ("linux-skills",),
    "proposal": ("proposal-skills",),
    "accounting": ("chwezi-accounting-doctrine",),
    "design": ("chwezi-design-engine", "design-system-skills"),
    "digital-research": ("digital-research-engine", "chwezi-research-engine", "digital-research-skills"),
    "chwezi-dev-engine": ("chwezi-dev-engine", "skills-web-dev"),
    "windows-admin": ("windows-admin-engine-skills",),
    "political": ("political-essay-skills", "political-skills"),
}


def env_name(engine_id: str) -> str:
    return f"SKILL_ENGINE_ROOT_{engine_id.upper().replace('-', '_')}"


def env_override(engine_id: str, environ: dict | None = None) -> Path | None:
    value = (environ if environ is not None else os.environ).get(env_name(engine_id))
    return Path(value).expanduser() if value else None


def roots_from_env(environ: dict | None = None) -> list[Path]:
    value = (environ if environ is not None else os.environ).get(ENV_ROOTS, "")
    return [Path(part).expanduser() for part in value.split(os.pathsep) if part.strip()]


def normalise_roots(roots: Path | str | Iterable[Path | str] | None) -> list[Path]:
    """Accept one parent, several, or none; keep order and drop duplicates."""
    if roots is None:
        return []
    if isinstance(roots, (str, os.PathLike)):
        roots = [roots]
    unique: list[Path] = []
    for item in roots:
        path = Path(item).expanduser()
        if path not in unique:
            unique.append(path)
    return unique


def candidates(
    engine_id: str,
    roots: Path | str | Sequence[Path | str] | None,
    environ: dict | None = None,
) -> list[Path]:
    """Ordered candidate checkouts for an engine. An environment override is sole and final."""
    if engine_id not in ENGINE_DIR_ALIASES:
        return []
    override = env_override(engine_id, environ)
    if override is not None:
        return [override]
    found: list[Path] = []
    for root in normalise_roots(roots):
        for name in ENGINE_DIR_ALIASES[engine_id]:
            candidate = root / name
            if candidate not in found:
                found.append(candidate)
    return found


def first_existing(paths: Iterable[Path]) -> Path | None:
    """The first candidate that is a directory. Later candidates are never a fallback for a broken one."""
    for path in paths:
        try:
            if path.is_dir():
                return path
        except OSError:
            return None
    return None
