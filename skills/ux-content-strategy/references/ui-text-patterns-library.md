# UI Text Patterns Library

This file is the working catalog the engine uses when asked to draft a specific kind of UI string. It is organized by element — title, button, description, control, error, confirmation, empty state, help text — because that is how copy gets requested in real product work. Each pattern names its job, the rules that make it succeed, and the failure modes the source books document.

Derived from Metts and Welfle, *Strategic Writing for UX*, and Wroblewski, *Web Form Design*.

## How To Use The Library

For each element type below:

- **Job** — what this string is doing for the person and the organization at this moment.
- **Rules** — the constraints derived from the source books. These are non-negotiable starting points.
- **Anti-patterns** — the specific ways this element fails in shipped products.
- **Voice-chart hook** — which row of the voice chart most controls this element.

The library does not provide finished strings because finished strings depend on the product's voice chart. It provides the gates a string must pass to be acceptable.

## Titles

**Job.** Tell the person, in a glance, where they are and what this screen is about. Titles are usually scanned, not read.

**Rules.**

- One idea per title. If two ideas are required, one is a title and the other is a description.
- Titles do *not* end with a period unless the voice chart says so. Most voice charts treat titles as labels, not sentences.
- A title shorter than the screen's reading level is a feature.

**Anti-patterns.**

- Titles that restate the company name (the user already knows where they are).
- Marketing slogans masquerading as titles ("Welcome to your new best friend"). The voice chart's *Concepts* row is the place for ideas like this; the title is not.

**Voice-chart hook.** Concepts and Capitalization.

## Buttons

**Job.** Tell the person what will happen when they tap this. Buttons promise a result and the next screen has to honor that promise.

**Rules.**

- **Three or fewer words.** This is the book's stated criterion in the UX content scorecard, and it survives almost every voice chart.
- The label names the action *that will happen*, not the abstract category. "Pay $42.18" beats "Continue" because Continue does not warn the person their card is about to be charged.
- The button does not lie about what comes next. Metts and Welfle's example: a "Next" or "Continue" button followed by a charge confirmation is a misleading button — the user did not reasonably expect to commit at that step.

**Anti-patterns.**

- Generic "Next" / "Continue" / "OK" on screens that change state in ways the user did not consent to.
- Two primary buttons of equal weight (the page now has no clear primary action — see the primary/secondary distinction in *Web Form Design*).
- Screen-reader collisions: ten buttons all labeled "Bookmark" so the screen reader says "Button: Bookmark" ten times. Each button must be distinguishable when read aloud in isolation.

**Voice-chart hook.** Vocabulary and Verbosity.

## Descriptions And Body Copy

**Job.** Fill the gap between title and action. Body copy explains, qualifies, sets expectation.

**Rules.**

- Reading level should match or be lower than the audience's. Metts and Welfle suggest pasting body text into reading-level calculators after appending periods to standalone phrases, then taking the median grade level.
- Sentences should be shorter than the longest the voice chart's Grammar row permits.
- Body copy is the place where the voice chart's *Concepts* most often surface, because there is room for them.

**Anti-patterns.**

- Body that re-says the title in different words.
- Body that contains the action word the button uses but in a sentence form ("Click 'Continue' to continue"). Body copy and button labels should not duplicate.

## Controls (Toggles, Checkboxes, Radio Groups)

**Job.** Let the person change a setting and immediately see or hear that the change took. The book emphasizes that interaction designers usually own the control, but the words determine whether the person *expects* the right thing to happen.

**Rules.**

- The label names the state in the *on* direction ("Email me weekly") so the toggle's on-position is unambiguous.
- Each control change is accompanied by a perceivable confirmation — a visible state change *and* the screen reader saying "checked" or equivalent.
- For substantial actions (committing money, deleting data), control changes alone are not enough — confirmation copy follows.

**Anti-patterns.**

- Double-negative labels ("Disable not-receiving emails").
- Labels that describe what the *off* state does — toggling becomes a guessing game.

## Errors

**Job.** Help the person move forward when they hit the end or edge of the experience. The book's scorecard criterion is exactly this: error messages help the person move forward.

**Rules.**

- Tell the person what to do, not what went wrong at the technical layer.
- The error must be in the same voice as the rest of the experience — errors are where voice most often slips into engineer-speak.
- If the same input has predictable error states, *Web Form Design* recommends preventing them entirely with input types that have no error states (drop-downs, smart defaults) before resorting to messages.

**Anti-patterns.**

- "An unexpected error occurred." The user cannot act on this.
- Stack traces or codes with no human-readable instruction.
- Errors that blame the user ("You did not enter a valid email"). Restate as: what is needed and what would satisfy it.

(Full taxonomy of errors lives in `error-state-taxonomy-and-recovery.md`.)

## Confirmations

**Job.** Close the loop after a substantial action so the person knows the action took.

**Rules.**

- Confirmation explicitly names what just happened, not just "Done."
- For irreversible or financial actions, the confirmation also tells the person what to expect next (when the email arrives, when the charge posts).
- A confirmation that does not match the button label that triggered it is a content bug. If the button said "Pay $42.18," the confirmation should reference $42.18.

**Anti-patterns.**

- Modal confirmations that disappear before they can be read.
- "Success!" with no description of what succeeded.

## Empty States

**Job.** Explain why the person sees nothing, and tell them how to make something appear.

**Rules.**

- Name the state ("No saved items yet") and the next action ("Save a recipe to see it here").
- The empty state is a *first-run* surface for many users — it teaches the feature. Treat it like onboarding copy.

**Anti-patterns.**

- "No data" / "Empty." This is technically true and operationally useless.
- Empty states that show a generic illustration and no instruction.

## Help Text

**Job.** Pre-empt confusion at the point of confusion. *Web Form Design* limits this to specific situations: when the input has constraints the user cannot guess, when the data is unfamiliar, when the format is non-obvious.

**Rules.**

- Help text appears beside or below the field it serves, not behind a tooltip the user has to discover.
- If the help text exists to tell people how many digits a zip code has, the field width is wrong. Fix the field; do not write help text for it.
- Help text is not a place for marketing reassurance.

**Anti-patterns.**

- "Required field" as help text — use the required indicator instead.
- Help text that contradicts the placeholder or the label.

## Form Labels

**Job.** Tell the person what each field wants. Labels are the most-read text in any form.

**Rules.**

- Labels are visible and persistent, not just placeholders. Placeholders disappear when the user types and become useless for re-checking.
- Label position (top, right, left) is a layout decision with measurable completion-time consequences (see `form-completion-gates.md`).
- Required vs. optional indicators must be consistent across the entire form. *Web Form Design*'s pop quiz makes the point: an asterisk universally means "required" — using it for "optional" breaks user expectation.

**Anti-patterns.**

- Mixing required and optional indication conventions inside the same form.
- Labels written in marketing voice when the rest of the form is utilitarian.

## Notifications And Transactional Messages

**Job.** Reach the person when they are not in the product. Subject lines, push titles, and the first line are the only parts most people read.

**Rules.**

- Front-load the actionable information.
- The voice chart still applies — push notifications are the place voice most often gets diluted because they are written by a different team.

**Anti-patterns.**

- "Important update from us." This says nothing.
- Reusing the same template for marketing and transactional pushes — they have different jobs.

## Voice-Chart-First Drafting

For *every* element above, the engine should:

1. Identify the element type.
2. Apply the rules in this file as gates — fail-closed if any rule is violated.
3. Apply the voice chart's row that governs that element.
4. Produce multiple variants per the content-first workflow's phase 3.

## Source Grounding

- Button criterion of three or fewer words from the UX content scorecard.
- Misleading-button example: "Next" / "Continue" used for a payment commit step in *Strategic Writing for UX*.
- Screen-reader bug example: ten buttons reading "Button: Bookmark" undermining accessibility scoring.
- Reading-level calculator workflow for evaluating body copy.
- *Web Form Design*'s preference for input types with no error states (drop-downs, smart defaults) over error messages.
- The asterisk pop quiz from *Web Form Design* establishing the universal "required" expectation and the Hogan counter-example using it for "optional."
- Help-text trigger conditions from *Web Form Design* — use only when constraints, unfamiliar data, or non-obvious formats demand it.
