Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Presentation and Slide Deck Design Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Chwezi Presentation and Slide Deck Design Standard

**Status:** Adopted into the Chwezi engines on 8 November 2026 on the instruction of Lead Developer
Peter Bamuhigire. Source: the full edition of the handbook (Version 1.0, 8 November 2026, Chwezi Core
Systems Design Standards Series), which treats its requirements as normative unless marked as
recommendations; its scores are internal governance thresholds, not an external certification.
**Version:** 1.0.0
**Owner:** Peter Bamuhigire / Chwezi Core Systems
**Applies with:** the Chwezi Document Reporting and Publishing Standard (identity, evidence, export
parity), the Chwezi Reporting and Dashboards Standard (figures, reconciliation, period rules), the
house style and product brand tokens (visual layer) and the engine's design quality gate
**Agent entry point:**
[chwezi-presentation-standard](../../SKILL.md)

The goal is not to imitate attractive templates. It is a persuasive, credible, exceptionally readable
deck whose narrative, evidence, visual hierarchy and technical reliability justify premium
professional fees. Every deck works in PowerPoint, as a landscape PDF, on a meeting-room projector
and on a laptop. AI generation is a production aid; editorial judgement and factual accountability
stay with people. Premium value comes from diagnosis, argument, reliable evidence, domain expertise,
visual clarity, reusable systems and tested delivery, never from slide count or generation speed.

## Scope

- Every deck Chwezi produces or a Chwezi product exports: executive reviews, investor pitches,
  consulting and tender proposals, project status, training, case studies, board and sales decks,
  in PowerPoint (PPTX) and landscape PDF.
- Out of scope: long-form documents (the Publishing standard), live app screens (Product
  Excellence) and marketing web pages.

## Precedence

This standard sits beside the Product Excellence, Reporting and Publishing standards at step 4 of
the Product Excellence ladder; where they differ, the stricter rule applies.

| Topic | Rule |
|---|---|
| Figures in a deck | The Reporting standard governs metric contracts, reconciliation, period comparisons and units; a deck never shows a total that does not reconcile. |
| Claims, imagery, testimonials, logos, signatures | The Publishing standard's content rules apply; no claim without a source in the claim ledger. |
| Colour and type | Product brand and house-style tokens; the banned-font doctrine applies; state the typeface and the reason. |
| Accessibility | WCAG 2.2 contrast (4.5:1 text, 3:1 large text) is used as a design benchmark; no claim of PowerPoint conformance is made. |
| Money and dates | ISO 4217 minor-unit decimals; dates read `4 Nov 2026`; quantities in different units are never summed (owner rules). |
| Reference images | Inspiration categories only; never reproduce protected template designs, watermarks or template marketplace imagery. |

## Design principles

1. One decision-relevant message per slide; the headline states the conclusion, not the topic.
2. The storyboard of headlines reads as a coherent argument with every visual hidden.
3. Evidence and audience first; a layout is chosen only after the message is defined.
4. Every chart has units, period, denominator or base, source and a meaningful comparison.
5. Text is legible where the deck will actually be seen: the minimum size is computed from the
   farthest viewing distance and the screen height, not guessed.
6. Colour supplements text and shape; status is never carried by hue alone.
7. Native, editable PowerPoint objects bound to the theme; a faithful landscape PDF counterpart.
8. Authentic, rights-cleared imagery; no watermark, placeholder text or synthetic image presented
   as evidence.

## Hard release gates

Any one of these blocks release. Each needs `MEASURED` evidence to close; an applicable gate with
`NOT_ASSESSED` evidence counts as open.

| Gate | Fails when | Also trips |
|---|---|---|
| DECK-GATE-01 Unsupported claim | A statistic, testimonial, name, credential, customer, product feature, award or source has no entry in the claim ledger, or illustrative data is shown as real. | PUB-GATE-02 |
| DECK-GATE-02 Illegible in use | Text on a presented slide is below the computed minimum for the venue (and never below 16 pt), or key content is illegible at 720p projection. | None (deck-specific) |
| DECK-GATE-03 Visual defect | Any clipped, overlapping or orphaned element, placeholder text, watermark, source-template branding, stretched or pixelated image. | PUB-GATE-04 |
| DECK-GATE-04 Export failure | The PDF differs from the PPTX in slide count, order, size or orientation, or has missing glyphs, rasterised body text or broken links. | PUB-GATE-01 |
| DECK-GATE-05 Not editable | Content that could be native (text, charts, tables, diagrams) is flattened into images, or fonts and colours are not bound to the theme. | None (deck-specific) |
| DECK-GATE-06 Rights or confidentiality | An image, logo, quote or icon lacks rights or permission; synthetic imagery is presented as documentary proof; sensitive client data is exposed. | PUB-GATE-07 |
| DECK-GATE-07 Misleading figure | A bar chart with a truncated axis, a 3D chart, an unlabelled unit, period or source, forecast shown as actual, percentage and percentage points mixed, or a total that does not reconcile. | RPT-GATE-01 |
| DECK-GATE-08 Uninspected release | Any slide was not rendered and inspected, the PDF was not compared page by page, or the release lacks its QA log and handoff manifest. | PUB-GATE-06 |

## Release decision

A deck is released only when:

- every applicable DECK gate is closed on measured evidence;
- each of the six deck dimensions (narrative, evidence, readability, visual craft, technical,
  actionability) scores at least 4 of 5;
- the slide scorecard averages at least 90 of 100 with no critical failure in evidence integrity,
  confidentiality, file corruption or readability;
- an editorial, a design and a technical reviewer have signed.

These are internal thresholds, not certification.

## Roles and gates in the workflow

| Gate | Reviewer | Checks |
|---|---|---|
| Editorial | Senior reviewer | Claim logic, evidence, tone, sequence, relevance; before visual polish |
| Design | Designer | Hierarchy, contrast, whitespace, composition, consistency, identity |
| Technical | Production reviewer | Editability, opening, compatibility, PDF fidelity, media, links, notes, file size |

## Rules

The normative rules, `DECK-<AREA>-NNN`, are in the skill's
[rules and gates reference](rules-and-gates.md).
MUST, SHOULD and MAY carry the Product Excellence meanings; a SHOULD departure needs a design
decision record. IDs are never reused.

## Rollout (owner plan)

1. Foundation: brand tokens, slide masters, the 20 blueprints, the claim ledger and file naming;
   rebuild three existing decks as benchmarks with before-and-after QA.
2. Production system: storyboard templates, data-to-chart pipelines, native PowerPoint
   construction, PDF export and regression screenshots; agents trained on failure modes.
3. Premium differentiation: sector libraries, executive narrative reviews, client personalisation,
   localised imagery, accessibility checks and reusable case-study evidence packs.

## Evidence states and currentness

The Product Excellence evidence vocabularies apply. Standards and methods cited (WCAG 2.2, PowerPoint
accessibility guidance, Office Open XML, PDF/UA, legibility by visual angle, display image size) are
recorded with access date and status in the skill's currentness register.

## Copies in other engines

Each Chwezi engine that serves presentation work carries its own complete copy of this doctrine, the
rules catalogue and the references, with identical IDs and wording, and works without any other
engine installed. This file is the canonical text; copies are re-synced whenever its version
changes.

## Change control

Peter Bamuhigire approves every change; semantic versions (patch for wording, minor for new SHOULD
or MAY rules and blueprints, major for any new, removed or re-levelled MUST, any gate or any
threshold); every release logged in the engine's change record (its `CHANGELOG.md` or dated update
notes) with the rule IDs affected. After each delivery a Kaizen retrospective records the failure,
cause, corrective rule, component change, added test and owner.
