Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Infographics Design and Production Quality Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Mathematics and algorithms

Use this reference to compute what an infographic needs instead of guessing: type size for a reading
distance, image resolution, canvas text on phones, honest encodings, correct diagram structure, ring
and timeline geometry, colour separation, ink limits, translation space and the release score. The
bundled checker, [check_infographic.py](check_infographic.py), implements tasks 1-8 and
11 with the Python standard library only. Figures were computed on 2026-11-08; external parameters
are in [currentness-register.md](currentness-register.md). Rule IDs:
[rules-and-gates.md](rules-and-gates.md).

## Task 1: minimum type size for a reading distance (INFO-TYPE-003)

Text is legible when its capital letters subtend enough visual angle. With a target cap height of
theta arc-minutes, reading distance D and cap height c as a fraction of the font size:

```text
cap height        h = D x tan(theta)
font size         s = h / c, converted to points (1 pt = 25.4/72 mm)
theta = 20', c = 0.70:   s ~= 23.6 x D(m) points at actual print size
```

| Reading distance | 0.3 m | 0.4 m | 0.5 m | 1 m | 1.5 m | 2 m | 3 m | 5 m |
|---|---|---|---|---|---|---|---|---|
| Minimum size | 7.1 pt | 9.4 pt | 11.8 pt | 23.6 pt | 35.3 pt | 47.1 pt | 70.7 pt | 117.8 pt |

Set each text role from the farthest distance at which that role must be read. For an A2 poster in
a corridor: the title is read at 3 m (at least 71 pt), the body at 1 m (at least 24 pt), annotations
and sources at 0.5 m (at least 12 pt). These agree with long-standing poster practice, which is a
useful cross-check; 20 arc-minutes is a Chwezi parameter (register IF4). For a projected
infographic use the Presentation standard's venue law (about 4.5 x D/H pt on a 540 pt slide); for a
document the printed size is read at 0.3-0.4 m.

## Task 2: image resolution for print (INFO-PRINT-002)

Effective resolution is what the printer actually receives, after scaling:

```text
effective ppi    = pixel width / printed width in inches
required ppi     ~= 3438 / D(in)     (one pixel per arc-minute at the closest reading distance)
```

| Closest reading distance | 0.3 m | 0.5 m | 1 m | 2 m | 3 m |
|---|---|---|---|---|---|
| Required ppi | 291 | 175 | 87 | 44 | 29 |

The familiar 300 ppi is the 0.3 m case; a poster read from 1 m needs only about 90 ppi, so Chwezi
uses at least 150 ppi for posters (Chwezi value) and 300 ppi for anything handled. A2 trim
(420 x 594 mm) is 2,480 x 3,508 px at 150 ppi and 4,961 x 7,016 px at 300 ppi; with 3 mm bleed
(426 x 600 mm) it is 2,516 x 3,543 and 5,031 x 7,087 px.

## Task 3: canvas text for phones and social feeds (INFO-SOCIAL-002)

A social image is drawn on a large canvas but displayed in a narrow slot. Text that must be read
without zoom needs:

```text
canvas text px  >=  minimum CSS px  x  (canvas width / slot width in CSS px)
```

A 1,080 px square shown in a 360 px slot is scaled by 3: 12 CSS px annotations need 36 px on the
canvas and 16 CSS px body text needs 48 px (Chwezi values for the minimums). In a 412 px slot the
factor is 2.62 (31 and 42 px). Measure the real slot on the target platform; it changes.

## Task 4: honest encoding (INFO-CHART-002/003/005)

**Lie factor** (Tufte) compares the size of an effect in the graphic with the size in the data:

```text
effect = |second - first| / first
lie factor = effect shown in the graphic / effect in the data;   accept 0.95 <= LF <= 1.05
```

Areas must scale with value, so a circle's radius scales with the square root. Scaling the radius
instead: a value that doubles is drawn with four times the area, so LF = (4 - 1) / (2 - 1) = 3. A bar
axis starting at 3,000,000 when values are 3,200,000 and 3,400,000 shows a 6% difference as 100%
of the visible bar change: LF about 16. Pictogram arrays and shares that must total 100% are
apportioned by largest remainder: floor every share, then give the spare units to the largest
fractional parts.

**Maps** (INFO-CHART-006): compare rates, not counts: rate = count / population x k, with k stated
(per 1,000, per 100,000). Web Mercator multiplies areas by 1 / cos^2(latitude): about 1.00 near the
equator (Uganda sits within about 4 degrees), 1.33 at 30 degrees and 4.00 at 60 degrees, so a map that
compares areas across a continent or a hemisphere uses an equal-area projection.

## Task 5: diagram structure as a graph (INFO-FLOW-001/002/003, INFO-CYCLE-001, INFO-TREE-001)

Keep the diagram as data: nodes (id, label, type: start, step, decision, end, exception) and directed
edges (from, to, label, kind: flow or feedback). Then check, each in O(V + E):

| Check | Algorithm | Failure means |
|---|---|---|
| Unique ids | Compare the id list with its set | Two steps share an identity |
| Duplicate stages | Normalise labels (case-fold, strip numbering and punctuation, collapse spaces); equal labels, or a similarity ratio of 0.9 or more, are flagged | The same step drawn twice |
| Orphans | In-degree plus out-degree equals zero | A floating box |
| Reachability | Breadth-first search from every start; reverse search from every end | A step nobody reaches, or a dead end |
| Decisions | Out-degree at least 2 and every exit labelled | An unlabelled branch |
| True order | Kahn's topological sort over flow edges (feedback edges set aside) | A hidden loop; numbering that disagrees with order |
| Numbering | Displayed step numbers equal positions in a topological order | "Step 4" happens before "step 3" |
| Strict hierarchy | One root, every other node exactly one parent, edges = nodes - 1, all reachable | A cycle or double parent in an org chart |
| Cycle diagram | Every ring node has one ring edge in and one out, and one walk visits all of them and returns | A "cycle" that is really a chain, or a skipped stage |

Connector crossings are counted pairwise with the orientation test for segment intersection
(O(E^2), trivial at infographic sizes); a procedure targets zero, and any crossing left is drawn with
a bridge. Layered (Sugiyama-style) layout with barycentre ordering is a good way to reach zero. The
long text equivalent (INFO-A11Y-001) is generated by walking the same validated graph in
topological order, so the picture and its description cannot disagree.

## Task 6: ring geometry for cycles (INFO-CYCLE-003)

Place n stages at angles theta_k = theta_0 + 360 k / n, clockwise from the entry point at the top.
Adjacent stage centres are a chord 2 r sin(pi / n) apart, so stages of width w with gap g need:

```text
r >= (w + g) / (2 sin(pi / n))
```

With w = 40 mm and g = 8 mm: n = 4 needs r of at least 33.9 mm, n = 5 needs 40.8 mm, n = 6 needs
48.0 mm and n = 8 needs 62.7 mm. Labels go outside the ring at r + offset.

## Task 7: truthful timelines (INFO-TIME-002)

Map time linearly: x(t) = x_0 + W (t - t_0) / (t_1 - t_0), with days counted from ISO dates. For each
segment, the spacing error is |(dx_i / dt_i) / (W / T) - 1|. Accept at most 2% (Chwezi value) when
the graphic claims a time scale; otherwise label it "sequence, not to scale". Equal-width boxes for
unequal durations fail.

## Task 8: colour that survives every reader and press (INFO-COLOUR-001/003/004)

- **Contrast:** relative luminance from linearised sRGB, ratio (L1 + 0.05) / (L2 + 0.05); targets
  4.5 and 3.0.
- **Colour-vision deficiency:** simulate protan, deutan and tritan vision with the
  Machado-Oliveira-Fernandes (2009) model (register IF6), then require CIEDE2000 of at least 10
  between every pair of categories in each simulation (Chwezi value).
- **Greyscale:** convert to CIELAB and require an L* difference of at least 20 between adjacent
  categories (Chwezi value), so photocopies keep the meaning.
- **Ink:** total area coverage = C + M + Y + K in percent, within the printer's limit (300% is a common
  ceiling, lower on uncoated stock; confirm the profile, register IF7). A rich black such as 60/40/40/100
  is 240%; small text stays 100% K to avoid misregistration.

## Task 9: space for translation (INFO-L10N-001)

Shorter English strings grow most in translation. Reserve width by source length (W3C, register
IF5): up to 10 characters 200-300%, 11-20 characters 180-200%, 21-30 160-180%, 31-50 140-160%, 51-70
151-170%, over 70 about 130%. Test with pseudo-localised strings of that length, and with Arabic for
right-to-left mirroring.

## Task 10: spacing and type scale (INFO-LAYOUT-002)

Spacing is the 8-point series 8, 16, 24, 32, 40, 48, 56, 64 (4 and 12 as justified exceptions). Type
roles come from task 1 per distance, then rounded to a modular scale (ratio 1.25 for print, 1.333 for
posters) so steps stay visibly distinct.

## Task 11: the release score (INFO-QA-004)

```text
score = 25 a + 20 c + 15 t + 15 h + 10 x + 10 o + 5 b,   each dimension rated 0-1
release when score >= 85, every gate closed, no critical and no open major finding
```

Example: accuracy 1.0, clarity 0.9, typography 0.8, hierarchy 0.9, accessibility 0.8, technical
0.9, brand 1.0 gives 25 + 18 + 12 + 13.5 + 8 + 9 + 5 = 90.5: releasable if no gate is open.

## Task 12: visual regression (INFO-QA-002)

Render each target at its approved size and compare with the baseline by structural similarity
(SSIM); flag any region below 0.98 (Chwezi value) and investigate it. A difference is accepted only
when a reviewer records why the new rendering is correct.
