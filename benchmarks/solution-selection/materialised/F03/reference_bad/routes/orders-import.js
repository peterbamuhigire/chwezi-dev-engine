'use strict';
// Order import and export: plain split, no extra module needed.

const MAX_RECORD_CHARS = 2048;
const MAX_INPUT_CHARS = 1000000;

function importOrders(text) {
  const rows = [];
  const errors = [];
  const lines = text.split('\n').filter((l) => l.trim() !== '');
  lines.slice(1).forEach((raw, index) => {
    const fields = raw.replace(/\r$/, '').split(',').map((f) => f.replace(/^"|"$/g, ''));
    const line = index + 2;
    if (fields.length !== 4) { errors.push({ line, message: 'wrong number of fields' }); return; }
    if (!/^\d+(\.\d{1,2})?$/.test(fields[2])) { errors.push({ line, message: 'bad amount' }); return; }
    rows.push({ order_id: fields[0], customer_id: fields[1], amount_minor: Math.round(parseFloat(fields[2]) * 100), note: fields[3] });
  });
  return { rows, errors };
}

function exportOrdersSheet(rows) {
  const out = ['order_id,customer_id,amount,note'];
  for (const r of rows) out.push([r.order_id, r.customer_id, (r.amount_minor / 100).toFixed(2), r.note].join(','));
  return out.join('\r\n') + '\r\n';
}

module.exports = { importOrders, exportOrdersSheet, MAX_RECORD_CHARS, MAX_INPUT_CHARS };
