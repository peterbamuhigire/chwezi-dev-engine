# Large-scale React + TypeScript architecture

Use when a React + TypeScript single-page app must survive many contributors,
many domains, several environments, and years of change. Load it before
proposing folder structure, state ownership, the HTTP/API layer, configuration,
localisation, a primitives library, or test layout. For Next.js server
boundaries use `nextjs-app-router`; for multi-package repos also load
`references/monorepo-turborepo.md`.

## Inputs to collect first

| Input | Why it changes the design |
|---|---|
| Number of domains (orders, stock, customers, reports) and owning teams | Decides domain folders vs. packages |
| Environments (local mock, dev, staging, production, demo/offline) | Decides config shape and mock/live client switching |
| Locales, currencies, number formats | Decides i18n and formatter boundary |
| Server state volume vs. purely client state | Decides whether a global store is needed at all |
| Other consumers of the UI kit (second app, partners) | Decides when to extract a component library |
| Build target (Vite SPA, SSR framework, embedded webview) | Decides env access and routing strategy |

## Target layout (single app)

```text
src/
  models/<domain>/        # types/interfaces only, no logic
  http-client/            # transport: one interface, swappable implementations
  api/<domain>/           # typed domain clients: live, mock, interface
  store/<domain>/         # client-state modules (only if needed, see below)
  config/                 # Config interface, per-env files, provider, validation
  localization/           # i18n init, locale files, Intl formatters
  primitives/<family>/    # design-system atoms, no domain knowledge
  components/<domain>/    # composites; children/ for private sub-components
  views/                  # routed pages that compose components
  hooks/                  # shared hooks (useConfig, useLocalization, useModal)
tests/unit/<domain>/      # non-component unit tests
```

Dependency rule: arrows point inward only. `primitives` never import `store`,
`api`, `config`, or i18n. `views` may depend on everything below them.
Enforce it with lint (`eslint-plugin-boundaries`, `dependency-cruiser`, or
TypeScript project references), not code review alone.

When one domain folder passes roughly 30 files or has its own team, switch to
feature slicing (`features/<domain>/{api,components,store,views}`) and expose
each feature through one public entry file. Do not mix both styles in one app.

## Naming conventions

- `Item.interface.ts` for type-only modules; one domain concept per file.
- `ItemsList.component.tsx` for composites, `ElButton.tsx` for primitives,
  `Items.view.tsx` (or `ItemsView.tsx`) for routed pages. Pick one and lint it.
- `useFoo.ts` hooks, `*.mock.ts` doubles, `*.test.ts(x)` colocated with the
  component under test.
- For permission-heavy screens, split tests by condition:
  `OrdersList.permissions.approve.denied.test.tsx`. The file name then states
  the rule being proven.
- Directory names are lower-case kebab (`order-history`); agree the scheme in
  writing and lint it (`eslint-plugin-check-file` or equivalent).
- Avoid wide barrel files (`index.ts` re-exporting dozens of modules); they
  slow type-checking and hide cycles. A small per-feature public entry is fine.

## State ownership decision

Most "global state" in business apps is really server state. Decide per value:

| Value | Owner | Tool |
|---|---|---|
| Data fetched from the API (lists, records) | Server-state cache | TanStack Query (or the framework's loader/cache) |
| Filters, pagination, selected tab that must survive reload/share | URL | Router search params |
| Form draft | Form library | React Hook Form + Zod resolver |
| UI-only state for one subtree | Component | `useState` / `useReducer` / focused Context |
| Cross-cutting client state (auth session, feature flags, offline queue) | Client store | Zustand or Redux Toolkit, one module per domain |

If you do adopt a store, keep the flow one-directional: a component calls a
domain action, the action does the async work through the API client, and a
synchronous reducer/setter commits the change. Each domain module exposes a
typed state interface (`OrdersState`), actions, and selectors; components
never reach into another domain's state shape.

## Configuration

1. `Config.interface.ts` declares every key; per-environment files satisfy it.
2. Select the file once at boot from `import.meta.env.MODE` (Vite) or the
   framework's equivalent; validate with Zod and fail loudly before mount.
3. Inject through `ConfigProvider`; components call `useConfig()`. Never read
   `import.meta.env` or `process.env` in leaf components.
4. Config selects implementations: `httpClient: "fetch" | "mock"`,
   `apiClient: "live" | "mock"`, token storage key, feature flags.
5. Anything in the client bundle is public. Secrets never go in frontend
   config, whatever the variable prefix.

## HTTP and API client layer

- One `HttpClient` interface with a single `request<TRes, TPayload>(params)`
  method; params carry method, endpoint template, payload, headers,
  `requiresToken`, and an `AbortSignal`. Implementations: `fetch` (default)
  and a mock with configurable delay. No third-party HTTP package is imported
  anywhere else, so replacing it touches one folder.
- One typed client per domain (`OrdersApiClient`) built on `HttpClient`, with
  an interface, a live implementation, and a mock returning fixture data.
- Parse and validate responses with Zod at the client boundary; the store and
  components only ever see validated domain types.
- Build URLs with `URL`/`URLSearchParams`, not string concatenation.
- Normalise errors into one typed shape (`{ kind: "network" | "auth" |
  "validation" | "server", status?, fieldErrors? }`) so every screen handles
  failure the same way.

## Localisation

- Strings through `i18next` + `react-i18next`, split into namespaces per
  domain (`locales/<lang>/<namespace>.json`), lazy-loaded.
- Numbers, currency, dates, relative times, and lists through `Intl.*`;
  derive currency from data (`UGX`, `KES`, `USD`), never hard-code symbols.
  UGX has no minor unit in practice - let `Intl.NumberFormat` decide digits.
- Expose one `useLocalization()` hook returning `t`, `locale`, `setLocale`,
  and formatters, so i18n can be swapped without touching components.
- Persist the chosen locale; set `<html lang>` and `dir` on change.

## Primitives and component library

- Primitives take a `variant`/`size` prop mapped to classes through a lookup
  table (or `cva`), not free `className` strings; they receive text and
  callbacks, never call stores, APIs, or `t()`.
- Build accessibility into primitives once: native elements first, visible
  focus, labelled icon buttons, and the modal as a focus-trapped `<dialog>` or
  a vetted headless library. A `useModal()` hook owns open/close state.
- Extract a shared library when any one holds: a second app needs the
  primitive, its API has been stable for about three sprints, or an outside
  team wants it. Ship ESM + types via Vite library mode or `tsup`, declare an
  `exports` map, and make `react`/`react-dom` peer dependencies.
- Document primitives in Storybook (or Ladle) with mock API clients.

## Testing tiers

- Vitest + React Testing Library for components; query by role and
  accessible name, assert on what the user sees.
- Plain Vitest for formatters, API clients (against the mock `HttpClient`),
  and store modules.
- Inject mock API clients through the provider in a shared `renderWithProviders`
  helper; do not monkey-patch global `fetch`.
- Playwright for the three to five revenue-critical journeys end to end.
- Type tests (`expectTypeOf`) for public API client and primitive props.

## Quality gate (block merge if any fail)

- [ ] Dependency-direction lint passes; no primitive imports domain code.
- [ ] Config validated at boot; no env reads outside `config/`.
- [ ] Every API response validated; error shape unified.
- [ ] Server state is not duplicated into a client store.
- [ ] All user-visible strings go through i18n; money/dates through `Intl`.
- [ ] Primitives pass axe checks and keyboard-only use in Storybook.
- [ ] `tsc --noEmit`, lint, unit tests, and production build are green.

## What senior work looks like vs. generic output

| Generic AI output | Senior output |
|---|---|
| `components/` with 150 flat files | Domain or feature folders with an enforced dependency rule |
| `axios` imported in 40 components | One `HttpClient` seam, domain clients, mocks via config |
| Redux holding every API response | Query cache for server data; small store for real client state |
| `` `UGX ${amount}` `` string templates | `Intl.NumberFormat(locale, { style: "currency", currency })` |
| Tests mocking `fetch` globally | Mock API clients injected through providers |

## Worked example (original)

A Kampala pharmacy chain runs a stock and dispensing web app for 14
branches, in English and Luganda, pricing in UGX. Domains: `stock`,
`dispensing`, `suppliers`, `reports`. Branch filters and date ranges live in
the URL so a regional manager can share a report link. Stock lists come from
TanStack Query keyed by branch; the only client store holds the signed-in
pharmacist's session and an offline dispensing queue. `config.demo.ts` wires
mock API clients so sales staff can demo the app on a laptop without a
network. Permission tests cover "pharmacist cannot approve a controlled-drug
write-off" as `WriteOffForm.permissions.approve.denied.test.tsx`.

## Anti-patterns

- Global singletons for store, config, or API client; use providers so tests
  can swap them.
- Env reads inside leaf components.
- One `types.ts` for the whole app.
- Translating inside primitives.
- Scattered `process.env.X ?? "default"` fallbacks instead of a validated
  config interface.
- Starting a new app on Create React App: it is deprecated. Use Vite or a
  React framework.

## Evidence/currentness

- Stack baseline checked 2026-09-24: React 19.3 (react.dev/versions), React
  Compiler 1.0 stable (react.dev blog), Vite 8.3 with Rolldown and Node
  20.19+/22.12+ (vite.dev/releases, Vite 8 announcement), TypeScript 7.0
  native compiler (Microsoft TypeScript blog). Create React App deprecation:
  react.dev blog, February 2025.
- With React Compiler enabled, do not add `useMemo`/`useCallback` by habit;
  see `skills/frontend-ux/react-development/references/react-18-19.md`.
- TypeScript 7 config changes: see
  `skills/languages/typescript-effective/references/tsconfig-production.md`.
- Library choices (TanStack Query, Zustand, Redux Toolkit, i18next, cva,
  dependency-cruiser) are patterns, not version claims; current major versions
  `NOT_ASSESSED` in this file.

Sources: Fusco (2023) *Large Scale Apps with React and TypeScript*; react.dev;
vite.dev; devblogs.microsoft.com/typescript.
