'use strict';
// Order import and spreadsheet export. Parsing reuses the locked lib/csv-parse.js (already used by
// routes/customers-import.js), which handles quoting, embedded line breaks, BOM and size limits.
const { parse } = require('../lib/csv-parse');

const HEADER = ['order_id', 'customer_id', 'amount', 'note'];
const MAX_RECORD_CHARS = 2048;
const MAX_INPUT_CHARS = 1000000;
const AMOUNT = /^(\d{1,12})(?:\.(\d{1,2}))?$/;
const FORMULA_START = /^[=+\-@\t\r]/;

function toMinor(text) {
  const match = AMOUNT.exec(text);
  if (!match) return null;
  return Number(match[1]) * 100 + Number((match[2] || '').padEnd(2, '0'));
}

function importOrders(text) {
  if (typeof text !== 'string') throw new TypeError('text must be a string');
  const { records, errors } = parse(text, { maxRecordChars: MAX_RECORD_CHARS, maxInputChars: MAX_INPUT_CHARS });
  const problems = [...errors];
  if (problems.some((e) => e.line === 0)) return { rows: [], errors: problems };
  if (records.length === 0 || records[0].line !== 1 || records[0].fields.join(',') !== HEADER.join(',')) {
    return { rows: [], errors: [{ line: 1, message: `header must be ${HEADER.join(',')}` }] };
  }
  const rows = [];
  for (const { line, fields } of records.slice(1)) {
    if (fields.length !== HEADER.length) { problems.push({ line, message: `expected ${HEADER.length} fields, got ${fields.length}` }); continue; }
    const [orderId, customerId, amount, note] = fields;
    if (!orderId.trim() || !customerId.trim()) { problems.push({ line, message: 'order_id and customer_id are required' }); continue; }
    const amountMinor = toMinor(amount.trim());
    if (amountMinor === null) { problems.push({ line, message: `invalid amount ${JSON.stringify(amount)}` }); continue; }
    rows.push({ order_id: orderId.trim(), customer_id: customerId.trim(), amount_minor: amountMinor, note });
  }
  return { rows, errors: problems.sort((a, b) => a.line - b.line) };
}

function cell(value) {
  let text = String(value ?? '');
  if (FORMULA_START.test(text)) text = `'${text}`;
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

function formatMinor(minor) {
  if (!Number.isSafeInteger(minor) || minor < 0) throw new RangeError(`invalid amount_minor ${minor}`);
  return `${Math.floor(minor / 100)}.${String(minor % 100).padStart(2, '0')}`;
}

function exportOrdersSheet(rows) {
  const lines = [HEADER.join(',')];
  for (const row of rows) {
    lines.push([cell(row.order_id), cell(row.customer_id), formatMinor(row.amount_minor), cell(row.note)].join(','));
  }
  return `${lines.join('\r\n')}\r\n`;
}

module.exports = { importOrders, exportOrdersSheet, MAX_RECORD_CHARS, MAX_INPUT_CHARS };
