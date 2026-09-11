# AI-Slop Responsible Publishing Standard

**Status:** active cross-engine reference
**Checked:** 11 September 2026
**Owner:** skills-web-dev control plane; domain engines adapt the standard to their artefact type

## Purpose

This standard treats AI slop as a publishing failure, not an authorship accusation. AI-generated or AI-assisted material is not automatically slop. Slop is material published with so little verification, specificity, editorial judgement, or audience care that fluency hides the absence of value.

The responsible question is therefore not “does this sound like AI?” It is “what would the reader lose if this unit disappeared, and can the publisher stand behind the claims, examples, design choices, and next action?”

## Non-diagnostic style rule

Punctuation, bullet counts, ordinary vocabulary, repeated sentence openings, formal register, three-part phrasing, and plausible names are editorial prompts only. They are not proof of authorship. Do not score an individual as machine-written from a stylistic irritation or a detector result. This matters especially for non-native English writers and for genres with legitimate conventions.

Use style observations to revise clarity, rhythm, relevance, and specificity. Use source evidence to verify claims. Keep those findings separate in the audit.

## Evidence-first publishing contract

For every consequential claim, record:

| Field | Required question |
|---|---|
| Claim | What exactly is being asserted, promised, or implied? |
| Scope | Who, where, what population or product, and what conditions does it cover? |
| Time | What measurement, publication, or validity period applies? |
| Source | Does the cited source actually support this sentence, rather than a neighbouring idea? |
| Transformation | Was the claim quoted, paraphrased, calculated, or inferred? |
| Limitation | What does the source not establish? |
| Decision | What should the reader do differently because this claim is present? |

If a source, date, definition, or limitation is unavailable, remove the unsupported specificity, qualify the statement, or mark the check `NOT_ASSESSED`. Never fill an evidence gap with a plausible number, invented quote, convenient customer, or unlabeled scenario.

## Examples and honesty

- Label a fictional business, customer, case, testimonial, result, or conversation as hypothetical.
- Never present an invented person as interviewed, a fabricated client as past performance, or a generated quotation as a source quotation.
- A name is not suspicious evidence. Audit provenance and labelling, not whether a name sounds common or convenient.
- Product promises must name the mechanism, conditions, limits, and failure behaviour where those details affect a buyer’s decision.

## Machine-error editorial overlay

Apply these checks to prose, proposals, plans, web pages, social sequences, infographics, interfaces, and code documentation. Cite the affected unit and the missing information delta. Do not infer a finding from a keyword count alone.

| ID | Check | Responsible action |
|---|---|---|
| ME1 | Repeated meaning | Merge or cut repetition unless it reconciles a model, repeats a required label, or serves accessibility. |
| ME2 | Decorative symmetry | Keep a list, contrast, or layout only when the parts express real distinctions. |
| ME3 | Over-explanation | Stop when the reader can act or decide; retain only a necessary qualification or handoff. |
| ME4 | Inflated significance | Reduce the consequence claim to the scale supported by evidence. |
| ME5 | Generic example | Replace with a traceable, task-specific example or label it hypothetical. |
| ME6 | Mannerism recurrence | Vary repeated transitions, headings, visual motifs, CTA patterns, or code structures when they add no function. |
| ME7 | Empty unit | Add a claim, warrant, evidence, comparison, implication, decision, state, or user task; otherwise remove the unit. |

The visual and product adaptation also checks: convergence on default layouts or assets, unearned hierarchy, module monoculture, decorative attention, placeholder content, copy tells, and delivery debt. A missing render, browser inspection, provenance record, or human review is `NOT_ASSESSED`, not clean.

## Domain adaptations

### Business plans and proposals

Every section must contain a business-specific decision, customer, competitor, dated source, price, operational constraint, assumption, risk, or counter-case. Market and financial claims need source, date, definition, and calculation lineage. Make founder or bidder judgement visible: why this route, why now, what is deliberately not being done, and what would invalidate the recommendation.

### Websites and social media

Write for a named audience, page or channel job, awareness level, and next action. Place proof beside the promise. Do not invent testimonials, urgency, outcomes, platform limits, or engagement results. Internal links are navigation; citations are evidence. A page-specific meta description is a usefulness and accuracy concern, not an authorship test. Scale only content that adds distinct value.

### Design and infographics

Start with a real audience question and one primary message. Every chart, annotation, icon, colour, hierarchy, and decorative element must have a task, state, accessibility, brand, or evidence reason. Cite the dataset and period inside the artefact or its evidence pack. Do not use AI-looking visual defaults, provenance gaps, or generic pictograms as authorship proof; judge whether the visual is authored, legible, truthful, and useful.

### Engineering and documentation

Require a real user or operator outcome, explicit constraints, failure paths, security and accessibility evidence, dependency verification, and rollback or handoff detail. Do not hide a missing implementation behind polished prose, generated code, or green-looking structure. Repeated identifiers, schemas, warnings, and test fixtures are functional exceptions when their role is documented.

## Release gate

- [ ] The artefact has a named audience, job, and consequence of failure.
- [ ] Every load-bearing claim has a source, scope, date, transformation, and limitation, or is qualified/removed.
- [ ] Hypothetical examples and generated assets are labelled where readers could mistake them for evidence.
- [ ] Style findings are separated from authorship claims; no individual is accused from surface cues.
- [ ] ME1-ME7 and the applicable visual overlay were reviewed with exact evidence.
- [ ] The hard case, counterargument, failure mode, or downside that could change the decision is covered.
- [ ] Each retained section, component, post, slide, chart, or function earns its space.
- [ ] Unavailable source, render, browser, provenance, or reviewer evidence is `NOT_ASSESSED`.
- [ ] A separate domain audit has a verdict consistent with all blockers.

## Evidence register checked 11 September 2026

| ID | Source and use | Scope and limitation |
|---|---|---|
| S1 | [Kobak et al., *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*](https://arxiv.org/abs/2406.07016) | Analysis of more than 15 million PubMed biomedical abstracts, 2010–2024; estimates at least 13.5% of 2024 abstracts were processed with LLMs. This is an aggregate estimate for a corpus, not an individual-authorship test. The arXiv record also lists a 2025 *Science Advances* journal reference. |
| S2 | [Rallapalli et al., *Interpretable Stylistic Variation in Human and LLM Writing Across Genres, Models, and Decoding Strategies*](https://arxiv.org/abs/2604.14111) | Submitted 15 April 2026; arXiv preprint. Analyses human writing and 11 models across eight genres and reports genre, model, and decoding effects. Treat as supporting preprint evidence, not a universal detection rule. |
| S3 | [Liang et al., *GPT detectors are biased against non-native English writers*](https://arxiv.org/abs/2304.02819) | Evaluates several detectors on native and non-native English samples and reports systematic misclassification in the tested setting. Do not generalise its sample or systems to every detector; use it to require caution and fair review. |
| S4 | [Google Search Central: crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) | Supports practical internal-link and crawlability guidance. It does not identify authorship. |
| S5 | [Google Search Central: snippets and meta descriptions](https://developers.google.com/search/docs/appearance/snippet) | Supports accurate, page-specific descriptions and explains that snippets may be generated from page content. Matching an opening sentence is not authorship evidence. |
| S6 | [Google Search Central: generative AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) | Supports accuracy, relevance, added value, and caution about scaled content abuse. It is a publishing-quality standard, not a word blacklist or detector. |

## Maintenance

Re-check changing platform guidance, research status, and model/runtime assumptions before each substantive Kaizen refresh. Do not turn a stylistic observation into a permanent ban without corroborated evidence. Domain engines may strengthen the gate for their risk surface, but may not weaken this responsibility contract.
