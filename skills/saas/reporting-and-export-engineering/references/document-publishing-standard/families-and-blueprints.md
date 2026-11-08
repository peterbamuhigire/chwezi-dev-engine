Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Archetypes, blueprints, components and page specifications

Use this reference to classify a document, order its sections, choose its components and build each
page. A blueprint is a section order, never a template to fill with invented content. Rule IDs:
[rules-and-gates.md](rules-and-gates.md).

## Task 1: choose the archetype (PUB-ARCH-001)

| Archetype | Examples | What comes first |
|---|---|---|
| Transactional and operational | Invoices, receipts, stock statements, payroll summaries, service orders | Compact header and identifiers, status and dates, parties, lines, totals, taxes, terms, authorisation; printer reliability over artwork; batch export with deterministic file names |
| Analytical and executive | Management reviews, sales reports, scorecards, audit summaries | Summary first; a small selected set of measures; fair comparisons; risks, exceptions, owner and next step; full tables and definitions after the narrative |
| Editorial and institutional | Company profiles, annual reports, proposals, manuals, newsletters | Cover, contents, section openers, narrative spreads, captions, case studies, process diagrams, back matter; every page stands alone in A4 print |

Then lay information on the narrative ladder (PUB-ARCH-002): level 1 the answer and the most
consequential numbers; level 2 explanation, trends, breakdowns and exceptions; level 3 detailed
tables, method, reconciliation and appendices.

## Task 2: follow the family blueprint

| Family | Section order |
|---|---|
| Executive performance report | Optional cover; executive decision summary; measure overview; key trends; drivers; exceptions; action register; methods; detailed data appendix |
| Financial statement pack | Cover or statement index; financial position; profit or loss; cash flows; changes in equity where applicable; accounting policies; notes; approvals |
| Operational daily report | Entity, date and shift; critical status; exceptions; short measure strip; action queue; operational detail; sign-off |
| Sales and inventory report | Sales and margin summary; category trends; best and worst movers; stock ageing; replenishment risks; transaction appendix |
| Hospital or clinic report | Audience-specific de-identified aggregates; care and service indicators; safety signals; source definitions; restricted access and review |
| Company profile | Cover; story; mission; capabilities; service lines; process; people; track record; case studies; footprint; contact |
| Technical proposal | Client context; problem; objectives; approach; architecture; work plan; milestones; deliverables; assumptions; pricing; risks; terms |
| Sponsorship proposal | Opportunity; audience; impact; event or programme; tiers; sponsor benefits; proof; budget; schedule; agreement |
| Annual report | Leadership message; highlights; strategic context; operations; results; governance; financials; notes; outlook |
| Training manual | Learning objectives; prerequisites; step-by-step instructions; screenshots; warnings; practice tasks; troubleshooting; glossary |
| Newsletter | Issue identity; editor note; feature story; brief updates; people; events; references and contact |
| Formal correspondence | Letterhead; recipient; date; subject; salutation; concise body; signature; attachments; document ID |

Acceptance for every blueprint: the reviewer confirms the required fields and reading order in the
browser preview, the generated PDF and the editable DOCX, and records any exception with its
approval.

## Task 3: use the component catalogue

| Component | Contents and rule |
|---|---|
| Cover | Title, subtitle, issuing entity, publication date, revision, image or graphic, confidentiality marker; restrained hierarchy and safe contrast |
| Executive summary | Question, decision, 3-5 evidence-backed findings, risks and recommended actions; each statement links to a section or source |
| Section opener | Chapter number, informative title, short summary, optional full-width image; a whole page only when it earns it |
| Measure panel (KPI) | Label, value, unit, period, comparison, calculation definition, source; only as many as the reading task needs; never split across pages |
| Narrative figure | Figure number, caption, data period, source, accessible description, interpretation, method note |
| Formal data table | Header row, units, row groups, totals, footnotes, repeated headers, right-aligned figures, clear continuation |
| Callout | Risk, decision, evidence limitation or recommendation only; no decorative callouts |
| Case study | Context, challenge, intervention, measured outcome, lessons, source and evidence limits |
| Approval block | Prepared, reviewed and approved by, role, date, version, signatures where required; never split across pages |
| Back matter | Definitions, notes, references, appendices, revision history, contact and legal information |

## Task 4: build each page from its specification sheet

Shared build rules for every sheet: shared type and spacing tokens; reading order and true text;
source and cutoff shown; no invented values; page-break and repeating-header logic; the PDF and
DOCX carry the same content; tested at 100% zoom, in A4 print preview, in greyscale and with a
long-data fixture. Deliverables: template source, schema mapping, populated example, PDF render,
DOCX render, visual snapshots, numerical validation log, accessibility findings, unresolved issues.

| Sheet | Format | Layout |
|---|---|---|
| Management executive summary | A4 portrait | Top: identity, reporting window, status. Upper quarter: one-sentence conclusion and three high-value measures. Middle: one trend figure with interpretation. Lower: exceptions and decision or action register. Bottom: provenance and page number |
| Monthly sales analysis | A4 portrait, 2-5 pages | Page 1 results and period comparison; page 2 category and branch contribution; page 3 margin, returns and anomalies; then the full transaction or product appendix |
| Inventory reorder report | A4 landscape when wide | Top: as-of time, site and stock policy. Summary: below-reorder count and value at risk. Table: item code, item, on hand, reserved, available, reorder point, lead time, supplier, action. Then assumptions and definitions |
| Income statement | A4 portrait | Entity, period, currency, current and comparative columns; revenue, cost of sales, gross profit, operating costs, operating result, other items, tax, net result; hierarchy and note references |
| Balance sheet | A4 portrait | Assets, liabilities and equity with comparatives, note references and a balance check; major section totals kept with their context |
| Treasurer statement | A4 portrait | Opening balance, dated receipts, dated payments, net movement, closing balance, reconciliation and sign-off; no decorative graphics that hide the arithmetic |
| Project proposal | A4 portrait, 8-25 pages | Cover, executive case, client problem, solution, method, deliverables, phased schedule, team, assumptions, price, risk, terms, acceptance; section openers only where warranted |
| Company profile | A4 portrait, 8-20 pages | Cover, who we are, mission, services, how we work, team, projects, case studies, coverage, governance, contact; authentic photography and measured evidence |
| Annual report | A4 portrait, 20+ pages | Editorial cover, leadership note, highlights, priorities, performance, financial statements, governance, risk, sustainability, method and references |
| Training handbook | A4 portrait | Purpose, audience, prerequisites, illustrated procedures, warnings, common mistakes, troubleshooting, quick-reference checklists, glossary, version history |
| System-generated audit report | A4 portrait or landscape | Metadata and immutable filters, findings summary, severity and owner, evidence rows, remediation status, method, reviewer, audit trail |
| Patient service report | A4 portrait | Aggregated scope, period, method, denominator and privacy restrictions; quality indicators and actions without individual records |

## Task 5: apply a visual recipe

| Recipe | Composition |
|---|---|
| Formal annual-report spread | White canvas, restrained running head in ink, broad margin, two-column commentary, precise financial table |
| Corporate profile spread | One full-width contextual photograph, concise company narrative, restrained service cards, consistent page furniture |
| Editorial case-study spread | Large pull quote or outcome measure, project photograph, evidence panel, before and after narrative, source note |
| Executive report page | One headline finding, a supporting trend chart, 2-4 critical measures, exception list, recommended action |
| Clean proposal page | Client-oriented heading, numbered deliverables, timeline graphic, clear cost and assumption panel |
| Low-ink operational statement | Minimal fill, thin rules in ink, high-contrast type, compact table, explicit totals, signature block |

## Task 6: lessons from the reference collection

Adopt: editorial covers with a restrained hero image, title, period and publisher; clear section
openings and recurring running heads or folios; balanced white space, deliberate accent panels,
large pull statistics and short captions; spreads for reading with every page valid on its own in
A4; well-structured financial tables with indentation, rules, notes and subtotal emphasis.

Reject: tiny body text copied from portfolio thumbnails; image-heavy pages that waste toner or fail in
greyscale; decorative diagrams without definition, source or interpretation; magazine columns on
legal, invoice or accounting documents; table headers split from rows; distorted photographs;
meaningless charts; placeholder data, reference watermarks and unverified testimonials or client
marks.

## Evidence/currentness

No external fact is cited here. Page counts, proportions and measure counts are Chwezi values from
the handbook.
