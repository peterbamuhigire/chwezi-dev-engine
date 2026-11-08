Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Chwezi Document Reporting and Publishing Standard

**Status:** Adopted into the Chwezi engines on 8 November 2026 on the instruction of Lead Developer
Peter Bamuhigire, as the publishing companion to the Chwezi Product Excellence Standard and the
Chwezi Reporting and Dashboards Standard. The source handbook (full edition, Version 1.0,
8 November 2026, Chwezi Core Systems Limited Design System Series) calls itself a proposed
normative standard for internal adoption and lists an eight-item adoption checklist; the items
that need product evidence are tracked as `NOT_ASSESSED` in the skill's adoption checklist until a
product team closes them.
**Version:** 1.0.0
**Owner:** Peter Bamuhigire / Chwezi Core Systems (source document owner: Design and Engineering
Leadership)
**Applies with:** the Chwezi Product Excellence Standard (product quality), the Chwezi Reporting and
Dashboards Standard (report data, reconciliation, print floors and exports), the business-app house
style (visual layer) and the engine's design quality gate
**Agent entry point:**
[chwezi-document-publishing-standard](../../SKILL.md)

A system report is a designed publication, not a raw database table with a logo attached. Each
output states its purpose, establishes context, supports decisions, stays trustworthy and keeps its
quality in the browser, as PDF, in print and as editable Word. Premium quality comes from disciplined
typography, hierarchy, evidence and usability, not decoration. A document succeeds when its reader
finds the conclusion, the evidence, the implications and the next action without hunting. This is
an internal policy, not a certification.

## Scope

- Every Chwezi product (Maduuka, Kraal Code ERP, Medic8, Aqar, SpannaMax and future systems) and
  every output channel: browser views, system-generated reports, A4 printing, PDF, DOCX and
  long-form publications. Product-specific rules may add to this standard but never weaken its
  gates.
- Formal documents Chwezi or its products publish: proposals (technical and sponsorship),
  company profiles, annual reports, manuals and handbooks, newsletters, policies and formal
  correspondence.
- Default format: A4 portrait, with justified A4 landscape exceptions.
- Out of scope: live operational screens with no publication output (Product Excellence governs
  them) and marketing web pages.

## Precedence

This standard sits at step 4 of the Product Excellence ladder, beside the Product Excellence and
Reporting standards; where they differ, the stricter rule applies.

| Topic | Rule |
|---|---|
| Report data, reconciliation, period rules, exports | The Reporting and Dashboards Standard governs; this standard adds the publication layer. Its print floors (body 9 pt, tables 8.5 pt, footnotes 8 pt) stay the minimum under every type default here. |
| Colour | Product brand and house-style tokens. The handbook's neutrals (ink #17324A, dark #0D2536, muted #526675, rule #D9E2E8, paper #FFFFFF, subtle fill #F3F7F9) are the default page palette. Measured: ink 13.19:1, dark 15.73:1 and muted 5.97:1 on paper; rule 1.31:1, so rule is decorative only and any line that carries meaning (subtotal and total rules, table structure) uses ink. |
| Typeface | One principal sans with a safe fallback, optional serif for editorial pull quotes; chosen under the engine's typography doctrine and banned-font list. |
| Widths and charts | Product Excellence width classes and chart rules (a donut has at most five parts). |
| Missing values | Never shown as zero. The handbook allows a dash or "Not available" by policy; the Chwezi policy is "Not available" with a reason, because a dash alone reads as zero to some readers and as nothing to screen readers. |
| Headline measures | The handbook allows 3-6 on analytical outputs; a Chwezi reporting surface keeps the Reporting standard's 3-5. |
| Money and dates | ISO 4217 minor-unit decimals; dates read `4 Nov 2026`; quantities in different units are never summed (owner rules). |
| Numbered documents | Contiguous per tenant and document type; a cancelled or corrected document is voided or revised, never deleted or silently overwritten (owner standing rule, 5 Nov 2026). |
| Reference designs | Inspiration only, never evidence; their figures, logos, testimonials, imagery and data are never reused. |

## Design invariants

1. **Outcome-led composition.** Lead with the reader's question, not the database schema; every
   output has a title, entity, period, scope and publication status.
2. **One canonical model.** Query, authorise, validate, normalise, calculate, narrative, layout,
   render, check, publish. One semantic report model feeds the HTML, print CSS, PDF and DOCX
   renderers; no total is ever derived from displayed strings.
3. **Consistency.** One grid, one type hierarchy, consistent whitespace, colour semantics and footer
   treatment; labels, units, precision, period and comparison baselines are preserved across media.
4. **True text.** Key data stays selectable text; whole pages are never rasterised.
5. **Evidence before aesthetics.** Every visible number traces to a validated source and
   reconciles; no fact, source, logo, signature, testimonial, total or compliance claim is invented;
   imagery is authentic, licensed and in context.
6. **Print-safe.** Everything critical survives greyscale, A4, office printers, PDF and DOCX editing.
7. **Accessible by default.** WCAG 2.2 AA in the browser; PDF/UA requirements evaluated for tagged
   PDF; accessibility is a baseline, not a special export mode.
8. **Controlled change.** Revisions, cancellations and corrected versions are issued as new
   versions with history, never by silent overwrite.

## Hard release gates

Any one of these blocks publication. Each needs `MEASURED` evidence to close; an applicable gate
with `NOT_ASSESSED` evidence counts as open. They cover the handbook's stop conditions (totals
mismatch, required data missing, sensitive data leaked, unreadable layout).

| Gate | Fails when | Also trips |
|---|---|---|
| PUB-GATE-01 Output parity | The approved numbers or facts differ between the browser report, PDF, print, DOCX and data export of the same snapshot, or a total does not reconcile to its rows and source ledger. | RPT-GATE-01 |
| PUB-GATE-02 Fabricated content | A fact, source, figure, logo, client mark, signature, testimonial, image, credential or compliance claim (IFRS, tax, statutory, PDF/UA) has no verified source, permission or review. | PX-GATE-09 |
| PUB-GATE-03 Missing identity or data | Title, entity, period, status, scope, currency, owner, generation time, timezone or as-of cutoff is missing, or required data is missing and the document is published anyway. | RPT-GATE-03 |
| PUB-GATE-04 Unreadable layout | An accidental blank page, an orphaned heading, a split KPI card or signature block, a cut table, a silently truncated row or column, overlapping or clipped text, or text below the legibility floor appears in any output. | RPT-GATE-06 |
| PUB-GATE-05 Screenshot output | A PDF or DOCX page is a raster of a screen, or a figure in it was computed from displayed strings. | RPT-GATE-06 |
| PUB-GATE-06 Uninspected output | Any page of a released PDF or DOCX, the DOCX reopened and re-rendered, or any acceptance viewport of the browser report was not rendered and inspected. | None (publishing-specific) |
| PUB-GATE-07 Data leaked | A document exposes personal, payroll or clinical data beyond its purpose or role, crosses a tenant boundary, or carries raw SQL, internal paths, secrets or hidden fields in its metadata. | RPT-GATE-04 |
| PUB-GATE-08 Unrecorded or overwritten release | The release has no record of report ID, version, generation ID, renderer and template versions, source snapshot, actor, parameter hash, approval and retention, or a published document was overwritten instead of revised or cancelled. | None (publishing-specific) |

## Release decision

Product reports use the Product Excellence verdicts (PASS, CONDITIONAL, BLOCKED) with the PUB gates
added to the PX and RPT gates that apply. Controlled publications (financial, legal, medical and
externally issued documents) also need a documented human review and approval. A standalone
publication passes only when every applicable PUB gate is closed on measured evidence and the named
approver has signed.

## Roles

| Role | Owns |
|---|---|
| Product owner | The reader and the business question |
| Data owner | Metrics, sources and calculations |
| Designer | Template tokens and editorial hierarchy |
| Engineering | Deterministic rendering and export reliability |
| QA | Cross-format verification |
| Approver | Sign-off of controlled publications |

## Rules

The normative rules, `PUB-<AREA>-NNN`, with levels, checks and evidence, are in the skill's
[rules and gates reference](rules-and-gates.md).
MUST, SHOULD and MAY carry the handbook's and Product Excellence's meanings; a SHOULD departure
needs a design decision record. IDs are never reused. The handbook's annexes are normative here:
their content is carried by the skill's references.

## Implementation sequence (owner plan)

1. Foundation: approve tokens, page geometry, semantic schema, report families and ownership.
2. Pilot: three golden templates (operational statement, executive analysis, editorial proposal).
3. Exports: browser, print or PDF, and DOCX renderers from one source snapshot.
4. Testing: golden-page visual regression, accessibility, arithmetic checks and a device matrix.
5. Scale: Maduuka, Kraal Code ERP, Medic8, Aqar and later products; monitor defects and reuse.

## Evidence states and currentness

The Product Excellence evidence vocabularies apply. Standards cited (WCAG 2.2, PDF/UA, CSS paged
media, ISO 32000) are recorded with access date and status in the skill's currentness register;
rendering-engine support for paged-media features differs and is tested, never assumed. No
DOCX-to-PDF conversion is assumed to produce a conformant tagged PDF without validation.

## Copies in other engines

Each Chwezi engine that serves document work carries its own complete copy of this doctrine, the
rules catalogue and the references, with identical IDs and wording, and works without any other
engine installed. This file is the canonical text; copies are re-synced whenever its version
changes.

## Change control

Peter Bamuhigire approves every change; semantic versions (patch for wording, minor for new SHOULD
or MAY rules, templates and blueprints, major for any new, removed or re-levelled MUST, any gate or
any threshold); every release logged in the engine's change record (its `CHANGELOG.md` or dated
update notes) with the rule IDs affected. Owners and reviewers for template changes are assigned in
the adoption checklist.
