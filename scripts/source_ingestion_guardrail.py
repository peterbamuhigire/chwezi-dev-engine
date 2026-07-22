#!/usr/bin/env python3
"""Reject raw books and likely reconstructive full-text conversions."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


LARGE_BOOK_TEXT_BYTES = 80_000
RAW_BOOK_EXTENSIONS = {".epub", ".mobi", ".azw", ".azw3"}
SOURCE_TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".html", ".htm"}
BOOK_SOURCE_PATH_RE = re.compile(
    r"(?:^|/)(?:book-extractions?|book-dumps?|raw-books?|source-books?)(?:/|$)",
    re.IGNORECASE,
)
FULL_TEXT_MARKERS = {
    "isbn": re.compile(r"\bISBN(?:-1[03])?\s*:?\s*[\dXx][\dXx\-\s]{8,}"),
    "copyright": re.compile(r"\bcopyright\s+(?:\u00a9|\(c\)|&copy;|[12]\d{3})", re.IGNORECASE),
    "rights-reserved": re.compile(r"\ball rights reserved\b", re.IGNORECASE),
    "reproduction-notice": re.compile(
        r"\bno part of this (?:book|publication|work) may be reproduced\b",
        re.IGNORECASE,
    ),
    "ebook-conversion": re.compile(
        r"(?:\[\]\{#[^}\n]*\.xhtml|calibre\d*|index_split_\d+\.html)",
        re.IGNORECASE,
    ),
}
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "node_modules"}


@dataclass(frozen=True)
class Finding:
    code: str
    path: Path
    message: str

    def format(self) -> str:
        return f"[ERROR] {self.code}: {self.path} {self.message}"


def scan(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue

        suffix = path.suffix.lower()
        if suffix in RAW_BOOK_EXTENSIONS:
            findings.append(
                Finding(
                    "raw-book-source",
                    relative,
                    "raw ebook source files are temporary inputs and must not be stored in the repository",
                )
            )
            continue

        in_book_source_path = BOOK_SOURCE_PATH_RE.search(relative.as_posix()) is not None
        size = path.stat().st_size
        if suffix == ".pdf" and in_book_source_path:
            findings.append(
                Finding(
                    "raw-book-source",
                    relative,
                    "PDFs under book/source-extraction paths must stay outside the repository",
                )
            )
            continue
        if suffix not in SOURCE_TEXT_EXTENSIONS:
            continue

        if in_book_source_path and size >= LARGE_BOOK_TEXT_BYTES:
            findings.append(
                Finding(
                    "source-fulltext-path",
                    relative,
                    f"{size} bytes under a book-extraction path; retain concise synthesis, not source text",
                )
            )

        if size < 30_000:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        markers = sorted(name for name, pattern in FULL_TEXT_MARKERS.items() if pattern.search(content))
        if len(markers) >= 3:
            findings.append(
                Finding(
                    "source-fulltext-markers",
                    relative,
                    "likely reconstructive book text; matched markers: " + ", ".join(markers),
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    findings = scan(args.root)
    print(f"source-ingestion-guardrail: {args.root.resolve()}")
    print(f"findings: {len(findings)}")
    for finding in findings:
        print(finding.format())
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
