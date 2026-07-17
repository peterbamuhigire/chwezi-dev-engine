#!/usr/bin/env python3
"""Run a verified, isolated LibreOffice headless conversion on supported desktops."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from shutil import which
from typing import Sequence


DEFAULT_TIMEOUT_SECONDS = 120


class LibreOfficeError(RuntimeError):
    """Raised when LibreOffice cannot safely complete a requested conversion."""


def executable_candidates() -> list[Path]:
    """Return platform-specific LibreOffice locations after PATH has been checked."""
    candidates: list[Path] = []
    if os.name == "nt":
        for variable in ("ProgramFiles", "ProgramFiles(x86)"):
            root = os.environ.get(variable)
            if root:
                candidates.append(Path(root) / "LibreOffice" / "program" / "soffice.exe")
    elif sys.platform == "darwin":
        candidates.append(Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"))
    return candidates


def find_soffice() -> Path | None:
    """Find the LibreOffice launcher without modifying the caller's PATH."""
    command_names = ("soffice.exe", "soffice", "libreoffice") if os.name == "nt" else (
        "soffice",
        "libreoffice",
    )
    for command_name in command_names:
        located = which(command_name)
        if located:
            return Path(located).resolve()

    for candidate in executable_candidates():
        if candidate.is_file():
            return candidate.resolve()
    return None


def user_installation_argument(profile_dir: Path) -> str:
    """Return a standards-compliant file URI for LibreOffice's isolated profile."""
    return "-env:UserInstallation=" + profile_dir.resolve().as_uri()


def output_extension(target_format: str) -> str:
    """Derive an expected extension from LibreOffice's format or filter syntax."""
    extension = target_format.split(":", maxsplit=1)[0].lstrip(".")
    if not extension:
        raise LibreOfficeError("The conversion format must start with an output extension.")
    return extension


def output_tail(value: str | None) -> str:
    """Limit captured process output while retaining the most useful diagnostics."""
    return (value or "")[-4_000:]


def run_conversion(
    soffice: Path,
    input_path: Path,
    output_dir: Path,
    target_format: str,
    timeout_seconds: int,
    profile_dir: Path,
    overwrite: bool,
) -> Path:
    """Convert one document and verify LibreOffice created a non-empty output file."""
    expected_output = output_dir / f"{input_path.stem}.{output_extension(target_format)}"
    if expected_output.exists():
        if not overwrite:
            raise LibreOfficeError(
                f"Refusing to reuse existing output: {expected_output}. "
                "Choose a fresh output directory or pass --overwrite explicitly."
            )
        if not expected_output.is_file():
            raise LibreOfficeError(f"Expected output path is not a regular file: {expected_output}")
        expected_output.unlink()

    command = [
        str(soffice),
        user_installation_argument(profile_dir),
        "--headless",
        "--invisible",
        "--nologo",
        "--nodefault",
        "--nofirststartwizard",
        "--norestore",
        "--convert-to",
        target_format,
        "--outdir",
        str(output_dir),
        str(input_path),
    ]
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise LibreOfficeError(
            f"LibreOffice timed out after {timeout_seconds} seconds. "
            f"stderr: {output_tail(exc.stderr)}"
        ) from exc

    if result.returncode != 0:
        raise LibreOfficeError(
            f"LibreOffice exited with status {result.returncode}. "
            f"stdout: {output_tail(result.stdout)} stderr: {output_tail(result.stderr)}"
        )
    if not expected_output.is_file() or expected_output.stat().st_size == 0:
        raise LibreOfficeError(
            "LibreOffice reported success but did not create a non-empty expected output. "
            f"Expected: {expected_output}. stdout: {output_tail(result.stdout)} "
            f"stderr: {output_tail(result.stderr)}"
        )
    return expected_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a document through isolated, cross-platform LibreOffice headless mode."
    )
    parser.add_argument("--check", action="store_true", help="Report LibreOffice discovery as JSON.")
    parser.add_argument("--input", type=Path, help="Input document to convert.")
    parser.add_argument("--output-dir", type=Path, help="Directory for the converted document.")
    parser.add_argument("--to", dest="target_format", help="LibreOffice target format, such as pdf.")
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Maximum conversion time in seconds (default: {DEFAULT_TIMEOUT_SECONDS}).",
    )
    parser.add_argument(
        "--profile-root",
        type=Path,
        help="Optional parent directory for a unique, isolated temporary LibreOffice profile.",
    )
    parser.add_argument(
        "--keep-profile",
        action="store_true",
        help="Keep the generated temporary profile for diagnosis after conversion.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Explicitly replace an existing output file with the same derived name.",
    )
    return parser


def validate_conversion_arguments(args: argparse.Namespace) -> tuple[Path, Path, str]:
    if not args.input or not args.output_dir or not args.target_format:
        raise LibreOfficeError("Conversion requires --input, --output-dir, and --to.")
    if args.timeout <= 0:
        raise LibreOfficeError("--timeout must be greater than zero.")

    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        raise LibreOfficeError(f"Input document does not exist or is not a file: {input_path}")
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    return input_path, output_dir, args.target_format


def emit(payload: dict[str, object], stream: object = sys.stdout) -> None:
    print(json.dumps(payload, sort_keys=True), file=stream)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    soffice = find_soffice()
    if args.check:
        emit(
            {
                "available": soffice is not None,
                "executable": str(soffice) if soffice else None,
                "platform": sys.platform,
            }
        )
        return 0 if soffice else 2
    if soffice is None:
        raise LibreOfficeError(
            "LibreOffice was not found. Install it or make soffice available on PATH, then run --check."
        )

    input_path, output_dir, target_format = validate_conversion_arguments(args)
    profile_parent = args.profile_root.expanduser().resolve() if args.profile_root else None
    if profile_parent:
        profile_parent.mkdir(parents=True, exist_ok=True)

    if args.keep_profile:
        profile_dir = Path(tempfile.mkdtemp(prefix="libreoffice-profile-", dir=profile_parent))
        output_path = run_conversion(
            soffice,
            input_path,
            output_dir,
            target_format,
            args.timeout,
            profile_dir,
            args.overwrite,
        )
        emit({"output": str(output_path), "profile": str(profile_dir), "status": "ok"})
        return 0

    with tempfile.TemporaryDirectory(prefix="libreoffice-profile-", dir=profile_parent) as raw_profile:
        output_path = run_conversion(
            soffice,
            input_path,
            output_dir,
            target_format,
            args.timeout,
            Path(raw_profile),
            args.overwrite,
        )
    emit({"output": str(output_path), "status": "ok"})
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LibreOfficeError as exc:
        emit({"error": str(exc), "status": "error"}, sys.stderr)
        raise SystemExit(1)
