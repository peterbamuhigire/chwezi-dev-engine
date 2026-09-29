'use strict';

// Grapheme-aware caret helpers. Offsets are UTF-16 code unit indices.
// Uses the runtime's native Intl.Segmenter (ICU, UAX #29); see DEPENDENCY-DECISION.md.
// Runtimes without it fail loudly with ERR_GRAPHEME_UNSUPPORTED rather than returning
// code-point boundaries that would split emoji sequences and combining marks.

function unsupported() {
  const error = new Error('Grapheme segmentation needs Intl.Segmenter (Node.js 20+ or an evergreen browser).');
  error.code = 'ERR_GRAPHEME_UNSUPPORTED';
  return error;
}

let segmenter = null;
function getSegmenter() {
  if (segmenter) return segmenter;
  if (typeof Intl === 'undefined' || typeof Intl.Segmenter !== 'function') throw unsupported();
  segmenter = new Intl.Segmenter(undefined, { granularity: 'grapheme' });
  return segmenter;
}

/** Start offsets of every grapheme, followed by text.length. */
function boundaries(text) {
  const starts = Array.from(getSegmenter().segment(text), (segment) => segment.index);
  starts.push(text.length);
  return starts;
}

function graphemeCount(text) {
  return boundaries(text).length - 1;
}

function nextBoundary(text, offset) {
  const found = boundaries(text).find((index) => index > offset);
  return found === undefined ? text.length : found;
}

function prevBoundary(text, offset) {
  const before = boundaries(text).filter((index) => index < offset);
  return before.length ? before[before.length - 1] : 0;
}

function sliceGraphemes(text, start, end) {
  const marks = boundaries(text);
  const last = marks.length - 1;
  const clamp = (value) => Math.max(0, Math.min(last, value));
  return text.slice(marks[clamp(start)], marks[clamp(end === undefined ? last : end)]);
}

module.exports = { graphemeCount, nextBoundary, prevBoundary, sliceGraphemes };
