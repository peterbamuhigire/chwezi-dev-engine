# Claude Code repository memory

@AGENTS.md

## Never store book extractions

Book extractions, book summaries and chapter-by-chapter notes must never be stored in this
repository (no `book-extractions/`, `extracted-books/` or `docs/book-study/` folder, no
`*-extraction.md` book files). Keeping them infringes copyright. Knowledge from purchased books
enters only as paraphrased, task-oriented skill content and `references/` files (procedures,
decision rules, checklists, templates, original worked examples) with a short citation
(Author (Year) *Title*). Verbatim quotations stay rare and under 25 words. Never cite a local
ebook path or shadow-library file name. Staging notes live outside the repository and are never
linked from skills. `scripts/source_ingestion_guardrail.py` (also run by
`scripts/skill_catalog_guardrails.py`) fails if an extraction folder exists, a `*-extraction.md`
book file exists, or a Markdown file links into an extraction folder. Plan and audit documents
may name books but must not store their content.
