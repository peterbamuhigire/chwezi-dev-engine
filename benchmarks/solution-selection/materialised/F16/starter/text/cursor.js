'use strict';

// Caret helpers. Offsets are UTF-16 code unit indices.

function graphemeCount(text) {
  return text.length;
}

function nextBoundary(text, offset) {
  return Math.min(text.length, offset + 1);
}

function prevBoundary(text, offset) {
  return Math.max(0, offset - 1);
}

function sliceGraphemes(text, start, end) {
  return text.slice(start, end);
}

module.exports = { graphemeCount, nextBoundary, prevBoundary, sliceGraphemes };
