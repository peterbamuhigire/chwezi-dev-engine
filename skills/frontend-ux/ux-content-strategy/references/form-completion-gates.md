# Form Completion Gates

Forms are the most expensive piece of UX a product owns: every additional field is a percentage of users who do not finish. This file is the engine's working set of decisions for designing forms that get completed — label position, required vs. optional convention, primary/secondary actions, smart defaults, inline validation, and the gradual-engagement option that lets a form be skipped entirely.

Derived from Wroblewski, *Web Form Design*.

## The Default Question: Does This Need To Be A Form At All?

Before optimizing a form, consider not having one. *Web Form Design* devotes Chapter 13 to **gradual engagement**: instead of greeting new customers with a sign-up form, let them produce value first and ask for the form later, or never. Three worked examples:

- **Geni** does not ask new visitors to register. The front page lets them start a family tree; the email arrives after they have done the thing the product is for.
- **TripIt** is started not with a sign-up form but by forwarding a travel-confirmation email. The user does the action; an itinerary comes back.
- The pattern across both: identify the smallest valuable thing the product can do, let the user trigger it without an account, and convert later.

Apply gradual engagement when the product can deliver early value without identity. Skip it when the value depends on persistent identity (banking, medical records, anything regulated).

## Label Position: A Measurable Decision

Label position has measurable consequences. Per Matteo Penzo's eye-tracking study cited in the book:

- **Top-aligned labels** require a single eye fixation to take in the label and the field. They were the fastest, with measured saccade durations as low as ~50 milliseconds.
- **Right-aligned labels** sat in the middle: about 240 ms saccade for novices.
- **Left-aligned labels** were slowest — a medium saccade duration around 500 ms — because the distance between label and field is largest.

The book gives an explicit decision rule:

| Goal | Choice |
|---|---|
| Reduce completion time, allow flexible label lengths for localization | **Top-aligned** |
| Similar speed goals but vertical screen real estate is constrained | **Right-aligned** |
| Form requires people to *scan* labels to find a few specific fields among many, or has lots of optional fields with unfamiliar data | **Left-aligned** |

The choice is functional, not aesthetic. Pick the column based on the form's purpose, not based on what the rest of the page looks like.

## Required Vs. Optional: Pick One Convention And Honor User Expectation

The book's pop quiz is the load-bearing rule: when most people see an asterisk next to a field, they read it as "required." A counter-example in the book — the Hogan sign-up form using asterisks for *optional* fields — illustrates the cost of breaking that expectation: users now have to discover the convention by reading help text.

Operating rules:

1. Indicate the *minority* class. If most fields are required, mark the optional ones with the word "(optional)." If most are optional, mark the required ones with an asterisk and a legend.
2. Never mix conventions inside one form.
3. Never use the asterisk to mean "optional" — the population-level expectation is too strong to override.

## Primary And Secondary Actions

The eye-tracking studies in the book (provided by Etre) show measurable differences in fixation count and duration when primary and secondary actions are styled identically vs. distinguished. Three configurations, in order of efficiency:

1. **Same color, same prominence** for primary and secondary — slowest, most fixations, users hesitate.
2. **Different color** for primary vs. secondary — faster, fewer fixations.
3. **Different color and physical separation** between primary and secondary — fastest decisions.

Operational rule: there is exactly one primary action per form. Secondary actions (Cancel, Save Draft) are visually weaker *and* placed away from the primary so an accidental click is unlikely.

## Smart Defaults — Answer The Question For Most People

Smart defaults pre-fill the answer the majority of users would have given. The eBay "sell your item" form defaults shipping service, insurance, and sales-tax behavior so most sellers do not have to choose. *Web Form Design*'s rule: smart defaults work when there is a clear option that applies to most people. They fail when there is no such majority — the gender example in the book uses a drop-down with a non-presumptuous default (e.g., a third option) precisely because no binary default applies fairly.

Two further sources of smart defaults:

- **Population defaults** based on what most users in this segment pick.
- **Personal defaults** based on this user's prior behavior — Expedia's travel options example uses prior trips as the source.

Smart defaults reduce the form, but they require honesty. A pre-checked marketing-opt-in is not a smart default; it is a dark pattern.

## Inline Validation — Confirm, Do Not Just Reject

Chapter 9 of *Web Form Design* defines inline validation as feedback that confirms or suggests valid answers as the user fills the field. Newsvine's display-name field uses inline validation to find an available name without bouncing the user between error states ("pogo-sticking"). Last.fm uses it on almost every field of sign-up. Yahoo! Local uses it to communicate character limits as the user types.

Operating rules:

- Validate when the field has a constraint the user cannot satisfy by guessing — uniqueness, length, format.
- Confirm successes, not only failures. The green check is part of the design.
- Do *not* use inline validation when the field is straightforward (name, common email format) — the validation noise becomes condescending.

When inline validation cannot prevent an error, fall through to the error taxonomy in `error-state-taxonomy-and-recovery.md`.

## Path To Completion

Chapter 3 of *Web Form Design* names the goal: **illuminate a path to completion**. The user always knows what form they are on, what step they are on, and how many steps remain — *truthfully*. The Fidelity Investments example is the cautionary tale: a two-level progress bar that disappears on step one (login) so the displayed step count is a lie.

Operating rules:

- Tell the user honestly how many steps. If steps can branch (e.g., new address adds a sub-page), say so or do not show a count at all.
- Group fields into logical, scannable groups. The book is explicit: organize content into logical groups to aid scanning and completion.
- For long forms, the choice between progress indicator and no indicator depends on whether you can be honest about the count.

## The Gates In Order

When the engine is asked to design or audit a form, it should walk these gates in order:

1. **Gradual-engagement gate.** Does this need to be a form at all, or can the value be delivered first?
2. **Field count gate.** Each field must justify itself against completion-rate cost.
3. **Label position gate.** Top, right, or left, based on the decision table.
4. **Required/optional gate.** One convention, honoring asterisk = required.
5. **Smart defaults gate.** Where is there a majority answer or a personal-history answer worth pre-filling?
6. **Primary/secondary gate.** Exactly one primary, visually separated.
7. **Inline validation gate.** Which fields have a constraint the user cannot guess?
8. **Path-to-completion gate.** Is the count honest? Are the groups scannable?
9. **Help-text gate.** Are any help strings actually compensating for a wrong field width or label?

A form that passes all nine has earned the user's completion. A form that skips any of them is gambling.

## Anti-Patterns

- Asterisk used for optional fields.
- Two equally weighted "primary" buttons.
- Pre-checked consent boxes posing as smart defaults.
- Help text that exists because the field is the wrong width (e.g., a 5-digit zip code field that needs help saying "5 digits only").
- Progress bars that lie about step count.
- Validation that fires on every keystroke for fields with no real constraint.

## Source Grounding

- Penzo eye-tracking results: top-aligned labels at ~50 ms saccade, right at ~240 ms, left averaging ~500 ms.
- The label-position decision table tying choice to completion-time goals, vertical real estate, and scanning behavior.
- The asterisk pop quiz and the Hogan counter-example using asterisks for "optional."
- Etre studies on primary/secondary action styling: identical vs. color-differentiated vs. color-and-position differentiated.
- eBay smart-defaults example for shipping, insurance, sales tax; Expedia personal-history defaults.
- Gradual engagement examples: Geni's family tree before registration, TripIt's email-forwarding entry point.
- Inline validation examples: Newsvine display-name uniqueness, Last.fm sign-up, Yahoo! Local character limits.
- Fidelity Investments progress bar that disappears on step one as the cautionary path-to-completion example.
