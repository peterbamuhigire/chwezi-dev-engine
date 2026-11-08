Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Presentation and Slide Deck Design Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Rules and gates

Every normative rule of the Chwezi Presentation and Slide Deck Design Standard, version 1.0.0,
adopted 8 November 2026. Binding text: `doctrine/presentation-standard.md`.

## How to read this catalogue

- **ID** `DECK-<AREA>-NNN` is stable and never reused. **Lvl**: MUST, SHOULD (departure needs a design
  decision record), MAY. **Gate**: the DECK hard gate a failure trips (blank = scored finding).
- **Ev**: RENDER (every slide rendered at full size and as thumbnails, inspected, reviewer named),
  PROJ (projection or simulation at 1920x1080 and 1280x720), PDF (page-by-page comparison with the
  PPTX), LEDGER (claim-ledger entry), CALC (recorded calculation), REVIEW (named review), RECORD (QA log
  or handoff manifest), AT (accessibility check).
- Values marked "Chwezi value" are internal defaults from the handbook or computed here, not external
  facts.

## Hard gates

| Gate | Short name | Main rules |
|---|---|---|
| DECK-GATE-01 | Unsupported claim | DECK-EVID-001/002/003 |
| DECK-GATE-02 | Illegible in use | DECK-LEGIB-001/002 |
| DECK-GATE-03 | Visual defect | DECK-QA-002, DECK-ASSET-003 |
| DECK-GATE-04 | Export failure | DECK-PDF-001/002 |
| DECK-GATE-05 | Not editable | DECK-PPTX-001/002 |
| DECK-GATE-06 | Rights or confidentiality | DECK-ASSET-001/002, DECK-GOV-002 |
| DECK-GATE-07 | Misleading figure | DECK-CHART-002/003/004 |
| DECK-GATE-08 | Uninspected release | DECK-QA-001/003 |

## Brief (BRIEF)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-BRIEF-001 | MUST | | Before design, record audience (board, investor, procurement panel, technical team, public), mode (live, self-reading, hybrid), decision sought, talk length, language, venue, brand, sources, sensitivity, deadline, deliverable formats and editability needs. | Brief record | RECORD |
| DECK-BRIEF-002 | MUST | | High-risk unknowns are recorded and resolved before build; minor gaps carry stated assumptions. | Decision record | RECORD |

## Story (STORY)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-STORY-001 | MUST | | A one-sentence thesis and a storyboard of assertion headlines exist before any slide is built; the headlines alone form a coherent argument. | Headline-only review | REVIEW |
| DECK-STORY-002 | MUST | | Each slide carries one decision-relevant message in a conclusion headline, not a topic label. | Review | REVIEW |
| DECK-STORY-003 | MUST | | The sequence fits the deck type (executive review, investor pitch, consulting proposal, project status, training, case study); within the first three slides the audience problem, why now and the decision sought are clear. | Review | REVIEW |
| DECK-STORY-004 | MUST | | The close restates the recommendation, quantified implications where evidenced, owner, timing, next action and open questions; a decorative "Thank you" is never the only conclusion. | Review | REVIEW |
| DECK-STORY-005 | MUST | | The executive summary gives 3-5 evidence-backed findings and an explicit decision or next action; an agenda is not a summary. | Review | REVIEW |
| DECK-STORY-006 | SHOULD | | Methods, source tables, workings, biographies and supplementary charts sit in a navigable appendix linked from the main deck. | Review | REVIEW |

## Layout (LAYOUT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-LAYOUT-001 | MUST | | The blueprint is selected by communication job, not by available template art; hierarchy, grid, safe zone, reading order, chart type, whitespace and brand tokens are assigned before rendering. | Selection record | RECORD |
| DECK-LAYOUT-002 | SHOULD | | The title zone sits at the top; the primary evidence or visual takes 55-70% of the content area; secondary explanation takes the rest; never several unrelated messages on one slide. | Render review | RENDER |
| DECK-LAYOUT-003 | MUST | | Each blueprint meets its content contract and excludes its failure modes (see the blueprint reference). | Review | REVIEW |

## Tokens (TOKEN)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-TOKEN-001 | MUST | | Canvas 16:9 at 13.333 x 7.5 in (4:3 only when the venue requires it); safe area at least 0.45 in horizontally and 0.35 in vertically, outer margins starting at 0.45-0.65 in, footer region reserved; nothing bleeds beyond the safe area. | Template check | RENDER |
| DECK-TOKEN-002 | SHOULD | | A 12-column grid with 0.16-0.24 in gutters; splits of 5:7 or 6:6, three-up comparisons, or one large evidence panel; every edge on a guide. | Template check | RENDER |
| DECK-TOKEN-003 | SHOULD | | Type ladder (Chwezi values): title 28-36 pt, section divider 34-48 pt, cover headline 30-48 pt, body 18-24 pt projected, labels 14-18 pt, sources 10-12 pt; a dense appendix may go to 12-16 pt and is marked as appendix. | Template check | RENDER |
| DECK-TOKEN-004 | MUST | | Palette: one primary, one secondary, one accent, neutral text and background, four semantic status colours; text contrast at least 4.5:1 (3:1 for large text); status also by label or icon. | Contrast record | CALC |
| DECK-TOKEN-005 | SHOULD | | 20-35% of most slides is intentional empty space (measured on the render); spacing from the scale 4, 8, 12, 16, 24, 32, 48 pt. | Measurement | CALC |
| DECK-TOKEN-006 | SHOULD | | Light and dark masters share the same semantic colour assignments; restraint over gradients, glass, bevels, shadows and novelty fonts. | Review | RENDER |

## Legibility (LEGIB)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-LEGIB-001 | MUST | 02 | Presented body text is at least the computed venue minimum: size >= 4.5 x (farthest viewing distance / screen image height) pt (20 arc-minute cap height, cap height 0.7 em, 540 pt slide height; recompute for the actual font), and never below 16 pt. | Calculation per venue | CALC |
| DECK-LEGIB-002 | MUST | 02 | Key content stays legible at 1920x1080 and 1280x720 projection and on a 1366x768 laptop. | Projection simulation | PROJ |
| DECK-LEGIB-003 | SHOULD | | Where room geometry is known, the screen is sized so each pixel subtends no more than about one arc-minute at the farthest seat for analytical content (image height >= distance x vertical pixels / 3438). | Calculation | CALC |

## Charts (CHART)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-CHART-001 | MUST | | Chart by question: trend line or column; ranking sorted horizontal bars; composition stacked bars with few categories (sorted bars before pies; a doughnut labels shares and total); distribution histogram or box plot; relationship scatter; workflow process diagram. | Review | REVIEW |
| DECK-CHART-002 | MUST | 07 | Bars start at zero; a non-zero line baseline is labelled; comparable small multiples share scales; no 3D, gratuitous gauges or pictograms in place of precise values. | Review | REVIEW |
| DECK-CHART-003 | MUST | 07 | Every chart shows unit, period, source, denominator, definitions and freshness; percentages and percentage points are never mixed; forecast, target, missing data and uncertainty (ranges or scenarios) are distinct from actuals. | Review | REVIEW |
| DECK-CHART-004 | MUST | 07 | Financial figures state currency, scale, period and whether they are actual, forecast or budget, nominal or constant, net or gross, tax-inclusive or exclusive; every displayed total reconciles to its source. | Reconciliation | CALC |
| DECK-CHART-005 | MUST | | Direct labels or textures and line styles where needed; a textual takeaway; maps label geography, avoid area distortion and add a table when precise values matter. | Review | REVIEW |
| DECK-CHART-006 | SHOULD | | Charts are editable chart objects built from the verified dataset with defined axes, transformations, missingness, comparison basis and annotations. | PPTX check | REVIEW |

## Evidence (EVID)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-EVID-001 | MUST | 01 | A claim ledger records for every material claim: claim ID, slide ID, exact source, evidence date, confidence, calculation, unit, interpretation and verification status. | Ledger | LEDGER |
| DECK-EVID-002 | MUST | 01 | No invented statistics, testimonials, names, affiliations, customers, credentials, awards, product features or sources; unsupported claims are blocked from export; illustrative values are marked as illustrative. | Ledger audit | LEDGER |
| DECK-EVID-003 | MUST | 01 | Case studies and impact slides state baseline, intervention, outcome, period, sample, source and limitations; correlation is never labelled as proven impact; clinical efficacy, carbon and similar claims need verified evidence. | Review | REVIEW |
| DECK-EVID-004 | MUST | | Source URLs and retrieval dates are kept, assumptions logged and externally distributed claims approved. | Source register | RECORD |

## Assets (ASSET)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-ASSET-001 | MUST | 06 | Only owned, commissioned, licensed or explicitly permitted images, icons and logos; marketplace and pinboard images are not reusable by default; quotes are attributed and permissioned. | Licence manifest | RECORD |
| DECK-ASSET-002 | MUST | 06 | AI-generated visuals are disclosed where relevant and never presented as real patients, employees, facilities, products or outcomes. | Review | REVIEW |
| DECK-ASSET-003 | MUST | 03 | Photographs keep their aspect ratio, are cropped to the subject without awkward face or hand crops, protect text safe zones and carry no watermark; authentic Ugandan and East African context is preferred where relevant, without tokenism. | Render review | RENDER |
| DECK-ASSET-004 | SHOULD | | Image resolution: at least 144 pixels per slide inch at the displayed size for 1080p (288 for 4K), without needlessly huge media. | Calculation | CALC |

## Motion and delivery (MOTION)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-MOTION-001 | MUST | | Animation only where it clarifies sequence, comparison or causality (simple appear, fade or build); every animation-driven explanation has a static readable equivalent. | Static PDF review | PDF |
| DECK-MOTION-002 | SHOULD | | Runtime fits the talk: about 30-90 seconds per substantive slide, so a 15-minute briefing carries about 10-30 substantive slides; speaker notes give 30-90 seconds of guidance per substantive slide (emphasis, interpretation, transition, caveat, likely question) and introduce no unverified claim. | Timing calculation | CALC |
| DECK-MOTION-003 | MUST | | The deck works without internet, remote fonts or external embedded content; no live linked charts without a validated update workflow. | Offline test | RENDER |

## PowerPoint (PPTX)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-PPTX-001 | MUST | 05 | Text as editable text boxes, charts as editable charts where supported, diagrams as grouped editable shapes, tables as native tables; raster only for photography or complex art. | Open and edit | REVIEW |
| DECK-PPTX-002 | MUST | 05 | Fonts and colours bound to the theme so rebranding needs no rebuild; Slide Master layouts for cover, section, assertion plus chart, image plus story, comparison, table, timeline, roadmap, quotation, conclusion and appendix. | Replace-theme test | REVIEW |
| DECK-PPTX-003 | SHOULD | | Shapes have meaningful names (title_main, chart_sales_by_month, source_note, brand_logo); layer order is consistent; no invisible or unintended overlapping objects; related objects grouped. | Selection pane review | REVIEW |
| DECK-PPTX-004 | MUST | | Explicit slide size; fonts embedded or consistently substituted and tested on a second machine; charts keep their source data or a documented extract; hyperlinks work. | Second-machine test | REVIEW |

## PDF (PDF)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-PDF-001 | MUST | 04 | The PDF is landscape at the slide's size and order, with embedded fonts, vector text and vector charts where possible; no clipping, rasterised body text, missing glyphs or distorted colours. | Page-by-page comparison | PDF |
| DECK-PDF-002 | MUST | 04 | Slide count equals page count; title metadata, bookmarks for major sections where tooling supports them, working links and meaningful page numbers. | Comparison | PDF |
| DECK-PDF-003 | MUST | | A tagged PDF is exported where supported and accessibility is validated separately; an ordinary slide export is not assumed accessible. | Validator record | AT |
| DECK-PDF-004 | SHOULD | | An optional printer-friendly variant: no full-bleed dark background on every slide, economical ink, readable greyscale. | Greyscale print | PDF |

## Accessibility and localisation (A11Y)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-A11Y-001 | MUST | | Meaningful reading order, unique descriptive slide titles, alt text for informative images, descriptive links, high-contrast labels, logical grouping; understandable without colour or animation. | Accessibility check | AT |
| DECK-A11Y-002 | MUST | | Right-to-left, accented languages, long labels, East African currency conventions and locale dates are supported without shrinking body copy to fit translations. | Locale fixtures | RENDER |

## Compatibility (COMPAT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-COMPAT-001 | SHOULD | | Common fonts, native shapes, simple effects, JPEG or PNG photography and conventional transitions; no heavyweight video, unsupported SVG filters or exotic codecs; tested in PowerPoint and a compatible viewer, and in older Office versions where required. | Compatibility test | REVIEW |
| DECK-COMPAT-002 | MUST | | Phone review uses a PDF with large headlines, optionally a vertical executive summary; a full 16:9 deck is never promised as comfortable phone reading. | Review | REVIEW |

## Governance (GOV)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-GOV-001 | MUST | | Each deck is versioned; the PPTX is the editable master; reusable templates are under version control and improved after each delivery. | Version record | RECORD |
| DECK-GOV-002 | MUST | 06 | Confidentiality, redaction and sharing permissions are checked before export of sensitive client material. | Sensitivity audit | REVIEW |

## Mathematics (MATH)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-MATH-001 | SHOULD | | Type sizes come from a modular scale: body 20 pt x 1.25^n gives sources 10.2, labels 16, body 20, title 31.3, divider 39.1 pt, each inside the handbook ladder. | Token record | CALC |
| DECK-MATH-002 | MUST | | Exact arithmetic for money and quantities; displayed shares that must sum to 100% use largest-remainder rounding. | Fixture | CALC |
| DECK-MATH-003 | SHOULD | | Axis ticks use nice numbers (1, 2 or 5 x 10^k); line charts are banked so the median segment slope is about 45 degrees. | Chart review | REVIEW |

## Quality assurance (QA)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| DECK-QA-001 | MUST | 08 | Every slide is rendered and inspected at full size and as thumbnails (bounding boxes, line wraps, contrast, crops, chart labels, footer position), and the PDF is compared page by page. | Render log | RENDER, PDF |
| DECK-QA-002 | MUST | 03 | No clipping, collision, orphaned text, tiny labels, placeholder text, watermark or source-template branding in any slide. | Render log | RENDER |
| DECK-QA-003 | MUST | 08 | The release package holds the PPTX, the landscape PDF when requested, the source and claim register, the visual QA log, the licence manifest, assumptions, the change log and the handoff manifest, with exact names and version. | Package check | RECORD |
| DECK-QA-004 | MUST | | The release test matrix passes (narrative, evidence, visual, projection, PPTX, PDF, accessibility, performance, governance); the six deck dimensions each score at least 4 of 5 and the slide scorecard averages at least 90 of 100 with no critical failure. | Scorecards | RECORD |

## Evidence/currentness

External facts behind DECK-TOKEN-004, DECK-LEGIB-001/003 and DECK-PDF-003 are recorded in
[currentness-register.md](currentness-register.md); the methods behind the MATH and LEGIB rules are
in [mathematics-and-legibility.md](mathematics-and-legibility.md).
