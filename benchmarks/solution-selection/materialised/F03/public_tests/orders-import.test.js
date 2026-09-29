'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { importOrders, exportOrdersSheet } = require('../routes/orders-import');

test('imports simple orders', () => {
  const { rows, errors } = importOrders('order_id,customer_id,amount,note\nO-1,C-7,12.50,first order\nO-2,C-9,3,\n');
  assert.deepEqual(errors, []);
  assert.deepEqual(rows, [
    { order_id: 'O-1', customer_id: 'C-7', amount_minor: 1250, note: 'first order' },
    { order_id: 'O-2', customer_id: 'C-9', amount_minor: 300, note: '' },
  ]);
});

test('rejects a row with a missing field', () => {
  const { rows, errors } = importOrders('order_id,customer_id,amount,note\nO-1,C-7,12.50\n');
  assert.equal(rows.length, 0);
  assert.equal(errors.length, 1);
});

test('exports a sheet with a header', () => {
  const text = exportOrdersSheet([{ order_id: 'O-1', customer_id: 'C-7', amount_minor: 1250, note: 'first order' }]);
  assert.equal(text.split(/\r?\n/)[0], 'order_id,customer_id,amount,note');
  assert.match(text, /O-1,C-7,12\.50,first order/);
});
