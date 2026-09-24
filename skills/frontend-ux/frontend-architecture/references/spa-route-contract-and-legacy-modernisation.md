# SPA Route Contract and Legacy Front-End Modernisation

Parent skill: [`../SKILL.md`](../SKILL.md) (`frontend-architecture`).

**Load when:** designing or reviewing client-side routing in a single-page or hybrid app, or
planning the migration of an inherited front end (jQuery-era, float grids, hash routing,
create-react-app, Bootstrap 3/4 remnants) to current practice.

Visual and layout decisions belong to the design engine
(`design-system-skills/skills/03-layout-grid-and-composition/responsive-and-adaptive-layout`,
including `references/modern-css-capability-baseline.md`). This file owns the implementation side.

---

## 1. The route-change contract

Every client-side navigation must satisfy all of the following; each is a test case.

| Concern | Requirement | Failure when skipped |
|---|---|---|
| URL | Each view has a real, shareable, server-resolvable URL (History or Navigation API); the server returns the app shell or a rendered page for deep links and refresh | Refresh gives a 404; links cannot be shared; search engines see one page |
| Back and forward | Browser history reproduces the previous view and its filters | Users trapped or thrown to the home view |
| Scroll | Restore scroll position on back; scroll to top (or to the target fragment) on new navigation | Users land mid-page on a new view |
| Document title | Updated per view, specific first ("Invoice 1042 - Billing - Acme") | Tabs and history entries indistinguishable |
| Focus | Move focus to the new view's main heading or `main` region after render | Keyboard and screen-reader users stay on the old link with no cue |
| Announcement | Announce the new view through a polite live region when focus movement alone is insufficient | Screen-reader users do not know the view changed |
| Data states | Loading, empty, error and success states for every fetch; loading indicators use `aria-busy` and never trap focus | Blank screens and silent failures |
| Cleanup | Remove listeners, cancel in-flight requests (`AbortController`), clear timers when leaving a view | Memory leaks and stale data painted into the wrong view |
| Security | Never inject fetched HTML or API strings with `innerHTML`, never execute fetched script text; use templating that escapes by default, sanitisation for any trusted rich text, and a Content Security Policy; no secrets in client code | Cross-site scripting; leaked API keys |
| Performance | Split code by route, prefetch likely next routes, use server rendering or static generation where first paint or search visibility matters | Large initial bundle; poor INP and LCP |

Use the framework router's built-in handling for scroll, focus and title where it exists, and
verify it; do not assume it is on by default.

## 2. Migration table for inherited front ends

| Inherited item | Current replacement (verify versions at migration time) |
|---|---|
| create-react-app (deprecated by the React team on 2025-02-14) | A framework (Next.js, React Router framework mode, Expo) or a build tool (Vite, Parcel, Rsbuild) per react.dev guidance |
| Hand-configured Webpack and Babel for a new project | Framework defaults or Vite |
| Class components and lifecycle methods | Function components and hooks; migrate incrementally, class components still run |
| Hash-fragment routing (`#/page`) | History or Navigation API routing with server fallback; the Navigation API reached Baseline Newly available in January 2026 |
| `XMLHttpRequest` with ready-state polling | `fetch` with `async`/`await` and `AbortController` |
| Separate mouse and touch handlers, `keyCode` | Pointer Events, `event.key` |
| `setInterval` smooth scrolling and scroll-listener parallax | CSS `scroll-behavior`, `IntersectionObserver`, CSS scroll-driven animations as enhancement, `prefers-reduced-motion` |
| Float grids and percentage maths from a fixed mock-up | CSS Grid, Flexbox, `gap`, container queries |
| Bootstrap classes removed in v5 (`.jumbotron`, `.form-group`) or Bootstrap's own JavaScript inside React | Current Bootstrap utilities or the project's token system; framework-native components rather than Bootstrap JS in a React tree |
| Icon fonts loaded from a CDN | Inline SVG or a sprite with accessible names |
| Vendor prefixes written by hand | Unprefixed properties; build-time prefixing from a browserslist policy only if the support policy requires it |
| `window.onload =` assignments | `addEventListener`, `defer` or module scripts |
| Client-side keys for third-party APIs | Server-side proxy |

## 3. Migration procedure

1. Inventory routes, entry points, global scripts and third-party includes; mark each with the
   replacement from section 2.
2. Write route-contract tests (section 1) against the *current* app first, so the migration has a
   baseline and does not regress behaviour.
3. Migrate one representative route end to end (routing, data states, focus, title), measure,
   then standardise the pattern.
4. Remove superseded libraries only after no route depends on them; record each removal.
5. Record residual risks and anything unverified as `NOT_ASSESSED`.

## Evidence and currentness

Accessed 2026-09-24: react.dev blog "Sunsetting Create React App" (2025-02-14); web-features
explorer, Navigation API (Baseline Newly available since 2026-01-13); web.dev "New to the web
platform in January" (2026). Framework and library versions are deliberately not pinned here;
check the official release pages at migration time.

Sources: LaGrone, B. (2016) *Web Design Blueprints*, Packt (route-table idea; its hash routing,
`innerHTML` partials and client-side keys are listed above as items to replace); Yang, C. D.
(c. 2024) *Building User Interfaces for Modern Web Applications: React Programming*, PA-ADOPT open
textbook (component decomposition; its tooling is superseded); W3C WAI-ARIA Authoring Practices;
react.dev.
