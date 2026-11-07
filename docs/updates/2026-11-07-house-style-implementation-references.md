# House style implementation references (7 Nov 2026)

Peter Bamuhigire asked on 7 November 2026 for the Maduuka Android interface style to become the
house style for his apps. The audit and the canonical standard live in `chwezi-design-engine`
(`docs/kaizen/2026-11-app-house-style/README.md`, and the skills
`chwezi-business-app-house-style` and `money-figures-and-statement-display`). This engine adds
the implementation side only; no new skill was created.

## Changed

- New `skills/android/android-development/references/house-style-compose.md`: Material 3 colour
  roles (light, dark), bundled fonts with `tnum` amount styles, spacing and shape objects, a
  compact/full money formatter, the house components, a reduced-motion gate, and guardrail
  tests G1-G9 as source-scanning JUnit tests with ratchet constants.
- New `skills/frontend-ux/tailwind-css/references/house-style-web.md`: the same roles as CSS
  custom properties, Tailwind v4 `@theme inline` and v3 config mapping, tabular amount utilities,
  HTML/Tailwind component patterns, `prefers-reduced-motion`, and CI checks W1-W9.
- Pointers: a row in the `android-development` reference table, a superseding note at the top of
  `ui-design-system.md`, and a line in the `tailwind-css` reference list.

## Evidence

WCAG 2.2, MDN `prefers-reduced-motion`, Tailwind theme docs and the Android `Settings.Global` and
`ValueAnimator` references were read on 2026-11-07; contrast ratios were recomputed from the hex
values. Material 3 target-size text, Stylelint rule names, the full dark role set and device
behaviour in a new app are `NOT_ASSESSED`.
