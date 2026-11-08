# Chwezi Business-App House Style for Web (CSS + Tailwind)

Parent skill: [`tailwind-css`](../SKILL.md). Android twin:
`skills/android/android-development/references/house-style-compose.md` in this engine.

The canonical standard is owned by the design engine:

- `chwezi-design-engine` -> `skills/09-design-systems-tokens-and-theming/chwezi-business-app-house-style/SKILL.md`
- `chwezi-design-engine` -> `skills/12-data-viz-and-dashboards/money-figures-and-statement-display/SKILL.md`
- Audit record: `chwezi-design-engine` -> `docs/kaizen/2026-11-app-house-style/README.md`
  (kept K1-K19, rejected R1-R11, probation P1-P2).

This file covers how to build that standard in a web app with CSS custom properties and Tailwind.
When it and the design skill disagree, the design skill wins. The reference values come from the
Maduuka app (November 2026); other apps swap the brand primary and its containers and keep every
role, rule and guard.

## 1. Put every colour in one tokens file

All colour values live in `tokens.css`. Templates and components use role names only
(guard W1). Light is the default; dark follows the system unless the person chose a theme, held
in `data-theme` on `<html>`.

```css
/* tokens.css - the only file allowed to hold raw colour values */
:root {
  --primary: #1A6DB3;           --on-primary: #FFFFFF;          /* 5.41:1 */
  --primary-container: #D6E8FA; --on-primary-container: #0B3566;/* 9.78:1 */
  --ground: #E8F1FC;            /* page background, pale brand tint (K1) */
  --surface: #F9FCFF;           --card: #FFFFFF;
  --ink: #1D273B;               --muted: #565E6C;               /* 14.9:1 / 6.54:1 on card */
  --hairline: #C3D0E1;          /* decorative 1px border, 1.56:1, never the only cue */
  --danger: #B42323;            --money-up: #2E7D32;            /* 6.55:1 / 5.13:1 on card */
  --accent: #F8B020;            --on-accent: #1B2430;           /* 8.36:1, ONE per view (K2) */
  --warm-container: #FFE9B8;    --on-warm-container: #3D2A00;   /* 11.51:1 */
  --space-1: 2px; --space-2: 4px; --space-3: 8px; --space-4: 12px;
  --space-5: 16px; --space-6: 24px; --space-7: 32px; --space-8: 48px;
  --radius-s: 8px; --radius-m: 12px; --radius-l: 16px; --radius-card: 20px; --radius-xl: 28px;
  --target: 48px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --ground: #161C24; --surface: #1E2631; --card: #1E2631;
    --primary: #8DBBF2; --on-primary: #0B3566; --ink: #E6EDF5; --muted: #A9B3C1; }
}
:root[data-theme="dark"] { --ground: #161C24; --surface: #1E2631; --card: #1E2631;
  --primary: #8DBBF2; --on-primary: #0B3566; --ink: #E6EDF5; --muted: #A9B3C1; }
```

Dark ground, surface and primary are the reference values. The dark ink, muted and on-primary
values above were computed for this file (12.93:1, 7.19:1 and 6.13:1 on `#1E2631`/`#8DBBF2`);
the rest of the dark set (containers, hairline, danger, money-up) must be chosen and measured per
app and is `NOT_ASSESSED` here. Keep the dark block in one place (a shared partial or a
preprocessor mixin) so the two dark selectors cannot drift.

Rule R7: on `--primary-container`, text is `--on-primary-container`; never `--primary` (4.32:1)
or `--money-up` (4.10:1).

## 2. Map the tokens into Tailwind

Tailwind v4 (CSS-first). `@theme inline` makes each utility read the switching variable, so
`bg-card` follows the theme without a `dark:` variant:

```css
@import "tailwindcss";
@import "./tokens.css";
@theme inline {
  --color-primary: var(--primary);       --color-on-primary: var(--on-primary);
  --color-primary-container: var(--primary-container);
  --color-on-primary-container: var(--on-primary-container);
  --color-ground: var(--ground); --color-surface: var(--surface); --color-card: var(--card);
  --color-ink: var(--ink); --color-muted: var(--muted); --color-hairline: var(--hairline);
  --color-danger: var(--danger); --color-money-up: var(--money-up);
  --color-accent: var(--accent); --color-on-accent: var(--on-accent);
  --color-warm: var(--warm-container); --color-on-warm: var(--on-warm-container);
  --radius-card: var(--radius-card); --radius-btn: var(--radius-l);
  --font-body: "Atkinson Hyperlegible", system-ui, sans-serif;
  --font-figure: "Public Sans", system-ui, sans-serif;
}
```

Tailwind v3 (`tailwind.config.js`, the version the parent skill's setup section shows): set
`theme.colors` (replace, do not `extend`, so the default palette is unavailable) to
`{ primary: 'var(--primary)', card: 'var(--card)', ... }` and `borderRadius.card` to
`'var(--radius-card)'`. Replacing the palette is itself a guard: `bg-red-500` stops compiling.

Spacing: restrict to the scale. In v4 reset `--spacing-*` to the eight steps; in v3 replace
`theme.spacing`. Arbitrary values such as `p-[13px]` are banned by guard W3.

## 3. Type and amount utilities

- Body and labels: Atkinson Hyperlegible; headings and money: Public Sans. Self-host the WOFF2
  subsets with `font-display: swap` and keep the OFL licence files. The design engine's banned
  primary faces (Inter, Roboto and the rest) stay banned; `system-ui` is a fallback only.
- Floor: 12px (0.75rem) for every text role. No arbitrary `text-[11px]` (guard W7).

```css
@layer components {
  .amount { font-family: var(--font-figure); font-variant-numeric: tabular-nums; }
  .amount-lg { @apply amount text-[2rem] font-semibold; }
  .amount-md { @apply amount text-[1.375rem] font-semibold; }
  .amount-sm { @apply amount text-base font-medium; }
  .amount-compact { @apply amount text-xs font-medium; } /* 12px, fits "888.88B" in a column */
}
```

(The rem sizes above live in the tokens/components layer, the one place literal sizes are
allowed.) Amounts inside sentences also get `.amount` (R6).

## 4. Format money once

One module, `money.js`, exports `compact(value)` and `full(value, currency)`; templates never format money
(guard W6).

- `compact`: below 1,000 the whole number; otherwise K, M or B with exactly two decimals. Round,
  then promote: `999995` gives `1.00M`, never `1000.00K`. No currency symbol.
- `full`: grouped, with the currency's ISO 4217 minor unit as its decimals (UGX and RWF 0; KES,
  TZS and USD 2), for documents, closing balances and inputs. This supersedes the earlier fixed
  two decimals (Chwezi Product Excellence Standard PX-L10N-001, owner default 2026-11-07); see
  [`product-excellence-engineering-gates.md`](../../frontend-architecture/references/product-excellence-engineering-gates.md).
- Use decimal strings or integer minor units from the API; do not do money arithmetic in floats.
- Screen readers always get the full amount:

```html
<span class="amount-compact" aria-hidden="true">79.43M</span>
<span class="sr-only">79,430,000</span> <!-- UGX: 0 minor-unit digits -->
```

Percentages (R2): never "0%" for a non-zero value; write "less than 1%".

## 5. Components as HTML/Tailwind patterns

### Hub menu card (K3)

```html
<a href="/reports/monthly" class="flex min-h-[88px] items-center gap-4 rounded-card border
   border-hairline bg-card p-4 text-ink shadow-none focus-visible:outline-2
   focus-visible:outline-primary">
  <img src="/icons/monthly.svg" alt="" width="44" height="44"> <!-- drawn as is: no filter, no disc (R10) -->
  <span class="min-w-0 flex-1">
    <span class="block font-semibold">Monthly reports</span>
    <span class="line-clamp-3 text-sm text-muted">See each closed month at a glance.</span>
  </span>
  <svg aria-hidden="true" class="size-5 rtl:-scale-x-100">...</svg>
</a>
```

The whole card is the link; nothing inside it is a second link. Every illustrated icon has a
recorded source and licence (R11).

### KPI tile with change chip (K4)

Label, a compact figure, and a chip with arrow, word and colour together:
`<span class="... text-money-up"><svg aria-hidden="true">...</svg> Up 12%</span>`. Colour is never
the only cue; the word carries the meaning.

### Hero card with softened decimals (K5, K6)

```html
<section class="rounded-card bg-gradient-to-b from-primary-container to-card p-6">
  <p class="text-sm text-on-primary-container">1 Oct - 31 Oct 2026</p> <!-- range only (R1) -->
  <p class="text-sm text-on-primary-container">Came in</p>
  <p class="amount-lg text-ink" aria-hidden="true">4,812<span class="text-[0.6em] text-muted">.50K</span></p>
  <p class="sr-only">Came in 4,812,500</p>
</section>
```

Follow it with "Came in", "Went out", "Profit" tiles and a bar captioned "You kept N% of what came
in". The period name appears once per page (top bar or navigator), never again in the hero.

### Top three (K8) and highlight tile (K7)

An ordered list; each item has a round rank badge (`bg-warm text-on-warm` for first, neutral for
second and third), the name with `truncate` on the left, `.amount-compact` on the right. One warm
highlight tile per page for the single best item.

### Period navigator (K9)

`<nav aria-label="Period">` holding a previous button ("Previous month, October 2026"), a pill
button with a calendar glyph, the period name and a dropdown arrow that opens the picker, and a
next button that is `disabled` at the latest period. Buttons are at least `size-12` (48px).

### Accent button (K2, K13)

```css
@layer components {
  .btn-accent { @apply inline-flex min-h-12 items-center justify-center rounded-btn
    bg-accent px-6 font-semibold text-on-accent; }
}
```

One `.btn-accent` per page view. Other main actions: filled `bg-primary text-on-primary`.
Destructive exits: outlined `border-danger text-danger`. Never an accent for a destructive action.

### Statement row (K10, K11)

Date and type on the left; on the right a `<dl>` with "Due", "Paid", "Balance" stacked, each
labelled, in `.amount-compact`. Closing balance in `full()`. Ten rows a page. On a phone the trial
balance is collapsible group cards (`<details>` with group totals in the `<summary>`) and a pinned
closing footer, not a wide table.

### Context strip and insight (K14, K18)

Date chip, a Switch action and the place name centred; one insight sentence with an action link.
No run ids, raw statuses or doubled labels on screen (R3).

## 6. Motion with prefers-reduced-motion (K15)

```css
@media (prefers-reduced-motion: no-preference) {
  :root:not([data-motion="reduced"]) .reveal {
    animation: rise 420ms ease-out both;
    animation-delay: calc(min(var(--i, 0), 7) * 70ms); /* 70 ms stagger, max 8 */
  }
}
@keyframes rise { from { opacity: 0; transform: translateY(24px); } }
```

- Set `style="--i: 0"` to `7` on the first eight cards; later cards share the eighth delay.
- Count-up (900 ms, once) and chart grow (700 ms after 250 ms) run in JS only when
  `matchMedia('(prefers-reduced-motion: reduce)').matches` is false and the app's own
  `data-motion` is not `reduced`. Otherwise render the final value at once.
- Play once per visit: mark the page in `sessionStorage` (wrapped in try/catch) so back
  navigation does not replay. The `sr-only` full amount is final from the first paint.
- No `animation-iteration-count: infinite` outside the `no-preference` block (guard W8).

## 7. Guardrails as CI checks (K19)

Run these in CI on every push. Ratchet baselines live in one file (`design-baselines.json`) and may
only go down; a change that removes violations lowers the number in the same commit.

| # | Check | How | Baseline |
|---|---|---|---|
| W1 | Raw colour | Stylelint `color-no-hex` and `color-named: "never"` everywhere except `tokens.css` (`overrides`); grep templates for `#[0-9a-fA-F]{3,8}\b` in `style=` and for default palette classes (`(bg|text|border)-(red|blue|green|gray|slate)-\d`) | 0 |
| W2 | One accent | Render each route (Playwright) and assert `document.querySelectorAll('.btn-accent:not([hidden])').length <= 1` | hard rule |
| W3 | Off-grid spacing | grep for arbitrary spacing `\b-?(m|p|gap|space-[xy])[trblxy]?-\[` | ratchet |
| W4 | Shape literals | grep for `rounded-\[` and `border-radius:` outside tokens | ratchet |
| W5 | Raw identifiers | grep templates for `{{ *\w+\.(id|run_id|status) *}}` printed as text | ratchet |
| W6 | Formatter | no `toFixed(` on money, no currency symbols in templates, `compact(` banned in table and statement templates except an allow-list | 0 plus allow-list |
| W7 | Typography | no `text-\[\d+px\]`, no `font-size:` outside the type layer | 0 |
| W8 | Reduced motion | `infinite` only inside a `prefers-reduced-motion: no-preference` block | 0 |
| W9 | Contrast | script recomputes WCAG ratios from `tokens.css` for every declared pair, light and dark | all pass |

A minimal ratchet runner:

```sh
#!/usr/bin/env sh
# check-ratchet.sh NAME PATTERN PATHS... ; fails when the count rises above the baseline
name=$1; pat=$2; shift 2
count=$(grep -rEo "$pat" "$@" | wc -l)
base=$(node -e "console.log(require('./design-baselines.json')['$name'])")
[ "$count" -le "$base" ] || { echo "$name: $count > $base"; exit 1; }
```

W9 computes, it does not copy: parse the custom properties, apply the WCAG relative-luminance
formula, and require 4.5:1 for text pairs and 3:1 for large text and non-text indicators (focus
ring, selected state, chart marks). Grep-based checks are heuristics: name each reasoned exception
in an allow-list with a comment.

Also run an automated accessibility scan (for example axe in Playwright) on the hub, report and
statement routes at 200% zoom, in both themes. Results not run are `NOT_ASSESSED`.

## 8. Anti-patterns

- `--primary` or `--money-up` text on `--primary-container` (R7).
- Two `.btn-accent` in one view, or an accent on a destructive action.
- CSS `filter`, tint or a coloured disc behind an illustrated icon (R10).
- The period name in the bar, navigator and hero (R1); two date formats (R4: "6 Nov 2026",
  short "Fri 6 Nov").
- `1000.00K`, "0%" beside a non-zero figure, a currency symbol, or only the compact amount exposed
  to assistive technology.
- Alternating grey row bands that look like selection (R5); a generic placeholder image instead of
  initials on a category tint (R9); more than eight illustration hues (R8).

## Evidence/currentness

Access date 2026-11-07.

- WCAG 2.2 (W3C Recommendation, 12 Dec 2024), https://www.w3.org/TR/WCAG22/ : SC 1.4.3 contrast
  4.5:1 for text, 3:1 for large text (18 pt, or 14 pt bold); SC 1.4.11 non-text contrast 3:1;
  SC 2.5.8 target size minimum 24 by 24 CSS px (AA); SC 2.5.5 44 by 44 (AAA); SC 2.3.3 animation
  from interactions (AAA). The 48px target is a house rule above these minimums.
- `prefers-reduced-motion` (`no-preference`, `reduce`), Baseline widely available since January
  2020: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Tailwind CSS theme variables, `@theme` and `@theme inline` (docs header showed v4.3):
  https://tailwindcss.com/docs/theme . Combining `@theme inline` with `data-theme` switching is
  this file's construction, not an example on that page; verify in the project's Tailwind version.
- Stylelint rule names `color-no-hex` and `color-named`: `NOT_ASSESSED` against the current
  Stylelint release on 2026-11-07; confirm before wiring CI.
- Contrast ratios were recomputed from the hex values on 2026-11-07 with the WCAG formula.

Sources: Maduuka app theme and guardrail tests (Nov 2026), read by role only; the design engine's
house-style audit record of 7 Nov 2026.
