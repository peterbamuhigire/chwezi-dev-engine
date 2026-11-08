Parent skill: [reporting-and-export-engineering](../SKILL.md)

# Chwezi Reporting and Dashboards Standard

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

**Status:** Adopted into the Chwezi engines on 8 November 2026 on the instruction of Lead Developer
Peter Bamuhigire, as the reporting companion to the Chwezi Product Excellence Standard. The
source design bible (Edition 1.0, November 2026) described itself as a proposed engineering
standard subject to product-specific validation; its numbers are starting values, and a product
that departs from a SHOULD records a design decision record (DDR).
**Version:** 1.0.0
**Owner:** Peter Bamuhigire / Chwezi Core Systems
**Applies with:** the Chwezi Product Excellence Standard (governing product quality; its hard gates
are restated for engineers in
[product-excellence-engineering-gates.md](../../../frontend-ux/frontend-architecture/references/product-excellence-engineering-gates.md)
and summarised in the parent skill), the Chwezi business-app house style (visual layer) and the
release gate of the product.
**Agent entry point in this engine:** [reporting-and-export-engineering](../SKILL.md). The full rule
catalogue is the local [rules-and-gates.md](rules-and-gates.md).

Local adaptation note: the normative text below is unchanged from the 1.0.0 doctrine. Only links
are adapted. Where the text names the house style, the money-figures skill or the Product
Excellence data-trust reference, those are visual-layer and screen-trust references maintained in
`chwezi-design-engine`; this engine's engineering procedure does not need them to run, and the
parent skill states every rule an engineer must apply.

A report is a decision system, not a chart gallery: it states the question, uses trustworthy
data, shows the evidence, supports an action, exports faithfully and leaves an auditable record.
A handsome report with a wrong total is a product defect. This standard says what every Chwezi
dashboard, analytical screen, fixed report, export and executive narrative must do, how that is
proved, and when a release is blocked. It is an internal policy, not a certification, and no
Chwezi proposal may present it as one.

## Scope

- Every reporting surface in a Chwezi app or system: home and owner dashboards, KPI cards,
  analytical screens, registers and lists with totals, financial statements, closeouts and night
  audits, scheduled reports, report centres, A4 print and PDF output, and CSV or XLSX exports.
- Written management reports, board packs and executive narratives built from product data:
  the narrative rules (RPT-NARR) apply to them as fully as the data and layout rules.
- Out of scope: marketing analytics pages on public websites, and slide decks that do not
  reproduce product figures.

## Precedence

This standard sits at step 4 of the Product Excellence ladder, beside it: law, safety and
privacy; accessibility; data integrity; then the two standards (the stricter rule applies when
they differ); then house style; then product brand. Concretely:

| Topic | Rule |
|---|---|
| Width classes | The Product Excellence classes (compact under 600, medium 600-839, expanded 840-1199, large 1200-1599, extra-large 1600 and above). The source bible's four-band list is superseded. |
| Card radius, spacing, type scale, colour roles | House style values. The source bible's 10-16 px radii and its spacing list are superseded. Tables and dense registers are never over-rounded. |
| Money decimals | The currency's ISO 4217 minor unit (UGX and RWF 0; KES, TZS and USD 2), as in the Product Excellence standard. Compact K, M and B forms follow the money-figures skill and are never used for a closing balance, statement total or payment figure. |
| On-screen data trust | The Product Excellence data-trust reference governs KPI cards, time series, tables, zero versus unavailable, freshness and accessible charts. This standard adds the metric contract, reconciliation, period rules, print, export and report lifecycle. |
| Reference mockups | Inspiration only. The 29 reference designs studied for the bible carried arithmetic errors, tiny labels and untested print layouts; none of their figures, fields or calculations may enter a product. |

## The four output contracts

Every reporting surface declares which one it is, because each has different rules.

| Contract | Job | Distinguishing rules |
|---|---|---|
| Operational dashboard | Monitor now and act | Freshness always shown; exceptions before trends; every figure drills to its records; no decorative charts |
| Analytical workspace | Explore, compare, drill | Filters typed, visible and reversible; comparisons comparable; saved views |
| Fixed report | Reproducible evidence | Immutable generation record; exact period, basis, filters and version on every page; repeatable output |
| Executive narrative | Findings, implications, decisions | Every claim cites a measure and filter; observation separate from inference; human approval for consequential content |

## The five reporting questions

What happened? Why? What is at risk? What action is required? How confident are we? A screen or
document answers them in that order where they apply. A widget, chart or section that answers none
of them is removed.

## Quality order

Correctness and confidentiality outrank legibility; legibility and usability outrank visual
polish; polish outranks novelty. Reject on sight: misleading charts, invented data, unexplained
percentages, inconsistent period comparisons, quantities summed across different units, and
exports that omit their filter context.

## Hard release gates

Any one of these on a reporting surface blocks release regardless of score. Each needs `MEASURED`
evidence to close; an applicable gate with `NOT_ASSESSED` evidence counts as open. The right-hand
column names the Product Excellence gate it also trips, where one applies.

| Gate | Fails when | Also trips |
|---|---|---|
| RPT-GATE-01 Report does not reconcile | A headline figure, its detail list, the ledger (where one exists), the PDF and the spreadsheet export disagree for the same scope, including zero, negative, reversed and missing-data cases. | PX-GATE-03 |
| RPT-GATE-02 Undefined metric | A headline or exported metric has no approved metric contract (definition, numerator, denominator, inclusions, unit, date basis, grain, source, owner, version). | PX-GATE-09 |
| RPT-GATE-03 Ambiguous scope | The exact period, timezone, tenant or branch, currency or applied filters are missing from the screen or from any exported page; or a comparison uses a non-comparable period without saying so. | None (reporting-specific) |
| RPT-GATE-04 Export leak | A download, print, scheduled delivery or share link returns rows or fields outside the requester's authorised scope, or relies on the interface hiding them. | PX-GATE-04, PX-GATE-05 |
| RPT-GATE-05 Unsafe spreadsheet | A CSV or XLSX cell that begins with a formula trigger is not neutralised, or identifiers lose leading zeros or precision. | None (reporting-specific) |
| RPT-GATE-06 Print failure | A4 output is a screenshot of the interactive screen, table headings do not repeat, a total is separated from its label, page "x of y" or the report identity is missing, or text is shrunk below the print legibility floor. | None (reporting-specific) |
| RPT-GATE-07 Ungrounded narrative | A written or AI-generated insight states a figure or a cause that does not trace to a cited measure and filter, or a consequential financial, clinical or regulatory narrative ships without human approval. | PX-GATE-09 |
| RPT-GATE-08 Unknown shown as known | No data, failed reconciliation, missing source or restricted access is displayed as zero, as complete or as live; or an integrity warning can be dismissed. | PX-GATE-02, PX-GATE-10 |

## Release decision

Reporting surfaces use the Product Excellence scorecard and verdicts (PASS at 85 or more with no
open gate and no dimension below 2; CONDITIONAL and BLOCKED as defined there). The RPT gates are
added to the PX gates for any surface in scope; a high score never buys back either.

## Rules

The normative rules, with IDs of the form `RPT-<AREA>-NNN`, levels (MUST, SHOULD, MAY), checks and
evidence, are in the [rules and gates reference](rules-and-gates.md) (local copy).
MUST, SHOULD and MAY have the Product Excellence meanings; a SHOULD departure needs a DDR. IDs are
never reused; a withdrawn rule keeps its ID with the status `WITHDRAWN`.

## Owner rules carried into this standard

These were set for Chwezi products before this standard and are binding here:

- Quantities in different units are never summed into one figure (spoons plus litres plus kilos
  means nothing); totals are per unit or expressed as value (owner rule, 7 November 2026).
- No raw keys, internal codes, ISO date strings or ungrouped decimals on any screen or document;
  dates read `4 Nov 2026`; every amount carries a label (owner rule, November 2026).
- Full amounts show the currency's ISO 4217 minor unit; compact K, M and B forms keep two digits of
  the abbreviation and never appear on a closing balance, statement total or payment figure
  (owner ruling, 8 November 2026).
- Every user-facing document number is contiguous per tenant and document type; a report that
  lists numbered documents shows the number as issued and never renumbers (owner standing rule,
  5 November 2026).

## How agents apply it

Load the skill for any reporting work, together with the Product Excellence skill, the house style
and the domain skill. In short: inspect the existing reports, metric definitions, permissions and
export services; write the report contract (decision, users, output contract, metrics, grain,
period, filters, states, export targets, acceptance tests); prototype the screen and the A4
composition separately; build on shared components with server-authoritative calculations;
verify data, interface and every exported page with measured evidence; have someone else review,
with a human domain reviewer for financial, clinical or regulatory reports; release with known
limits and a rollback; measure use and misreading afterwards. Unrun checks are `NOT_ASSESSED`.

## Evidence states and currentness

The Product Excellence vocabularies apply unchanged: `VERIFIED`, `CHANGED`, `NOT_ASSESSED` for
facts; `MEASURED`, `HEURISTIC`, `NOT_ASSESSED` for release evidence. Standards cited by this
standard (WCAG 2.2, PDF/UA-1 and PDF/UA-2, PDF/A, spreadsheet formula injection guidance) are
recorded with access date and status in this engine's change record
`docs/updates/2026-11-08-reporting-and-dashboards-standard.md`. Following this standard
does not make a product, report or PDF conformant with any of them; conformance needs tool and
manual validation.

## Copies in other engines

Each Chwezi engine that serves reporting work carries its own complete copy of this doctrine and
the rules catalogue, with identical rule IDs and wording, and works without any other engine
installed. This file is the canonical text; copies are re-synced whenever its version changes.

## Change control

As for the Product Excellence standard: Peter Bamuhigire approves every change; semantic versions
(patch for wording, minor for new SHOULD or MAY rules and new contracts, major for any new,
removed or re-levelled MUST, any gate or any threshold); every release logged in the engine's
change record (its `CHANGELOG.md` or dated update notes) with the rule IDs affected; product repositories record the version they were
assessed against.
