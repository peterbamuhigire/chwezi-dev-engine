# Journal descriptions carry the document number

Parent skill: [tenant-document-numbering](../SKILL.md). Owner standing rule of
6 Nov 2026, rule 12 of the standard. Reference implementation: Maduuka
`src/Accounting/JournalDescription.php` and its generated matrix test.

## 1. The form

Every journal entry posted by a numbered document ends its description with the
document number in brackets: `Goods received (GRN-00012)`, `Sale (INV-00000042)`.

- The number is last, in brackets, always the same form. No other trailing text.
- Header (description) only. Line memos keep their account-specific words and carry no
  number.
- Companion entries of the same document (cost of goods sold of an invoice, the tax
  line of a bill) carry the same number as their sibling entry.
- A reversal resolves the same source document as the journal it undoes and carries the
  same number.
- No placeholder when a document has no number on record: omit the suffix.
- No row ids (`#123`) or any other database id in a description.
- The description column cap (255) is respected by shortening the words, never the
  number. Trim the text before the suffix.

## 2. History is never rewritten

Old journals keep their text. A report may show the source number beside a legacy
journal as a display fallback. Load it in batch: group the rows by source route and run
one query per distinct route (O(distinct source routes) per report), never one query
per row.

## 3. Enforce centrally, in the ledger writer

Put the rule in the one writer all modules post through, not in every poster. The poster
hands over the source type (reference type plus source id); the writer resolves the
number and appends the suffix. The source type matters because one reference type can
come from different tables, so the route must be chosen by source, not by reference type
alone. A poster that formats its own tail is a defect even if it looks right today.

## 4. Route map and exemptions

Keep one map of reference type to source table, number column and key. Every reference
type is either routed or on an exempt list, and each exempt entry carries a written
reason (for example opening balances, manual journals typed by a person, period close).
An unlisted type is a failing test, never a silent skip.

## 5. Generated test

A test generated from the authoritative type list posts a real document of every
posting and reference type through the application (not by inserting rows) and asserts
the exact form, including the companion and reversal cases. The list of types comes from
code (the posting constants or enum), not from a database that may be stale. A new type
fails the test until it is routed, exempt with a reason, or posted by the test.

## 6. CI ratchet

Count description builders that interpolate ids: `sprintf` with `%d`, `number_format`,
helpers returning `'#'.$id`, `implode` of ids, and string interpolation into a
description. Store the count as a baseline that may only go down; a rise fails CI, a
fall lowers the baseline.

## 7. Checklist

- [ ] Suffix is last, bracketed, one form; line memos untouched.
- [ ] Companion entries and reversals show the sibling or original number.
- [ ] No placeholder, no `#id`; cap met by shortening words.
- [ ] Single enforcement point; posters pass the source type.
- [ ] Route map with reasoned exemptions; generated test fails on an unrouted type.
- [ ] Ratchet baseline recorded and only falling.
- [ ] Old journals untouched; report fallback batch-loaded per route.
