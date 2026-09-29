'use strict';

// Caret helpers that work on code points instead of code units, so emoji are not split.

function points(text) {
  return Array.from(text);
}

function graphemeCount(text) {
  return points(text).length;
}

function nextBoundary(text, offset) {
  let index = 0;
  for (const point of points(text)) {
    index += point.length;
    if (index > offset) return index;
  }
  return text.length;
}

function prevBoundary(text, offset) {
  let index = 0;
  let previous = 0;
  for (const point of points(text)) {
    if (index >= offset) break;
    previous = index;
    index += point.length;
  }
  return offset > 0 ? previous : 0;
}

function sliceGraphemes(text, start, end) {
  return points(text).slice(start, end).join('');
}

module.exports = { graphemeCount, nextBoundary, prevBoundary, sliceGraphemes };
