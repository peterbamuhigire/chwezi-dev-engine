#!/usr/bin/env node
/**
 * Direct tests for destructive-bash-gate.js.
 * Run: node hooks/test-destructive-bash-gate.js
 */

'use strict';

const { spawnSync } = require('child_process');
const path = require('path');

const HOOK = path.join(__dirname, 'destructive-bash-gate.js');

function run(input, env = {}) {
  const result = spawnSync(process.execPath, [HOOK], {
    input,
    encoding: 'utf8',
    env: { ...process.env, ...env },
  });
  return { code: result.status, stderr: result.stderr };
}

function payload(command) {
  return JSON.stringify({ tool_name: 'Bash', tool_input: { command } });
}

const cases = [
  { name: 'rm -rf is blocked', input: payload('rm -rf /some/skills/dir'), expect: 2 },
  { name: 'repeating the same destructive command remains blocked', input: payload('rm -rf /some/skills/dir'), expect: 2 },
  { name: 'split rm recursive and force flags are blocked', input: payload('rm -r -f /some/skills/dir'), expect: 2 },
  { name: 'long rm flags are blocked in either order', input: payload('rm --force --recursive /some/skills/dir'), expect: 2 },
  { name: 'PowerShell recursive force flags are blocked in either order', input: payload('Remove-Item C:\\temp\\cache -Force -Recurse'), expect: 2 },
  { name: 'git reset --hard is blocked', input: payload('git reset --hard origin/main'), expect: 2 },
  { name: 'git push --force is blocked', input: payload('git push --force origin main'), expect: 2 },
  { name: 'git push --force-with-lease is also blocked', input: payload('git push --force-with-lease origin main'), expect: 2 },
  { name: 'git push --force-with-lease ref form is blocked', input: payload('git push --force-with-lease=refs/heads/main origin main'), expect: 2 },
  { name: 'git push --force-with-lease expected-value form is blocked', input: payload('git push --force-with-lease=refs/heads/main:deadbeef origin main'), expect: 2 },
  { name: '--no-force-with-lease is not mistaken for a force option', input: payload('git push --no-force-with-lease origin main'), expect: 0 },
  { name: 'git push --delete is blocked', input: payload('git push --delete origin main'), expect: 2 },
  { name: 'git push -d is blocked', input: payload('git push -d origin main'), expect: 2 },
  { name: 'empty-source branch deletion refspec is blocked', input: payload('git push origin :main'), expect: 2 },
  { name: 'git push --prune is blocked', input: payload('git push --prune origin'), expect: 2 },
  { name: 'git push --mirror is blocked', input: payload('git push --mirror origin'), expect: 2 },
  { name: 'ordinary source-to-destination refspec is allowed', input: payload('git push origin HEAD:main'), expect: 0 },
  { name: 'git -C before destructive push is blocked', input: payload('git -C C:\\repo push --delete origin main'), expect: 2 },
  { name: 'quoted git -C path before destructive push is blocked', input: payload('git -C "C:\\repo with spaces" push --force origin main'), expect: 2 },
  { name: 'git -c before destructive push is blocked', input: payload('git -c remote.origin.mirror=true push --mirror origin'), expect: 2 },
  { name: 'git -c mirror override blocks otherwise ordinary push', input: payload('git -c remote.origin.mirror=true push origin HEAD:main'), expect: 2 },
  { name: 'quoted git -c mirror override with -C is blocked', input: payload('git -C "C:\\repo with spaces" -c "remote.backup.mirror=yes" push backup main'), expect: 2 },
  { name: 'git -c mirror override accepts boolean on synonym', input: payload('git -c remote.origin.mirror=on push origin main'), expect: 2 },
  { name: 'git -c false mirror override does not block ordinary push', input: payload('git -c remote.origin.mirror=false push origin HEAD:main'), expect: 0 },
  { name: 'last git -c mirror override controls matching remote', input: payload('git -c remote.origin.mirror=true -c remote.origin.mirror=no push origin HEAD:main'), expect: 0 },
  { name: 'git -c mirror override does not block non-push command', input: payload('git -c remote.origin.mirror=true status'), expect: 0 },
  { name: 'git --git-dir before destructive push is blocked', input: payload('git --git-dir=C:\\repo\\.git push --mirror origin'), expect: 2 },
  { name: 'git -C before destructive reset is blocked', input: payload('git -C C:\\repo reset --hard HEAD~1'), expect: 2 },
  { name: 'git -C before ordinary status is allowed', input: payload('git -C C:\\repo status'), expect: 0 },
  { name: 'git push force refspec is blocked', input: payload('git push origin +main'), expect: 2 },
  { name: 'robocopy /MIR is blocked', input: payload('robocopy C:\\src C:\\dst /MIR'), expect: 2 },
  { name: 'rsync --delete is blocked', input: payload('rsync -av --delete src/ dst/'), expect: 2 },
  { name: 'DROP TABLE is blocked', input: payload('psql -c "DROP TABLE users;"'), expect: 2 },
  { name: 'ordinary ls is allowed', input: payload('ls -la'), expect: 0 },
  { name: 'ordinary git status is allowed', input: payload('git status'), expect: 0 },
  { name: 'single-file rm without recursion is allowed', input: payload('rm old-notes.txt'), expect: 0 },
  { name: 'single-file Remove-Item is allowed', input: payload('Remove-Item C:\\temp\\cache.txt'), expect: 0 },
  { name: 'ordinary Get-ChildItem is allowed', input: payload('Get-ChildItem -Path C:\\temp'), expect: 0 },
  { name: 'plugin configuration false disables enforcement', input: payload('git reset --hard origin/main'), env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: 'false' }, expect: 0 },
  { name: 'plugin configuration true keeps enforcement enabled', input: payload('git reset --hard origin/main'), env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: 'true' }, expect: 2 },
  { name: 'invalid payload JSON fails closed', input: '{not-json', expect: 2 },
  { name: 'missing tool_input fails closed', input: JSON.stringify({ tool_name: 'Bash' }), expect: 2 },
  { name: 'missing command fails closed', input: JSON.stringify({ tool_name: 'Bash', tool_input: {} }), expect: 2 },
  { name: 'explicit environment override remains observable', input: payload('rm -rf /whatever'), env: { CHWEZI_GATEGUARD: 'off' }, expect: 0 },
];

let failures = 0;
for (const testCase of cases) {
  const result = run(testCase.input, testCase.env || {});
  const passed = result.code === testCase.expect;
  console.log(`${passed ? 'PASS' : 'FAIL'} — ${testCase.name} (expected exit ${testCase.expect}, got ${result.code})`);
  if (!passed) {
    failures += 1;
    if (result.stderr) console.log(`       stderr: ${result.stderr.split('\n')[0]}`);
  }
}

console.log(`\n${cases.length - failures}/${cases.length} passed`);
process.exit(failures > 0 ? 1 : 0);
