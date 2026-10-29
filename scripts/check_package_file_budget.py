#!/usr/bin/env python3
"""Measure repository and package-oriented file entries against the 5,000 cap."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

PACKAGE_EXCLUSIONS = {".git", ".cache", "cache", "__pycache__", "node_modules", ".venv", "venv"}
LIMIT = 5000


def counts(root: Path) -> tuple[int, int]:
    checkout = package = 0
    walk_errors: list[OSError] = []
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_errors.append):
        current = Path(directory)
        # Count symlink entries, but do not traverse a symlink directory.
        linked_dirs = [name for name in dirs if (current / name).is_symlink()]
        for name in linked_dirs:
            checkout += 1
            parts = (current / name).relative_to(root).parts
            if not any(part in PACKAGE_EXCLUSIONS for part in parts):
                package += 1
        dirs[:] = [name for name in dirs if name not in linked_dirs]
        for name in files:
            checkout += 1
            parts = (current / name).relative_to(root).parts
            if not any(part in PACKAGE_EXCLUSIONS for part in parts):
                package += 1
    if walk_errors:
        raise OSError(f"could not count all entries under {root}: {walk_errors[0]}")
    return checkout, package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        checkout, package = counts(args.root.resolve())
    except OSError as exc:
        print(f"FAIL: could not count all entries: {exc}")
        return 1
    print(f"checkout entries (including .git): {checkout}")
    print(f"package-oriented entries (documented exclusions): {package}")
    if checkout > LIMIT or package > LIMIT:
        print(f"FAIL: each count must be at most {LIMIT}")
        return 1
    print(f"PASS: both counts are at most {LIMIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
