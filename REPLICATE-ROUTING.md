# Replicate Controlled Skill-Engine Routing on Another Machine

This sets up the same "Claude is always aware of my skill engines and routes to them by
context" behavior on any machine where these repos exist — **even at different folder paths**.
Works on Windows, macOS, and Linux. Last updated: 2026-06-15.

---

## How the routing works (concepts you must preserve)

1. **Router-based engines** — listed in the user-global `CLAUDE.md`. Claude reads their
   `SKILL.md` files *on demand* by context. These can live at ANY path; you just record the
   real path in the routing table. Seven of the eight engines work this way.
2. **One native engine** — Claude Code auto-discovers skills ONLY from `~/.claude/skills`.
   The **engineering catalog (skills-web-dev)** must be cloned to `~/.claude/skills` to stay
   natively discovered. If you clone it elsewhere, it simply becomes another router engine
   (add it to the table like the rest).
3. **Finance is cross-cutting** — it activates *in addition to* whatever domain engine is
   active, whenever finance/accounting/IFRS/IAS/tax/bookkeeping arises.
4. **No cross-engine submodules / no mirroring.** Each engine's `main` already has the
   decoupled structure, so a fresh clone needs no submodule surgery. (Exception: `website-skills`
   intentionally embeds `proposal-skills` as a submodule — clone it with `--recurse-submodules`.)

`~/.claude/` means the per-user Claude directory: `C:\Users\<you>\.claude` on Windows,
`/Users/<you>/.claude` on macOS, `/home/<you>/.claude` on Linux. `~/.claude/CLAUDE.md` is the
user-global instruction file Claude Code loads in **every** session, in every directory.

---

## Step 1 — Clone the eight repos

Clone anywhere you like (e.g. a `repos/` or `www/` folder). The engineering catalog is the
one exception — it goes to `~/.claude/skills`.

```bash
# Engineering catalog -> MUST be ~/.claude/skills for native discovery
git clone https://github.com/peterbamuhigire/skills-web-dev.git ~/.claude/skills

# The other engines -> any folder (set BASE to wherever you keep repos)
BASE=~/repos          # <- change to your location
git clone https://github.com/peterbamuhigire/srs-skills.git                 "$BASE/srs-skills"
git clone https://github.com/peterbamuhigire/business-plan-skills.git       "$BASE/business-plan-skills"
git clone --recurse-submodules https://github.com/peterbamuhigire/website-skills.git "$BASE/website-skills"
git clone https://github.com/peterbamuhigire/social-media-skills.git        "$BASE/social-media-skills"
git clone https://github.com/peterbamuhigire/linux-skills.git               "$BASE/linux-skills"
git clone https://github.com/peterbamuhigire/proposal-skills.git            "$BASE/proposal-skills"
git clone https://github.com/peterbamuhigire/chwezi-accounting-doctrine.git "$BASE/chwezi-accounting-doctrine"
```

(On Windows PowerShell, use `$env:USERPROFILE\.claude\skills` and a `$BASE` like `C:\repos`.)

If the repos already exist on the machine, skip cloning — just make sure they're on `main`
and up to date (`git -C <path> pull`), and that the engineering catalog is reachable at
`~/.claude/skills` (clone or symlink it there).

## Step 2 — Record the real local paths

Note where each engine actually landed on THIS machine. You'll paste these into the routing
table in Step 3. Example (yours will differ):

```
srs-skills                 = /home/you/repos/srs-skills
business-plan-skills       = /home/you/repos/business-plan-skills
website-skills             = /home/you/repos/website-skills
social-media-skills        = /home/you/repos/social-media-skills
linux-skills               = /home/you/repos/linux-skills
proposal-skills            = /home/you/repos/proposal-skills
chwezi-accounting-doctrine = /home/you/repos/chwezi-accounting-doctrine
engineering catalog        = /home/you/.claude/skills
```

## Step 3 — Create `~/.claude/CLAUDE.md`

Create the file `~/.claude/CLAUDE.md` with the content below. **Replace every `<PATH:...>`
placeholder with the real path from Step 2.** Keep the structure and the protocol text intact.

````markdown
# Global Instructions (this machine)

## Skill Engines — ALWAYS aware, route by context

This machine hosts several large, self-contained **skill engines**. Each is a git repo of
routed `SKILL.md` files with its own `CLAUDE.md`/`AGENTS.md`/`README.md` controller. They are
NOT on Claude Code's native skill-discovery path (except the engineering catalog at
`~/.claude/skills`), so they are invisible unless you deliberately consult them.

**You must always be aware these engines exist, regardless of the current working directory.**
Whenever the user refers to one by name, OR the task falls within one of their domains (see
table), treat that engine as the **default source of skills** for the work:

1. **First** read the engine's `CLAUDE.md` (and `AGENTS.md` if present, or `README.md` where
   that is the engine's router — e.g. the finance engine) — these are the routers that tell
   you how the engine is organized and which skill to pick.
2. **Then** locate the relevant skill by globbing `SKILL.md` inside that engine and read the
   matching one(s). Do NOT use the `Skill` tool for these (they are not registered there) —
   read the `SKILL.md` files directly.
3. Follow the engine's own conventions and templates. Prefer its skills over improvising.

### Engine routing table

| Engine path | Use as default when the work involves… |
|---|---|
| `<PATH:srs-skills>` | Software Requirements Specifications, PRDs, business cases, vision/lean-canvas, system design docs, IEEE-style requirements & SaaS spec artifacts. (Engineering/methodology skills come from the engineering-catalog engine; finance from the finance engine.) |
| `<PATH:business-plan-skills>` | Business plans, investor/bankable plans, country/market context, business strategy. (Finance/accounting standards: the finance engine activates cross-cutting alongside it.) |
| `<PATH:website-skills>` | Building static websites from markdown content & assets, web project scaffolding, site performance/lighthouse work |
| `<PATH:social-media-skills>` | Social media / digital-marketing consultancy deliverables: proposals, strategies, content plans, platform playbooks, decks, reports, training (content-only — no code/design/ads ops) |
| `<PATH:linux-skills>` | Linux sysadmin: provisioning, hardening, networking, DNS/mail, firewall/SSL, storage, security analysis, observability, DR. Hub skill: `linux-sysadmin` (start there) |
| `<PATH:proposal-skills>` | Consulting proposals, Expressions of Interest, procurement/tender responses (East & Central African market) |
| `<PATH:chwezi-accounting-doctrine>` | **Cross-cutting finance/accounting engine** (Chwezi Doctrine). ANY finance/accounting work: bookkeeping, IFRS/IAS standards, financial statements, tax/statutory, close/consolidation, controls, sector accounting. Consult IN ADDITION to whatever domain engine is active. Router doc is `README.md`; skills under `skills/<group>/<skill-name>/SKILL.md`. |
| `~/.claude/skills` | **Engineering-catalog engine** (= skills-web-dev): general engineering / AI-systems / SaaS / security / product / UX / docs skills. This one IS natively discovered; routed by name. |

### Notes
- Engine structures vary: `srs-skills` uses `NN-category/NN-skill/SKILL.md`;
  `business-plan-skills`, `website-skills`, `social-media-skills`, `proposal-skills` use
  `skills/<category>/<skill-name>/SKILL.md`; `linux-skills` uses `linux-<area>/SKILL.md`;
  the finance engine uses `skills/<group>/<skill-name>/SKILL.md` with `README.md` as router.
- **Finance is cross-cutting** — activate it ALONGSIDE the active domain engine whenever
  finance/accounting/IFRS/IAS/tax/bookkeeping arises; it is not a mutually exclusive choice.
- Each engine is independent (no git-submodule embedding between engines, no mirroring).
- When unsure which engine applies, ask the user briefly rather than guessing.
- If a task spans two domains, consult both relevant engines.
````

> On Windows, write the paths in the table as `C:\...` (backslashes are fine inside the
> markdown table). On macOS/Linux use `/Users/...` or `/home/...`. Always-discovered engine
> stays written as `~/.claude/skills`.

## Step 4 (optional) — Persistent memory backup

`CLAUDE.md` already enforces the behavior. If you also want a memory note, create a file in
the memory folder for the project/working directory you use most (the folder name is derived
from that working directory — let Claude create it, or copy the pattern from the origin
machine: `~/.claude/projects/<slug>/memory/skill-engines.md` plus a one-line pointer in that
folder's `MEMORY.md`). This is machine- and working-directory-specific, so it's optional.

## Step 5 (optional) — Carry the overview doc

Copy `skill-engines-overview.md` (the engine catalog with purposes) to `~/.claude/` on the new
machine, updating the folder paths to match Step 2.

## Step 6 — Verify

1. Start a fresh Claude Code session in any directory (so the new `~/.claude/CLAUDE.md` loads).
2. Without naming a path, ask something domain-specific, e.g. *"draft a tender response for a
   road project"* (should route to `proposal-skills`) or *"book a month-end close"* (should
   route to the finance engine). Confirm Claude consults the right engine's router and reads
   the matching `SKILL.md`.
3. Confirm cross-cutting finance: ask for *"a business plan with IFRS revenue recognition"* —
   Claude should use `business-plan-skills` **and** the finance engine together.

---

## Engine remotes (reference)

```
srs-skills                  https://github.com/peterbamuhigire/srs-skills.git
business-plan-skills        https://github.com/peterbamuhigire/business-plan-skills.git
website-skills              https://github.com/peterbamuhigire/website-skills.git   (embeds proposal-skills submodule)
social-media-skills         https://github.com/peterbamuhigire/social-media-skills.git
linux-skills                https://github.com/peterbamuhigire/linux-skills.git
proposal-skills             https://github.com/peterbamuhigire/proposal-skills.git
chwezi-accounting-doctrine  https://github.com/peterbamuhigire/chwezi-accounting-doctrine.git   (finance, cross-cutting)
skills-web-dev              https://github.com/peterbamuhigire/skills-web-dev.git   (engineering catalog -> clone to ~/.claude/skills)
```

## Troubleshooting
- **Claude doesn't seem aware of the engines:** confirm `~/.claude/CLAUDE.md` exists and you
  started a NEW session after creating it (it loads at session start).
- **Engineering catalog skills not auto-discovered:** it must be at `~/.claude/skills`
  (clone or symlink there). Elsewhere it works only as a router engine.
- **Paths with spaces:** wrap them in backticks inside the table; they still read fine.
- **A repo still shows a `doctrine`/`skills` submodule after clone:** you cloned an old
  branch — ensure you're on `main` (`git checkout main && git pull`). The decoupled structure
  is on `main`.
```
