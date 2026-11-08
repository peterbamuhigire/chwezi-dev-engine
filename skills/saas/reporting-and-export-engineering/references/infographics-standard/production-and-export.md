Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Infographics Design and Production Quality Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Production and export

Use this reference to set tokens and to produce each delivery format. Calculations:
[mathematics-and-algorithms.md](mathematics-and-algorithms.md). Rules:
[rules-and-gates.md](rules-and-gates.md).

## Typography token sheet (handbook Annex C)

| Field | Content |
|---|---|
| Roles | Display, heading, subheading, body, annotation, source; each with family, weight, size and line height per medium |
| Families | At most two, chosen under the banned-font doctrine. Defaults: Public Sans with tabular figures for headings, body and data; Source Serif 4 for editorial serif text; Atkinson Hyperlegible for low-vision and signage work; matching Noto family for non-Latin scripts; Georgia and Aptos as fallbacks only |
| Minimum size | Computed per role from its reading distance at actual output size (task 1), never below the floor of the medium |
| Numbers | Tabular figures, thousands grouping, ISO 4217 decimals, true minus sign, units with a space, dates as `4 Nov 2026`, sentence case |
| Fallbacks and glyphs | Fallback chain recorded; every glyph of every shipped language verified in the rendered output |
| Pseudo-text | Zero tolerance: any generated or warped lettering is a gate failure, not a minor defect |

## Layout token sheet (handbook Annex D)

| Field | Content |
|---|---|
| Canvas | Size, orientation, safe area, margins, columns and gutters per rendition |
| Spacing | 8-point base (8 to 64); 4 and 12 as recorded optical exceptions |
| Strokes and shapes | Border, radius, stroke weight, icon size and connector style tokens; no stroke under 0.5 pt in pale colours for print (Chwezi value) |
| Image to text | The image-to-text proportion and the focal region are stated |
| Adaptation | Mobile stacking order and print adaptation keep the narrative order |
| Alignment | Edges aligned to the grid, with optical adjustments recorded (round and pointed shapes overshoot slightly) |

## Illustration commissioning sheet (handbook Annex E)

Objective and exact subject; required objects, relationships and excluded elements; style (flat,
editorial, isometric) and palette; no photorealistic generated people or scenes; no generated
embedded text or fake logos; illustration and editable text on separate layers; expert review for
technical accuracy.

## Delivery formats

| Format | Master and build | Checks before release |
|---|---|---|
| Web and SaaS | Semantic HTML plus accessible SVG (`role="img"`, `title`, `desc`, or a figure with a linked description); print stylesheet and server-side PDF share the tokens | States designed; period, filters, generation time and provenance shown; keyboard and screen-reader order; zoom and reflow |
| Social and mobile | Canvas per variant (square, portrait, story); text sized by the canvas-to-slot scale | Real phone at normal brightness, after platform compression, without zoom; crops and overlays clear; alt text |
| PowerPoint | Native shapes, editable charts and SVG; high-resolution raster only where appropriate | 16:9 projection, presenter view, PDF conversion, font substitution, cropping, projector contrast |
| DOCX | Inline or deliberately anchored images; captions and source notes | Paginated render: no overlap on repagination, no split caption, cross-references and bookmarks, embedded resolution |
| Screen PDF | Selectable live text, bookmarks, tags where feasible | Text selectable, links work, reading order |
| Press PDF | Trim, bleed (commonly 3 mm), safe margin (at least 5-10 mm, per finishing), embedded fonts, agreed colour profile, page boxes, crop marks if asked | Preflight: effective ppi, total ink, overprint, black text, transparency policy; actual-size proof signed |
| SVG | Master for diagrams, icons and text-rich art: viewBox, explicit size, semantic groups, stable ids, no external links | Validates; renders identically in target browsers; text remains text |
| PNG | Export only, at target size and 2x where needed | Antialiasing, transparency, edge sharpness, file size |

## Print vendor handoff (handbook Annex K)

1. Trim size and orientation (A2: 420 x 594 mm portrait or 594 x 420 mm landscape).
2. Bleed, crop marks, safe margins and finishing (lamination, mounting, eyelets).
3. Colour space, ICC profile, total ink limit and black treatment, agreed with the printer.
4. Font embedding and transparency flattening policy.
5. Effective resolution of every image and vector integrity.
6. Proof sign-off, print run quantity and the version identifier printed in the slug.

## Responsive and export matrix (handbook Annex H)

Each rendition is rendered and inspected at actual size, with the result recorded (requirement,
specified value, observed result, pass or fail, issue reference, reviewer, date):

| Rendition | Inspect |
|---|---|
| Desktop browser SVG/HTML | Layout, live text, links, hover and focus |
| Tablet portrait and landscape (medium width, 600-839) | Two-column or side-by-side layouts hold; touch targets for interactive versions; rotation keeps order |
| Mobile portrait and narrow screen (compact width, under 600) | Stacking order, text size, no horizontal scroll |
| Social square, portrait, story | Safe zones, first frame, compression |
| Presentation 16:9 | Projected legibility at the venue |
| DOCX inline or anchored | Repagination, caption, resolution |
| Screen PDF | Selectable text, bookmarks |
| A2 print PDF | Bleed, colour profile, actual-size proof |

## Performance and privacy

Compress appropriately; lazy-load below-the-fold visuals; prefer vectors to large raster backgrounds;
keep SVG `title`, `desc` and ids when optimising. Redact names, account identifiers, patient details
and location-sensitive data in examples; validate export authorisation; clean up temporary files.
