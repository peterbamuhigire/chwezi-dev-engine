#!/usr/bin/env node
/**
 * test-destructive-bash-gate.js — direct unit test.
 * Run: node hooks/test-destructive-bash-gate.js
 */

'use strict';

const { spawnSync } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

const HOOK = path.join(__dirname, 'destructive-bash-gate.js');
const TEST_STATE_DIR = path.join(os.tmpdir(), 'chwezi-gate-state-test-' + Date.now());

function run(command, env = {}) {
  const result = spawnSync(process.execPath, [HOOK], {
    input: JSON.stringify({ tool_input: { command } }),
    encoding: 'utf8',
    env: { ...process.env, CHWEZI_GATE_STATE_DIR: TEST_STATE_DIR, ...env },
  });
  return { code: result.status, stderr: result.stderr };
}

const cases = [
  { name: 'rm -rf — first attempt BLOCKED', cmd: 'rm -rf /some/skills/dir', expect: 2 },
  { name: 'rm -rf — same command retried, ALLOWED', cmd: 'rm -rf /some/skills/dir', expect: 0, sameAsAbove: true },
  { name: 'git reset --hard — BLOCKED', cmd: 'git reset --hard origin/main', expect: 2 },
  { name: 'git push --force — BLOCKED', cmd: 'git push --force origin main', expect: 2 },
  { name: 'git push --force-with-lease — ALLOWED (safer variant, not matched)', cmd: 'git push --force-with-lease origin main', expect: 0 },
  { name: 'robocopy /MIR — BLOCKED', cmd: 'robocopy C:\\src C:\\dst /MIR', expect: 2 },
  { name: 'rsync --delete — BLOCKED', cmd: 'rsync -av --delete src/ dst/', expect: 2 },
  { name: 'DROP TABLE — BLOCKED', cmd: 'psql -c "DROP TABLE users;"', expect: 2 },
  { name: 'ordinary ls — ALLOWED', cmd: 'ls -la', expect: 0 },
  { name: 'ordinary git status — ALLOWED', cmd: 'git status', expect: 0 },
  { name: 'ordinary rm of one file — ALLOWED (not -rf)', cmd: 'rm old-notes.txt', expect: 0 },
  { name: 'CHWEZI_GATEGUARD=off — ALLOWED despite rm -rf', cmd: 'rm -rf /whatever', expect: 0, env: { CHWEZI_GATEGUARD: 'off' } },
];

let failures = 0;
for (const c of cases) {
  const result = run(c.cmd, c.env || {});
  const pass = result.code === c.expect;
  console.log(`${pass ? 'PASS' : 'FAIL'} — ${c.name} (expected exit ${c.expect}, got ${result.code})`);
  if (!pass) {
    failures++;
    if (result.stderr) console.log(`       stderr: ${result.stderr.split('\n')[0]}`);
  }
}

try {
  fs.rmSync(TEST_STATE_DIR, { recursive: true, force: true });
} catch (e) { /* best effort cleanup */ }

console.log(`\n${cases.length - failures}/${cases.length} passed`);
process.exit(failures > 0 ? 1 : 0);
