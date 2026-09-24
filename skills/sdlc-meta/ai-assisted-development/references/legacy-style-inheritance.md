# Legacy Style Inheritance

Load when onboarding an AI coding agent to a hand-written legacy project and you must stop the
agent drifting from the project's implicit conventions (file anatomy, state naming,
infrastructure placement, error handling). It aligns meta-architecture, not syntax or taste,
and is language- and framework-agnostic. Not for pure research or one-off questions.

Absorbed from the retired `sdlc-meta/inherit-legacy-style` skill (origin: adapted from
affaan-m/ECC `skills/inherit-legacy-style/SKILL.md`).

Output: an owner-approved `.ai-style-rules.md` (golden files, naming and state-control rules,
DONTs, evolution log) and a decision log of resolved conflicts. Directly applicable to
hand-written WAMP/PHP client codebases, where a model's pretrained instinct to impose a
framework-idiomatic structure the client never adopted is a recurring failure mode.

## When to Activate

- User asks to onboard AI coding help onto an older codebase
- User is worried about AI-generated code "drifting" from existing project conventions
- User wants to extract and codify a project's implicit coding rules before extensive AI-assisted work begins

## Prerequisites

- Git (recommended; non-Git projects fall back to file timestamps for incremental mode)
- Read/write access to the project root (generates `.ai-style-rules.md` and optionally references it from `CLAUDE.md`)

## Workflow

### Step 0 — Auto-Detect Mode

Check for `.ai-style-rules.md` at the project root: absent means first-time full scan; present means
incremental sniff. Announce the mode in one line and proceed — never ask the user to pick.

### Branch A — First-Time Full Scan

**1. Measure scale, pick a scanning tier**

```bash
git ls-files | grep -cE '\.(js|ts|jsx|tsx|vue|py|go|rs|java|kt|rb|php|cs|swift|c|cpp|h)$'
```

| Tier | Source files | Strategy |
|---|---|---|
| Small | ≲ 50 | Full close-read of every source file |
| Medium | 50–500 | Infra layer = full read; business layer = sample 2–3 per dimension |
| Large | ≳ 500 | Strict sampling + budget cap; `--stat` summary first, then targeted reads |

**2. Scan along 4 dimensions**

1. **File Anatomy** — in-file declaration order (imports → types → main logic → helpers → export)
2. **State & Control Flow** — naming conventions for async state, pagination, flags
3. **Infrastructure** — where cross-cutting utilities live (interceptors, formatters, middleware, PHP traits/service providers)
4. **Error Handling** — try/catch vs. global handler vs. return-code convention; null-check habits

**3. Apply signal-threshold noise reduction**

Before interrupting the user, evaluate signal strength:

- **Weak signal** → auto-suppress: minority <5% AND count <10 → majority wins, minority recorded under DONTs
- **Strong signal** → grill: near-even split, or a semantic fork on a core dimension
- **Small-project exception**: at ≲50 sources, "3 vs 2" is NOT a majority — grill it anyway

**4. Resolve conflicts one at a time (Grilling Protocol)**

For each strong-signal conflict, present exactly ONE question with four options:

> Evidence: `pathA` uses style X, `pathB` uses style Y
> Risk: mixing both fractures the project's style
> Choose: `1` follow X  `2` follow Y  `3` this is evolution, update rules  `4` I have a new rule

Suspend until the user answers, then move to the next conflict. Never stack questions.

**5. Generate `.ai-style-rules.md`** with three mandatory sections:
- **Golden Files** — real exemplar paths, annotated with what they demonstrate
- **Naming & State-Control Rules** — concrete, checkable conventions
- **DONTs** — anti-patterns that must not propagate

**6. Install the persistent hook**

Ask the user for enforcement strength:

| Option | Mechanism |
|---|---|
| **1** Soft hook (recommended) | Reference `.ai-style-rules.md` from the project's own `CLAUDE.md`/`AGENTS.md` |
| **2** Hard hook | Soft hook + a `PreToolUse` hook on `Write`/`Edit` in that project's `.claude/settings.json` — see this engine's `rules/README.md` for the rules-vs-hooks distinction before adding one |
| **3** No hook | Keep the rules file; user references it manually |

### Branch B — Incremental Sniff

1. Read the existing `.ai-style-rules.md`; if it carries a commit fingerprint, run `git diff <last_hash> HEAD --stat` to pinpoint the delta.
2. Read recent Git changes (`git log -3 --stat`, then inspect suspect files on demand).
3. For oversized diffs (hundreds of files), use `--stat` summary only, then sample the largest changes.
4. Compare new code against recorded rules; route conflicts through the Grilling Protocol.
5. Append an evolution log at the end of `.ai-style-rules.md` — never overwrite prior rules.

### Per-Turn Enforcement

When `.ai-style-rules.md` is in context, every code-writing task should open with a compliance
declaration naming the exemplar file being followed and the DONTs being avoided.

## Anti-Patterns

- Skipping the scale-measurement step — sampling a 30-file project starves it; full-scanning a 5,000-file repo blows the budget
- Stacking multiple conflict questions at once — grilling is strictly one at a time
- Overwriting old rules in incremental mode — always append evolution logs
- Defaulting to "hard hook" without asking — enforcement strength is the user's call
- Judging syntax or tech-stack quality — this skill aligns meta-architecture only, not taste
- Copying bugs from exemplar files — reuse structure, flag defects instead of propagating them

## Best Practices

- Announce the detected mode and scale tier in one line before scanning
- For large projects, read `--stat` summaries first, then targeted `Read` on suspect files
- Let the signal threshold handle noise — an 843-vs-8 naming split should auto-resolve without interrupting the user
- When in doubt about signal strength, lean toward asking
- The soft hook is usually sufficient; reach for a hard hook only when the user wants mechanical enforcement

## Examples

1. **First-time onboarding a WAMP/PHP client codebase**: run Branch A → measure scale → scan the 4 dimensions → grill conflicts → generate `.ai-style-rules.md` → offer hook strength.
2. **Incremental update after a client team change**: run Branch B → compare Git deltas to recorded rules → grill any new conflicts → append an evolution log without overwriting.
3. **Enforcing DONTs going forward**: soft hook installed → rules auto-load every session → every code-writing task opens with a compliance declaration.
