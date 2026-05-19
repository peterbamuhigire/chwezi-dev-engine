# Data Visualization And Dashboard UX

Use this reference for reports, business intelligence, SaaS dashboards, KPI pages, and any interface where data must drive decisions.

## Start With The Decision

Before choosing a chart, answer:

- What question should the user answer?
- What decision or action follows?
- What comparison matters: category, time, distribution, geography, relationship, part-to-whole, or qualitative evidence?
- Does the user need exact values, a pattern, an exception, or a story?

## Chart Selection

- Compare categories: bar chart, dot plot, lollipop, ranked table.
- Change over time: line chart, slope chart, small multiples, horizon chart when space is constrained.
- Distribution: histogram, box plot, violin, strip plot.
- Relationship: scatterplot, connected scatterplot, matrix, network only when relationships are the real subject.
- Part-to-whole: stacked bar, waffle, treemap; use pie/donut sparingly and only for simple parts.
- Geography: map only when location matters; otherwise use a ranked chart.
- Qualitative or evidence-heavy data: annotated lists, matrices, timelines, tagged tables.
- Exact lookup: table, not chart.

## Perception Rules

- Position and length are easier to compare accurately than angle, area, volume, and color intensity.
- Use shared baselines for comparisons where precision matters.
- Avoid 3D, heavy shadows, glossy effects, and gradients that distort perceived values.
- Reduce non-data ink: heavy gridlines, markers, borders, decorative photos, and redundant labels.
- Use preattentive attributes carefully: color, weight, shape, enclosure, and position should draw attention to what matters.

## Labels And Annotation

- Prefer direct labels over disconnected legends when space allows.
- Keep legend order consistent with visual order.
- Use active titles that state the takeaway, not generic titles like "Revenue Chart".
- Annotate important events, anomalies, thresholds, and data caveats.
- Use the right precision. Excess decimals imply confidence the data may not have.

## Dashboard Principles

A dashboard is a single-screen monitoring surface for the most important information needed to do a job. It is not a decorated report portal.

- Put urgent operational exceptions in the highest-attention area.
- Show current state, target, trend, and context where decisions require them.
- Group metrics by task and decision owner, not by database table.
- Use ranking for exceptions and performance lists.
- Preserve comparison. Do not fragment related metrics across tabs if users must compare them.
- Use muted neutrals for structure and strong color only for exceptions or selected focus.
- Provide drill-down for diagnosis, but keep the overview clear.

## Tables

- Right-align numbers and use tabular figures.
- Left-align text.
- Sort by the column that supports the task.
- Freeze headers for long tables.
- Use subtle row separators; heavy gridlines slow scanning.
- Put units in headers where practical.
- Show totals, baselines, targets, or variance when they clarify decisions.

## Dashboard Anti-Patterns

- Gauges for simple KPI values when a bullet chart, bar, or number-plus-context would be clearer.
- Pie charts with many slices or similar values.
- Text-only KPI tables where users must do mental math.
- Photo-realistic dashboard metaphors, decorative backgrounds, and logo-dominated first screen real estate.
- Bright colors everywhere.
- Multiple filters that hide needed comparisons.
- Charts that look interesting but require memorizing a private visual language for routine decisions.

## Business Soundness Check

- Can a manager identify the problem, magnitude, owner, and next action in under 30 seconds?
- Are good/bad thresholds explicit and defensible?
- Does the design reveal trends and exceptions instead of only showing current values?
- Is the dashboard dense enough to be useful but calm enough to scan daily?
- Would the same data be clearer as a table, chart, or annotated narrative?
