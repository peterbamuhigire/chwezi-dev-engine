#!/usr/bin/env node
/**
 * generate-plugin-manifest.js — shared, engine-agnostic version.
 *
 * Regenerates <engine>/.claude-plugin/plugin.json from that engine's actual
 * skill tree, using the explicit-path-array form documented in the ECC audit
 * (installation report, §3, "Fallback A"): every SKILL.md's containing
 * directory is listed individually, so the Claude Code plugin loader never
 * has to walk an arbitrary, unverified nesting depth.
 *
 * Handles the three skill-root shapes found across the Chwezi engines:
 *   - skills/<skill>/SKILL.md                      (flat)          e.g. digital-research-engine
 *   - skills/<category>/<skill>/SKILL.md            (one level)     e.g. business-plan, proposal, website, social-media, chwezi-dev-engine
 *   - skills/<NN-category>/<NN-skill>/SKILL.md      (one level)     e.g. design-system, srs (roots differ — see --root)
 *   - <NN-area>/SKILL.md at the repo root, no skills/ dir           e.g. linux-skills (use --root .)
 *
 * Follows the constraints in ECC's .claude-plugin/PLUGIN_SCHEMA_NOTES.md:
 *   - "version" is mandatory
 *   - "skills" must be an array
 *   - NEVER add an "agents" field (auto-discovered by convention)
 *   - NEVER add a "hooks" field for the standard hooks/hooks.json
 *   - keep "mcpServers": {} as an explicit opt-out
 *
 * Usage:
 *   node generate-plugin-manifest.js --engine <path> [--root <skills-subdir>] [--check] [--exclude <name,name>]
 *
 * Examples:
 *   node generate-plugin-manifest.js --engine ../../digital-research-engine
 *   node generate-plugin-manifest.js --engine ../../srs-skills --exclude "%SystemDrive%,projects,docs,references,templates,engine,book-extractions"
 *   node generate-plugin-manifest.js --engine ../../linux-skills --root . --exclude "docs,scripts,templates,tests,commands,meta,notes,prompts"
 */

'use strict';

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = { root: 'skills', exclude: '_TEMPLATE,node_modules,.git', check: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--engine') args.engine = argv[++i];
    else if (a === '--root') args.root = argv[++i];
    else if (a === '--exclude') args.exclude = argv[++i];
    else if (a === '--check') args.check = true;
    else if (a === '--version') args.version = argv[++i];
  }
  if (!args.engine) {
    console.error('Usage: node generate-plugin-manifest.js --engine <path> [--root <dir>] [--check] [--exclude a,b,c]');
    process.exit(2);
  }
  return args;
}

/**
 * A directory can simultaneously BE a skill (own SKILL.md) and CONTAIN
 * further nested skills one or more levels down — e.g.
 * proposal-skills/skills/profiles-sectors/{SKILL.md, sectors/<name>/SKILL.md}.
 * So "found a SKILL.md here" must never stop the recursion — it only adds
 * this directory to the result and continues into every subdirectory
 * regardless. An earlier version of this script stopped at the first
 * SKILL.md per branch and silently dropped every skill nested beneath it;
 * verified against proposal-skills, where it missed 17 of 111 real skills.
 */
function findSkillDirs(dir, excludeSet, out) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (e) {
    return out;
  }
  if (fs.existsSync(path.join(dir, 'SKILL.md'))) {
    out.push(dir);
  }
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (entry.name.startsWith('.')) continue;
    if (excludeSet.has(entry.name)) continue;
    findSkillDirs(path.join(dir, entry.name), excludeSet, out);
  }
  return out;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const ROOT = path.resolve(args.engine);
  const SKILLS_DIR = path.join(ROOT, args.root);
  const MANIFEST_PATH = path.join(ROOT, '.claude-plugin', 'plugin.json');
  const EXCLUDE_DIRS = new Set(args.exclude.split(',').map((s) => s.trim()).filter(Boolean));

  if (!fs.existsSync(SKILLS_DIR)) {
    console.error(`No skill root at ${SKILLS_DIR}`);
    process.exit(1);
  }

  const skillDirs = findSkillDirs(SKILLS_DIR, EXCLUDE_DIRS, []).sort();
  if (skillDirs.length === 0) {
    console.error(`No SKILL.md files found under ${SKILLS_DIR} — refusing to write an empty manifest.`);
    process.exit(1);
  }

  const skillPaths = skillDirs.map((p) => {
    const rel = path.relative(ROOT, p).split(path.sep).join('/');
    return './' + rel + '/';
  });

  const leafNames = new Map();
  let collision = false;
  for (const p of skillDirs) {
    const leaf = path.basename(p);
    if (leafNames.has(leaf)) {
      console.error(`Skill name collision: "${leaf}" at\n  ${leafNames.get(leaf)}\n  and\n  ${p}`);
      collision = true;
    }
    leafNames.set(leaf, p);
  }
  if (collision) process.exit(1);

  let existingVersion = '1.0.0';
  if (fs.existsSync(MANIFEST_PATH)) {
    try {
      const existing = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
      if (existing.version) existingVersion = existing.version;
    } catch (e) {
      /* ignore malformed existing file, regenerate */
    }
  }

  const manifest = {
    version: args.version || existingVersion,
    skills: skillPaths,
    mcpServers: {},
  };

  // If this engine ships a hooks/hooks.json, expose the standard on/off +
  // profile toggle at install time (Claude Code's userConfig mechanism) so
  // a user can control hook enforcement without editing files. Does NOT
  // declare "hooks" itself here — that stays auto-loaded by convention per
  // PLUGIN_SCHEMA_NOTES.md.
  if (fs.existsSync(path.join(ROOT, 'hooks', 'hooks.json'))) {
    manifest.userConfig = {
      hooks_enabled: {
        type: 'boolean',
        title: 'Enable Chwezi hooks',
        description: 'Run this engine\'s enforcement hooks (e.g. destructive-command gate, banned-font gate where applicable). Disable to install skills only, with no local automation.',
        default: true,
      },
    };
  }

  const rendered = JSON.stringify(manifest, null, 2) + '\n';

  if (args.check) {
    const current = fs.existsSync(MANIFEST_PATH) ? fs.readFileSync(MANIFEST_PATH, 'utf8') : null;
    if (current !== rendered) {
      console.error(`${path.basename(ROOT)}: plugin.json is stale (${skillPaths.length} skills on disk).`);
      process.exit(1);
    }
    console.log(`${path.basename(ROOT)}: plugin.json is current — ${skillPaths.length} skills.`);
    return;
  }

  fs.mkdirSync(path.dirname(MANIFEST_PATH), { recursive: true });
  fs.writeFileSync(MANIFEST_PATH, rendered);
  console.log(`${path.basename(ROOT)}: wrote plugin.json — ${skillPaths.length} skills.`);
}

main();
