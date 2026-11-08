Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Infographics Design and Production Quality Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Rules and gates

Every normative rule of the Chwezi Infographics Design and Production Quality Standard, version
1.0.0, adopted 8 November 2026. Binding text: `doctrine/infographics-standard.md`.

## How to read this catalogue

- **ID** `INFO-<AREA>-NNN` is stable and never reused. **Lvl**: MUST, SHOULD (departure needs a design
  decision record), MAY. **Gate**: the INFO hard gate a failure trips (blank = scored finding).
- **Ev**: RENDER (rendered in the real target at actual size and inspected, reviewer named), PROOF
  (print proof at actual size), REG (provenance register entry), CALC (recorded calculation or
  checker output), TOPO (graph check output), LINT (automated lint), REVIEW (named review), AT
  (accessibility check), RECORD (brief, log, manifest or declaration).
- Values marked "Chwezi value" are internal defaults from the handbook or computed here, not external
  facts.

## Hard gates

| Gate | Short name | Main rules |
|---|---|---|
| INFO-GATE-01 | Invented or unsourced fact | INFO-DATA-001/002/003, INFO-AGENT-001 |
| INFO-GATE-02 | Pseudo-text or illegible text | INFO-TYPE-002/003, INFO-SOCIAL-002 |
| INFO-GATE-03 | Synthetic or unlicensed imagery | INFO-ILLUS-002/003, INFO-ICON-003 |
| INFO-GATE-04 | Misleading encoding | INFO-CHART-002/003/004, INFO-TIME-002, INFO-COMP-001 |
| INFO-GATE-05 | Broken structure | INFO-FLOW-001/002/003, INFO-CYCLE-001, INFO-TREE-001 |
| INFO-GATE-06 | Unreviewed regulated or unsafe content | INFO-SAFE-001/002, INFO-TECH-002 |
| INFO-GATE-07 | Inaccessible | INFO-A11Y-001/002, INFO-COLOUR-001 |
| INFO-GATE-08 | Uninspected or unarchived release | INFO-QA-001/003, INFO-PRINT-001/002 |

## Brief and message (BRIEF)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-BRIEF-001 | MUST | | Before artwork, record the production brief: identifier, owner, reviewer, due date, audience, what they already know, the decision or action expected, the encounter context and reading distance, the one-sentence takeaway, mandatory wording, prohibited content, formats and dimensions, languages and accessibility needs, and approval roles. | Brief record | RECORD |
| INFO-BRIEF-002 | MUST | | One communication goal and one primary audience; the artefact remains understandable without a presenter. | Cold read by someone outside the project | REVIEW |
| INFO-BRIEF-003 | SHOULD | | Three to seven supporting information units per infographic; surplus goes to a series, a companion text or an appendix. | Element inventory | RECORD |

## Information architecture (IA)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-IA-001 | MUST | | Every fact is mapped to a numbered visible element before layout; every element is mapped back to a fact or a stated purpose. | Element inventory | RECORD |
| INFO-IA-002 | MUST | | Reading order is natural (top to bottom, or in the script direction); branches are labelled; the key result is visible before secondary detail. | Render review | RENDER |
| INFO-IA-003 | MUST | | Headline, explanatory subtitle, stage headings, evidence labels, annotations, source and date are distinct, consistent roles. | Typography token sheet | RECORD |
| INFO-IA-004 | SHOULD | | One focal region with supporting regions; not every statistic carries equal visual weight, and there is no empty decorative acreage. | Render review | REVIEW |

## Typography (TYPE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-TYPE-001 | MUST | | Conventional, licensed typefaces with normal letterforms and full glyph coverage for every language shipped, chosen under the banned-font doctrine; at most two families and a disciplined weight scale; the typeface and reason are stated. | Font record | RECORD |
| INFO-TYPE-002 | MUST | 02 | No warped pseudo-letters, imitation handwriting for body text, random mixed capitals, impossible ligatures, distorted numerals or generated illegible labels; if a generator cannot render text correctly, the layout is redrawn with real text. | Proof at actual size | RENDER |
| INFO-TYPE-003 | MUST | 02 | Every text role meets the minimum size computed from its farthest reading distance and the output scale ([mathematics](mathematics-and-algorithms.md), task 1); critical text is never shrunk to force a fit. | Size calculation per role | CALC |
| INFO-TYPE-004 | MUST | | Text is typeset and editable in the master (live text layers in SVG, PPTX, DOCX and PDF), proofread by a person, and matches the approved copy sheet exactly. | Exact-text diff and proofread | LINT, REVIEW |
| INFO-TYPE-005 | MUST | | Numbers use tabular figures, the approved number, unit, date and case policy, and correct minus signs, units and currency codes. | Copy check | REVIEW |

## Colour (COLOUR)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-COLOUR-001 | MUST | 07 | On-screen text meets 4.5:1 (3:1 for large text and meaningful graphics); status and categories are never encoded by colour alone, but paired with labels, symbols or patterns. | Contrast calculation | CALC, AT |
| INFO-COLOUR-002 | MUST | | A restrained palette (one dominant colour, one accent, neutrals) with each colour holding one stable meaning across the artefact. | Palette record | RECORD |
| INFO-COLOUR-003 | SHOULD | | Categorical colours stay distinguishable under protan, deutan and tritan simulation and in greyscale (Chwezi values: CIEDE2000 at least 10 between any two categories under each simulation; L* difference at least 20 between adjacent categories in greyscale). | Simulation output | CALC |
| INFO-COLOUR-004 | MUST | | Print colour is converted and proofed: no thin pale lines on white, small black text in 100% K only, total ink coverage and rich black agreed with the printer, spot colours distinguished from process colour. | Print proof | PROOF |

## Layout (LAYOUT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-LAYOUT-001 | MUST | | A grid is chosen before elements are placed: canvas, safe area, margins, columns and gutters recorded in the layout token sheet. | Token sheet | RECORD |
| INFO-LAYOUT-002 | SHOULD | | Spacing from an 8-point base scale (8, 16, 24, 32, 40, 48, 56, 64); 4 and 12 only as justified optical exceptions; edges of labels, cards and illustrations align. | Token audit | LINT |
| INFO-LAYOUT-003 | MUST | | Desktop, tablet, phone and print are designed as separate renditions when one canvas would compromise legibility, following the Product Excellence width classes (compact under 600, medium 600-839, expanded 840 and above, in dp or CSS px); rearrangement preserves narrative order and every relationship. | Rendition review | RENDER |

## Illustration (ILLUS)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-ILLUS-001 | MUST | | Newly made people and scenes are explicit illustration: flat vector, limited-shade editorial art, isometric, schematic cutaway, technical line art, simple cartoon or branded pictogram. | Commissioning sheet | RECORD |
| INFO-ILLUS-002 | MUST | 03 | No synthetic photorealistic people or scenes; a synthetic image is never presented as documentary evidence. | Asset review | REVIEW |
| INFO-ILLUS-003 | MUST | 03 | Real photographs are client-supplied or licensed, accurate and relevant, with the licence recorded; generated art carries no embedded text or fake logos, and illustration sits on a separate layer from editable text. | Licence manifest | RECORD |
| INFO-ILLUS-004 | MUST | | Illustrations clarify a mechanism; they never imply impossible connections, quantities or scale. | Expert review | REVIEW |

## Icons (ICON)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-ICON-001 | MUST | | One icon family with consistent stroke, perspective, corners and weight; each icon supports a specific concept and means the same thing everywhere it repeats. | Icon inventory | REVIEW |
| INFO-ICON-002 | MUST | | Unfamiliar icons are paired with text; culturally variable symbols are avoided; arrows, units, currency and domain safety symbols are correct; icons survive final size and greyscale. | Proof | RENDER |
| INFO-ICON-003 | MUST | 03 | Source and partner logos are real, current, used with permission and unaltered. | Permission record | RECORD |

## Data and provenance (DATA)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-DATA-001 | MUST | 01 | Every quantitative claim has a register entry: claim ID, exact approved wording, location in the graphic, source title, author, publication and retrieval dates, period, unit, denominator, method, calculation, rounding, confidence, caveat, sign-off and licence. | Register | REG |
| INFO-DATA-002 | MUST | 01 | Never invent percentages, counts, dates, locations, citations, rankings or source logos; illustrative numbers are flagged prominently on the graphic. | Register cross-check | REG |
| INFO-DATA-003 | MUST | 01 | Calculations are reproducible from the stored inputs; displayed totals and percentages are cross-checked against the data. | Recalculation | CALC |
| INFO-DATA-004 | MUST | | A dated source note sits on the graphic; transformations, filters and missing values are recorded with the artwork. | Render review | RENDER |

## Charts (CHART)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-CHART-001 | MUST | | Geometry follows the question: bars for categories, lines for ordered time, scatter for relationships, maps only for spatial evidence, small multiples for consistent comparison; no pie with many categories. | Chart specification | RECORD |
| INFO-CHART-002 | MUST | 04 | Bar length starts at zero; line scales are honest and labelled; no 3D or perspective that alters perceived magnitude. | Chart audit | REVIEW |
| INFO-CHART-003 | MUST | 04 | The lie factor of every encoded comparison lies between 0.95 and 1.05; areas and pictogram counts scale with value (radius with the square root). | Checker output | CALC |
| INFO-CHART-004 | MUST | 04 | Units, period, meaningful ticks, readable labels, direct labels for key results and uncertainty where relevant are shown. | Chart audit | REVIEW |
| INFO-CHART-005 | MUST | | Shares that must sum to 100% use largest-remainder rounding; percentages and percentage points are never mixed. | Checker output | CALC |

## Process flows (FLOW)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-FLOW-001 | MUST | 05 | Each step has a unique identifier; displayed numbering equals the true process order; no stage is duplicated and no node is orphaned. | Graph check | TOPO |
| INFO-FLOW-002 | MUST | 05 | Start, end, decision, branch and exception nodes are explicit; every node is reachable from a start and can reach an end; every decision has two or more labelled exits. | Graph check | TOPO |
| INFO-FLOW-003 | MUST | 05 | Arrowheads are unambiguous; connectors do not silently cross (crossings are zero, or each one is marked with a bridge); rejoining paths are explicit. | Graph check, render | TOPO, RENDER |
| INFO-FLOW-004 | MUST | | Inputs, transformations, decisions, outputs and exceptions are distinguished; responsibilities are mapped where the process has actors. | Topology audit | REVIEW |
| INFO-FLOW-005 | MUST | 06 | Procedures are validated by a subject expert: prerequisites, tools, safety warnings, time estimates, failure states and final verification. | Expert sign-off | REVIEW |

## Cycles (CYCLE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-CYCLE-001 | MUST | 05 | A circular diagram is used only for a genuinely recurring process; it marks the entry point and one consistent direction, every stage appears once, and the ring forms a single closed cycle. | Graph check | TOPO |
| INFO-CYCLE-002 | MUST | | Feedback paths appear only when real and are distinguished from backward rework; the diagram says whether stages repeat identically or evolve. | Topology audit | REVIEW |
| INFO-CYCLE-003 | SHOULD | | Labels sit outside crowded rings; the ring radius gives every adjacent pair of stages at least the stage width plus a gap ([mathematics](mathematics-and-algorithms.md), task 6). | Geometry calculation | CALC |

## Timelines (TIME)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-TIME-001 | MUST | | Dates, order, overlaps and milestones are checked against the source; planned, in progress, completed and delayed states are distinct; operational roadmaps show owners and dependencies. | Date audit | REG |
| INFO-TIME-002 | MUST | 04 | Where duration matters, positions follow a true time scale (spacing error within 2%, Chwezi value); otherwise the graphic is labelled a sequence, not to scale. | Checker output | CALC |

## Comparisons (COMP)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-COMP-001 | MUST | 04 | Criteria are defined first and applied symmetrically, with comparable denominators, periods, units and image sizes; weaknesses are not omitted. | Comparison audit | REVIEW |
| INFO-COMP-002 | MUST | | Every option has a value or a visible "N/A"; subjective judgements and the scoring basis are flagged; evidence is separated from judgement. | Comparison audit | REVIEW |

## Hierarchies (TREE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-TREE-001 | MUST | 05 | Edges represent real reporting or containment; a strict hierarchy has one root, every other node one parent, no cycle and no duplicate node name. | Graph check | TOPO |
| INFO-TREE-002 | SHOULD | | Dotted advisory lines are distinguished from solid reporting lines; deep trees offer an expandable form on small screens. | Render review | RENDER |

## Journeys and blueprints (JOURNEY)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-JOURNEY-001 | MUST | | Stages, actors, channels, actions and touchpoints are distinct; service blueprints separate frontstage and backstage; loops back appear only for real repeat engagement. | Structure audit | REVIEW |
| INFO-JOURNEY-002 | MUST | | Pain points trace to observations or research; hypothesised emotions are labelled apart from measured customer feedback. | Register | REG |

## Technical cutaways (TECH)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-TECH-001 | MUST | | Flows, valves, inputs, outputs, controls, safety boundaries and scale limits are labelled with consistent line styles; no false physical scale. | Legend audit | REVIEW |
| INFO-TECH-002 | MUST | 06 | A domain expert verifies topology, quantities, direction, naming, separation of hazardous paths and omitted components. | Expert sign-off | REVIEW |

## Education and safety (SAFE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-SAFE-001 | MUST | 06 | Medical, safety, engineering, legal and financial content has a named qualified reviewer before publication, checking contraindications, warnings, units, guidance date, applicability and the line between general education and individual advice. | Reviewer sign-off | REVIEW |
| INFO-SAFE-002 | MUST | 06 | Every instructional step matches authoritative guidance, and no hazardous or incorrect shortcut can be inferred; ambiguity on a safety-critical point stops production until resolved. | Expert review | REVIEW |
| INFO-SAFE-003 | SHOULD | | Educational graphics state the learning outcome, define terms, move from familiar to unfamiliar and end with an actionable takeaway or self-check. | Learning review | REVIEW |

## Social and mobile (SOCIAL)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-SOCIAL-001 | MUST | | Square, portrait and story variants are designed where relevant, with a strong first-frame message and critical text outside platform crops and overlays (current safe zones checked per platform). | Channel proof | RENDER |
| INFO-SOCIAL-002 | MUST | 02 | Canvas text meets the minimum CSS size times the canvas-to-slot scale ([mathematics](mathematics-and-algorithms.md), task 3) and is proofed on a real phone at normal brightness, after platform compression, without zoom. | Phone proof | RENDER |

## Web and SaaS (SAAS)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-SAAS-001 | MUST | | Live infographics use semantic HTML and accessible SVG; print and server-side PDF share the same tokens. | Build review | REVIEW |
| INFO-SAAS-002 | MUST | | Empty, loading, partial, error, restricted and stale-data states are designed; report period, filters, generation time and provenance are always shown. | State review | RENDER |

## Slides, documents and print (SLIDE, DOCX, PRINT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-SLIDE-001 | MUST | | In slides, prefer native shapes, editable charts and vector; test 16:9 projection, presenter view, PDF conversion, font substitution and cropping. | Slide proof | RENDER |
| INFO-DOCX-001 | MUST | | In DOCX, inline or deliberately anchored images that do not overlap on repagination; captions and source notes do not split from the figure; embedded resolution suffices. | Paginated render | RENDER |
| INFO-PRINT-001 | MUST | 08 | Screen PDF and press PDF are separate deliverables; the press file has the agreed trim (A2 is 420 x 594 mm portrait or 594 x 420 mm landscape), bleed (commonly 3 mm) and safe margin (at least 5-10 mm, per finishing), embedded fonts, colour profile and correct page boxes. | Preflight report | PROOF |
| INFO-PRINT-002 | MUST | 08 | Effective image resolution meets the requirement for the closest reading distance ([mathematics](mathematics-and-algorithms.md), task 2); vectors remain vectors; an actual-size proof is signed before the run. | Preflight, proof | CALC, PROOF |

## Vector and raster (VECTOR)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-VECTOR-001 | MUST | | SVG is the master for diagrams, icons and text-rich artwork: viewBox, explicit dimensions, grouped semantic layers, stable ids, `title` and `desc`, no external linked assets; PNG is an export, never the master. | SVG lint | LINT |
| INFO-VECTOR-002 | MUST | | Raster exports are made at the target pixel size and at 2x where high-density screens need it, and inspected for antialiasing, transparency and edge sharpness. | Export review | RENDER |

## Accessibility and localisation (A11Y, L10N)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-A11Y-001 | MUST | 07 | Every infographic has a short alt text (what it is and its takeaway) and a long text equivalent (structured list or table, generated from the validated data or graph where possible). | Text equivalent | AT |
| INFO-A11Y-002 | MUST | 07 | Interactive infographics have logical focus and reading order; static ones read in order when tagged (PDF) or marked up (HTML/SVG); zoom, reflow and high-contrast modes are tested. | AT walkthrough | AT |
| INFO-L10N-001 | MUST | | Translated labels are tested for expansion (with space reserved by string length), RTL direction, currency, date and number conventions and culturally appropriate illustration. | Pseudo-localised render | RENDER |

## AI agents (AGENT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-AGENT-001 | MUST | 01 | Agents never fabricate claims, citations or measurements, render photorealistic people or scenes, or generate decorative or illegible pseudo-fonts. | Agent log review | REVIEW |
| INFO-AGENT-002 | MUST | | Research, editorial, illustration, layout, QA and release are separate responsibilities, even when one agent runs them in sequence. | Workflow record | RECORD |
| INFO-AGENT-003 | MUST | | Approved copy is preserved verbatim (exact-text comparison); numbers are re-verified; agents stop and ask when a safety-critical ambiguity remains, and emit machine-readable QA findings and release evidence. | QA findings file | LINT, RECORD |

## Quality assurance (QA)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-QA-001 | MUST | 08 | Every target format in the responsive and export matrix (desktop SVG/HTML, tablet portrait and landscape, phone, social, 16:9, DOCX, screen PDF, print PDF) is rendered and inspected at actual size, and the native working file is inspected too. | Export matrix | RENDER |
| INFO-QA-002 | MUST | | Automated lint covers overflow, text under minimum size, broken source links, duplicate step numbers, orphan connectors, missing alt text, off-palette colours and missing metadata; visual regression compares each target against an approved baseline and differences are investigated, never auto-accepted. | Lint and regression report | LINT |
| INFO-QA-003 | MUST | 08 | The release declaration is signed by the content, design and technical approvers; the brief, register, calculations, design files, proofs, change log, export manifest and editable sources are archived. | Archive record | RECORD |
| INFO-QA-004 | MUST | | Weighted score at least 85 of 100 after all gates; critical findings reject, major findings block until fixed, minor findings are logged. | Scorecard | RECORD |

## Performance, privacy and governance (PERF, PRIV, GOV)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-PERF-001 | SHOULD | | Assets are compressed appropriately, below-the-fold visuals lazy-load and vectors replace large raster backgrounds where they suffice. | Asset budget | CALC |
| INFO-PRIV-001 | MUST | | Names, account identifiers, patient details and location-sensitive data in examples are redacted; export authorisation is validated and temporary files are cleaned up. | Privacy review | REVIEW |
| INFO-GOV-001 | MUST | | Projects keep `/briefs`, `/data`, `/sources`, `/design`, `/exports`, `/qa` and `/licenses`; templates carry semantic versions; approvals are retained. | Repository check | RECORD |

## Mathematics (MATH)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| INFO-MATH-001 | MUST | | Exact arithmetic for money and quantities; quantities in different units are never summed. | Fixture | CALC |
| INFO-MATH-002 | SHOULD | | Axis ticks use nice numbers (1, 2 or 5 x 10^k). | Chart review | REVIEW |
| INFO-MATH-003 | SHOULD | | Process and hierarchy diagrams are kept as data (nodes and edges) and checked by the bundled checker before layout; the long text equivalent is generated from the same data. | Checker output | TOPO |

## Evidence/currentness

External facts behind INFO-COLOUR-001/004, INFO-PRINT-001/002, INFO-A11Y-001 and INFO-L10N-001 are
recorded in [currentness-register.md](currentness-register.md); the methods behind the MATH, TYPE,
CHART, FLOW, CYCLE, TIME and SOCIAL calculations are in
[mathematics-and-algorithms.md](mathematics-and-algorithms.md).
