# Replicate Skill-Engine Routing on Another Machine

**Superseded.** This page described a 2026-06 set-up in which the engineering catalogue had to live
at `~/.claude/skills` for native discovery. That model was retired on 2026-06-21: this engine is now
a router-based engine like the others and can be cloned to any path.

To set up routing on another machine:

1. Clone each engine to any folder and record its real path in the user-global engine routing table
   (`~/.claude/CLAUDE.md` for Claude Code; the runner's global instructions or `AGENTS.md` for other
   runners).
2. Follow the install and adapter guides in the coordination package,
   [chwezi-engine-agents](https://github.com/peterbamuhigire/chwezi-engine-agents): `docs/distribution.md`
   and `docs/adapters/` (Claude Code, Codex, Gemini CLI, OpenCode, generic CLI, MCP).
3. For this engine alone, the plugin route in [README.md](README.md#installation) also works.

The full previous text of this page remains in the Git history of this file.
