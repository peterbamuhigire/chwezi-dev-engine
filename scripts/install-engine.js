#!/usr/bin/env node
/**
 * install-engine.js — shared installer runtime for Chwezi skill engines.
 *
 * One engine, installed standalone, with zero dependency on any other
 * Chwezi engine or on this coordination package being installed. This
 * implements the "Tier 1 — STANDALONE" model from the ECC audit's
 * installation report (10-installation-and-distribution.md).
 *
 * What it does:
 *   - Copies an engine's skills/ (and agents/, commands/, hooks/ when
 *     present) into the target Claude root.
 *   - Records what it installed in <target>/.chwezi/install-state.json,
 *     keyed by engine name with a content hash per file, so update and
 *     uninstall only ever touch files this installer actually wrote —
 *     never a user's own files, even ones that happen to share a name.
 *   - Supports --dry-run (prints the plan, writes nothing) and --json.
 *   - Supports --scope user (~/.claude, default) or --scope project (.claude
 *     under the current directory) — mirrors ECC's scope choice.
 *   - uninstall removes only files this installer's state record owns.
 *
 * This does NOT touch a Claude Code plugin install performed via
 * `/plugin marketplace add` / `/plugin install` — that path is native and
 * needs no script. This script exists for: users without the plugin system,
 * users who want project-local scope, and CI verification.
 *
 * Usage:
 *   node install-engine.js install   --engine <path> [--scope user|project] [--dry-run] [--json]
 *   node install-engine.js uninstall --engine <name> [--scope user|project] [--dry-run] [--json]
 *   node install-engine.js doctor    [--scope user|project] [--json]
 *   node install-engine.js list-installed [--scope user|project] [--json]
 */

'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const COMPONENT_DIRS = ['skills', 'agents', 'commands', 'hooks', 'rules'];

// Non-skills component discovery stays a fixed directory-name list — agents,
// commands, hooks and rules are conventional across every engine. Skills are
// not: srs-skills and linux-skills keep numbered category directories
// (01-strategic-vision/, 03-networking-and-dns/) at the engine root instead
// of under a skills/ subdirectory. When no skills/ directory exists, fall
// back to scanning the engine root for directories that contain at least
// one SKILL.md, excluding known non-skill directories, so a single
// installer works across every layout in the estate without per-engine
// hardcoding.
// Deliberately does NOT exclude "meta" — linux-skills keeps genuine skills
// (kaizen-improvement-system, skill-safety-audit, skill-writing) there, and
// this set must never silently drop real content the manifest generator
// would include. Only directories confirmed to hold no SKILL.md content in
// any current engine belong here; verify against `find <root> -name SKILL.md`
// before adding a new entry.
const ROOT_EXCLUDE = new Set([
  'skills', 'agents', 'commands', 'hooks', 'rules', // handled separately / not applicable at root
  'scripts', 'docs', 'templates', 'tests', 'examples', 'references', 'prompts',
  'book-extractions', 'domains', 'engine', 'projects', 'clients', 'notes',
  'node_modules', '.git', '.github', '.claude-plugin', '.chwezi',
  '_TEMPLATE', '__pycache__',
]);

/**
 * Returns { mode: 'explicit', dirs: [<engineRoot>/skills] } when a
 * conventional skills/ directory exists, or
 * { mode: 'root-scan', dirs: [...category dirs at engine root] } when it
 * does not (srs-skills, linux-skills: numbered category directories live
 * directly at the engine root).
 */
function findSkillRootDirs(engineRoot) {
  const explicitSkillsDir = path.join(engineRoot, 'skills');
  if (fs.existsSync(explicitSkillsDir)) {
    return { mode: 'explicit', dirs: [explicitSkillsDir] };
  }

  const found = [];
  let entries;
  try {
    entries = fs.readdirSync(engineRoot, { withFileTypes: true });
  } catch (e) {
    entries = [];
  }
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (entry.name.startsWith('.')) continue;
    if (ROOT_EXCLUDE.has(entry.name.toLowerCase())) continue;
    if (entry.name.startsWith('%')) continue; // e.g. a stray "%SystemDrive%"
    found.push(path.join(engineRoot, entry.name));
  }
  return { mode: 'root-scan', dirs: found };
}

function parseArgs(argv) {
  const cmd = argv[0];
  const rest = argv.slice(1);
  const args = { cmd, scope: 'user', dryRun: false, json: false };
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--engine') args.engine = rest[++i];
    else if (a === '--scope') args.scope = rest[++i];
    else if (a === '--dry-run') args.dryRun = true;
    else if (a === '--json') args.json = true;
    else if (a === '--force') args.force = true;
  }
  return args;
}

function resolveTargetRoot(scope) {
  if (scope === 'project') return path.join(process.cwd(), '.claude');
  return path.join(os.homedir(), '.claude');
}

function sha256(filePath) {
  const buf = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(buf).digest('hex');
}

const SKIP_DIR_NAMES = new Set(['_TEMPLATE', 'node_modules', '.git', '__pycache__']);

function walkFiles(dir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.') && entry.name !== '.claude-plugin') continue;
    if (entry.isDirectory() && SKIP_DIR_NAMES.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walkFiles(full, out);
    else out.push(full);
  }
  return out;
}

/**
 * Like walkFiles, but stops descending into any subdirectory that is
 * itself a skill (has its own SKILL.md) — that subdirectory is a separate
 * manifest entry with its own walkFilesToSkillBoundary call, and copying it
 * again from the parent would duplicate its files under two destinations.
 * A handful of engines nest one skill inside another (e.g.
 * proposal-skills/skills/profiles-sectors/sectors/ is itself a skill that
 * contains proposal-skills/skills/profiles-sectors/sectors/<name>/, each
 * also its own skill) — this boundary is what makes install output match
 * the manifest's file count exactly instead of double-counting the nested
 * ones. `topDir` is the entry directory itself, which must always be
 * descended into regardless of whether it has its own SKILL.md.
 */
function walkFilesToSkillBoundary(dir, topDir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.') && entry.name !== '.claude-plugin') continue;
    if (entry.isDirectory() && SKIP_DIR_NAMES.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (full !== topDir && fs.existsSync(path.join(full, 'SKILL.md'))) continue;
      walkFilesToSkillBoundary(full, topDir, out);
    } else {
      out.push(full);
    }
  }
  return out;
}

function readState(targetRoot) {
  const statePath = path.join(targetRoot, '.chwezi', 'install-state.json');
  if (!fs.existsSync(statePath)) return { version: 1, engines: {} };
  try {
    return JSON.parse(fs.readFileSync(statePath, 'utf8'));
  } catch (e) {
    return { version: 1, engines: {} };
  }
}

function writeState(targetRoot, state) {
  const stateDir = path.join(targetRoot, '.chwezi');
  fs.mkdirSync(stateDir, { recursive: true });
  fs.writeFileSync(path.join(stateDir, 'install-state.json'), JSON.stringify(state, null, 2) + '\n');
}

function engineName(engineRoot) {
  const pkgPath = path.join(engineRoot, 'package.json');
  if (fs.existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      if (pkg.name) return pkg.name.replace(/^@chwezi\//, '');
    } catch (e) { /* fall through */ }
  }
  return path.basename(engineRoot);
}

function cmdInstall(args) {
  if (!args.engine) {
    console.error('install requires --engine <path>');
    process.exit(2);
  }
  const engineRoot = path.resolve(args.engine);
  const name = engineName(engineRoot);
  const targetRoot = resolveTargetRoot(args.scope);

  const plan = [];
  const addTree = (srcDir) => {
    if (!fs.existsSync(srcDir)) return;
    for (const f of walkFiles(srcDir, [])) {
      const rel = path.relative(engineRoot, f).split(path.sep).join('/');
      plan.push({ src: f, dest: path.join(targetRoot, rel), rel });
    }
  };

  for (const comp of ['agents', 'commands', 'hooks', 'rules']) {
    addTree(path.join(engineRoot, comp));
  }

  // Prefer the engine's own .claude-plugin/plugin.json as the single source
  // of truth for which directories are skills: it is produced and verified
  // by scripts/generate-plugin-manifest.js against the raw filesystem for
  // every engine in this estate. Deriving from it here — rather than
  // maintaining a second, separately-hand-tuned exclude list — means there
  // is exactly one place that decides "what counts as a skill". An earlier
  // version of this script kept its own root-scan exclude list and it
  // silently dropped linux-skills' meta/ directory (three real skills)
  // because that list drifted out of sync with the manifest generator's.
  const pluginManifestPath = path.join(engineRoot, '.claude-plugin', 'plugin.json');
  let manifest = null;
  if (fs.existsSync(pluginManifestPath)) {
    try {
      manifest = JSON.parse(fs.readFileSync(pluginManifestPath, 'utf8'));
    } catch (e) {
      manifest = null;
    }
  }

  if (manifest && Array.isArray(manifest.skills) && manifest.skills.length > 0) {
    for (const entry of manifest.skills) {
      let relRoot = entry.replace(/^\.\//, '').replace(/\/$/, '');
      // Engines whose skills live at conventional skills/<category>/<skill>/
      // paths already have that prefix in the manifest. Engines with
      // numbered category directories at the engine root (srs-skills,
      // linux-skills) do not — synthesize the prefix so every install
      // target ends up with a uniform <root>/skills/... shape regardless of
      // how the source engine organizes its own working tree.
      if (!relRoot.startsWith('skills/')) relRoot = 'skills/' + relRoot;
      // Resolve the actual source directory against the manifest entry as
      // written (pre-prefix) — the "skills/" prefix above is a target-side
      // convention only; it does not necessarily exist on the source side.
      const srcDir = path.join(engineRoot, entry.replace(/^\.\//, '').replace(/\/$/, ''));
      if (!fs.existsSync(srcDir)) continue;
      for (const f of walkFilesToSkillBoundary(srcDir, srcDir, [])) {
        const rel = relRoot + '/' + path.relative(srcDir, f).split(path.sep).join('/');
        plan.push({ src: f, dest: path.join(targetRoot, rel), rel });
      }
    }
  } else {
    // No plugin.json yet for this engine — fall back to the heuristic
    // root-scan. Kept only for engines this installer has never been run
    // against; run generate-plugin-manifest.js first when possible.
    const { mode, dirs: skillRoots } = findSkillRootDirs(engineRoot);
    if (mode === 'explicit') {
      for (const root of skillRoots) addTree(root);
    } else {
      for (const root of skillRoots) {
        const catName = path.basename(root);
        for (const f of walkFiles(root, [])) {
          const rel = 'skills/' + catName + '/' + path.relative(root, f).split(path.sep).join('/');
          plan.push({ src: f, dest: path.join(targetRoot, rel), rel });
        }
      }
    }
  }

  if (plan.length === 0) {
    console.error(`No skills/, agents/, commands/, hooks/, or rules/ found under ${engineRoot}`);
    process.exit(1);
  }

  const state = readState(targetRoot);
  const existing = state.engines[name];
  const owningAnotherEngine = [];
  for (const item of plan) {
    for (const [otherName, otherRecord] of Object.entries(state.engines)) {
      if (otherName === name) continue;
      if (otherRecord.files && otherRecord.files[item.rel]) {
        owningAnotherEngine.push({ rel: item.rel, owner: otherName });
      }
    }
  }
  if (owningAnotherEngine.length > 0 && !args.force) {
    console.error(
      `Refusing to install "${name}": ${owningAnotherEngine.length} file(s) are already owned by another installed engine, e.g. "${owningAnotherEngine[0].rel}" owned by "${owningAnotherEngine[0].owner}". Pass --force to override.`
    );
    process.exit(1);
  }

  if (args.dryRun) {
    const summary = {
      engine: name,
      scope: args.scope,
      targetRoot,
      filesPlanned: plan.length,
      previouslyInstalled: !!existing,
      sample: plan.slice(0, 5).map((p) => p.rel),
    };
    if (args.json) console.log(JSON.stringify(summary, null, 2));
    else {
      console.log(`[dry-run] Would install "${name}" (${plan.length} files) into ${targetRoot}`);
      for (const p of plan.slice(0, 10)) console.log(`  ${p.rel}`);
      if (plan.length > 10) console.log(`  ... and ${plan.length - 10} more`);
    }
    return;
  }

  const fileRecord = {};
  for (const item of plan) {
    fs.mkdirSync(path.dirname(item.dest), { recursive: true });
    fs.copyFileSync(item.src, item.dest);
    fileRecord[item.rel] = sha256(item.dest);
  }

  state.engines[name] = {
    source: engineRoot,
    installedAt: new Date().toISOString(),
    fileCount: plan.length,
    files: fileRecord,
  };
  writeState(targetRoot, state);

  const result = { engine: name, scope: args.scope, targetRoot, filesInstalled: plan.length };
  if (args.json) console.log(JSON.stringify(result, null, 2));
  else console.log(`Installed "${name}": ${plan.length} files into ${targetRoot}`);
}

function cmdUninstall(args) {
  if (!args.engine) {
    console.error('uninstall requires --engine <name>');
    process.exit(2);
  }
  const targetRoot = resolveTargetRoot(args.scope);
  const state = readState(targetRoot);
  const record = state.engines[args.engine];
  if (!record) {
    console.error(`"${args.engine}" is not recorded as installed at ${targetRoot}`);
    process.exit(1);
  }

  const toRemove = [];
  for (const [rel, expectedHash] of Object.entries(record.files)) {
    const full = path.join(targetRoot, rel);
    if (!fs.existsSync(full)) continue;
    const actualHash = sha256(full);
    toRemove.push({ rel, full, modified: actualHash !== expectedHash });
  }

  if (args.dryRun) {
    const modified = toRemove.filter((f) => f.modified);
    const summary = { engine: args.engine, filesToRemove: toRemove.length, modifiedSinceInstall: modified.length };
    if (args.json) console.log(JSON.stringify(summary, null, 2));
    else {
      console.log(`[dry-run] Would remove ${toRemove.length} files for "${args.engine}"`);
      if (modified.length > 0) {
        console.log(`  WARNING: ${modified.length} file(s) were modified since install and will still be removed unless you pass --force is respected below (this tool always warns, never silently skips):`);
        for (const f of modified.slice(0, 10)) console.log(`    ${f.rel}`);
      }
    }
    return;
  }

  const modified = toRemove.filter((f) => f.modified);
  if (modified.length > 0 && !args.force) {
    console.error(
      `${modified.length} installed file(s) were modified since install (e.g. "${modified[0].rel}"). Pass --force to remove anyway, or review changes first.`
    );
    process.exit(1);
  }

  const touchedDirs = new Set();
  for (const f of toRemove) {
    fs.unlinkSync(f.full);
    touchedDirs.add(path.dirname(f.full));
  }
  // Prune directories left empty by the removal, walking upward from each
  // touched leaf. Never removes targetRoot itself, and stops at the first
  // non-empty ancestor.
  for (const dir of touchedDirs) {
    let cur = dir;
    while (cur.startsWith(targetRoot) && cur !== targetRoot) {
      let entries;
      try {
        entries = fs.readdirSync(cur);
      } catch (e) {
        break;
      }
      if (entries.length > 0) break;
      fs.rmdirSync(cur);
      cur = path.dirname(cur);
    }
  }
  delete state.engines[args.engine];
  writeState(targetRoot, state);

  const result = { engine: args.engine, filesRemoved: toRemove.length };
  if (args.json) console.log(JSON.stringify(result, null, 2));
  else console.log(`Uninstalled "${args.engine}": removed ${toRemove.length} files`);
}

function cmdListInstalled(args) {
  const targetRoot = resolveTargetRoot(args.scope);
  const state = readState(targetRoot);
  const entries = Object.entries(state.engines).map(([name, r]) => ({
    name,
    installedAt: r.installedAt,
    fileCount: r.fileCount,
    source: r.source,
  }));
  if (args.json) {
    console.log(JSON.stringify(entries, null, 2));
    return;
  }
  if (entries.length === 0) {
    console.log(`No Chwezi engines installed at ${targetRoot}`);
    return;
  }
  console.log(`Installed at ${targetRoot}:`);
  for (const e of entries) console.log(`  ${e.name} — ${e.fileCount} files, installed ${e.installedAt}`);
}

function cmdDoctor(args) {
  const targetRoot = resolveTargetRoot(args.scope);
  const state = readState(targetRoot);
  const report = { targetRoot, engines: [] };
  for (const [name, record] of Object.entries(state.engines)) {
    let missing = 0;
    let modified = 0;
    for (const [rel, expectedHash] of Object.entries(record.files)) {
      const full = path.join(targetRoot, rel);
      if (!fs.existsSync(full)) { missing++; continue; }
      if (sha256(full) !== expectedHash) modified++;
    }
    const sourceExists = fs.existsSync(record.source);
    report.engines.push({
      name,
      fileCount: record.fileCount,
      missing,
      modifiedSinceInstall: modified,
      sourceStillPresent: sourceExists,
      status: missing > 0 ? 'DAMAGED' : modified > 0 ? 'LOCALLY MODIFIED' : 'OK',
    });
  }
  if (args.json) {
    console.log(JSON.stringify(report, null, 2));
    return;
  }
  console.log(`Doctor report for ${targetRoot}:`);
  for (const e of report.engines) {
    console.log(`  ${e.name}: ${e.status} (${e.fileCount} files, ${e.missing} missing, ${e.modifiedSinceInstall} locally modified)`);
  }
  if (report.engines.length === 0) console.log('  (nothing installed)');
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  switch (args.cmd) {
    case 'install': return cmdInstall(args);
    case 'uninstall': return cmdUninstall(args);
    case 'list-installed': return cmdListInstalled(args);
    case 'doctor': return cmdDoctor(args);
    default:
      console.error('Usage: install-engine.js <install|uninstall|list-installed|doctor> [options]');
      process.exit(2);
  }
}

main();
