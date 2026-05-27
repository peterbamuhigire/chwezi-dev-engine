# SaaS Web App Pattern Selector

This reference is self-contained. It distills the user's supplied Design Studio UI/UX
web-app pattern article and SaaS design article into operational pattern choices.

Sources used:

- https://www.designstudiouiux.com/blog/web-app-ui-design-patterns/
- https://www.designstudiouiux.com/blog/how-to-design-and-build-saas-product/

## Pattern Selection Rule

Choose patterns by user job and data shape. Do not choose a fashionable pattern before
you know whether the user is browsing, comparing, completing, monitoring, deciding, or
recovering from an error.

## Fast Selector

| User Job | Prefer | Avoid |
|---|---|---|
| Compare records or make bulk decisions | Data table with sort, filter, selection, sticky header, pagination | Cards, infinite scroll |
| Browse visually distinct items | Cards or grid of equals | Dense table without visual preview |
| Complete a long task | Stepper, progressive disclosure, save/resume, inline validation | One long ungrouped form |
| Move between app areas | Sidebar or top-level tabs, stable active state, breadcrumbs for depth | Hidden hamburger-only navigation on desktop |
| Inspect one item while keeping context | Split view, master-detail, drawer detail | Full-page jump for every quick inspection |
| Explain missing data | Empty state with cause, next action, and permission/support path | "No data" only |
| Wait for data | Skeleton matching final layout, optimistic update where safe | Full-screen spinner after initial load |
| Recover from failure | Error state with retry, details, support/escalation route | Silent failure or raw exception text |
| Confirm high-impact action | Review screen, explicit confirmation, undo when reversible | Habitual OK dialog for irreversible actions |
| Monitor operational status | Dashboard with thresholds, freshness, drill-down, owner | Decorative KPI cards with no decision path |
| Work with AI output | Streaming response, confidence/uncertainty, citations/evidence, edit/retry, human override | Magic answer with no controls or provenance |

## SaaS MVP UX Rules

- First value must be visible in the first session. If onboarding blocks value, shorten it.
- MVPs should prove 3-5 core capabilities, not every future module.
- Track activation rate, time-to-value, and day-7 retention as design metrics.
- Add a design system soon after MVP if more than one team or product area will extend the UI.
- Multi-tenant complexity should show in UX only where it matters: tenant switcher, permissions, billing, audit, data boundaries, and support.

## Pattern Register Template

Use this inside UX specs or design handoffs.

| Screen / Flow | User Job | Pattern | Why This Pattern | Accessibility / State Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Accessibility Baseline

Each chosen pattern must define keyboard operation, focus order, focus visible state,
ARIA labels where required, reduced-motion behavior, screen-reader announcement for
async changes, disabled/loading behavior, and mobile touch target sizes.

## Anti-Patterns

- Infinite scroll for financial records, search results, audit logs, or anything users
  need to bookmark, return to, export, or reconcile.
- Modals for complex multi-step creation flows that need save/resume.
- Cards for dense numeric comparison.
- Tabs used as filters when the user needs combined or multi-select filtering.
- AI interfaces that stream text but provide no undo, retry, source, confidence, or
  human escalation path.
