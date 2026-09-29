'use strict';
// New route: order import and spreadsheet export. See README.md for the contract.

const MAX_RECORD_CHARS = 2048;
const MAX_INPUT_CHARS = 1000000;

function importOrders(text) {
  throw new Error('not implemented');
}

function exportOrdersSheet(rows) {
  throw new Error('not implemented');
}

module.exports = { importOrders, exportOrdersSheet, MAX_RECORD_CHARS, MAX_INPUT_CHARS };
