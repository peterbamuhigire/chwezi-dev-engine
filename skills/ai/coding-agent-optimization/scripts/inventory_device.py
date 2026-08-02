#!/usr/bin/env python3
"""Emit a secret-free, read-only profile for coding-agent optimisation."""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def memory_bytes() -> int | None:
    """Return physical memory without importing a third-party package."""
    if os.name == "nt":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.c_ulong),
                ("memory_load", ctypes.c_ulong),
                ("total", ctypes.c_ulonglong),
                ("available", ctypes.c_ulonglong),
                ("total_page_file", ctypes.c_ulonglong),
                ("available_page_file", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong),
                ("available_virtual", ctypes.c_ulonglong),
                ("available_extended", ctypes.c_ulonglong),
            ]

        status = MemoryStatus()
        status.length = ctypes.sizeof(MemoryStatus)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return int(status.total)
        return None

    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        return int(pages * page_size)
    except (AttributeError, OSError, ValueError):
        return None


def version_for(executable: str) -> dict[str, Any]:
    """Discover an executable and run only its version probe."""
    path = shutil.which(executable)
    result: dict[str, Any] = {"available": bool(path), "path": path}
    if not path:
        return result
    try:
        completed = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=4,
            check=False,
        )
        output = (completed.stdout or completed.stderr).strip().splitlines()
        result["version"] = output[0][:300] if output else None
        result["probe_exit_code"] = completed.returncode
    except (OSError, subprocess.SubprocessError) as error:
        result["probe_error"] = type(error).__name__
    return result


def candidate_path(value: str | None, default: Path) -> Path:
    return Path(value).expanduser() if value else default


def path_metadata(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"path": str(path), "exists": path.exists()}
    if not path.exists():
        return result
    result["kind"] = "directory" if path.is_dir() else "file"
    try:
        result["size_bytes"] = path.stat().st_size if path.is_file() else None
    except OSError:
        result["metadata_error"] = True
    return result


def runner_surfaces() -> dict[str, Any]:
    home = Path.home()
    codex_home = candidate_path(os.environ.get("CODEX_HOME"), home / ".codex")
    claude_home = candidate_path(os.environ.get("CLAUDE_CONFIG_DIR"), home / ".claude")
    return {
        "codex": [
            path_metadata(codex_home),
            path_metadata(codex_home / "config.toml"),
            path_metadata(codex_home / "AGENTS.md"),
            path_metadata(codex_home / "agents"),
        ],
        "claude_code": [
            path_metadata(claude_home),
            path_metadata(home / ".claude.json"),
            path_metadata(claude_home / "CLAUDE.md"),
            path_metadata(claude_home / "settings.json"),
            path_metadata(claude_home / "agents"),
        ],
    }


def build_profile() -> dict[str, Any]:
    logical_cpus = os.cpu_count()
    memory = memory_bytes()
    disk = shutil.disk_usage(Path.cwd())
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python_implementation": platform.python_implementation(),
        },
        "resources": {
            "logical_cpus": logical_cpus,
            "memory_bytes": memory,
            "cwd_disk_free_bytes": disk.free,
        },
        "runners": {
            name: version_for(name)
            for name in ("codex", "claude", "node", "python", "git", "pwsh")
        },
        "environment_paths": {
            key: os.environ.get(key)
            for key in ("CODEX_HOME", "CLAUDE_CONFIG_DIR")
            if os.environ.get(key)
        },
        "configuration_surfaces": runner_surfaces(),
        "secret_policy": "File contents, credentials, tokens, and history were not read.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretty", action="store_true", help="indent the JSON output")
    args = parser.parse_args()
    print(json.dumps(build_profile(), indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
