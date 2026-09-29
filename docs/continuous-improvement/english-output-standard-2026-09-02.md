# English Output Standard - Engineering Catalogue

Owner: Peter Bamuhigire. Apply with the relevant product, technical-writing,
anti-slop, security, accessibility, and currentness gates.

Canonical study: `C:\wamp64\www\digital-research-engine\docs\continuous-improvement\english-collocations-and-lexical-precision-2026-09-02.md`.

- Use British English by default and preserve approved product, API, code, protocol, legal, and standards terminology.
- Write with exact actors, states, constraints, dependencies, examples, acceptance evidence, and failure paths.
- Check collocations and grammatical frames before changing technical wording; do not replace an established term with a fashionable synonym.
- Replace subjective adjectives with observable criteria. Treat `secure`, `scalable`, `robust`, `seamless`, and `intuitive` as prompts for a measurable definition, not praise.
- Keep idioms and metaphor out of interfaces, requirements, operations, security, and compliance unless their meaning is explicit and tested.
- Proof identifiers, commands, units, version strings, names, links, code fences, and user-facing messages. Never add typos or false warmth to simulate humanity.

## Re-pitch unclear material

When a reader says the explanation does not make sense, do not merely shorten or repeat it. Identify
the missing prerequisite, use the project's established terms, state the actor and concrete example,
then explain the consequence or next action. Preserve necessary technical precision. ASD-STE100 or
another controlled-language standard applies only when the artefact or client requires it; it is not
the universal definition of plain English.

The supplied books inform durable language craft only. They are not authority for
current software, standards, APIs, or security claims; Digital Research verification
is mandatory whenever a statement may have changed.

## Output registers

Every piece of output is written in one of three registers. Pick the register from the reader, not
from the writer's mood or a token budget.

| Register | Reader | Use for | Style |
|---|---|---|---|
| R0 Formal | A client, funder, evaluator or end user | Client deliverables: proposals, SRS and other requirements documents, business plans, website copy, and any DOCX, PPTX or PDF handed over | Full sentences, British English, the project's approved terms, no shorthand. R0 is absolute for client deliverables: no terse or machine forms, whatever the length pressure |
| R1 Working prose | Peter, a colleague or a reviewer | Chat replies, status reports, review findings, commit bodies, evidence files, handoff notes | Plain, complete sentences; short paragraphs and tables; lead with the result |
| R2 Machine-facing terse | Another agent, a script or a log | Subagent reports, lane output (`path:line — finding`), status tokens, log lines, JSON | Fixed shapes and tokens; fragments allowed; nothing a person must read unedited |

Rules that hold in every register:

- **Always preserve** negators (not, never, no, without), numbers and units, identifiers, file paths,
  commands, version strings, exact error text and quoted source text. Shortening must never drop or
  alter any of these.
- **No invented abbreviations.** Use only abbreviations the reader already knows or the project has
  defined. `cfg`, `impl` or `w/o` coined to save space are not allowed in R0 or R1.
- **Security warnings and irreversible-action confirmations are always full R1 sentences** (or R0 in
  a client deliverable), even inside R2 output: what will happen, to what, and whether it can be
  undone.
- R2 output is rewritten into R1 before a person reads it. The rewrite keeps every preserved item
  above exactly as written.

(Register table adapted from JuliusBrussee/caveman, MIT, https://github.com/JuliusBrussee/caveman,
commit `2fd153c`, reworded for this engine.)
