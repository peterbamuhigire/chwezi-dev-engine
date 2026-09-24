# Accessibility Testing: Automated and Manual

Load when a web or mobile release needs accessibility evidence: axe-core scans in Playwright,
keyboard and screen-reader passes, reflow and zoom checks, and an honest statement of what was
not verified. Target conformance is WCAG 2.2 Level AA unless the contract states otherwise.

Boundary: this reference covers how engineering *verifies* accessibility. Design intent (focus
styling, contrast choices, target sizes, motion policy, content order) is owned by the design
engine; read `C:\wamp64\www\design-system-skills\governance\design-quality-gate.md` and its
`accessibility-wcag-2-2-compliance` skill for what the experience must do. Requirements stating
the measurable target belong in the SRS.

## Inputs

| Input | Required | Why |
|---|---|---|
| Conformance target (WCAG 2.2 AA, EN 301 549, Section 508) | yes | Sets tags and pass criteria |
| Critical user journeys (sign-in, pay, submit, recover) | yes | Manual passes are journey-based, not page-based |
| Supported platforms and assistive technologies | yes | Decides which screen readers to smoke |
| Known third-party widgets | if any | Scoped exclusions need an owner and a ticket |

## Layer 1: automated scans (necessary, never sufficient)

Automation reliably finds missing names, invalid ARIA, missing form labels, duplicate IDs,
many contrast failures and missing document language. It cannot judge whether a name is
*meaningful*, whether focus order matches the task, whether an announcement is timely, or
whether a flow is usable with a screen reader. Playwright's own documentation says many
problems "can only be discovered through manual testing".

```typescript
// tests/a11y.fixture.ts
import { test as base } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

export const test = base.extend<{ makeAxe: () => AxeBuilder }>({
  makeAxe: async ({ page }, use) => {
    await use(() =>
      new AxeBuilder({ page })
        // wcag22aa alone covers only rules new in 2.2; list every level you claim.
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
        .exclude('#vendor-chat'), // exclusion owned by ticket A11Y-142, expires 2026-12-31
    );
  },
});
```

```typescript
// tests/checkout.a11y.spec.ts
import { expect } from '@playwright/test';
import { test } from './a11y.fixture';

test('checkout payment step has no detectable WCAG A/AA violations', async ({ page, makeAxe }, testInfo) => {
  await page.goto('/checkout/payment');
  await page.getByRole('button', { name: 'Pay with Mobile Money' }).click(); // scan the opened state too
  const results = await makeAxe().analyze();
  await testInfo.attach('axe-results', { body: JSON.stringify(results, null, 2), contentType: 'application/json' });
  expect(results.violations).toEqual([]);
});
```

Rules:

- Scan each **state**, not just each URL: open menus, dialogs, validation errors, empty and
  loading states. A clean initial render proves little.
- Use `include()` to scope a component test; use `exclude()` only for code you do not own, with
  a ticket and expiry. `disableRules()` requires a written justification in the test.
- Add `expect(locator).toMatchAriaSnapshot()` for critical components so a refactor that changes
  roles, names or structure fails review even when axe stays green.
- Native mobile: run the platform checkers (Android Accessibility Scanner or Espresso
  accessibility checks; Xcode Accessibility Inspector audits) as the automated layer.
- Gate CI on zero violations for new code; track legacy violations as a burn-down list, never
  as a silent baseline.

## Layer 2: manual passes (the evidence automation cannot produce)

Run per critical journey, per release that touches it. Record device, browser, AT version.

1. **Keyboard only** (unplug the mouse): every action reachable; visible focus at every step;
   order follows the task; no trap; Escape closes dialogs and returns focus to the trigger;
   focused element never hidden under sticky headers or banners (WCAG 2.4.11).
2. **Screen-reader smoke**: VoiceOver on macOS with Safari and on iOS; NVDA with Firefox or
   Chrome on Windows; TalkBack with Chrome on Android. Check that headings and landmarks let a
   user skim, controls announce name, role and state, errors are announced when they appear,
   and the success confirmation is announced without moving the user unexpectedly.
3. **Reflow and zoom**: at a 320 CSS px wide viewport (equal to 1280 px at 400% zoom, WCAG
   1.4.10) content needs no two-dimensional scrolling and loses no function; at 200% text
   resize (1.4.4) nothing clips or overlaps; with the 1.4.12 text-spacing overrides applied,
   text remains readable.
4. **Pointer and touch**: targets at least 24 by 24 CSS px or adequately spaced (2.5.8); drag
   actions have a single-pointer alternative (2.5.7).
5. **Preferences**: reduced motion honoured; dark mode and forced colours (Windows High
   Contrast) keep focus indicators and control boundaries visible.

## Quality gate

- [ ] axe scans cover every critical journey state, tags include all claimed WCAG levels.
- [ ] Every exclusion or disabled rule has an owner, ticket and expiry.
- [ ] Keyboard and at least one screen reader per supported platform were exercised on the
      changed journeys, with AT and browser versions recorded.
- [ ] Reflow at 320 CSS px and 200% text resize checked.
- [ ] Release evidence lists what was not tested as `NOT_ASSESSED`, never as passed.

## Premium versus generic output

- Generic: "Ran Lighthouse, score 100, accessible." A score is not conformance and says
  nothing about screen-reader usability.
- Premium: a per-journey table of automated result, keyboard result, screen-reader result
  (with AT/browser versions), reflow result, open defects with WCAG criterion and severity, and
  an explicit list of untested combinations.

## Failure modes

- Treating a green axe run as a conformance claim.
- Testing only the landing page while the payment dialog, the part users cannot avoid, fails.
- Using `aria-label` to silence a scanner instead of fixing the visible label.
- Screen-reader testing only in one pairing (for example VoiceOver on macOS) and inferring
  Android behaviour.

## Evidence/currentness

Checked 2026-09-24: Playwright accessibility testing guide (playwright.dev/docs/accessibility-testing:
`AxeBuilder`, `include`, `exclude`, `withTags`, `disableRules`, `testInfo.attach`, fixture
pattern); Playwright aria snapshots (playwright.dev/docs/aria-snapshots: `toMatchAriaSnapshot`);
axe-core API tag list (github.com/dequelabs/axe-core `doc/API.md`: `wcag2a` through `wcag22aa`);
W3C Understanding SC 1.4.10 Reflow (320 CSS px, 1280 px at 400%). Exact current package
versions of `@axe-core/playwright` and screen-reader releases: `NOT_ASSESSED`; record them at run
time. Native mobile checker capabilities: `NOT_ASSESSED` against current platform docs.
