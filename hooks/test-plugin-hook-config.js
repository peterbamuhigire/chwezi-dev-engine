'use strict';

const assert = require('node:assert/strict');
const { isEnabled } = require('./plugin-hook-config');

const cases = [
  { name: 'unset config keeps hooks enabled', env: {}, expected: true },
  { name: 'true config keeps hooks enabled', env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: 'true' }, expected: true },
  { name: 'false config disables hooks', env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: 'false' }, expected: false },
  { name: 'false config matching is case-insensitive', env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: 'FALSE' }, expected: false },
  { name: 'common false values disable hooks', env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: 'off' }, expected: false },
  { name: 'unknown values fail enabled', env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: 'maybe' }, expected: true },
  { name: 'empty values preserve the default', env: { CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED: '' }, expected: true },
];

for (const testCase of cases) {
  assert.equal(isEnabled(testCase.env), testCase.expected, testCase.name);
  console.log(`PASS ${testCase.name}`);
}

console.log(`${cases.length}/${cases.length} passed`);
