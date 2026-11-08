Parent skill: [reporting-and-export-engineering](../SKILL.md)

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

# Screen composition and components

Use this reference to lay out a dashboard or analytical screen and to specify its components. The
Product Excellence data-trust reference already governs KPI cards, time series, donuts and gauges,
tables, alerts, money, zero versus unavailable and chart accessibility; this file adds the
reporting layer on top and does not repeat those rules. House style supplies tokens, type,
radius and spacing. Rule IDs: [rules-and-gates.md](rules-and-gates.md).

## Task 1: compose the page

Order (RPT-VIEW-001, RPT-PURPOSE-003):

1. **Shell and context row** (RPT-SCOPE-001): title that states the decision ("Can the shift be
   closed safely?"), then organisation, branch or outlet, exact period with dates ("Mon 3 Nov 2026,
   07:00-22:00 EAT"), currency, freshness ("Updated 14:02") and the active filters as chips.
2. **Headline row**: 3 to 5 measures, each a KPI card with label, value and unit, period,
   comparison basis, direction in words and a drill-down.
3. **Primary analysis and exceptions**: one dominant trend or comparison, and the exception queue
   (sorted by consequence and age, with owner, due date and action; RPT-VIEW-004).
4. **Supporting breakdowns**: ranked entities, small multiples; disclosed progressively, not
   stacked without end.
5. **Records**: the detail table, with a preview drawer that keeps list position (RPT-VIEW-006).

Keep visual competition low: one dominant analysis area per screen. An equal-weight grid of ten
to twenty panels is the most common failure in the reference set and is rejected.

## Task 2: adapt to width (Product Excellence width classes)

| Class | Layout |
|---|---|
| Compact (under 600) | One column; one primary KPI or a 2-up grid; one chart at a time; filters in a dismissible sheet; searchable record list (never a sideways table that loses its headers); drawer becomes full screen |
| Medium (600-839) | Two panes where meaningful (list and detail); charts above records |
| Expanded (840-1199) | Navigation rail or sidebar, two or three content columns |
| Large and extra-large (1200 and above) | Sidebar, main workspace and an optional context rail; content width capped so lines stay readable |

Breakpoint behaviour is tested at 200% text (PX-GATE-07) and in the longest supported language and
Arabic RTL.

## Task 3: filters and dates

- Filters are typed parameters (period, branch, status, category); each states whether it is
  global or local to one widget. Applying one updates every widget in its scope together, and the
  chips show what is applied. Reset returns to a documented default. Saved views for repeated
  analysis (RPT-SCOPE-002/003).
- The date control shows exact dates, timezone and fiscal-calendar rule; presets are allowed
  ("This month") but the resolved dates are always visible; incomplete periods are marked; the
  comparison basis is named (RPT-PERIOD-001/002).
- The tenant and branch selector never offers a branch the user cannot see, and changing it never
  silently keeps a stale figure from the previous branch.

## Task 4: the reporting states

Add these to the Product Excellence state matrix for every reporting surface (RPT-STATE-001):

| State | What the user sees | Never |
|---|---|---|
| Partial data | Figures with "Partial: Kireka branch has not synced since 11:40" | A total that looks complete |
| Stale snapshot | Last values kept, "Stale" chip with time, Refresh | Blank screen or silent old data |
| Reconciliation failure | Non-dismissable warning with the difference and cause, last good snapshot, Retry | A toast, or hiding the difference |
| Source disconnected | Which source, since when, what is affected | Zeros |
| Access restricted | "You can see Kampala branch only" and how to request more | Zeros, or an empty table with no reason |
| Export pending | Job progress, where the file will appear, Cancel | Blocking the screen |

No data versus zero versus unknown follows the Product Excellence rule (Task 9 of data trust):
a measured zero shows `0` with its unit; anything unknown says why (RPT-STATE-002).

## Task 5: choose the chart

| Question | Chart | Rules |
|---|---|---|
| Ranking, magnitude | Bar, sorted, zero baseline | Direct value labels when few bars |
| Change over time | Line | Gaps for missing periods; labelled non-zero baseline only |
| Relationship | Scatter | Units on both axes |
| Matrix (day by hour) | Heatmap | Legend and data table mandatory |
| Part of a whole | Donut (at most 5 parts) or sorted bar | Exact totals and a text legend |
| Progress to a known bound | Bar with target line (gauge replacement) | Exact value and bound in text |
| Stage conversion | Funnel | One population; never mixed denominators (RPT-VIEW-005) |

No 3D, no gauge without exact labels, no unlabelled sparkline, no placeholder percentages. Every
chart has a precise title, units, period, legend, a one-line factual takeaway and a data-table
alternative (RPT-VIEW-002).

## Task 6: specify each component

Every component: uses house-style tokens; contains no domain arithmetic (it receives computed
values); has accessible names and focus order, touch and keyboard behaviour, responsive wrapping
and a reduced-motion fallback; and ships with four fixtures: normal, extreme value, missing data
and permission-restricted (RPT-VIEW-007). Its print variant drops hover and click-only content.

| Component | Inputs | States beyond default | Quality rule |
|---|---|---|---|
| KPI card | label, value, unit, period, comparison, drill target | stale, empty, error, restricted | Large figure, short context; direction in words, never a colour-only arrow |
| Variance indicator | actual, baseline, favourable rule, magnitude | positive, negative, zero, not comparable | Status from the metric's direction rule, not the sign |
| Filter bar | schema, applied values, scope, reset | changed, invalid, loading | Visible chips; no silent scope change |
| Date range | start, end, timezone, fiscal calendar, comparison | preset, custom, partial period | Exact dates shown; incomplete period disclosed |
| Tenant and branch filter | allowed scopes, current scope | single-scope, restricted | Only permitted scopes offered |
| Data table | columns, sort, filter, row key, actions | loading, empty, selected, overflow | Virtualise large data; numbers right-aligned, tabular |
| Hierarchy table | parent key, child count, expansion | collapsed, expanded, loading children | Accessible expand state; stable sort; subtotals labelled |
| Record preview | entity id, role, permitted fields, history | loading, redacted, error | Keeps focus and list position |
| Time-series chart | grain, measure, unit, comparison, missingness | no data, partial, focus | Gaps, not invented zeros |
| Ranked bar chart | category, value, sort, unit | negative, truncated | Zero baseline for magnitude |
| Donut or share | categories, counts, denominator | small slices, missing, overflow | Exact totals; text legend; no 3D |
| Heatmap | x and y categories, cell measure, scale | missing, outlier, selected | Legend and data table |
| Funnel or pipeline | stages, population, conversion rule | drop-off, skipped, missing | One denominator |
| Exception queue | severity, due, owner, action | open, assigned, resolved, overdue | Sort by consequence and age |
| Reconciliation warning | difference, cause, last good snapshot | resolving, resolved | Not dismissable until resolved |
| Narrative insight card | claim, evidence, caveat, action | draft, verified, disputed | Never causation from correlation |
| Action recommendation | action, owner, evidence, consequence | proposed, accepted, done | Names who acts and why |
| Report catalogue tile | report id, title, owner, scope, formats | favourite, restricted, archived | Definition distinct from a generated file |
| Scheduled report row | schedule, timezone, recipients, permission | active, paused, failed, last run | Recipients and failures audited |
| Export status | job id, snapshot, output, expiry | queued, running, ready, failed | Immutable parameters; safe retry |
| Report metadata header | entity, report id, period, status, filters | draft, final, revised | Repeated briefly on later pages |
| Approval register or summary | authority, items, consequences, evidence | pending, approved, rejected, reversed | Bulk actions reviewed and audited |
| Empty or error state | reason, scope, recovery action | no records, restricted, unavailable | Zero never stands for unknown |
| Print preview | paper, orientation, margins, page count | overflow, failed, ready | Shows the exact export, not a screenshot |

## Task 7: interaction and trust

- Drill-down opens the exact contributing records with the measure, scope and dates preserved;
  back returns to the same scroll and filters (RPT-RECON-004).
- Refresh keeps the last valid figures with an indicator; skeletons only where data is awaited
  (RPT-STATE-005).
- Errors are dialogs or inline states, never only a toast; irreversible actions confirm their
  consequence (house rule: every error uses the product's alert dialog).
- Explain why a value changed when it changes after a refresh, a back-dated posting or a sync.

## Evidence/currentness

Width classes and target sizes cite the Product Excellence currentness register (M3, A5). The
3-5 headline range and the five-part donut limit are Chwezi values.
