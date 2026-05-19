# Content-First Design Workflow

The default workflow ships a layout with lorem ipsum, hands it to a writer, and discovers the words won't fit. The content-first workflow inverts that: decide what the experience needs to *say and do* for the person and the organization, then let the layout follow. This file describes that workflow as Metts and Welfle frame it in *Strategic Writing for UX* — anchored in the goals of the people *and* the organization, drafted on top of real screens, and reviewed asynchronously by the broader team.

Derived from Metts and Welfle, *Strategic Writing for UX*.

## Why "Content First" — The Two Sets Of Goals

The strategic purpose of UX content is to meet two sets of goals at once: the goals of the *organization* responsible for the experience, and the goals of the *people* using it. Content that serves only the organization extracts value but fails the user; content that serves only the user fails to justify its place in the product. The workflow below exists to keep both sets visible at every step.

Before any content is drafted, the workflow forces the team to write down:

1. What the person is trying to do at this moment in the experience.
2. What the organization needs to get out of this same moment.
3. Where, on the virtuous cycle from awareness to retention, this moment falls — because content type changes by phase (marketing copy attracts, first-run copy onboards, transactional copy sustains).

If those three answers are not on paper, the workflow has not started yet.

## The Phases Of The Workflow

The workflow has six phases that loop. They are not waterfall — drafting feeds back into goal-setting when a draft reveals the goal was wrong.

1. Goals and audience for this specific moment.
2. Conversational design (the dialogue, before the layout).
3. First ideas (imagining widely).
4. Drafting on screenshots or in design files.
5. Review document with the larger team.
6. Measurement against goals.

Phase 6 returns to phase 1 when a measurement shows a gap.

## Phase 1: Lock The Moment Before Writing The Words

Pick *one* moment — one screen, one notification, one error condition — and write its goals contextually and briefly. The book's UX content scorecard begins exactly this way: list what the person is trying to do and what the organization wants out of this experience. Brief is the keyword. A goal that takes a paragraph is a paragraph someone will skip.

Anti-pattern: writing copy for "the onboarding flow." There is no such single artifact. Each screen in onboarding has its own goal pair, and copy that aggregates them produces marketing slush.

## Phase 2: Conversational Design Before Layout

Treat the screen as a turn in a conversation. What does the experience say? What does the person reasonably say back? The conversational sequence comes before any wireframe because layout decisions made before the dialogue is settled get rebuilt later.

This phase produces a script-like artifact: speaker, line, expected response. If the script does not make sense out loud, no amount of typography is going to rescue it on screen.

## Phase 3: First Ideas — Imagine Across The Voice Chart

With the script in hand, generate multiple options by deliberately *varying along the voice chart's principles*. If the product has three principles, write a version that leans on each, and at least one version that exploits the tension between two. The point is not to ship all of them — it is to surface what each principle costs and what it earns.

A common shortcut here is to write one option, like it, and call it done. The book's process treats that as a failure of imagination. The voice chart is the tool that makes generating *different* options cheap.

## Phase 4: Drafting On Screenshots Or In Design Files

There are two practical drafting modes:

- **Drafting on screenshots.** When the words live as pixels in a screenshot, they are not editable. Pull the image into Sketch, Figma, PowerPoint, Slides, or Paint, lay a text box over the existing text, type the same text in, then duplicate the layered group and edit the text in each copy. You end up with several stacked editable variants of the same screen, each one a candidate.
- **Drafting in design files.** The same idea, but inside the team's actual design tool. The mechanic is identical: get to the text box, edit, save versioned variants of the screen.

The deliverable from this phase is *several candidate screens*, not one. If only one option exists, the writer is not done.

## Phase 5: The Review Document — Bridging Tight Team And Wider Org

Drafting is collaborative within a small team; review needs to reach engineers, legal, support, leadership, localization, and anyone else whose work depends on the words. The review document bridges the gap.

Structure the review document with:

- Context at the top: which moment this is, which goals it serves, any constraints (character limits, legal requirements, localization concerns).
- For each screen: an image of the screen on one side, an editable and commentable list of the text on the other, and space for alternates the team is still considering.
- A clear deadline ("review before noon, March 25") and a clear list of reviewers.

The output of review is a final set of text the engineers can copy-paste into code without retyping. Retyping is where typos get reintroduced — eliminate it.

## Phase 6: Measure And Loop

Once shipped, the content is a hypothesis to be tested against the goals locked in phase 1. The book defines three measurement methods: direct measurement (engagement, conversion, retention, sentiment), UX research, and heuristic analysis using the UX content scorecard. If a measurement shows the content is not meeting the phase-1 goals, the workflow returns to phase 1 — *not* to phase 4. Re-drafting words against the same flawed goal produces the same flawed result faster.

## Where The Workflow Slots Into Existing Org Processes

Three integration points:

1. **Sprint planning.** Treat content goals as user stories with acceptance criteria taken from the scorecard. "Onboarding screen 2 scores at least 7/10 on Conversational" is a measurable acceptance criterion; "the copy is friendly" is not.
2. **Design handoff.** No design ships to engineering with placeholder copy. The review document outcome is the source of truth.
3. **Post-launch.** The 30/60/90-day plan from the measurement framework owns phase 6 — content is reviewed, not abandoned, after launch.

## Workflow Anti-Patterns

- **Lorem ipsum in design files.** It commits the team to a layout that may not survive real copy. Draft real text, even rough, before the layout is locked.
- **Single-option drafts.** Skipping phase 3's variation makes the voice chart inert.
- **Synchronous review meetings as the primary mechanism.** The book's approach is asynchronous review in a document, with people commenting in their own time. Meetings are reserved for unresolved threads.
- **Skipping the goals row.** The scorecard begins with goals for a reason — every later judgment depends on whether the content served them.
- **Drafting without screenshots.** Words evaluated outside their visual context will be wrong about length, hierarchy, and adjacent labels.

## How The Engine Uses This Workflow

When asked to produce copy, the engine should walk the phases visibly:

1. Restate the moment and the two goal sets.
2. Draft a brief conversational script.
3. Produce *multiple* options derived from the voice chart's principles.
4. Present them on or beside the screen image they refer to.
5. Recommend a primary and explain what each alternative trades off.
6. Specify the measurement that would confirm or falsify the recommendation.

Skipping any phase is a tell that the engine is producing copy without strategy.

## Source Grounding

- The two goal sets — organization and people — used as the strategic frame for all UX content.
- The virtuous cycle of attraction, first-run, and ongoing use, with content type changing by phase.
- Conversational design exercise as the step that precedes layout decisions.
- Drafting on screenshots using a text-box-and-rectangle technique inside Sketch, Figma, PowerPoint, Slides, or Paint to produce stacked editable variants.
- The content review document as an asynchronous bridge between core team and wider reviewers, with copy-pasteable final text.
- Three measurement methods named in Chapter 6: direct measurement, UX research, and heuristic analysis with the UX content scorecard.
