Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Mathematics and algorithms

Use this reference to replace guesswork with computation wherever a proven method gives a better
document: type scale, line length, vertical rhythm, page breaking, rounding, chart axes and
proportions, colour, image resolution, output identity and visual regression. Craft decides what a
page should say; these methods make sure every page says it precisely and reproducibly. Rule IDs:
[rules-and-gates.md](rules-and-gates.md). Numbers below were computed on 2026-11-08; sources are cited
as durable concepts, not currentness facts.

## Task 1: derive the type scale (PUB-MATH-001)

Use a modular scale: `size(n) = body x ratio^n`, rounded to 0.5 pt.

| Step n | Role | Body 10.5 pt, ratio 1.25 | Handbook range |
|---|---|---|---|
| -1 | Notes, captions | 8.4 pt | 8-9 pt |
| 0 | Body | 10.5 pt | 9.5-11 pt |
| 1 | H2 | 13.1 pt | 12-16 pt |
| 3 | H1 | 20.5 pt | 17-22 pt |
| 5 | Cover title | 32.0 pt | 26-36 pt |

Every derived size falls inside the handbook's range, so the hierarchy is both mathematically
consistent and compliant. Ratio 1.2 at body 10 pt also fits (8.3, 10, 12, 17.3; cover at step 7 is
35.8 pt). Record the body size and ratio as tokens; never type one-off sizes.

## Task 2: set the measure (PUB-MATH-002)

Comfortable running text holds about 45-75 characters per line, with about 66 as a target
(Bringhurst, *The Elements of Typographic Style*). Characters per line = text width / (body size x
average character width), where the average character width comes from the chosen font's metrics
(measure it on a reference paragraph; it is typically 0.45-0.55 em).

| A4 portrait, 18 mm margins (174 mm text width) | Characters per line |
|---|---|
| One full-width column, body 10.5 pt | 85-104 (too long for running prose) |
| Two columns with a 6 mm gutter, body 10.5 pt | 41-50 (lower edge of the range) |
| Width for 66 characters at 10.5 pt | 110-134 mm |

Consequence: on A4 portrait, running prose sits in a text block of about 110-135 mm (the rest of the
width carries notes, figures or white space) or in two columns; full width is for tables and figures.
Compute the exact width from the real font before fixing the template.

## Task 3: hold the vertical rhythm (PUB-MATH-003)

- Leading L = body x 1.15-1.4 (handbook); at 10.5 pt and 1.3, L = 13.65 pt.
- Every vertical space (paragraph gap, heading space, figure padding) is a multiple of L/2 so text
  across columns and pages lines up on one baseline grid.
- Lines per page = floor(text height / L). A4 with 18 mm margins and 10 mm header and footer zones
  leaves 241 mm of text height: 50 lines at 13.65 pt, 52 at 13 pt, 47 at 14.3 pt. Multiply by words
  per line to budget page counts for proposals and profiles before writing.

## Task 4: break lines well (PUB-MATH-004)

Justified text needs a whole-paragraph line-breaking algorithm with hyphenation (Knuth and Plass,
"Breaking paragraphs into lines", 1981: choose breaks that minimise the total badness of all lines,
not line by line). Where the renderer lacks one, set body text ragged-right; never justify narrow
columns without it, because greedy justification opens rivers of white space.

## Task 5: break pages optimally (PUB-MATH-005)

Treat pagination as a minimum-cost path. Candidate break points are the places a page may end;
each candidate page gets a cost; dynamic programming picks the sequence of breaks with the lowest
total cost (O(n^2) over candidates; the same idea Knuth and Plass applied to lines).

```text
cost(page) = sum of penalties + underfill
  heading or caption last on the page          infinite
  KPI card, signature or approval block split  infinite
  total separated from its label or last line  infinite
  table continued without repeated header      infinite
  single line of a paragraph left alone        100   (Chwezi weight)
  table group or subtotal block split          50    (Chwezi weight)
  underfill = 100 x (1 - fill)^3               (fill = used height / text height; last page exempt)
best[j] = min over i < j of best[i] + cost(page from break i to break j)
```

Infinite penalties enforce the hard pagination rules (PUB-PAGE-004); the weights trade a slightly
emptier page for a cleaner break. Tune the weights per template and record them.

## Task 6: round so the parts add up (PUB-MATH-006)

Compute in exact arithmetic (integers in the currency's minor unit, or exact decimals); never in
binary floating point (PUB-MATH-007). When displayed parts must add to a displayed whole (shares of
100%, an allocation split across lines, a bill split), use the largest-remainder method: floor every
part, then give the leftover units one each to the parts with the largest fractional remainders.

| Case | Naive rounding | Largest remainder |
|---|---|---|
| Three equal shares | 33% + 33% + 33% = 99% | 34% + 33% + 33% = 100% |

The rounding mode for single values (half up or half to even) is a stated policy in the metric
contract; totals are always computed from full precision and any unavoidable difference is
disclosed (PUB-FIN-005).

## Task 7: draw honest axes (PUB-MATH-008)

- Ticks use "nice numbers": the step is 1, 2 or 5 x 10^k, chosen from the data range and the wanted
  tick count (Heckbert, "Nice numbers for graph labels", 1990); for best results optimise
  simplicity, coverage, density and legibility together (Talbot, Lin and Hanrahan, 2010). Example:
  0 to 4,823,500 gives ticks every 1,000,000 from 0 to 5,000,000 (labels 0, 1M, ... 5M).
- Bars start at zero; a non-zero line baseline is labelled.
- Line charts choose their aspect ratio by banking to 45 degrees: scale height and width so the
  median absolute slope of the line segments is about 45 degrees (Cleveland, *Visualizing Data*,
  1993); trends are then neither flattened nor exaggerated.

## Task 8: compute colour, never eyeball it (PUB-MATH-009)

- Contrast uses the WCAG relative-luminance formula: linearise each sRGB channel
  (c / 12.92 if c <= 0.04045, else ((c + 0.055) / 1.055)^2.4), L = 0.2126 R + 0.7152 G + 0.0722 B,
  ratio = (L_light + 0.05) / (L_dark + 0.05). The handbook palette measures 13.19:1 (ink), 15.73:1
  (dark), 5.97:1 (muted) and 1.31:1 (rule) on white.
- Sequential palettes are interpolated in a perceptually uniform space (OKLab or OKLCH, Ottosson
  2020) with lightness changing monotonically, so equal data steps look equal.
- Categorical colours stay distinguishable: check adjacent pairs with a colour-difference formula
  (CIEDE2000) and with colour-vision-deficiency simulation, and keep series that must survive
  greyscale print apart in lightness, or add patterns.

## Task 9: check image resolution (PUB-MATH-010)

Effective resolution = image pixels / printed size in inches. Photographs target 300 ppi at their
printed size and are rejected below 150 ppi (Chwezi values); charts, diagrams and logos are vectors.
Oversized images are downsampled before embedding so documents stay light.

## Task 10: identify outputs and catch regressions (PUB-MATH-011)

- **Content identity.** Serialise the semantic model canonically (sorted keys, numbers as exact
  decimal strings, UTF-8) and hash it with SHA-256 together with the template and renderer versions.
  Equal hashes prove the same content; the hash is the generation ID or sits in the release record.
- **Numeric parity.** Extract the text layer of the PDF and the DOCX, pull every figure as an exact
  decimal string and compare it with the model; never compare through rounded floats or OCR when a
  text layer exists.
- **Visual regression.** Render pages at a fixed resolution and compare them with the approved golden
  pages using a perceptual similarity index such as SSIM (Wang et al., 2004) plus a pixel-difference
  map; flag any page below the agreed threshold for human review.

## Evidence/currentness

Methods are cited as durable concepts: Bringhurst (measure), Knuth and Plass 1981 (line breaking),
Heckbert 1990 and Talbot, Lin and Hanrahan 2010 (axis ticks), Cleveland 1993 (banking to 45
degrees), Ottosson 2020 (OKLab), CIEDE2000 (colour difference), Wang et al. 2004 (SSIM), the
largest-remainder method of apportionment, the WCAG 2.2 luminance formula. Penalty weights, the
ppi targets and the 1.3 leading example are Chwezi values; computed figures were produced on
2026-11-08.
