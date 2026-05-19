# Voice Chart Construction

A voice chart is what lets a whole organization produce text in one voice without a single owner gating every word. Without it, you do not have a voice — you have whichever writer happened to draft the screen. This reference rebuilds the chart the way Metts and Welfle teach it in *Strategic Writing for UX*: as a grid of product principles across the top and six aspects of voice down the side.

Derived from Metts and Welfle, *Strategic Writing for UX*, especially the Sturgeon Club, 'appee, and TAPP voice charts.

## What The Chart Is And What It Replaces

A voice chart replaces three failure modes:

1. The lone writer who cannot scale, so the rest of the company copy-and-pastes inconsistently while waiting for review.
2. The brand deck of personality adjectives ("friendly, smart, bold") that cannot be applied to a single button label.
3. The endless re-litigation of the same punctuation and capitalization bugs in JIRA.

The chart is a tool for *anybody at the company* to make a defensible content decision, including engineers writing the next error string at 11pm.

## Structure: Columns Are Principles, Rows Are Aspects

The grid has two axes:

- **Columns** are the **product principles** — what the experience is trying to be to the people using it. Three is typical. The Sturgeon Club uses *Imbued with Elegance*, *Build Camaraderie*, *Connect to Tradition*. 'appee uses *Playful*, *Insightful*, *Surprising*. TAPP uses *Efficient*, *Trustworthy*, *Accessible*.
- **Rows** are the **six aspects of voice**: Concepts, Vocabulary, Verbosity, Grammar, Punctuation, Capitalization.

Every cell is the answer to: "When we are expressing *this principle*, what does *this aspect* look like?"

If a cell is blank, you have not yet decided. If a cell is identical across every column, that aspect is not actually doing voice work for you and the row can be omitted.

## Step 1: Set The Product Principles First

Principles are the foundation. Without them the rows have nothing to vary against. Pick principles that:

- Describe what the experience is to the *person*, not what the company believes about itself.
- Are different enough that one piece of copy could plausibly satisfy one and violate another. (If "Friendly" and "Welcoming" are two of your three principles, collapse them.)
- Survive translation into a button label. "Imbued with Elegance" must be able to argue for "Reserve a Table" over "Book Now."

Get these signed off at the highest level you can reach, the way the book recommends ratifying the chart with a ceremony so the team knows it is authoritative.

## Step 2: Fill The Concepts Row

Concepts are the *ideas or topics* the organization wants to surface at any open opportunity, even when those ideas are not the literal task on screen. They are not slogans and they do not specify words. They name the territory the experience wants to be associated with in the user's life.

Examples of concept-level decisions:

- The Sturgeon Club concepts under *Camaraderie* center on shared meals, recurring events, and members by name — so when there is room to say something extra, those are the ideas that get said.
- 'appee concepts under *Surprising* include coincidences and small delights — when image data is mentioned, mention it as a coincidence, not as analytics.
- TAPP under *Accessible* foregrounds availability and readiness — describe what *is* available, not what is broken.

If your concepts row reads like a values poster, rewrite it. It should read like editorial guidance.

## Step 3: Vocabulary — Only The Words That Carry The Voice

The Vocabulary row is *not* a glossary. It is the short list of words that are so identity-bearing that their presence (or absence) tells you which experience you are inside. TAPP's Accessible column, for instance, tells the team to never use "disabled" or "invalid" and to prefer "available," "easy," or "ready." That one decision excludes a category of phrasing that would otherwise sneak in.

Keep this row short. If a word is just normal English, it does not belong here. If a word would be a fight in a review, it belongs here.

If a principle does not need vocabulary policing, leave that cell blank — Metts and Welfle explicitly say to omit the row where it does no work.

## Step 4: Verbosity — How Much Air The Voice Takes

Verbosity is the rule for how much copy a principle wants. TAPP's Verbosity row tells writers to avoid unnecessary adjectives or adverbs except when they are required for accuracy or to ensure the person succeeds. That is utilitarian by design — it matches what a transit system is for.

When you write this row, take a position on:

- Whether the principle wants tight or expansive sentences.
- Whether modifiers (adjectives, adverbs) are earned or deleted by default.
- Whether the principle ever permits two sentences where one would do, and on what justification (accuracy, success, accessibility, etc.).

## Step 5: Grammar — Tense, Mood, Sentence Shape

Grammar carries voice as much as vocabulary does. The Sturgeon Club's grammar row uses complex sentence structure and passive voice when speaking *about the club* — because that grammar is what feels formal — but switches to simple grammar when speaking *about people*, because that is what feels intimate. 'appee, in contrast, prefers present and future tense and is willing to ship phrases instead of complete sentences.

For each column, decide:

- Tense (past / present / future preferences).
- Voice (active vs. passive — and when each is correct, not just preferred).
- Sentence completeness (are fragments allowed, where, why).
- Sentence complexity.

## Step 6: Punctuation And Capitalization

Per the book, these are the most frequent UX-text bugs filed in real organizations. Recording the decision in the chart is the entire point — the chart exists so future arguments about exclamation marks are settled by reference instead of by debate.

Decide explicitly:

- Which marks are forbidden (e.g. TAPP avoids semicolons, dashes, parentheticals, and question marks; the Sturgeon Club drops exclamation marks and tildes).
- Which marks carry meaning (commas vs. periods, ellipses, em dashes if any).
- What is capitalized for hierarchy (titles vs. buttons vs. body), and what is capitalized for relationships and roles (the Sturgeon Club capitalizes Member, President, etc.).

## Step 7: Look For Productive Tensions

A finished chart will contain internal tensions. 'appee's chart, for instance, asks for non-metaphoric description *and* for unpredictability *and* for fewer words than necessary — three rules that pull against each other. This is a feature, not a bug. The tensions are what force a writer to imagine multiple solutions for the same screen and choose the one that best balances the principles.

When a screen feels off, do not patch the screen — locate which two principles are pulling against each other and decide which one wins this time. Record the rationale in the review document so the next person inherits the precedent.

## Step 8: Ratify And Operationalize

The chart only works if the team treats it as authoritative. Three operational moves:

1. **High-level sign-off, with a ceremony.** Walk decision-makers through the chart cell by cell. Show before-and-after copy where alignment changed the result. Commit to measuring the chart's effect on engagement, sentiment, or other metrics from the measurement framework.
2. **Apply it during review, not after.** Every content review document references the chart by column and row, not by adjective. "This violates *Trustworthy / Punctuation*" beats "this feels off."
3. **Re-edit the chart when the product changes.** Principles drift when the product expands. Re-run Step 1 with new samples annually or when the product's audience materially changes.

## Anti-Patterns

- **Aspect rows that all say the same thing.** If every column's Grammar cell says "use simple sentences," Grammar is not doing voice work — your principles are too similar or your row is being padded.
- **Adjective-only cells.** "Friendly, warm, approachable" is not a voice instruction. Replace with a rule that can be applied to a single sentence.
- **A chart with no forbidden words or marks.** The chart's value is in what it excludes. A chart that only adds is unfalsifiable.
- **One person writing the chart in private.** It will not survive contact with the org. Build it with the team that has to apply it.

## How The Engine Uses The Chart

When asked to draft or critique copy, the engine should:

1. Identify which product principle most applies to the moment (welcome, error, confirmation, etc.).
2. Read down that column for Concepts, Vocabulary, Verbosity, Grammar, Punctuation, Capitalization.
3. Where two principles compete for the same screen, name the tension and choose deliberately.
4. Cite the column and row in the rationale.

Without these citations, the engine is producing opinion, not voice.

## Source Grounding

- Voice chart structure: product principles as columns, six aspects (concepts, vocabulary, verbosity, grammar, punctuation, capitalization) as rows.
- Three worked examples used throughout the book: The Sturgeon Club, 'appee, TAPP Transit System, each with its own three principles.
- Concepts row defined as the ideas the organization wants to emphasize at any open opportunity, distinct from words or slogans.
- TAPP's Accessible vocabulary rule excluding "disabled" and "invalid" in favor of "available," "easy," "ready."
- Ratification advice: high-level sign-off and ceremony to make the chart authoritative.
- Productive tensions inside the chart used as a generative tool for imagining multiple solutions.
