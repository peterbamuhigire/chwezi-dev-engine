# Rules

## Why this exists

Skills are on-demand, token-expensive playbooks — the *how*. They only load into
context when something makes the harness reach for them, which per the
`capability-surface-selection.md` narrowest-surface principle is exactly right for
deep, situational knowledge. But this engine also carries principles that are
**always supposed to apply** — no hardcoded secrets, treat fetched/untrusted content
as data not instructions, never run a destructive command without stating the
blast radius first — and those were, until this rules layer existed, only as
reliable as whichever skill happened to be loaded when the situation came up.

**Rules are the always-on layer.** They are short, deterministic-in-spirit
statements of "what", kept separate from the skills that carry the "how". A rule
should be checkable in one sentence; if it needs a worked example, a decision
tree, or a code sample, that content belongs in a skill, and the rule should link
to it.

## Structure

```
rules/
├── common/          # Language- and domain-agnostic principles
│   ├── security.md
│   ├── coding-style.md
│   ├── verification.md
│   └── agentic-engineering.md
└── README.md        # this file
```

This mirrors the pattern audited from `affaan-m/ECC`'s `rules/` layer, adapted:
ECC layers per-language directories on top of `common/`; this engine's per-language
conventions already live in `skills/languages/*` and are deliberately left there —
only what is genuinely cross-cutting belongs here. Do not duplicate language-specific
guidance into this directory; link to the relevant skill instead.

## Rules vs Skills — the test

Before adding something here, ask:

1. **Is it checkable without a code example?** "Never commit a hardcoded secret" —
   yes. "How to configure a secrets manager for a Django project" — no, that's a
   skill.
2. **Does it apply regardless of language, framework, or project type?** If it only
   applies to React projects, it is not a common rule.
3. **Would violating it be a security, correctness, or trust problem, not a style
   preference?** Style preferences belong in language-specific skills, where they
   can carry the nuance a blanket rule would lose.

If a candidate rule fails any of these, it stays a skill (or a skill's reference
file) and this file links to it instead of restating it.

## Adding a rule

Rules are added deliberately, not by default. The audit-recommended process
(`rules-distill`, not yet built into this engine) is: a principle earns a place
here only once it has been observed recurring across **two or more skills** —
otherwise it is that one skill's concern, not a cross-cutting one. Until that
tooling exists, add a rule here only when you can point to at least two places in
this engine (or another Chwezi engine) that already assume it.

Every rule file states, at the top, which skills or engines it was distilled from
— so a reader can go find the fuller "how" and so a future audit can tell whether
the rule is still grounded in real content or has drifted from it.
