#!/usr/bin/env python3
"""Reject raw books, stored book extractions, and reconstructive full-text conversions.

Books are temporary inputs. The repository may keep only paraphrased,
task-oriented skill content and references. This gate therefore fails on:

- raw ebook files anywhere, and PDFs under book/source-extraction paths;
- ANY file inside a book-extraction folder (``book-extractions/``,
  ``extracted-books/``, ``book-study/`` and similar), whatever its size;
- ``*-extraction.md`` files that present themselves as a book extraction;
- Markdown links that point into a book-extraction folder;
- shadow-library file names and local ebook download paths used as citations;
- large or marker-rich text that looks like a reconstructed book.

Plan and audit documents may name books; they must not store book content.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


LARGE_BOOK_TEXT_BYTES = 80_000
RAW_BOOK_EXTENSIONS = {".epub", ".mobi", ".azw", ".azw3"}
SOURCE_TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".html", ".htm"}
BOOK_SOURCE_PATH_RE = re.compile(
    r"(?:^|/)(?:book-extractions?|extracted-books?|book-study|book-dumps?|raw-books?|source-books?)(?:/|$)",
    re.IGNORECASE,
)
BOOK_EXTRACTION_LINK_RE = re.compile(
    r"\]\(\s*<?[^)\s>]*(?:book-extractions?|extracted-books?|book-study)/",
    re.IGNORECASE,
)
EXTRACTION_TITLE_RE = re.compile(r"^#[^\n]*\bextraction\b", re.IGNORECASE | re.MULTILINE)
EXTRACTION_SOURCE_RE = re.compile(r"^\s*\*{0,2}sources?:\*{0,2}", re.IGNORECASE | re.MULTILINE)
SHADOW_LIBRARY_RE = re.compile(r"\b(?:z-library|z-lib|1lib)\.[a-z]{2,}\b", re.IGNORECASE)
LOCAL_EBOOK_PATH_RE = re.compile(
    r"[A-Za-z]:\\Users\\[^\\\n`]+\\Downloads\\[^`\n]*\.(?:epub|mobi|azw3?|pdf)\b",
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
        if in_book_source_path:
            findings.append(
                Finding(
                    "book-extraction-folder",
                    relative,
                    "book-extraction folders must not exist; fold paraphrased, task-oriented "
                    "knowledge into skill references/ and delete the folder",
                )
            )
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

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        findings.extend(_scan_text_policy(relative, content))
        if size < 30_000:
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


def _scan_text_policy(relative: Path, content: str) -> list[Finding]:
    """Small-file checks that do not depend on size."""
    findings: list[Finding] = []
    if relative.suffix.lower() == ".md":
        if BOOK_EXTRACTION_LINK_RE.search(content):
            findings.append(
                Finding(
                    "book-extraction-link",
                    relative,
                    "links into a book-extraction folder; point to a paraphrased skill reference instead",
                )
            )
        head = content[:1500]
        if (
            relative.name.lower().endswith("-extraction.md")
            and EXTRACTION_TITLE_RE.search(head)
            and EXTRACTION_SOURCE_RE.search(head)
        ):
            findings.append(
                Finding(
                    "book-extraction-file",
                    relative,
                    "stored book extraction; keep only paraphrased, task-oriented references",
                )
            )
    if SHADOW_LIBRARY_RE.search(content) or LOCAL_EBOOK_PATH_RE.search(content):
        findings.append(
            Finding(
                "source-file-citation",
                relative,
                "cites a local ebook path or shadow-library file name; cite Author (Year) Title instead",
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
