'use strict';
// Existing route: customer import (header: customer_id,name,phone).
const { parse } = require('../lib/csv-parse');

const HEADER = ['customer_id', 'name', 'phone'];
const LIMITS = { maxRecordChars: 2048, maxInputChars: 1000000 };

function importCustomers(text) {
  const { records, errors } = parse(text, LIMITS);
  const rows = [];
  const problems = [...errors];
  if (records.length === 0 || records[0].fields.join(',') !== HEADER.join(',')) {
    return { rows, errors: [{ line: 1, message: `header must be ${HEADER.join(',')}` }, ...problems] };
  }
  for (const { line, fields } of records.slice(1)) {
    if (fields.length !== HEADER.length) { problems.push({ line, message: `expected ${HEADER.length} fields, got ${fields.length}` }); continue; }
    if (!fields[0].trim()) { problems.push({ line, message: 'customer_id is empty' }); continue; }
    rows.push({ customer_id: fields[0].trim(), name: fields[1], phone: fields[2] });
  }
  return { rows, errors: problems.sort((a, b) => a.line - b.line) };
}

module.exports = { importCustomers };
