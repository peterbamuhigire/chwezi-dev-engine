Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Presentation and Slide Deck Design Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Production contracts

Use this reference to build the deck in PowerPoint, export the landscape PDF, govern images and
motion, and make the deck work on every device. Rule IDs: [rules-and-gates.md](rules-and-gates.md);
facts: [currentness-register.md](currentness-register.md).

## Task 1: set the design tokens

| Token | Default (Chwezi value) |
|---|---|
| Canvas | 16:9, 13.333 x 7.5 in; 4:3 only for constrained venues |
| Safe area | At least 0.45 in left and right, 0.35 in top and bottom; outer margins start at 0.45-0.65 in; footer region reserved |
| Grid | 12 columns, 0.16-0.24 in gutters; 5:7 or 6:6 splits, three-up comparisons or one large evidence panel |
| Type | Title 28-36 pt; divider 34-48 pt; cover headline 30-48 pt; body 18-24 pt projected (never below the venue minimum or 16 pt); labels 14-18 pt; sources 10-12 pt; marked appendix 12-16 pt |
| Palette | Primary, secondary, accent, neutral text and background, four semantic status colours; status also by label or icon |
| Spacing | 4, 8, 12, 16, 24, 32, 48 pt |
| White space | 20-35% of most slides, measured on the render |
| Tone | Crisp vectors, authentic photographs, confident headings, precise figures, consistent geometry, restrained animation; no excess gradients, shadows, glass, bevels or novelty fonts |

Typeface choice follows the engine's typography doctrine and banned-font list; state the typeface and
the reason. Light and dark masters keep the same semantic colour assignments.

## Task 2: build editable PowerPoint (DECK-PPTX-001 to 004)

- **Native objects.** Editable text boxes; editable charts where supported; diagrams as grouped
  editable shapes; native tables; raster only for photographs or complex art.
- **Masters.** Slide Master layouts for cover, section, assertion plus chart, image plus story,
  comparison, table, timeline, roadmap, quotation, conclusion and appendix.
- **Names and layers.** Meaningful shape names (title_main, chart_sales_by_month, source_note,
  brand_logo); consistent layer order; related objects grouped; no invisible objects or unintended
  overlaps.
- **Theme.** Fonts and colours bound to the theme, so a client can be rebranded without rebuilding.
- **Notes.** Speaker notes for claims that need interpretation, likely objections, source caveats and
  transitions; no unverified claim enters the notes.
- **Accessibility.** Reading order, alt text for informative images, descriptive links, high-contrast
  labels, unique meaningful slide titles, logical grouping.
- **Reliability.** Explicit slide size; fonts embedded or consistently substituted and tested on a
  second machine; charts keep their source data or a documented extract; hyperlinks work; image sizes
  sensible.

## Task 3: export the landscape PDF (DECK-PDF-001 to 004)

- Same size, order and orientation as the slides; embedded fonts; vector text and charts where
  possible; no clipping, rasterised body text, missing glyphs or colour shifts.
- Title metadata, bookmarks for major sections where tooling allows, working links, meaningful page
  numbers; slide count equals page count.
- Export a tagged PDF where supported and validate accessibility separately; a plain slide export is
  not assumed accessible.
- Optional printer-friendly variant: no full-bleed dark backgrounds on every page, economical ink,
  readable greyscale.
- Compare every PDF page with its slide: count, orientation, margins, tables, charts, images, links.

## Task 4: govern images and icons (DECK-ASSET-001 to 004)

| Topic | Rule |
|---|---|
| Licensing | Owned, commissioned, licensed or explicitly permitted only; marketplace and pinboard images are not reusable by default; keep a licence manifest |
| Authenticity | Real client locations, teams, facilities and products first; Ugandan and East African context where relevant, without tokenism |
| Cropping | Crop to the subject, protect text safe zones, never stretch, avoid awkward face and hand crops |
| AI imagery | Disclose where relevant; never present synthetic patients, employees, facilities or outcomes as real evidence |
| Performance | Enough resolution for 1080p (144 pixels per slide inch) with a high-quality master for print; no needlessly huge media |

## Task 5: use motion with care (DECK-MOTION-001 to 003)

Simple appear, fade or build only where it clarifies sequence, comparison or causality; no distracting
transitions or long chains. Every animation-driven explanation has a static readable counterpart, and
every essential point is visible in the static PDF. Plan one key claim per slide and a realistic total
runtime. Presenter mode uses notes, section markers and optional backup slides; the deck runs without
internet, remote fonts or external embedded content.

## Task 6: test across devices (DECK-LEGIB-002, DECK-COMPAT-001/002)

| Context | Test |
|---|---|
| Projection | 1920x1080 and 1280x720; legible at the back of the room (compute the venue minimum) |
| Laptop | 1366x768, where dense grids and tiny labels fail; no interactive dependencies |
| Phone review | A PDF with large headlines, optionally a separate vertical executive summary; never promise comfortable phone reading of a full 16:9 deck |
| Older systems | Common fonts, native shapes, simple effects, JPEG or PNG photographs, conventional transitions; no heavy video, unsupported SVG filters or exotic codecs |
| Offline | Embedded assets; no live linked charts without a validated update workflow |

## Task 7: charts with statistical integrity (DECK-CHART-001 to 006)

| Question | Chart |
|---|---|
| Trend | Line (or column) |
| Ranking | Sorted horizontal bars |
| Composition | Stacked bars with few categories; sorted bars before pies; a doughnut labels shares and total |
| Distribution | Histogram or box plot |
| Relationship | Scatter |
| Workflow | Process diagram |

Bars start at zero; a non-zero line baseline is labelled; comparable small multiples share scales; no
3D. Each chart carries unit, period, source, denominator, definitions and freshness; percentages and
percentage points are kept apart; forecasts show ranges or scenarios and are marked as forecasts;
missing observations are explained; illustrative data is labelled. Financial charts state currency,
scale, period and whether figures are actual, forecast or budget, nominal or constant, net or gross,
tax-inclusive or exclusive, and every total reconciles to its source.

## Evidence/currentness

PowerPoint accessibility guidance, Office Open XML and tagged-PDF facts: register PR2, PR5 and PR6.
Token values are Chwezi values from the handbook.
