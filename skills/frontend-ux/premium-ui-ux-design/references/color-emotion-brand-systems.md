# Color, Emotion, And Brand Systems

Color is a business and usability tool. It helps people notice, group, compare, remember, trust, and act.

## Color Jobs

- Identify: brand, product family, section, account, plan, or workflow.
- Prioritize: primary action, active route, urgent exception, selected item.
- Structure: group related content, separate sections, code categories.
- Signal state: success, warning, danger, info, disabled, pending.
- Create emotion: calm, energy, authority, warmth, luxury, urgency.
- Support comprehension: charts, maps, dashboards, and infographics.

Do not add a color unless its job is clear.

## Palette Construction

1. Define brand primitives: core hue(s), neutral scale, and supporting accents.
2. Define semantic tokens: `action`, `success`, `warning`, `danger`, `info`, `surface`, `text`, `border`, `focus`.
3. Define component tokens only after semantic tokens are stable.
4. Test all tokens in light mode, dark mode, disabled states, error states, and data-dense screens.
5. Reserve the strongest accent for the highest-value action or alert.

## Dominant, Subordinate, Accent

- Dominant color creates the general feel.
- Subordinate colors support structure and variation.
- Accent colors attract attention and should be rare.

If every card, button, chart, and heading uses the accent, nothing is accented.

## Contrast And Value

- Value contrast is often more important than hue contrast for readability.
- Test foreground/background contrast before approving the palette.
- Do not put important text over busy imagery unless there is a reliable overlay or reserved quiet area.
- Use color plus label, icon, pattern, or position for status. Never rely on color alone.

## Emotion And Culture

- Color meaning changes by market, culture, sector, and context. Validate assumptions for the intended audience.
- Financial, healthcare, legal, and government interfaces need restraint and trust before excitement.
- Retail, hospitality, entertainment, and consumer brands can carry more expressive color if readability and hierarchy survive.
- A color that wins attention can still be wrong if it creates the wrong expectation.

## Data And Dashboard Color

- Use muted neutrals for most dashboard structure so exceptions stand out.
- Use sequential palettes for low-to-high quantities, diverging palettes for above/below baseline, and categorical palettes for distinct groups.
- Avoid rainbow palettes for ordered data.
- Directly label important series where possible.
- Test charts for color vision deficiency and grayscale comprehension.

## Screen And Production Reality

- Screens vary. Validate color on common laptop, external monitor, Android, and iPhone displays when possible.
- RGB/screen color can look different from print and brand files. Document conversions and acceptable ranges.
- Compressing images, changing backgrounds, and dark mode can change perceived color. Test in context, not only in swatches.

## Approval Checklist

- Palette fits the product promise and target buyer.
- Primary action is obvious without overusing accent color.
- Semantic colors are consistent across components.
- Text contrast meets WCAG AA or better.
- Data colors match the relationship being shown.
- Dark mode is designed, not inverted blindly.
- A non-designer stakeholder can explain what each major color means.
