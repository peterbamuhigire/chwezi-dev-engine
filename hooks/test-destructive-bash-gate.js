#!/usr/bin/env node
/**
 * Direct tests for destructive-bash-gate.js.
 * Run: node hooks/test-destructive-bash-gate.js
 */

'use strict';

const { spawnSync } = require('child_process');
const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const HOOK = path.join(__dirname, 'destructive-bash-gate.js');

function run(input, env = {}) {
  let cwd = process.cwd();
  try {
    cwd = JSON.parse(input).cwd || cwd;
  } catch (error) {
    // Malformed payload fixtures still run from the current test directory.
  }
  const result = spawnSync(process.execPath, [HOOK], {
    input,
    encoding: 'utf8',
    cwd,
    env: { ...process.env, ...env },
  });
  return { code: result.status, stderr: result.stderr };
}

function payload(command, cwd = process.cwd()) {
  return JSON.stringify({ cwd, tool_name: 'Bash', tool_input: { command } });
}

const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'chwezi-git-mirror-gate-'));
const mirrorRepo = path.join(fixtureRoot, 'mirror-repo');
const ordinaryRepo = path.join(fixtureRoot, 'ordinary-repo');
const globalConfig = path.join(fixtureRoot, 'global-gitconfig');
fs.mkdirSync(mirrorRepo);
fs.mkdirSync(ordinaryRepo);
execFileSync('git', ['-C', mirrorRepo, 'init', '-q']);
execFileSync('git', ['-C', mirrorRepo, 'config', 'remote.origin.url', 'https://example.invalid/mirror.git']);
execFileSync('git', ['-C', mirrorRepo, 'config', 'remote.origin.mirror', 'true']);
execFileSync('git', ['-C', ordinaryRepo, 'init', '-q']);
execFileSync('git', ['-C', ordinaryRepo, 'config', 'remote.origin.url', 'https://example.invalid/ordinary.git']);
fs.writeFileSync(globalConfig, '[remote "origin"]\n\tmirror = true\n');

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
  { name: 'effective repository mirror config blocks ordinary-looking push', input: payload('git push origin HEAD:main', mirrorRepo), expect: 2 },
  { name: 'effective global mirror config blocks ordinary-looking push', input: payload('git push origin HEAD:main', ordinaryRepo), env: { GIT_CONFIG_GLOBAL: globalConfig, GIT_CONFIG_NOSYSTEM: '1' }, expect: 2 },
  { name: 'git -C repository mirror config blocks push', input: payload(`git -C "${mirrorRepo}" push origin HEAD:main`, ordinaryRepo), expect: 2 },
  { name: 'literal cd before push checks the changed repository config', input: payload(`cd "${mirrorRepo}" && git push origin HEAD:main`, ordinaryRepo), expect: 2 },
  { name: 'pipeline directory change makes push configuration unknown and blocks', input: payload(`cd "${mirrorRepo}" | git push origin HEAD:main`, ordinaryRepo), expect: 2 },
  { name: 'explicit false command override disables repository mirror setting', input: payload(`git -C "${mirrorRepo}" -c remote.origin.mirror=false push origin HEAD:main`, ordinaryRepo), expect: 0 },
  { name: 'ordinary repository push remains allowed', input: payload('git push origin HEAD:main', ordinaryRepo), expect: 0 },
  { name: 'unrelated unresolved cd does not block a command without Git push', input: payload('cd C:\\path-that-does-not-exist'), expect: 0 },
  { name: 'later push in a compound command is still checked for mirror config', input: payload(`git -C "${ordinaryRepo}" push origin HEAD:main && git -C "${mirrorRepo}" push origin HEAD:main`, ordinaryRepo), expect: 2 },
  { name: 'inherited Git config environment mirror override blocks push', input: payload('git push origin HEAD:main', ordinaryRepo), env: { GIT_CONFIG_COUNT: '1', GIT_CONFIG_KEY_0: 'remote.origin.mirror', GIT_CONFIG_VALUE_0: 'true' }, expect: 2 },
  { name: 'git --config-env mirror override blocks push', input: payload('git --config-env=remote.origin.mirror=CHWEZI_TEST_MIRROR push origin HEAD:main', ordinaryRepo), env: { CHWEZI_TEST_MIRROR: 'yes' }, expect: 2 },
  { name: 'missing cwd fails closed for push configuration check', input: JSON.stringify({ tool_name: 'Bash', tool_input: { command: 'git push origin HEAD:main' } }), expect: 2 },
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
fs.rmSync(fixtureRoot, { recursive: true, force: true });
process.exit(failures > 0 ? 1 : 0);
