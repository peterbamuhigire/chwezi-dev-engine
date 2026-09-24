# Web Performance Engineering Procedure

Parent skill: `../SKILL.md`. Load when you must take a web product from "feels slow" (or "new, unmeasured") to an enforced budget: diagnose by metric sub-part, fix in impact order, accelerate navigations, govern third parties and AI surfaces, and wire the gate with a current toolchain. The budget, SLI, and gate templates stay in `budgets-and-regression-gate.md`; this file is the procedure that fills them.

## Inputs

| Input | Source | If missing |
|---|---|---|
| Field p75 for LCP, INP, CLS, split mobile/desktop, per template/route | RUM via `web-vitals`, or CrUX for public origins | Lab-only baseline; mark field status `NOT_ASSESSED` and schedule RUM before release |
| Critical-flow table | `system-architecture-design` | Stop; budgets without flows are guesses |
| Reference device and network | Analytics device mix | Default: low-to-mid Android on congested 4G |
| Third-party inventory (tag, owner, purpose, bytes, main-thread ms) | Tag manager export plus a trace | Build it in step 2 |
| AI surfaces (chat, streaming, generated UI) | Product spec | Skip step 6 |

## Procedure

1. **Baseline in the field first.** Record p75 per metric, per device class, per template. Lab numbers (Lighthouse, WebPageTest, DevTools) explain causes; they never prove the user outcome. A Lighthouse 95 with field INP of 380 ms is a failing product.
2. **Inventory what ships.** Per route: compressed JS/CSS/image/font bytes, request count, third-party origins, and main-thread time by script (trace or Long Animation Frames). Attribute every item to an owner. Unowned code is a removal candidate.
3. **Diagnose by sub-part, not by metric name.**
   - LCP = TTFB + resource load delay + resource load duration + element render delay. Aim for the two delays to be small (web.dev guidance: each under roughly 10% of LCP) so that time is spent fetching the document and the LCP resource. Large load delay means late discovery (image injected by JS, CSS background, lazy-loaded hero); large render delay means render-blocking CSS/JS or client-side rendering.
   - INP = input delay + processing duration + presentation delay. Input delay points at competing long tasks (hydration, third parties); processing at handler cost; presentation at DOM size, layout, and paint. Capture attribution with the `web-vitals` attribution build, which includes Long Animation Frame script data.
   - CLS: identify the shifting element and its cause (unsized media, late insertion above viewport, font swap, injected banners).
4. **Fix in impact order.** Rank candidates by (users affected x metric gap closed) / effort. Typical order: server/edge TTFB and caching; LCP discoverability and priority; remove or defer third parties; cut and split JS; break long tasks; reserve space. Stop optimising a flow when it meets budget with margin at p75; spend remaining effort on the next failing flow, not on micro-gains.
5. **Accelerate navigations.** Apply the navigation table below. These change what users feel on the second page more than any bundle tweak.
6. **Budget AI and streaming surfaces** (if present) using the streaming table below.
7. **Gate and re-measure.** Encode budgets in CI per `budgets-and-regression-gate.md`, ship, and compare field p75 after one full traffic cycle (at least 7 days, 28 for CrUX). A fix is done when field p75 moves, not when the PR merges.

## Decision rules

### Navigation acceleration

| Situation | Decision | Wrong choice |
|---|---|---|
| Multi-page site, predictable next page (listing to detail, step to step) | Speculation Rules document rules, `prerender` with `moderate` eagerness scoped by `href_matches` and excluding logout, cart mutation, and personalised side-effect URLs | `immediate` prerender of many URLs wastes data and server capacity; prerendering side-effect URLs performs actions the user did not take |
| Data-sensitive or low-data audience | `prefetch` with `conservative` eagerness only | Prerender on metered connections spends users' bundles; Chrome already suppresses speculation under Save-Data |
| Back/forward navigation is common (search, catalogue) | Make pages bfcache-eligible: no `unload` handlers (use `pagehide`), close IndexedDB/WebSocket/in-flight requests on `pagehide` and reopen on `pageshow`, reserve `Cache-Control: no-store` for truly sensitive pages | One `unload` listener (often from a third-party tag) silently disables instant back navigation |
| LCP image in HTML | `fetchpriority="high"` on the `<img>`, eager loading, explicit dimensions | `preload` alone discovers early but fetches at default priority |
| LCP image as CSS background | `preload` with `fetchpriority="high"`, or move it into HTML | Late discovery dominates LCP load delay |
| Origin still on HTTP/1.1 or HTTP/2 only | Enable HTTP/3 at the CDN/edge with HTTP/2 fallback; verify with the Network panel protocol column | Assuming the protocol fixes payload bloat; HTTP/3 reduces connection and loss penalties, not bytes |

Measure speculation and bfcache in RUM by segmenting on the `web-vitals` metric `navigationType` (it distinguishes `prerender` and `back-forward-cache` from ordinary navigations). Test bfcache with DevTools Application > Back/forward cache and collect `NotRestoredReasons` in the field.

### Third-party scripts

| Tag class | Decision |
|---|---|
| No named owner or no measured value | Remove |
| Needed but not for first paint (chat, reviews, video) | Facade (static placeholder of final size) and load on interaction or visibility |
| Analytics/marketing | Load after LCP with `async`/`defer`; consider server-side collection |
| AI chat widget or assistant | Facade plus import-on-interaction; budget its JS and main-thread time like first-party code; confirm it does not register `unload` |
| Consent banner | Reserve its space; it is often the LCP element and a CLS source |

### Streaming AI interfaces (starting budgets, tune per product)

| Metric | Starting budget | Measurement |
|---|---|---|
| Time to first token, warm session | <= 500 ms p75 | `performance.mark` at prompt sent and first non-whitespace token |
| Time to first token, cold | <= 1 s p75 | Same, first request of session |
| Time to first useful token (answer content, not preamble) | <= 1 s for simple prompts | Mark first token of substantive content |
| Stream stall gap | <= 200 ms p95 | Gap between chunks |
| Token-to-screen commit latency | <= 50 ms p95 | Chunk arrival to DOM commit |
| INP while streaming | Same as page INP budget | Measure during active streams, not only on load |

Implementation rules: parse markdown and highlight code off the main thread; batch DOM commits per animation frame or per semantic unit (sentence, row); reserve and grow the response container without shifting content above the reader; virtualise long transcripts; apply backpressure when the client render queue grows; keep a visible stop control responsive during the stream. Treat these as product SLOs owned alongside the model-latency SLOs in `ai-evaluation`.

## Toolchain currentness (checked 2026-09-24)

- Lighthouse 13.5.0 is current on npm (2026-09-18). Lighthouse 13 replaced several legacy audits with performance insights, so old audit IDs in scripts may no longer exist.
- `@lhci/cli` 0.15.1 (last published 2025-06) bundles Lighthouse 12.6.1. CI lab scores can therefore differ from DevTools/PageSpeed Insights on Lighthouse 13. Pin the version, compare against a CI-produced baseline only, and do not mix baselines across engines.
- `web-vitals` 6.x is current: `onFID` was removed in v5 (use INP); v6 adds soft-navigation reporting where the browser supports it. Use the attribution build for diagnosis.
- `scheduler.yield()` is not Baseline (MDN, 2026-09-24). Feature-detect and fall back to `setTimeout`-based yielding.
- Long Animation Frames API: Chromium 123+ only; treat it as diagnostic attribution, not a cross-browser SLI.
- CI runtime: Node.js 24 is the active LTS line; Node 20 is past end of life. Update `setup-node` and action majors deliberately and read their release notes before bumping.

## Worked example (original)

A Kampala electronics marketplace reports sales falling on mobile. Field p75 on Android: LCP 4.1 s, INP 310 ms, CLS 0.18. Sub-part analysis shows LCP resource load delay at 1.6 s because the product hero is set by JavaScript after hydration, and INP input delay dominated by a chat widget and a tag manager running long tasks during the first 10 seconds. Changes: server-render the hero `<img>` with `fetchpriority="high"` and dimensions; facade the chat widget until tapped; move marketing tags after LCP; add document speculation rules (`moderate`, product-detail URLs only, excluding `/cart/*`); remove an `unload` handler inherited from an old analytics snippet. After 28 days: LCP 2.3 s, INP 170 ms, CLS 0.04, and back-navigation from product detail to listing becomes instant because pages are restored from bfcache. The CI gate now fails any PR that adds a third-party origin without an owner entry.

## Premium versus generic output

- Generic: "Optimise images, minify JS, use a CDN" with no numbers, no flow, no owner.
- Premium: per-flow field baseline, sub-part diagnosis naming the dominant delay, a ranked fix list with expected metric movement, navigation strategy with exclusions, and a gate with a pinned toolchain and a post-release field check date.

## Evidence and currentness

Accessed 2026-09-24: web.dev *Web Vitals* (thresholds LCP 2.5 s, INP 200 ms, CLS 0.1 at p75, INP replaced FID in 2024; page updated 2024-10-31); web.dev *Optimize LCP* (sub-parts, updated 2025-03-31); web.dev *bfcache* (updated 2026-07-02; Chrome `no-store` behaviour change in progress, `NOT_ASSESSED` whether shipped); developer.chrome.com *Prerender pages* (Speculation Rules, eagerness values and limits, updated 2026-01-23; Firefox unsupported, Safari behind a flag); web.dev *Fetch Priority* (Chrome/Edge 102, Firefox 132, Safari 17.2); developer.chrome.com *Long Animation Frames API*; MDN `scheduler.yield()`; GitHub CHANGELOG for `web-vitals`; npm registry for `lighthouse`, `@lhci/cli`, `web-vitals`, `size-limit`; nodejs.org release index. HTTP/3: RFC 9114 (2022) is the standard; current adoption percentages came only from secondary sources and are `NOT_ASSESSED`. Streaming budgets are starting points from practitioner guidance, not standards.

Sources: Osmani (2026) *Web Performance Engineering in the Age of AI*; web.dev and developer.chrome.com documentation listed above.
