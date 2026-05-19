# Content Measurement Framework

Content that is not measured is content that cannot be defended in a budget meeting. This file is the engine's working framework for measuring UX content: the three methods Metts and Welfle name in *Strategic Writing for UX*, the heuristic scorecard that operationalizes them, and the 30/60/90-day plan that turns measurement from a one-off into an organizational habit.

Derived from Metts and Welfle, *Strategic Writing for UX*, especially the chapter on direct measurement, the UX content scorecard, and the 30/60/90-day plan.

## The Three Methods

The book defines three complementary measurement methods. The engine should be able to recommend the right one for a given question.

| Method | Question it answers | Example |
|---|---|---|
| **Direct measurement** | Did the content move a number? | A/B test, conversion analytics, sentiment tracking |
| **UX research** | Why did the content do or not do what we expected? | Moderated study, interview, usability test |
| **Heuristic analysis (the UX content scorecard)** | Is the content well-formed against criteria the team agrees on? | Self- or peer-scored audit |

Treat these as a stack, not alternatives. Direct measurement reveals *what* moved. Research reveals *why*. Heuristic analysis reveals *whether the artifact is even shaped to succeed* before it ships.

## Method 1: Direct Measurement

Direct measurement is the bridge between content work and the rest of the business. The book maps content directly to engagement, conversion, and retention metrics — the same metrics product, marketing, and growth teams already report against.

Operating rules:

- For each piece of content, declare in advance which metric is its primary measure. "Onboarding screen 2 → step-2 completion rate." If you cannot pick one metric, you cannot ship the content.
- Sentiment can be a primary metric, but only when a sentiment instrument is in place (CSAT, NPS open-ended coding, support ticket categorization). Vague "user feedback" is not direct measurement.
- A change to UX content is a hypothesis, not a redesign. Run it like one.

Connect the measurement back to the two goal sets from the content-first workflow. A metric that improves only the organization's goals (e.g., conversion up but support tickets up too) is partial success at best.

## Method 2: UX Research

When direct measurement shows a number moved but does not say why, run UX research. The book's standard chain is:

1. Direct measurement raises a question.
2. Research designs a study to answer it (think-alouds, moderated tasks, diary studies).
3. The findings feed back into the content-first workflow's phase 1 — re-stating the goals if they were wrong, re-stating the content if the goals were right.

Specifically for UX content questions, prioritize study designs that capture:

- Whether participants read the words at all (eye-tracking, attention probes).
- What they thought the words meant.
- What they expected to happen next after a button label.
- Whether the words used vocabulary they recognized.

## Method 3: The UX Content Scorecard

The scorecard is the book's heuristic instrument. It is the method available without users and without analytics — and therefore the one that runs *before* shipping. The 'appee onboarding example in the book walks the scorecard end-to-end.

The scorecard has five sections, each with criteria scored as fraction of points:

1. **Goals** — what is the person trying to do, what does the organization need; goals stated briefly and contextually.
2. **Usability — Accessible** — language available; reading level; screen-reader behavior.
3. **Usability — Purposeful** — does the content serve the person's goal; does it serve the organization's goal.
4. **Usability — Concise** — visible text length; relevance of every idea included.
5. **Usability — Conversational** — familiar words; logical order.
6. **Usability — Clear** — unambiguous; help findable; **error messages help the person move forward**.

For each criterion the experience either earns the points or does not (with N/A for criteria that do not apply, like the 'appee onboarding flow with no error conditions). The total tells the team where to invest.

Operating rules for the scorecard:

- Score the artifact against the *specific* moment's goal, not the product overall.
- Run the scorecard during phase 4 of the workflow (drafting), not after launch — its job is gating.
- Comments matter as much as scores. The book's example notes "we can't be sure what the person actually wants" rather than fabricating a clean number.
- Bugs that affect scoring (e.g., the screen-reader collision saying "Button: Bookmark" ten times) get filed against engineering, not buried in the score.

## The 30/60/90-Day Plan

The book closes with a 30/60/90-day plan because measurement only matters if it becomes a recurring practice. Apply this scaffold whenever a UX content function is being established or rebuilt.

### First 30 Days — Stand Up The Instruments

- Inventory the content that already ships. Pick three to five surfaces that touch the most users.
- Build (or borrow) the voice chart from `voice-chart-construction.md`.
- Run the scorecard against those three to five surfaces. Record scores. These are the baseline.
- Identify which direct-measurement metrics already exist for those surfaces and which are missing.

### Days 30 to 60 — Run The Loop Once

- Pick one surface from the inventory and run the full content-first workflow on it: re-state goals, re-draft variants, review document, ship one change.
- Use direct measurement to test the change.
- Score the post-change artifact against the same scorecard criteria. Record the delta.

### Days 60 to 90 — Operationalize

- Convert the workflow into a repeatable process (templates, review cadence, scorecard built into design tooling).
- Set the cadence for re-scoring (quarterly is a defensible default).
- Bring the result to leadership: voice chart status, three to five before/after surfaces, direct-measurement deltas, scorecard deltas. This is the artifact that justifies the next budget cycle.

The 30/60/90 plan is also the answer to "what would a UX-content function even produce?" The deliverables across 90 days — a voice chart, a scored inventory, one ship-and-measure cycle, and a recurring cadence — are concrete.

## Choosing Metrics That Map To The Two Goal Sets

Per the workflow, every piece of content serves both organizational and personal goals. Measurement should reflect both:

| Goal type | Sample metrics |
|---|---|
| Organizational | Conversion rate, activation rate, retention, support volume reduction, ARPU |
| Personal | Task completion rate, task time, error rate, satisfaction (CSAT/NPS), perceived effort |

A change that moves only one column is suspect. Measurement that ignores one column is incomplete.

## Anti-Patterns

- Shipping content with no declared metric.
- Treating sentiment as "the users seemed happy" rather than as a measured construct.
- Using scorecard scores as a leaderboard between teams instead of as a targeted improvement tool.
- Stopping at direct measurement — the number moved but no one ran the research that explains why.
- Skipping the 30/60/90 plan because the team is "too busy to plan."
- Running the scorecard once and never again.

## How The Engine Uses This Framework

When asked to evaluate or plan content measurement:

1. Identify which of the three methods fits the question.
2. If the question is "is this content well-formed?", run the scorecard.
3. If the question is "did the content work?", set up direct measurement with a declared metric tied to both goal sets.
4. If the question is "why did the number move (or not)?", design a UX research study.
5. If the team is asking "where do we even start?", recommend the 30/60/90 plan.

## Source Grounding

- The three measurement methods named in Chapter 6: direct measurement, UX research, and heuristic analysis.
- The UX content scorecard's section structure: Goals, Accessible, Purposeful, Concise, Conversational, Clear — each scored as fractional points.
- 'appee onboarding worked example: scorecard fills, including N/A for error criteria and comments where data is uncertain.
- Scorecard criterion that error messages help the person move forward when they hit the end or edge of the experience.
- The 30/60/90-day plan from Chapter 8 used here as the operationalization scaffold.
- Direct measurement tied to engagement, conversion, retention, and sentiment as named drivers for content work.
