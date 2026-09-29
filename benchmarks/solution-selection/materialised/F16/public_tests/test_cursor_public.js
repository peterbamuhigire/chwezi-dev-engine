'use strict';
// Public happy-path tests: node public_tests/test_cursor_public.js
const assert = require('node:assert/strict');
const path = require('node:path');
const cursor = require(path.join(__dirname, '..', 'text', 'cursor.js'));

const cases = [
  ['ascii count', () => assert.equal(cursor.graphemeCount('Kampala'), 7)],
  ['precomposed accent', () => assert.equal(cursor.graphemeCount('café'), 4)],
  ['single emoji is one character', () => assert.equal(cursor.graphemeCount('ok \u{1F600}'), 4)],
  ['next boundary over emoji', () => assert.equal(cursor.nextBoundary('\u{1F600}x', 0), 2)],
  ['previous boundary over emoji', () => assert.equal(cursor.prevBoundary('x\u{1F600}', 3), 1)],
  ['slice', () => assert.equal(cursor.sliceGraphemes('Gulu town', 0, 4), 'Gulu')],
];

let failed = 0;
for (const [name, run] of cases) {
  try { run(); console.log(`ok - ${name}`); } catch (error) { failed += 1; console.log(`not ok - ${name}: ${error.message}`); }
}
process.exitCode = failed ? 1 : 0;
