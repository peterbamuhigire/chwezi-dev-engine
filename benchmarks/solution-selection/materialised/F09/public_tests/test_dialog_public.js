'use strict';
// Public happy-path tests: node public_tests/test_dialog_public.js
const assert = require('node:assert/strict');
const path = require('node:path');
const { buildPage } = require('./fake-dom.js');
const { createConfirmDialog } = require(path.join(__dirname, '..', 'web', 'dialog-controller.js'));

function setup(perform) {
  const page = buildPage();
  let n = 0;
  const calls = [];
  const controller = createConfirmDialog({
    document: page.document, trigger: page.trigger, dialog: page.dialog,
    confirmButton: page.confirmButton, cancelButton: page.cancelButton, errorRegion: page.errorRegion,
    fallbackFocus: page.heading, makeKey: () => `op-${(n += 1)}`,
    perform: (key) => { calls.push(key); return perform(key); },
  });
  page.trigger.focus();
  return { page, controller, calls };
}

const cases = [
  ['opening moves focus into the dialog', async () => {
    const { page, controller } = setup(async () => {});
    controller.open();
    assert.equal(page.dialog.hidden, false);
    assert.ok(page.dialog.contains(page.document.activeElement));
  }],
  ['cancel returns focus to the trigger', async () => {
    const { page, controller } = setup(async () => {});
    controller.open();
    controller.cancel();
    assert.equal(page.dialog.hidden, true);
    assert.equal(page.document.activeElement, page.trigger);
  }],
  ['successful deletion closes and returns focus', async () => {
    const { page, controller, calls } = setup(async () => {});
    controller.open();
    await controller.confirm();
    assert.equal(calls.length, 1);
    assert.equal(page.dialog.hidden, true);
    assert.equal(page.document.activeElement, page.trigger);
  }],
];

(async () => {
  let failed = 0;
  for (const [name, run] of cases) {
    try { await run(); console.log(`ok - ${name}`); } catch (error) { failed += 1; console.log(`not ok - ${name}: ${error.message}`); }
  }
  process.exitCode = failed ? 1 : 0;
})();
