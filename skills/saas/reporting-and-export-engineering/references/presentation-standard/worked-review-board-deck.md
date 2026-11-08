Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Presentation and Slide Deck Design Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Worked review: quarterly board deck (fictional)

All names and figures are fictional. A 20-minute quarterly board briefing for "Example Traders Ltd",
presented live in a boardroom whose farthest seat is 6 m from a screen image 1.2 m high, then
circulated as a PDF.

## Findings

| # | Finding | Rule | Gate | Evidence | Fix |
|---|---|---|---|---|---|
| 1 | Body text set at 18 pt; the venue minimum is 4.5 x 6 / 1.2 = 22.5 pt, so the back of the room could not read the drivers slide | DECK-LEGIB-001 | DECK-GATE-02 | CALC | Body raised to 24 pt; two bullets moved to the notes |
| 2 | "Sales up 12.5%" had no ledger entry; the figure came from an old draft | DECK-EVID-001/002 | DECK-GATE-01 | LEDGER | Ledger entry C-07 added from the verified snapshot |
| 3 | The revenue bar chart started at 3,000,000, making a 6% gap look like 60% | DECK-CHART-002 | DECK-GATE-07 | REVIEW | Axis from zero with nice ticks every 1,000,000 |
| 4 | Shares of revenue by branch (exact 41.4%, 33.3%, 25.3%) printed 41%, 33%, 25%, totalling 99% | DECK-MATH-002 | | CALC | Largest remainder gives the spare point to the largest fraction (0.4): 42%, 33%, 25% |
| 5 | The cover used a marketplace photograph with a faint watermark | DECK-ASSET-001, DECK-QA-002 | DECK-GATE-06, 03 | RECORD | Replaced with an owned photograph of the client's shop; licence manifest updated |
| 6 | The roadmap slide was a pasted screenshot of a spreadsheet | DECK-PPTX-001 | DECK-GATE-05 | REVIEW | Rebuilt as native shapes and a native table |
| 7 | The PDF had 23 pages for 24 slides (a hidden slide) and the KPI font fell back to a substitute | DECK-PDF-001/002 | DECK-GATE-04 | PDF | Hidden slide removed; fonts embedded; pages compared one by one |
| 8 | 34 slides planned for 20 minutes, mostly dense tables | DECK-MOTION-002 | | CALC | Cut to 18 substantive slides; tables moved to a linked appendix |
| 9 | Status shown only by red and green dots | DECK-A11Y-001, DECK-TOKEN-004 | | AT | Labels "On track", "At risk", "Blocked" with icons |
| 10 | The last slide said only "Thank you" | DECK-STORY-004 | | REVIEW | Closing ask: approve the stock-system rollout, owner, cost, start date |

## Verdict

Before fixes: BLOCKED (DECK-GATE-01 to 07 open; actionability scored 2 of 5). After fixes and a
re-run with every gate on `MEASURED` evidence, all six dimensions at 4 or 5 and the slide scorecard
averaging 92: ready for release with the editorial, design and technical sign-offs.
