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

    def test_allows_concise_independent_synthesis(self):
        findings = self.scan(
            {
                "book-extractions/topic-extraction.md": (
                    "# Topic synthesis\n\nSource: Example Author, Example Book.\n\n"
                    "Use idempotency keys for retry-safe writes."
                )
            }
        )
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
