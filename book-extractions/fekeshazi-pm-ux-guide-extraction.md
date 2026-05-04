# Product Managers' Guide to UX Design — Zoltan Fekeshazi (UX Studio) — Extraction
**Source:** Zoltan Fekeshazi, *Product Managers' Guide to UX Design* (UX Studio, ~2017). Tier: **Focused**.
**Coverage:** A short PM-facing handbook (~32 pages) covering 5 things managers should know, the UX process, communication tools, team-building, and case studies. The unique value is **practical PM-side wisdom** rare in design-craft books.

---

## 1. The 5 + 1 Things Managers Should Know About Design

This is the canonical opener — useful as a stakeholder-education talk track.

### 1. Design is not just a pretty skin
> "Design is not just what it looks like and feels like. Design is how it works." — Steve Jobs

A good UX designer can answer questions far beyond aesthetics: What will the user see first vs later? In what direction are we drawing her attention? Why will she remember us? "The nice outlook is just the tip of the iceberg."

### 2. Good design improves understanding
- Most who try a SaaS product but don't subscribe do so because they don't understand how it works.
- **At first use, you have a maximum of 5–10 minutes** to give users answers.
- **Tutorials are futile attempts** — no one watches them. The interface itself must explain how it works.

### 3. Design is about experimentation
- Jony Ive created **561 prototypes** before debuting the final Leica M camera design.
- "If one of the world's leading designers has to do so much experimenting, how could you expect anyone to create something perfect at once?"

### 4. Good design is teamwork — and you have to take part
- "Many people believe that when they have something to be designed, they just make a deal with a designer and only meet again when the designer is handing over a wonderfully completed design. Bad news: it doesn't work like this."
- The designer needs **constant feedback** to proceed in the right direction.
- "No one knows your business better than you do." Active client/PM participation is non-negotiable.

### 5. Design must be measured and tested
- Research is an inherent part of UX design.
- Test methods cited: user tests, fieldwork, A/B tests, interviews, remote tests, **guerrilla tests, 5-second tests, ghetto tests, grandma tests**.
- "Without applying these, you whistle in the dark."

### +1: Design is not a project — it is an ongoing process
- "There is no such thing as a finished design."
- New functions arise; old functions need improvement.
- UX Studio works in subscription-based engagements for this reason.
- "A developer team without a design team is a few bricks short of a load."

---

## 2. The 7-Step UX Design Process (UX Studio's house process)

Lean and explicit. Use as a default project template.

1. **Personas and Analytics** — who we design for; how people use the product; demographic + behavioral data
2. **User Journeys** — the big picture; "design better experience by thinking in processes, instead of screens"
3. **Wireframes and Prototypes** — layout, element placement, proportions, copy, navigation; clickable for testing
4. **User Testing** — real users; videos + written report listing problems and suggestions; **iterate on the prototype until everything works well** before committing dev time
5. **Look & Feel Drafts** — explore styles based on target group; collection of inspirations + 2–3 style drafts on a specific wireframe screen
6. **Detailed Designs** — start with one screen, then all screens and states; PSD files, fonts, icons, style guide, documentation for developers
7. **A/B Testing** — recommend variants of important texts (value prop, CTA) and design solutions to test; optimize for highest conversion / task-completion rate

### Agile delivery model
- Delegate **one designer + one UX researcher** to the product
- **Week-long design sprints**
- Beginning of each week: design
- Then: user tests / research
- Output: **tested design inputs that developers can build in their next sprint**

---

## 3. Four Ways UX Helps Foster Better Communication & Collaboration

PM-focused — the "bridge constructor" between teams with different languages and interests.

### 3.1 Workshops (kickoff)
- Persona, customer journey, look-and-feel workshops
- Attendance: **everyone with even a tiny responsibility for the product** — PM, marketer, developer, designer, business strategy
- Purpose: align the picture of product/features/goals; explain across functions

### 3.2 Weekly design meetings
- Attended by one rep from each department (UX, dev, business, marketing)
- Cover: previous week's work, next week's plan, challenges, difficulties
- **Cap: 5 people max, 90 minutes max** (UX Studio rule)

### 3.3 Wireframes (clickable) replace specification documents
> "A good wireframe worth more than thousand pages."
- "No one likes to read." Specification documents create misunderstandings.
- Clickable wireframes = single communication platform across business person, user, developer
- Best validation tool: when stakeholders see a prototype, all the details and questions they hadn't thought about surface

### 3.4 User research as decision-arbiter
- For meetings where everyone has a different opinion and someone must "decide": **let the users answer instead.**
- User research gives objective data instead of subjective opinions.
- Practice: record every user test; show key elements to clients via video.

---

## 4. How to Build a Killer Product Design Team

### Three essential roles (don't conflate them)

1. **UI Design** — pixel-perfect, beautiful screen design
2. **UX Design** — wireframes, prototypes, structures and flows; communicates with other players; brainstorms; runs workshops
3. **UX Research** — tests designs with real users, validates feature ideas, runs interviews, evaluates analytics, builds personas, delivers customer feedback

> "That doesn't mean you need 3 people."

### One-person-show warning
- Common in startups; **risky** because research is very time-consuming.
- One person doing everything is too busy to do research → **the most important feedback signal goes missing**.
- UX Studio's structure: product designers (UX → UI) work alongside a dedicated UX researcher.

### Junior vs senior
- Methods (the recipe) matter as much as people (the ingredients).
- Senior people know the methods, have real-life experience, know what to do in your specific project.
- **Hiring a junior as a one-person show will probably do more harm than good.**
- Hiring a senior + a junior to assist works.

### Designer development practices (UX Studio's "9 ways to evolve"; sample listed)
- Intense training program teaching methods
- External speakers every 2nd Friday
- Mentoring
- Common sketching sessions
- **Weekly feedback from 3 different sources** (research, designer peer, client)

### Role of the Product Manager
- Emphasize business goals
- Give feedback
- Make sure the design team gets whatever they need
- **Stakeholder buy-in:** convince top management to hire and run a product design team

### Sprint structure
- Week-long design sprints
- Each sprint starts with a design meeting attended by designer + researcher + business leader + technical leader
- Show: designs made, research results
- Decide: design choices together, tasks for next sprint

---

## 5. Case Study Insights (memorable principles)

### 5.1 "If I can't do it right here, I will just close your app"
**Insight:** "Most people won't even give a try to the menu. They will just leave your app if they can't do what they want on the screen they are."

The Trace project (microservices monitoring) had its key actions hidden in a top-right profile-icon menu. **Nobody found them.** Solution: surface key actions inline on the relevant entity (e.g., a "Setup Alert" button inside the service-detail modal).

> **Rule: Don't hide important functions in the menu. They have to be on the screen when the users need them.**

### 5.2 Call-Center QA — observe before you design
**The problem:** quality-assurance specialists evaluate calls. 100 calls × 3 min = 5 hours of audio. Brutal.

**The observation (from field-watching):** experienced QA specialists *don't listen to the full call*. They guess where the critical points are (e.g., "yes" usually 45 seconds before end), click, listen, re-guess if wrong.

**The features designed:**
1. **Visualize the operator's and client's voice as waveforms** — QA can see instantly when operator was reciting conditions or when client replied → jump straight to critical points
2. **Variable playback speed (without pitch change)** — calls are still understandable at 1.25×, experienced QAs go up to 1.75×

**Outcome:** halved QA time. QA team quote: "The new player is f\*\*n great! Awesome! I am in love with it. It saves me hours. Every day."

> **Rule: Observe how experienced users actually work. Their workarounds reveal the features you should build natively.**

### 5.3 Self-Driving Cars — building trust by showing intent
**Problem:** how do passengers trust an autonomous car?

**Insight:** People look at the driver's face to make sure they're in control. This instinctive behavior won't disappear. Adapt to it.

**Design:** A central display visible to all passengers showing the car's "face":
- Schematic top-down view of all surrounding cars, bikes, pedestrians (proven easily understandable in tests)
- The route ahead so passengers can predict the car's moves
- "When there's a risky situation it's always there in the same place in the middle, so you can check it quickly"

**Iteration insight (red signs):**
- **First iteration:** highlight obstacles with **red boxes** → users became stressed. Red = danger → impulse to act → can't act in autonomous mode → stress.
- **Second iteration:** **red lines instead of red boxes**. Lines = fence/boundary, communicating "the car sees this and is staying on its side." Way more successful.

> **Rule: Visual semantics matter. Red boxes ≠ red lines, even though both are red, because containment shape signals different intent (danger vs boundary).**

---

## 6. Application to Our Engines (Phase 2 cross-reference)

- **`srs-skills`** — The 5+1 (Section 1) is a stakeholder-education one-pager that should accompany any SRS engagement kickoff
- **`website-skills`** — The 7-step UX process (Section 2) is a direct candidate for a project-template in proposal-skills; the "Don't hide important functions in the menu" rule (5.1) should be a heuristic in dont-make-me-think-extraction successor docs
- **`social-media-skills`** — The user-research-as-arbiter principle (3.4) translates directly to A/B testing decisions on copy/creative
- **`~/.claude/skills/enterprise-ux-process`** — The 3 essential roles (Section 4) should be referenced when defining the team-shape requirement for enterprise UX engagements
