# UX/UI Design — Steven Branson — Extraction
**Source:** Steven Branson, *UX / UI Design: Introduction Guide to Intuitive Design and User-Friendly Experience* (2020). Tier: **Focused**.
**Coverage:** 7 chapters. Most principle lists overlap with other UX books — this extraction isolates the **distinct contributions**: the Three Paradigms of HCI design, Three Design Perspectives, persona discipline (stories, edge cases, "essential persona"), and a thorough treatment of Human Memory Limitations.

---

## 1. Three Paradigms of HCI Design (Harrison, Tatar, Sengers, 2007)

Branson's most distinctive contribution. **Use this when stakeholders disagree about what "good design" means** — they're often working in different paradigms.

### Paradigm 1: Engineering / Building
- Roots: software engineering + human factors
- Approach: take inventory of functionality → build interaction with best resources available
- Goal: user productivity, eliminate user errors
- Origin example: assembly-line work studied, deconstructed, modeled — each action described carefully → translated into requirements
- Success metric: how much the user could accomplish, summative statistical analyses
- **When dominant:** systems with complex, well-understood work domains (factory floor, accounting, ERP)

### Paradigm 2: Human Information Processing (HIP)
- Roots: psychology + human factors (cognitive theory)
- Approach: model how information is sensed and transformed in the human mind; mirror those models in computer-side processing requirements
- Defined by Card, Moran, Newell (1983); Williges (1982)
- Famous output: **"Miller's 7 ± 2"** rule — UI lists shouldn't exceed ~7 items because of working memory limits
- **When dominant:** when the goal is to fit the machine to a well-characterized cognitive task

### Paradigm 3: Design Thinking / Phenomenological
- Roots: phenomenology, sociology
- Approach: emphasize the *experiential* nature of interaction — how users *experience meaning* in the artifact
- Focuses on **emotional, social, situated, embodied** aspects
- Cares about the variety of human practices, not just the predominance — the 2% that don't fit are interesting, not statistical noise
- Key authors: Bødker & Buur (2002), McCullough (2004), Buxton (2007)
- Designing the *experience the product creates*, not just the product

### The Cockpit Voice example (canonical paradigm comparison)
The same problem of pilot-warning voice systems analyzed three ways:
1. **Engineering paradigm** — "pilots crashing too often; female voice cuts through male-dominated cockpit; reduce errors." Empirical, basic.
2. **HIP paradigm** — "female voices effectively differentiate signal from noise in the system-pilot communication channel; experiments showed that *familiar* female voices (wives, girlfriends) further improved pilot performance." Generalizable parameter (signal/noise differentiation), classifiable.
3. **Design Thinking paradigm** — "the original female voice was selected for its sultry/charming tone; this reinforced the cockpit-as-male space and became inappropriate as women became pilots and controllers." Cares about social meaning and minorities.

> **Rule:** All three paradigms have a place. They are complementary, not mutually exclusive. Even a creatively design-thinking project benefits from HIP-grounded ergonomics. Even a building paradigm project should have *some* design-thinking ideation.

---

## 2. Three Design Perspectives (orthogonal lenses)

**Environmental** — How does the system/product function in its external context? Social interaction, long-term phenomenological aspects, lifestyle integration.
**Connection** — How does the user operate the system/product? Where user and system meet — examining displays and controls, doing sensory/cognitive/physical actions.
**Emotional** — Emotional impact, social implications, aesthetics, joy of use. "An item isn't only an item; it is an encounter" (Buxton).

---

## 3. The Beauty/Usability Tradeoff (research-backed)

**The counterintuitive finding:** Users will *defend* a beautiful product even when its usability is poor.

- Encountering an ugly, cluttered website: users leave on the next click — before assessing data quality
- Already decided to buy from a specific merchant: users push through usability friction, *justifying their initial choice*
- Users actively defend their choice of beautiful-but-broken sites in studies; they emotionally rationalize past decisions
- **First impressions are easy, powerful, and based on affect — "what my body tells me to feel"**

### The "Canadian Government" example
Government built a colorful, animated site to attract new graduates. The target audience said: "Yeah, we like lots of bright color and movement — *but not when searching for a job in the Government.*"

> **Rule:** Visual appeal works as a *screening device* — it determines whether you'll evaluate content quality at all. Then context matters: same audience can flip preference depending on use-context expectations.

---

## 4. Personas — Stories at the Center

Branson's persona chapter is unusually rigorous. Critical points:

### Stories ARE the deliverable
- Personas + scenarios are skeletons; **stories are the whole human**.
- Effective design ideation requires stories: "people in a situation, with a problem, and a solution."
- Start with a **frustrating situation** to find pain. Add context, imagery, sensible setting.
- Then change the story to a *bittersweet* ending — that's the innovation story.

### "Did everything seem too easy? Did the story seem too perfect?"
> "If yes, take a 10-minute break and start over. It is easy to fall into the trap of writing tales about the users we wish we had."

### Edge cases — the Cooper rule
**Don't try to cover all edge cases in design.** Cooper's argument:
> "It can be far better to have a much smaller percentage be elated. Elated users are loyal users and powerful marketing agents."

Personas defuse "edge-cased to death" arguments:
- "What if the user wants to do X?"
- "Sorry, but Noah won't need to do X."
- "But somebody might."
- "Maybe, but we are designing for Noah, not 'somebody.'"

### The "designing for themselves" trap
- Designers naturally substitute themselves into the persona's seat.
- Personas, when **specific and richly characterized**, prevent this. The persona's name, photo, biography, and quirks make substitution impossible.

### Choosing the Essential Persona
For a sub-role with multiple candidate personas:
- The chosen primary persona's design must **at least work** for the other personas
- A design specifically for any other persona may **not** work for the primary
- **Don't average users** — a Mr. Potato Head amalgam works for none of them

### Mechanics
- First and last name (fictional, to protect real users)
- Photograph (volunteer match or non-copyrighted stock)
- Short biographies: work role, goals, main tasks, use stories, problems, concerns, biggest obstacles

### Make personas "clingy" (memorability)
UX teams have used:
- Posters, trading cards, T-shirts
- Coffee cups, screen wallpapers
- Full-size cardboard cutout figures
- Cisco even staged "action figure" dolls in dressed/posed photos in different work settings

> **Rule:** Personas need visibility and stickiness in everyone's minds — not just the design team's.

---

## 5. Human Memory Limitations (UI design rules)

The most quotable section. Use these as design constraints.

### Sensory Memory
- Visual: ~2 seconds, raw sensory data, no interpretation
- Persistence enables movie/TV continuity from individual frames
- **Few UX issues here** — it's a property of the eye/ear, not the mind

### Working Memory (the critical zone)
- Span: ~30 seconds (extendable by repetition or rehearsal)
- "Proactive interference" — intervening activities make working memory fade faster
- **Capacity: 7 ± 2 items** under specific conditions (Miller, 1956); usually less
- Items are encoded as "chunks" (Simon, 1974) — a basic memory unit gestalt
- For spoken expressions: a chunk is a word, not a phoneme
- For written: a chunk is a word or sentence, not a letter
- **Length matters**: more chunks → less time they can be held

### Phone-number example (canonical illustration)
- 7 digits = 7 chunks, exactly Miller's limit
- Found in directory → loaded → can hold ~30 seconds
- Practiced + uninterrupted → ~2 minutes
- *If* the prefix is familiar, it becomes a single chunk → easier
- **Interruption between memorization and use → look it up again**

### Chunking trick example
- `001010110111000` (15 digits) — way over working memory limit
- Group into threes: `001 010 110 111 000` → 5 chunks → fits
- `NTHEDOGSAWTHECATRU` (18 letters) → moves the N to the end → `THE DOG SAW THE CAT RUN` → 6 words → 1 sentence chunk → trivial

### Stacking (interruption cost)
- When a new situation interrupts a task, current context goes on a memory "stack"
- User stacks are **small in capacity, short in duration, defective**
- Sufficient time/interruption → the user **forgets what they were doing**
- "Pop" = closure = subjective relief from cognitive load
- **Design rule:** Break large complex tasks into a series of smaller activities, NOT one big stacked structure. Let users surface for oxygen periodically.

### Cognitive Load (Sweller, 1988, 1994)
- The load on working memory at a particular moment in time
- Cascading menus and long Web flows put users at risk of overload
- **Design rule:** Plot working-memory load over time across task steps. Whenever load reaches zero = task closure. Organize tasks to drive frequent closure.

### Long-term Memory
- Capacity: practically unlimited
- Duration: unlimited, but **retrieval not always guaranteed**
- Items move easily into long-term memory if associations exist with already-stored things
- Retrieval depends on reconstructing auxiliary encoding

### Recognition vs Recall
- **Computers are better at memory; humans at pattern recognition.**
- Design rule: let the user choose from a list of possibilities rather than recall the choice from memory
- **Recognition over recall** is the principle name
- Works best for *initial or infrequent* use (learning + remembering are operational)
- For experienced users who learn the commands, GUI selection becomes *slower than typing memorized commands* — once-helpful affordances become barriers
- Solution: **shortcuts** (Ctrl-S for Save, etc.) — physical affordances bypassing the cognitive interpretation

---

## 6. Cognitive Affordance — the four-stage discipline

Branson dissects what makes an affordance work. Each stage is a separate design problem.

### 6.1 Presence
Does the affordance exist at all?
- Show which UI object to manipulate
- Show how to manipulate
- Help users start a task
- Guide entry into form fields
- Indicate active defaults
- Indicate system states/modes/parameters
- Remind about steps the user might forget
- Avoid inappropriate choices
- Support error recovery
- Help answer questions from the system

> "Not giving cognitive affordances — labels, input field formats, icons — is what Cooper calls **clueless consent**. The user must continue without understanding the consequences."

### 6.2 Visibility / Perceivability
Can it be seen at all?
- Is it actually rendered?
- Is it occluded by another item?
- Is it small/peripheral/lost in clutter?

**Anti-pattern: "Where the hell is the sign in?"** — many websites have small, indistinct sign-in boxes mixed with other items in the far top edge. Users waste time.

**Anti-pattern: status lines** — message lines, status lines, title lines at top/bottom of screen are notoriously unnoticed. **A pop-up message near the cursor is far more noticeable than a message at the bottom.**

### 6.3 Recognizability
Once visible, can it be detected/identified without searching?
- Location (within central focus of attention)
- Contrast, size, layout complexity
- Separation from background and other UI clutter

### 6.4 Intelligibility
Once recognized, is the *content* understandable?
- Legibility (font, size, weight, color, contrast) — about *being readable*, not whether words are meaningful
- Meaning — once read, does the user understand? (This is content/copy work)

> **Design heuristic:** Walk through these four stages for every important affordance. Failure at any stage breaks the chain.

---

## 7. The "Don't make it up" rule for designers

> "Designing to 'meet the needs of users' is a vague, ill-defined idea giving designers leeway to make it up as they go."

Use research, personas, scenarios — not "what feels right to me."

---

## 8. Process iteration philosophy (Chapter 7 — "The Wheel")

Common project failure mode (named verbatim by Branson):
- 25% into the project: UX expert asked to do screen designs
- "Where is the task analysis?" "The what?"
- "OK, you have done contextual inquiry and analysis and have requirements?"
- "Oh, yes, lots of requirements documents — we pride ourselves on gathering all the essential functionality up front."
- "Do you have any use scenarios?" "Uh, well, we have a bunch of O-O use cases."

The UX expert then has to stay late and work through requirements docs to manufacture user scenarios. When delivered to actual users, **it's the first time anybody asked them about the new system.** Storm of feedback ("That's not how we do it!") and massive change requests.

> **Two outcomes:**
> - Lucky/savvy management with time → go back, do contextual inquiry, redo. Major rework but salvaged.
> - Unlucky/no time → ignore the user uproar, ship → "yet one more piece of shelfware."

> **Lifecycle wisdom:** Iteration alone is not enough. Iteration must start *early* — before requirements are frozen.

---

## 9. The "Be credible and dependable" principle

> "The only way to gain the confidence of your users is to earn it. It's hard to tell who can be trusted these days — do what you say you will do, don't over-promise and under-deliver, and don't sell somebody out to satisfy a business goal."

**Design implication:** error tolerance + reversible actions. "Undo is probably the most powerful control you can give a person — if only we had an undo button in everyday life."

---

## 10. Application to Our Engines (Phase 2 cross-reference)

- **`srs-skills`** — The Three Paradigms (Section 1) become a required scoping declaration in any SRS: which paradigm dominates? The cockpit-voice example is a stakeholder-education vignette.
- **`website-skills`** — Cognitive affordance four-stage discipline (Section 6) is a direct heuristic upgrade for design reviews. Memory limitations (Section 5) bound list lengths, menu depths, form chunking.
- **`social-media-skills`** — Recognition-over-recall (Section 5) and "first impressions are emotional" (Section 3) inform thumbnail and ad-creative decisions.
- **`~/.claude/skills/enterprise-ux-process`** — Persona discipline (Section 4) — Essential Persona, "designing for themselves" trap, "clingy" — should be required artifacts in enterprise discovery phases.
