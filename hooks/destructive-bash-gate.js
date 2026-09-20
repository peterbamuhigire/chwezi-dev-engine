#!/usr/bin/env node
/**
 * destructive-bash-gate.js — PreToolUse hook on Bash/PowerShell.
 *
 * Three-stage gate for destructive commands, modelled on the DENY -> FORCE
 * -> ALLOW pattern documented in the ECC audit's gateguard skill: the first
 * attempt at a destructive command is denied with a demand for concrete
 * facts (what does this touch, what's the rollback, what did the user
 * actually ask for); a repeated attempt at the SAME command is allowed,
 * on the theory that presenting those facts is itself what changes the
 * outcome, not a second automated check.
 *
 * This exists because of a real, recorded incident: ~30 skill folders were
 * deleted from .claude/skills/skills/ on 2026-05-12 by a destructive sync
 * run without per-operation confirmation. That is exactly the failure mode
 * this hook targets.
 *
 * Contract: reads a JSON payload on stdin (Claude Code PreToolUse hook),
 * inspects the pending Bash/PowerShell command string, and exits 0 (allow)
 * or 2 (block, reason on stderr). As with banned-font-gate.js, this has
 * been unit-tested directly (see hooks/test-destructive-bash-gate.js) but
 * NOT exercised inside a live Claude Code session — verify the stdin field
 * names against the installed version before relying on it in production.
 *
 * State (for the deny-once-then-allow behaviour): a per-command-hash marker
 * file under CHWEZI_GATE_STATE_DIR (default: a temp dir under the OS temp
 * root), expiring after CHWEZI_GATE_STATE_TTL_HOURS (default 8). This is a
 * TIME-WINDOW approximation of "this session already saw this command", not
 * a true session ID — Claude Code's exact session-scoping hook environment
 * variable was not confirmed against live documentation before writing
 * this, so a fixed time window is the honestly-uncertain choice rather than
 * asserting a specific env var name with false confidence. Widen or narrow
 * the TTL, or wire in a confirmed session-ID env var, once verified.
 *
 * Graduated controls (matches gateguard's pattern):
 *   CHWEZI_GATEGUARD=off                  — disable entirely
 *   CHWEZI_GATE_EXTRA_PATTERNS=<regex>     — additional destructive regex,
 *                                            appended to the built-in set
 *   CHWEZI_GATE_STATE_DIR=<path>           — override the state directory
 *
 * Fails open: if state cannot be read or written, the gate ALLOWS the
 * operation rather than looping or blocking on its own malfunction, and
 * says so on stderr.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const BUILTIN_DESTRUCTIVE_PATTERNS = [
  /\brm\s+(-\w*r\w*f\w*|-\w*f\w*r\w*)\b/i, // rm -rf, rm -fr, rm -Rf, etc.
  /\bgit\s+reset\s+--hard\b/i,
  /\bgit\s+push\s+.*--force(?!-with-lease)\b/i, // --force, not --force-with-lease
  /\bgit\s+clean\s+-[a-z]*[dfx][a-z]*\b/i,
  /\bdrop\s+table\b/i,
  /\bdrop\s+database\b/i,
  /\btruncate\s+table\b/i,
  /\bdd\s+if=/i,
  /\brobocopy\b.*\/MIR\b/i,
  /\brsync\b.*--delete\b/i,
  /\bRemove-Item\b.*-Recurse\b.*-Force\b/i, // PowerShell equivalent of rm -rf
  /\bformat\s+[a-z]:/i, // Windows format <drive>:
  /\bshred\b/i,
];

function readStdin() {
  try {
    return fs.readFileSync(0, 'utf8');
  } catch (e) {
    return '';
  }
}

function extractCommand(toolInput) {
  if (!toolInput) return '';
  return toolInput.command || toolInput.script || toolInput.cmd || '';
}

function stateDir() {
  return process.env.CHWEZI_GATE_STATE_DIR || path.join(os.tmpdir(), 'chwezi-gate-state');
}

function ttlMs() {
  const hours = Number(process.env.CHWEZI_GATE_STATE_TTL_HOURS) || 8;
  return hours * 60 * 60 * 1000;
}

function commandHash(command) {
  return crypto.createHash('sha256').update(command.trim()).digest('hex').slice(0, 24);
}

/**
 * Returns true if this exact command was already denied within the TTL
 * window (i.e. this is a retry that should now be allowed), and marks it
 * as seen for next time either way. Returns false (fail open, allow) if the
 * state directory itself is unusable.
 */
function alreadyDeniedRecently(command) {
  const dir = stateDir();
  const file = path.join(dir, commandHash(command) + '.json');
  try {
    fs.mkdirSync(dir, { recursive: true });
  } catch (e) {
    console.error(`[chwezi:destructive-bash-gate] Could not create state dir ${dir} — allowing (fail-open).`);
    return true; // fail open: treat as already-seen so we don't loop-deny
  }

  let previouslyDenied = false;
  try {
    const stat = fs.statSync(file);
    const age = Date.now() - stat.mtimeMs;
    if (age < ttlMs()) previouslyDenied = true;
  } catch (e) {
    previouslyDenied = false;
  }

  try {
    fs.writeFileSync(file, JSON.stringify({ deniedAt: new Date().toISOString() }));
  } catch (e) {
    console.error(`[chwezi:destructive-bash-gate] Could not write state file — allowing (fail-open).`);
    return true;
  }

  return previouslyDenied;
}

function matchesDestructive(command) {
  const patterns = [...BUILTIN_DESTRUCTIVE_PATTERNS];
  const extra = process.env.CHWEZI_GATE_EXTRA_PATTERNS;
  if (extra) {
    try {
      patterns.push(new RegExp(extra, 'i'));
    } catch (e) {
      console.error(`[chwezi:destructive-bash-gate] CHWEZI_GATE_EXTRA_PATTERNS is not a valid regex — ignoring it.`);
    }
  }
  return patterns.find((re) => re.test(command)) || null;
}

function main() {
  if (['off', '0', 'false', 'disabled', 'disable'].includes((process.env.CHWEZI_GATEGUARD || '').toLowerCase())) {
    process.exit(0);
  }

  const raw = readStdin();
  let payload;
  try {
    payload = JSON.parse(raw);
  } catch (e) {
    process.exit(0); // fail open on unparseable payload
  }

  const toolInput = payload.tool_input || payload.toolInput || payload.input || {};
  const command = extractCommand(toolInput);
  if (!command) process.exit(0);

  const matched = matchesDestructive(command);
  if (!matched) process.exit(0);

  if (alreadyDeniedRecently(command)) {
    // This exact command was already fact-forced once in the recent past —
    // allow the retry rather than deny-looping on it forever.
    process.exit(0);
  }

  console.error(
    `BLOCKED (destructive command) — before running this, present these facts:\n\n` +
    `1. List every file, table, branch, or remote ref this command will modify or delete.\n` +
    `2. Write a one-line rollback procedure — what restores the prior state if this is wrong.\n` +
    `3. Quote the user's current instruction verbatim.\n\n` +
    `Command matched: ${matched}\n` +
    `Retrying the exact same command after presenting these facts will be allowed.\n` +
    `Override for this session: CHWEZI_GATEGUARD=off (use only when you have already\n` +
    `confirmed the operation with the user through another channel).`
  );
  process.exit(2);
}

main();
