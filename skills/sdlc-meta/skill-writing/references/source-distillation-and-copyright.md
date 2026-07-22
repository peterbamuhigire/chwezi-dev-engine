# Source Distillation and Copyright Gate

Use this gate whenever a book, EPUB, PDF, course, article, transcript, or other
third-party source informs a skill.

## Non-negotiable rule

Extract the operational knowledge needed for the skill. Never retain or commit
the whole work, a format conversion, an OCR dump, or a chapter-by-chapter
substitute from which the source can be substantially reconstructed.

Lawful access to a source does not grant permission to republish it. Keep the
source outside the repository and treat any temporary extracted text as
disposable processing material.

## Allowed repository content

- Bibliographic attribution and a source register.
- Independently worded workflows, decision rules, checklists, failure modes,
  examples, and quality gates.
- A concise synthesis organised by the skill's practical topics rather than by
  the source's chapter sequence.
- Short quotations only when necessary, attributed, and no longer than needed
  for the specific analytical point.
- Public-domain, permissively licensed, or user-authored material only when its
  licence and repository purpose are explicit; prefer synthesis even then.

## Prohibited repository content

- `.epub`, `.mobi`, `.azw`, or `.azw3` source files.
- PDFs stored as book inputs under extraction or source-material directories.
- EPUB/PDF-to-Markdown conversions, OCR output, page images, covers, or embedded
  book assets.
- Long verbatim passages, full tables or figures, or sequential paraphrases that
  reproduce the source's expressive structure.
- A reference file that functions as a replacement for buying or accessing the
  original work.
- Local download paths or piracy-site metadata in a committed source register.

## Workflow

1. Record bibliographic identity, licence/permission status, and the skill
   questions the source is expected to answer.
2. Process the source in an operating-system temporary directory outside the
   repository. Do not stage the source or its raw extraction.
3. Capture only claim-sized notes needed for the target workflow. Separate
   direct quotations from paraphrase and synthesis while working.
4. Write the skill material independently, grouped by operational topic. Add
   decisions, failure handling, and verification that the source itself may not
   provide.
5. Compare the draft against the source notes. Remove long matching passages,
   chapter mirroring, page markers, ISBN/copyright front matter, and book assets.
6. Delete temporary converted text after the synthesis is verified.
7. Inspect the staged diff and run:

   ```powershell
   python -X utf8 scripts\skill_catalog_guardrails.py
   ```

8. Block release on any `raw-book-source`, `source-fulltext-path`, or
   `source-fulltext-markers` finding.

## Stop conditions

Stop and request a narrower source-processing plan when the task asks to commit
the source, preserve a full conversion, reconstruct chapters, or produce a
substitute for the original. If permission or licence terms are unclear, retain
only minimal bibliographic facts and independently developed general knowledge
until the rights question is resolved.

## Acceptance evidence

- The source files and temporary conversions are absent from the repository.
- The committed material is concise, independently structured, and useful only
  as operational skill guidance.
- Attributions are accurate and quotations are minimal.
- The repository guardrail and the skill's normal validators pass.
