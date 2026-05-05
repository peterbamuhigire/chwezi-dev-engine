# Product Narrative Arcs

A product is a sequence of moments the user moves through over time. Treating that sequence as a narrative — with characters, structure, and emotional shape — surfaces design problems that flat task analysis misses. This file is the engine's working framework for product narrative: who the characters are, which structural model fits which kind of product flow, and how plot points organize a user journey.

Derived from Anna Dahlström, *Storytelling in Design*.

## Why Narrative At All

Storytelling has been a respected and effective communication form since at least 1380 (the *Oxford English Dictionary* date for "once upon a time"). Stories work because they make us see, move us emotionally and into action, and help us process and remember facts. Responding to and telling stories is part of what makes us human.

Product design borrows from storytelling for the same reasons: a flow with narrative shape is more memorable, more emotionally legible, and more actionable than one without. Narrative is not decoration — it is structure.

## The Cast: Who Are The Characters

Dahlström adapts traditional storytelling roles to product design. The engine should be able to identify the cast for any product flow it is asked to evaluate.

### The Protagonist Is Always The User

The user is the protagonist and the hero of the product or service. *Always*. Even when the brand is a strong character — for chatbots, voice UIs, products with personalities — the brand should never be the hero. The user is who the story is about, and the user is why the product exists.

If the engine is reviewing a flow where the brand is doing more talking than the user is doing acting, the cast is wrong.

Within the protagonist role:

- **Primary user** — the person the flow is designed for.
- **Secondary user** — present in the flow but not the focal user.
- **Tertiary user** — adjacent to the flow.

### Supporting Characters

People closest to the protagonist who play a big part in the protagonist's life — often appearing in only one part of the experience. In product terms, these are roles like the friend who shares a referral, the colleague tagged in a doc, the family member added to an account.

### The Antagonist

Traditional storytelling's antagonist wants things to go badly for the protagonist. Product design often skips this role and designs only for best-case scenarios — Dahlström flags this as a missed opportunity. Three types:

- **Internal antagonists** — doubt, fatigue, distraction, self-imposed friction.
- **External direct antagonists** — competitors, scammers, people who actively work against the user.
- **External indirect antagonists** — circumstances and systems that block the user without intent (network failures, regulatory friction, time pressure).

The antagonist isn't always visible, physical, or digital, but is *present by putting obstacles in the way of what the user is trying to accomplish*. Designing for the antagonist means asking, at every step, what could oppose the protagonist here.

### The Brand And Devices

The brand is increasingly a character — especially in voice UIs and chatbots. As soon as something is given a voice, people project human traits onto it; the design must commit to a personality whether you intended one or not. Devices and technology often play the role of *assistant*, *companion*, or *extension of the user*, as in Iron Man or Her — supporting the protagonist's quest, not taking center stage.

## The Structural Models

Dahlström uses several structural models from drama. The engine should be able to pick the model that fits the flow it is shaping.

### Aristotle's Three-Act Structure

The base case. Setup, confrontation, resolution. Maps cleanly to:

- **Act 1 — Setup.** The user arrives, learns what the product is, decides to engage. Onboarding lives here.
- **Act 2 — Confrontation.** The user does the work the product is for, encountering obstacles (the antagonists). The bulk of product use lives here.
- **Act 3 — Resolution.** Outcome, conclusion, success or failure. Confirmation, summary, hand-off, or churn.

When a product flow is one-sitting (a sign-up, a checkout, a single-task tool), three-act is usually the right model.

### Variations On The Three-Act Structure

The book covers variations — five-act, hero's-journey, in medias res — that fit longer arcs. Some product flows benefit from these:

- **Five-act** for products with extended usage arcs and explicit climaxes (subscription products, fitness apps with milestones).
- **Hero's-journey shape** for products where the user is meant to be transformed by use (learning products, behavior-change apps).
- **In medias res** when re-engagement starts mid-action (the user returns to a saved state, not a fresh start).

### Freytag's Pyramid

Adds rising action, climax, falling action, denouement. Useful when the design needs to deliberately shape emotional intensity — a release flow with anticipation, peak, and aftermath.

### Aristotle's Seven Golden Rules

Dahlström references Aristotle's seven golden rules of storytelling as a checklist of attributes a story (or product flow) should have. Apply them as gates: does this flow have a clear central character with a clear purpose, a beginning-middle-end, dramatic tension, etc.?

## Plot Points: The Joints Of The Arc

Plot points are the structural moments where the flow turns. In product design, plot points are the moments that change the user's relationship to the product:

- The moment they decide to sign up.
- The moment they first complete the core action.
- The moment they invite someone else.
- The moment they would have churned but didn't.
- The moment they consider canceling.

Designing plot points means designing those moments deliberately — not letting them happen by accident. Each plot point deserves explicit copy, explicit interaction, and explicit measurement.

## How To Use Dramaturgy To Define Narrative Structure

Dahlström's process for using dramaturgy and plot points to shape product experiences:

1. **Identify the arc** — what is the full sequence the user moves through over time, including outside the product?
2. **Pick the structural model** — three-act, five-act, hero's-journey — based on the arc's length and emotional shape.
3. **Place plot points** — the moments where the user's relationship to the product changes.
4. **Identify the antagonists at each plot point** — internal, direct external, indirect external.
5. **Decide the emotional register** at each plot point.
6. **Specify the supporting cast** — who else appears, who else is referenced.

The output is a narrative spec that lives alongside the user-flow diagram. It tells the team what the user is *feeling* and *deciding*, not just what they are clicking.

## Main Plots And Subplots In User Journeys

For longer user journeys, the book introduces main plots and subplots. The main plot is the arc of the core value proposition — the reason the user is here. Subplots are the secondary arcs that braid through it: the social subplot (sharing, inviting), the mastery subplot (learning the advanced feature), the financial subplot (upgrading, paying), the failure-and-recovery subplot.

Operating rules:

- The main plot must always be legible. If the user cannot tell what story they are in, the subplots are noise.
- Subplots that run too long without intersecting the main plot become abandoned features.
- The product's analytics should reveal which subplots actually exist, not just the ones the team intended.

## Emotion Across The Arc

Emotion is not a polish layer — it is structural. Dahlström's emotion chapter argues that great storytelling and great product design both consciously evoke emotion, and that emotion correlates with what the user remembers and acts on.

For each plot point, the engine should specify the *intended* emotion: anticipation, relief, confidence, delight, accomplishment. Then the team can ask whether the design (copy, motion, sound, timing) actually delivers it. This is the emotional spec, parallel to the structural spec.

Different levels of needs (the book references Maslow-style frames) call for different emotional registers — basic need flows (banking, health) call for confidence and trust; aspirational flows call for delight and surprise.

## Anti-Patterns

- Treating the brand as the protagonist.
- Designing only the best case (no antagonists in the model).
- Flat flows with no plot points — every screen feels equally important, so none is.
- Subplots that crowd out the main plot.
- Emotional registers that mismatch the level of need (cheery copy in a banking-error state, somber copy in a celebratory state).
- One-sitting structural models forced onto multi-month arcs, or vice versa.

## How The Engine Uses Narrative Models

When asked to evaluate or design a product flow:

1. Identify the protagonist and confirm the user — not the brand — is in that role.
2. Identify the antagonists at each step (internal, direct, indirect).
3. Pick a structural model based on flow length and emotional shape.
4. Place plot points and assign each an intended emotion.
5. Distinguish main plot from subplots.
6. Recommend copy and interaction work for the highest-leverage plot point first.

The narrative spec complements, not replaces, the user flow. Both are required.

## Source Grounding

- The user as protagonist and hero, with the brand never the hero — even in voice UIs and chatbot products.
- Antagonist taxonomy: internal antagonists (doubt and similar), external direct antagonists, external indirect antagonists; the observation that product design often designs only for best cases.
- Aristotle's three-act structure as the base structural model and the existence of variations including five-act, hero's-journey shape, and in medias res.
- Freytag's pyramid as a tool for shaping emotional intensity.
- Aristotle's seven golden rules of storytelling as an attribute checklist.
- Plot points as structural turning moments and the dramaturgy-based process for defining the narrative structure of product experiences.
- Main plots and subplots applied to user journeys and flows; emotion treated as structural rather than decorative, including the levels-of-needs frame.
