# Production Quality And Handoff

Premium UI/UX survives implementation. This reference prevents beautiful mockups from degrading into inconsistent production screens.

## Production Polish

- Align edges, baselines, icons, labels, and chart axes.
- Keep spacing tokenized and consistent.
- Use stable component dimensions so hover, loading, and error states do not shift layout.
- Create real responsive rules; do not let cards simply wrap into awkward stacks.
- Test with realistic data: long names, empty values, high values, errors, permissions, and slow network.
- Use real copy for important workflows. Placeholder copy hides hierarchy and state problems.

## Assets

- Use SVG for logos, icons, and simple illustrations.
- Use WebP/AVIF with JPEG/PNG fallback where the stack requires it.
- Keep source images large enough for high-density screens, then serve responsive sizes.
- Do not upscale raster images beyond their useful resolution.
- Compress images without visible artifacts.
- Document crop rules for hero, card, avatar, gallery, and mobile variants.

## Typography Production

- Define font loading strategy and fallback metrics to reduce layout shift.
- Use semantic type tokens, not one-off sizes.
- Test bold, long labels, translated text, and numeric columns.
- Avoid font weights unavailable in the chosen family.

## Color Production

- Define RGB screen tokens and any print/export conversions separately.
- Verify dark mode tokens manually.
- Document chart palettes and semantic status colors separately from brand accents.
- Use focus colors that remain visible on every surface.

## Interaction Handoff

For every interactive component, specify:

- Default, hover, focus, pressed, selected, disabled, loading, error, and success states.
- Keyboard behavior and focus order.
- Screen reader labels or announcements.
- Motion duration, easing, and reduced-motion fallback.
- Empty, offline, timeout, and permission-denied behavior where relevant.

## Engineering Acceptance

- Tokens are consumed from the shared token source.
- Components use shared primitives before custom code.
- No hard-coded colors, spacing, radius, or shadow values outside the token definition layer.
- Screens pass responsive checks at small mobile, tablet, laptop, and large desktop widths.
- Accessibility checks cover keyboard, contrast, focus, labels, semantics, and reduced motion.
- Visual QA includes screenshots of major states, not only the happy path.

## Handoff Evidence

- Token table.
- Component inventory.
- State matrix.
- Responsive behavior notes.
- Asset manifest.
- Accessibility notes.
- Known tradeoffs and open questions.
- Premium UI/UX gate score.
