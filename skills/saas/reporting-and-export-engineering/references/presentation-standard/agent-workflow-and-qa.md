Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Presentation and Slide Deck Design Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Agent workflow, scorecards and release

Use this reference to run a deck from brief to release, as a human team or an agent. Rule IDs:
[rules-and-gates.md](rules-and-gates.md).

## Task 1: follow the ten steps

| Step | Work | Exit |
|---|---|---|
| 1 Brief | Audience, decision, topic, constraints, references, brand, evidence, formats, talk length, venue, confidentiality, localisation, compatibility | Decision record with unresolved high-risk unknowns |
| 2 Evidence | Inventory sources; verify dates and numbers; log uncertainty; build the claim ledger | No material claim without evidence |
| 3 Storyboard | One-sentence thesis; conclusion-led headlines; remove repetition; executive summary, not an agenda; appendix kept separate | Headline-only read makes the argument |
| 4 Design system | Palette, typography, master layouts, grid, chart rules, image treatment; compute the venue minimum size | Tokens recorded |
| 5 Build | Blueprint by communication job; native objects; charts from the verified dataset; diagrams, tables, notes, appendix | Editable PPTX |
| 6 Editorial QA | Logic, terminology, tone, plain English, spelling, data consistency, decision usefulness | Senior reviewer sign-off |
| 7 Visual QA | Render every slide at full size and as thumbnails: bounding boxes, line wraps, contrast, crops, chart labels, footer position | No clipped element |
| 8 Accessibility QA | Reading order, contrast, text size, slide titles, alt text, link text, status coding, localisation; understandable without colour or animation | Accessibility record |
| 9 Export QA | Export the landscape PDF; compare page count and every page; verify links and fonts; open in PowerPoint and a compatible viewer; offline test | PDF parity record |
| 10 Handoff | PPTX, PDF when requested, source and claim register, visual QA log, licence manifest, assumptions, change log, handoff manifest | Release package |

**Do not proceed** when evidence for a material claim is unavailable, the requested representation
would mislead, licensing is unclear, or the output cannot be checked for clipping, corruption and
compatibility.

## Task 2: keep the claim ledger (DECK-EVID-001)

```yaml
claims:
  - id: C-07
    slide: S04
    claim: "Branch sales rose 12.5% on the previous month"
    source: "sales.net_sales v1.2, snapshot sales/2026-10/r3 (fictional)"
    evidence_date: 2026-11-01
    calculation: "(4,500,000 - 4,000,000) / 4,000,000"
    unit: "% change, UGX basis"
    interpretation: "Observed; cause not verified"
    confidence: high
    status: verified          # verified | needs-confirmation | illustrative | blocked
```

A claim marked blocked never reaches the exported deck; an illustrative value is labelled on the slide.

## Task 3: score the deck

**Deck dimensions** (each 1 to 5; release needs at least 4 in every one):

| Dimension | 1 (poor) | 5 (excellent) |
|---|---|---|
| Narrative | Unrelated topic slides | A compelling, decision-led argument |
| Evidence | Unverified claims | Traceable, qualified data |
| Readability | Tiny dense text | A projection-safe hierarchy |
| Visual craft | Template clutter | Cohesive, intentional design |
| Technical | Broken exports | Editable PPTX and a verified PDF |
| Actionability | No decision | Explicit ask, owner and next step |

**Slide scorecard** (100 points; release needs an average of at least 90 and no critical failure in
evidence integrity, confidentiality, file corruption or readability):

| Category | Points | Scored on |
|---|---|---|
| Story and relevance | 20 | Clear assertion, audience fit, decision contribution |
| Evidence and accuracy | 20 | Traceable sources, correct calculations, caveats |
| Readability | 20 | Hierarchy, typography, contrast, projection legibility |
| Design consistency | 15 | Master, alignment, spacing, restrained visuals |
| Editability and technical | 15 | Native objects, clean export, nothing broken |
| Accessibility and compliance | 10 | Alt text, reading order, rights, confidentiality |

## Task 4: pass the release test matrix (DECK-QA-004)

| Dimension | Test | Pass condition |
|---|---|---|
| Narrative | Headline-only review | A clear argument and an actionable conclusion |
| Evidence | Claim-ledger reconciliation | No unsupported material claim |
| Visual | Rendered slide review | No clipping, collisions or tiny labels |
| Projection | 720p and 1080p simulation, venue minimum computed | Key content legible |
| PPTX | Open, edit, replace the theme | Objects stay editable |
| PDF | Page-by-page comparison | Visual parity at the correct landscape size |
| Accessibility | Reading order, contrast, alt text | Material information accessible |
| Performance | Offline open and navigation | No broken links or assets, no undue delay |
| Governance | Licence and sensitivity audit | Approved assets and data handling |

## Task 5: hand over (DECK-QA-003)

The handoff manifest names: client or project and document title; audience and decision sought; deck
version and date; PPTX and PDF file names; source register and claims still to confirm; licensed
imagery inventory; runtime and recommended delivery mode; known compatibility limits; final QA reviewer
and sign-off status.

## Task 6: improve after delivery

After stakeholder feedback, record the observed failure, its cause, the corrective design rule, the
reusable component change, the added test and the owner; re-test the affected blueprints and update the
standard's version through change control.

## Master instruction (agents)

"Produce a decision-ready, visually exceptional, technically robust PowerPoint deck and, when
requested, a matching landscape PDF. First establish the audience, the decision and the claim ledger.
Build a storyboard of assertion headlines. Use the approved 16:9 master, the brand tokens and the most
relevant blueprint for each communication job. Compute the minimum legible size for the venue. Use only
verified data and licensed assets. Keep text, charts, tables and diagrams editable. Make the deck
legible at 720p, accessible, offline-capable and compatible with older Office versions. Include source
notes, caveats and speaker notes as appropriate. Render and inspect every slide, export and compare the
PDF, correct defects, and deliver a QA log and a handoff manifest. Never fabricate figures,
credentials, testimonials, customers, product features or sources."

## Evidence/currentness

No external fact is cited here. The scorecard weights and thresholds are the handbook's internal
governance values; the claim-ledger example is fictional.
