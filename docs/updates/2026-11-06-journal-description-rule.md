# Journal descriptions carry the document number (6 Nov 2026)

Owner standing rule of 6 Nov 2026, added to the tenant document numbering standard as
rule 12. Every journal entry posted by a numbered document ends its description with
the number in brackets, for example `Goods received (GRN-00012)`.

## Changed

- `skills/saas/tenant-document-numbering/SKILL.md`: rule 12 (twelve rules now), four
  anti-patterns, one decision rule, a reference link.
- New `skills/saas/tenant-document-numbering/references/journal-descriptions.md`: the
  form, companion and reversal handling, history never rewritten (batch-loaded display
  fallback), central enforcement in the ledger writer, route map with reasoned
  exemptions, generated test, CI ratchet, checklist.
- `references/api-offline-and-guardrails.md`: one review-checklist line.
- `saas-accounting-system/references/journal-posting-rules.md`: pointer to the rule.

Reference implementation: Maduuka `src/Accounting/JournalDescription.php`. Not a
statutory requirement; an internal control standard.
