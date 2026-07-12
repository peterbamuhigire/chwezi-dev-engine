#!/usr/bin/env python3
"""
Repair common UTF-8/Latin-1 mojibake in repository text files.
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
ACTIVE_ROOTS = (REPO_ROOT / "skills", REPO_ROOT / "00-meta-initialization")
TARGET_SUFFIXES = {".md", ".skill", ".yml", ".yaml"}
SUSPICIOUS = ("â", "Ã", "Â", "ðŸ", "\ufffd")
TOKEN_RE = re.compile(r"\S+")


def badness(text: str) -> int:
    return sum(text.count(marker) for marker in SUSPICIOUS)


def repair_token(token: str) -> str:
    candidate = token
    for _ in range(3):
        if not any(marker in candidate for marker in ("â", "Ã", "Â", "ð")):
            break
        improved = candidate
        for encoding in ("latin1", "cp1252"):
            try:
                decoded = candidate.encode(encoding).decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
            if badness(decoded) < badness(improved):
                improved = decoded
        # Mixed Windows-1252/control-code mojibake (for example U+009D plus
        # U+0152) cannot be encoded by either codec as one string. Rebuild the
        # original byte stream character by character, preserving C1 controls.
        raw = bytearray()
        try:
            for char in candidate:
                try:
                    raw.extend(char.encode("cp1252"))
                except UnicodeEncodeError:
                    codepoint = ord(char)
                    if codepoint > 255:
                        raise
                    raw.append(codepoint)
            decoded = bytes(raw).decode("utf-8")
            if badness(decoded) < badness(improved):
                improved = decoded
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        if improved == candidate:
            break
        candidate = improved
    return candidate


def repair_text(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return repair_token(token)

    repaired = TOKEN_RE.sub(replace, text)
    # Repair a common escaped-path artefact where ``\references`` was parsed
    # as a carriage return followed by ``eferences``.
    return repaired.replace("\references/", "references/")


def main() -> None:
    changed = []
    paths = (path for root in ACTIVE_ROOTS for path in root.rglob("*"))
    for path in paths:
        if path.suffix not in TARGET_SUFFIXES or not path.is_file():
            continue
        raw = path.read_bytes()
        escaped_reference = b"\references/"
        repaired_escaped_path = escaped_reference in raw
        if repaired_escaped_path:
            raw = raw.replace(escaped_reference, b"references/")
            path.write_bytes(raw)
        text = path.read_text(encoding="utf-8", errors="replace")
        if not any(marker in text for marker in SUSPICIOUS):
            if repaired_escaped_path:
                changed.append(path.relative_to(REPO_ROOT))
            continue
        repaired = repair_text(text)
        if badness(repaired) < badness(text):
            path.write_text(repaired, encoding="utf-8", newline="\n")
            changed.append(path.relative_to(REPO_ROOT))

    print(f"Repaired {len(changed)} files.")
    for rel in changed[:200]:
        print(rel)


if __name__ == "__main__":
    main()
