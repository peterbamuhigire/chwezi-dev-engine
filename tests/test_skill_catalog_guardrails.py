from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill_catalog_guardrails.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("skill_catalog_guardrails", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
guardrails = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = guardrails
SPEC.loader.exec_module(guardrails)


class SourceIngestionGuardrailTests(unittest.TestCase):
    def scan(self, files: dict[str, bytes | str]):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(content, bytes):
                    path.write_bytes(content)
                else:
                    path.write_text(content, encoding="utf-8")
            return guardrails.check_source_ingestion(root)

    def test_rejects_raw_ebook(self):
        findings = self.scan({"sources/book.epub": b"ebook"})
        self.assertIn("raw-book-source", {finding.code for finding in findings})

    def test_rejects_large_text_in_book_extraction_path(self):
        findings = self.scan({"book-extractions/book.md": "x" * 80_000})
        self.assertIn("source-fulltext-path", {finding.code for finding in findings})

    def test_rejects_marker_rich_full_text_outside_named_path(self):
        text = (
            "ISBN 978-1-234567-89-0\nCopyright 2026 Example Author\n"
            "All rights reserved.\nNo part of this book may be reproduced.\n"
            + "body " * 7_000
        )
        findings = self.scan({"references/innocent-name.md": text})
        self.assertIn("source-fulltext-markers", {finding.code for finding in findings})

    def test_allows_concise_independent_synthesis_in_skill_references(self):
        findings = self.scan(
            {
                "skills/x/references/retry-safe-writes.md": (
                    "# Retry-safe writes\n\nSources: Example Author (2024) *Example Book*.\n\n"
                    "Use idempotency keys for retry-safe writes."
                ),
                "skills/python/references/pdf-extraction.md": "# PDF Extraction\n\nPick a parser.",
            }
        )
        self.assertEqual([], findings)

    def test_rejects_any_file_in_book_extraction_folder(self):
        for folder in ("book-extractions", "extracted-books", "docs/book-study"):
            findings = self.scan({f"{folder}/tiny-note.md": "# Note\n\nOne line."})
            self.assertIn("book-extraction-folder", {finding.code for finding in findings}, folder)

    def test_rejects_link_into_book_extraction_folder(self):
        findings = self.scan(
            {"skills/x/SKILL.md": "Load [notes](../../book-extractions/topic.md) first."}
        )
        self.assertIn("book-extraction-link", {finding.code for finding in findings})

    def test_rejects_extraction_file_outside_named_folder(self):
        findings = self.scan(
            {
                "docs/ux-strategy-extraction.md": (
                    "# UX Strategy - Example Author - Extraction\n"
                    "**Source:** Example Author, *Example Book* (2015).\n"
                )
            }
        )
        self.assertIn("book-extraction-file", {finding.code for finding in findings})

    def test_rejects_shadow_library_or_local_ebook_citation(self):
        for text in (
            "- `Example Book (Author) (z-library.sk, 1lib.sk).epub`",
            "Source input: `C:\\Users\\someone\\Downloads\\Example Book.epub`",
        ):
            findings = self.scan({"skills/x/references/source-register.md": text})
            self.assertIn("source-file-citation", {finding.code for finding in findings}, text)


if __name__ == "__main__":
    unittest.main()
