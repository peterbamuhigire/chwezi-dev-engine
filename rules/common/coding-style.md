# Coding Style — Common Rules

> Distilled from: `sdlc-meta/world-class-engineering` (the baseline operating
> contract this engine's skills already assume) and `sdlc-meta/skill-composition-standards`
> (house style for the engine's own artefacts). This file states only what is
> genuinely cross-language; framework and language idiom belong in
> `skills/languages/*` and `skills/frontend-ux/*`, not here.

## Every output solves a stated problem under stated constraints

Not "write a function that does X" in the abstract — the real user or business
problem, with the constraints that actually bound it (performance budget,
existing data shape, compliance requirement). Code that satisfies the letter of
a request while ignoring its context is not correct, it is merely compiling.

*Full output contract (what "world-class" means for this engine's work):*
`sdlc-meta/world-class-engineering`.

## Small, focused files over large ones

Prefer many files with high cohesion and low coupling over few files that do
everything. When a file's purpose can no longer be stated in one sentence, it is
a sign to split it — not a hard line-count rule, since the right size varies by
language and content, but the direction is consistent across every skill in this
engine that touches architecture.

## No hardcoded values that should be configuration

Magic numbers, environment-specific URLs, and tunable thresholds belong in
configuration or named constants, not inline literals scattered through logic.
This is a correctness rule, not a taste preference: a hardcoded value is a value
nobody can find to change when it turns out to be wrong.

## Match the surrounding code, not a personal default

When editing an existing codebase, match its comment density, naming
conventions, and idiom before introducing a different style — even one you would
otherwise prefer. A codebase with two competing styles is worse than one with a
style you disagree with. (This mirrors the ECC-audited `inherit-legacy-style`
pattern: align to the codebase's meta-architecture, not your pretrained default.)

## House style for this engine's own artefacts

Skill files, rule files, and documentation in this engine follow
`sdlc-meta/skill-composition-standards` — read it before adding or editing a
`SKILL.md`, not only before writing prose elsewhere.
