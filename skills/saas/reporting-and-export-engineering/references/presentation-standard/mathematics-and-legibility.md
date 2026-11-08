Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Presentation and Slide Deck Design Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Mathematics and legibility

Use this reference to compute what a deck needs instead of guessing: the smallest legible text for a
room, the type scale, the grid, image resolution, white space, the talk budget, contrast, axes and
rounding. Rule IDs: [rules-and-gates.md](rules-and-gates.md). Figures were computed on 2026-11-08;
external parameters are recorded in [currentness-register.md](currentness-register.md).

## Task 1: compute the minimum legible size for the venue (DECK-LEGIB-001)

Text is legible when its characters subtend enough visual angle at the farthest seat. With a target
character height of theta arc-minutes, viewing distance D, screen image height H, a slide 540 pt tall
(7.5 in) and a cap height c (as a fraction of the font size):

```text
cap height on screen  h = D x tan(theta)
minimum font size     s = (h / H) x 540 / c   points
with theta = 20', c = 0.70:   s ~= 4.5 x (D / H)   points
```

| Farthest viewer D | Screen image height 1.0 m | 1.5 m | 2.0 m |
|---|---|---|---|
| 4 m | 18.0 pt | 12.0 pt | 9.0 pt |
| 6 m | 26.9 pt | 18.0 pt | 13.5 pt |
| 8 m | 35.9 pt | 23.9 pt | 18.0 pt |
| 10 m | 44.9 pt | 29.9 pt | 22.4 pt |
| 12 m | 53.9 pt | 35.9 pt | 26.9 pt |

Reading the table: the handbook's 18 pt body is right exactly when the farthest viewer sits within
four screen heights (D/H <= 4). At six screen heights the minimum is 27 pt, so either enlarge the
type, cut words, or move the content to a handout. A 1366x768 laptop (about 0.19 m tall) read at
0.6 m needs about 14 pt, which the 16 pt floor covers. Recompute c for the chosen typeface from its
metrics; theta = 20' is a Chwezi parameter informed by ergonomic guidance (register PR3).

## Task 2: size the screen for analytical content (DECK-LEGIB-003)

For dense, analytical slides, size the image so one pixel subtends no more than about one arc-minute
at the farthest seat. One radian is 3438 arc-minutes, so:

```text
image height >= farthest viewer distance x vertical pixels / 3438
```

| Farthest viewer | 1080 lines | 720 lines |
|---|---|---|
| 6 m | 1.88 m | 1.26 m |
| 8 m | 2.51 m | 1.68 m |
| 10 m | 3.14 m | 2.09 m |

This is the analytical-decision form of the display image size method (register PR4). When the room
cannot meet it, simplify the slide.

## Task 3: derive the type scale (DECK-MATH-001)

`size(n) = body x 1.25^n` with body 20 pt:

| n | Size | Role | Handbook range |
|---|---|---|---|
| -3 | 10.2 pt | Sources, footnotes | 10-12 pt |
| -1 | 16.0 pt | Labels, floor for presented text | 14-18 pt |
| 0 | 20.0 pt | Body | 18-24 pt |
| 2 | 31.3 pt | Slide title | 28-36 pt |
| 3 | 39.1 pt | Section divider, cover headline | 34-48 pt |

Every step lands inside the handbook ladder. Body never drops below the venue minimum from Task 1.

## Task 4: lay out the grid

On 13.333 x 7.5 in with side margins m and 12 columns with gutter g:

```text
column width = (13.333 - 2m - 11g) / 12
```

At m = 0.5 in and g = 0.2 in: (13.333 - 1.0 - 2.2) / 12 = 0.844 in per column. A 5:7 split gives
5 x 0.844 + 4 x 0.2 = 5.02 in and 7 x 0.844 + 6 x 0.2 = 7.11 in, separated by one gutter.

## Task 5: check image resolution (DECK-ASSET-004)

A 1920-pixel-wide output spreads over 13.333 in, so a slide inch shows 1920 / 13.333 = 144 pixels
(288 at 4K). An image displayed 6 in wide needs at least 6 x 144 = 864 pixels for crisp 1080p; keep a
higher-resolution master for print export, and compress the deck copy.

## Task 6: measure white space (DECK-TOKEN-005)

Render the slide at 1920x1080. Count the pixels whose colour lies within a small colour difference of
the background (for example CIEDE2000 below 2); white space = background pixels / all pixels. Most
slides land at 20-35%. Below 20% the slide is crowded; far above 35% on a content slide, the message
may be too thin. A measured ratio replaces "feels busy".

## Task 7: budget the talk (DECK-MOTION-002)

Substantive slides take about 30-90 seconds each, so slides = runtime / (30 to 90 s):

| Runtime | Substantive slides (30-90 s) | At 60 s each |
|---|---|---|
| 10 min | 6-20 | 10 |
| 15 min | 10-30 | 15 |
| 20 min | 13-40 | 20 |
| 30 min | 20-60 | 30 |

A plan above the upper bound is a lecture in disguise; time the rehearsal and cut.

## Task 8: compute colour and figures

- Contrast: linearise each sRGB channel (c / 12.92 if c <= 0.04045, else ((c + 0.055) / 1.055)^2.4),
  L = 0.2126 R + 0.7152 G + 0.0722 B, ratio = (L_light + 0.05) / (L_dark + 0.05); text at least 4.5:1,
  large text 3:1 (DECK-TOKEN-004).
- Sequential colour ramps are interpolated in a perceptually uniform space (OKLab or OKLCH) with
  monotonic lightness; categorical colours are checked for colour difference, colour-vision deficiency
  and greyscale.
- Axis ticks use nice numbers, steps of 1, 2 or 5 x 10^k; line charts are banked to about 45 degrees
  (DECK-MATH-003).
- Money is computed exactly in minor units; shares that must total 100% use largest-remainder
  rounding: three equal shares show 34%, 33%, 33%, never 99% (DECK-MATH-002).

## Evidence/currentness

Methods: visual-angle legibility (ergonomic guidance, register PR3), display image size for analytical
content (register PR4), WCAG 2.2 contrast (PR1), OKLab (Ottosson 2020), nice numbers (Heckbert 1990),
banking to 45 degrees (Cleveland 1993), largest-remainder apportionment. theta = 20', c = 0.70, the
white-space thresholds and the timing ranges are Chwezi values; all tables were computed on
2026-11-08.
