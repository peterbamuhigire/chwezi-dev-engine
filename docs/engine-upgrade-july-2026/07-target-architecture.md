# Target Architecture

The target architecture keeps the current engine identity but separates routing, doctrine, examples, templates, validation, and delivery evidence so an agent can find the right skill and prove the output is ready.

```text
skills-web-dev/
|-- README.md                         # router and domain contract
|-- AGENTS.md                         # Codex operating rules
|-- CLAUDE.md                         # Claude operating rules, if used
|-- docs/
|   |-- engine-upgrade-july-2026/     # this audit report set
|   |-- source-registers/             # NEW: dated official/current sources
|   |-- quality-gates/                # NEW: release-blocking QA gates
|   `-- world-class-exemplars/        # NEW: finished reference outputs
|-- skills/
|   |-- <category>/<skill>/SKILL.md   # active entrypoints with strong frontmatter
|   |-- <category>/<skill>/references/# supporting doctrine, standards, examples
|   `-- <category>/<skill>/templates/ # reusable templates where needed
|-- examples/                         # NEW: public, sanitized full workflows
|-- templates/                        # shared document/workbook/code templates
|-- scripts/ or tools/                # validators, generators, conformance checks
|-- tests/                            # NEW: routing, positive, and negative fixtures
`-- projects/                          # optional local workspaces, excluded from engine scoring
```

New elements are marked `NEW`. Existing folders should be retained only when they are active, routed, or documented as examples; empty and legacy paths should become explicit aliases or be removed.
