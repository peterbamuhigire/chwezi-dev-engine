#!/usr/bin/env node
/**
 * destructive-bash-gate.js — PreToolUse hook for destructive shell commands.
 *
 * This is a defense-in-depth prompt to name the blast radius and rollback. It
 * is not an authorization system or a complete shell parser. Matching commands
 * are denied on every attempt: repeating one does not create authority.
 *
 * The hook reads the documented Claude Code PreToolUse JSON payload from
 * stdin. Invalid or missing input fails closed with exit code 2. A deliberate
 * administrator override remains available through CHWEZI_GATEGUARD=off in
 * the hook process environment; do not treat that setting as user approval.
 */

'use strict';

if (!require('./plugin-hook-config').isEnabled()) process.exit(0);

const fs = require('fs');

const BUILTIN_DESTRUCTIVE_PATTERNS = [
  /\bgit\s+reset\s+--hard\b/i,
  /\bgit\s+push\b(?:(?![;&|\r\n]).)*(?:--force(?:-with-lease)?(?=\s|$)|(?:^|\s)-f(?=\s|$)|(?:^|\s)\+[^\s;&|]+)/i,
  /\bgit\s+clean\s+-[a-z]*[dfx][a-z]*\b/i,
  /\bdrop\s+table\b/i,
  /\bdrop\s+database\b/i,
  /\btruncate\s+table\b/i,
  /\bdd\s+if=/i,
  /\brobocopy\b.*\/MIR\b/i,
  /\brsync\b.*--delete\b/i,
  /\bformat\s+[a-z]:/i,
  /\bshred\b/i,
];

function block(reason) {
  console.error(`[chwezi:destructive-bash-gate] BLOCKED: ${reason}`);
  process.exit(2);
}

function readStdin() {
  try {
    return fs.readFileSync(0, 'utf8');
  } catch (error) {
    return null;
  }
}

function shellSegments(command) {
  // Conservative lexical split. This is deliberately not presented as a
  // complete shell grammar; unusual quoting and shell features remain a gap.
  return command.split(/(?:&&|\|\||[;&|\r\n])/);
}

function shellWords(command) {
  return command.match(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[^\s]+/g) || [];
}

function unquote(word) {
  if (word.length >= 2 && ((word[0] === '"' && word.at(-1) === '"') || (word[0] === "'" && word.at(-1) === "'"))) {
    return word.slice(1, -1);
  }
  return word;
}

function hasRecursiveForceRemove(command) {
  return shellSegments(command).some((segment) => {
    const match = /\brm\b/i.exec(segment);
    if (!match) return false;

    const words = shellWords(segment.slice(match.index + match[0].length)).map(unquote);
    let recursive = false;
    let force = false;
    for (const word of words) {
      if (word === '--') break;
      if (word === '--recursive' || /^-(?!-)[^-]*r[^-]*$/i.test(word)) recursive = true;
      if (word === '--force' || /^-(?!-)[^-]*f[^-]*$/i.test(word)) force = true;
    }
    return recursive && force;
  });
}

function hasRecursiveForcePowerShellRemove(command) {
  return shellSegments(command).some((segment) => {
    const match = /\bRemove-Item\b/i.exec(segment);
    if (!match) return false;

    const words = shellWords(segment.slice(match.index + match[0].length)).map(unquote);
    const recursive = words.some((word) => /^-Recurse(?:$|:)/i.test(word));
    const force = words.some((word) => /^-Force(?:$|:)/i.test(word));
    return recursive && force;
  });
}

function matchesDestructive(command) {
  if (hasRecursiveForceRemove(command)) return 'recursive forced rm';
  if (hasRecursiveForcePowerShellRemove(command)) return 'recursive forced Remove-Item';

  const patterns = [...BUILTIN_DESTRUCTIVE_PATTERNS];
  const extra = process.env.CHWEZI_GATE_EXTRA_PATTERNS;
  if (extra) {
    try {
      patterns.push(new RegExp(extra, 'i'));
    } catch (error) {
      console.error('[chwezi:destructive-bash-gate] Invalid CHWEZI_GATE_EXTRA_PATTERNS; ignoring the optional pattern.');
    }
  }
  return patterns.find((pattern) => pattern.test(command)) || null;
}

function main() {
  if (['off', '0', 'false', 'disabled', 'disable'].includes((process.env.CHWEZI_GATEGUARD || '').toLowerCase())) {
    process.exit(0);
  }

  const raw = readStdin();
  if (raw === null) block('could not read the PreToolUse payload; refusing to assume the command is safe');

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch (error) {
    block('invalid JSON PreToolUse payload; refusing to assume the command is safe');
  }

  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    block('unexpected PreToolUse payload; refusing to assume the command is safe');
  }

  const toolInput = payload.tool_input;
  if (!toolInput || typeof toolInput !== 'object' || Array.isArray(toolInput)) {
    block('missing tool_input object; refusing to assume the command is safe');
  }

  const command = toolInput.command;
  if (typeof command !== 'string' || !command.trim()) {
    block('missing shell command; refusing to assume the command is safe');
  }

  const matched = matchesDestructive(command);
  if (!matched) process.exit(0);

  block(
    `destructive command matched (${matched}). Before requesting an approved override, state every affected file, table, branch, or remote ref; give the one-line rollback; and quote the user's current authorization. Repeating the same command does not authorize it. If the user/operator separately approves an override, set CHWEZI_GATEGUARD=off in the hook process environment.`,
  );
}

main();
