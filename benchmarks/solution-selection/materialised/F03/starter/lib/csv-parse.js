'use strict';
/**
 * csv-parse (in-repo, locked since 2024; used by routes/customers-import.js).
 *
 * RFC 4180 parser: comma separator, double-quote quoting with "" escapes, quoted fields may hold
 * separators and line breaks, CRLF or LF record endings, optional leading UTF-8 BOM.
 *
 * parse(text, { maxRecordChars, maxInputChars }) returns
 *   { records: [{ line, fields }], errors: [{ line, message }] }
 * where `line` is the 1-based source line on which the record starts. A malformed or oversized
 * record is reported in `errors` and skipped; parsing continues with the next record. Input longer
 * than maxInputChars is refused before any parsing.
 */

class CsvError extends Error {
  constructor(line, message) {
    super(`line ${line}: ${message}`);
    this.line = line;
  }
}

function parse(text, options = {}) {
  const maxRecordChars = options.maxRecordChars ?? Infinity;
  const maxInputChars = options.maxInputChars ?? Infinity;
  if (typeof text !== 'string') throw new TypeError('csv text must be a string');
  if (text.length > maxInputChars) {
    return { records: [], errors: [{ line: 0, message: `input exceeds ${maxInputChars} characters` }] };
  }
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);

  const records = [];
  const errors = [];
  let i = 0;
  let line = 1;
  const n = text.length;

  while (i < n) {
    const startLine = line;
    const startIndex = i;
    const fields = [];
    let field = '';
    let problem = null;
    let atFieldStart = true;
    let inQuotes = false;
    let ended = false;

    while (i < n && !ended) {
      const ch = text[i];
      if (inQuotes) {
        if (ch === '"') {
          if (text[i + 1] === '"') { field += '"'; i += 2; continue; }
          inQuotes = false; i += 1;
          const next = text[i];
          if (i < n && next !== ',' && next !== '\n' && next !== '\r') { problem = problem || 'unexpected character after closing quote'; }
          continue;
        }
        if (ch === '\n') line += 1;
        field += ch; i += 1; continue;
      }
      if (ch === '"') {
        if (atFieldStart) { inQuotes = true; atFieldStart = false; i += 1; continue; }
        problem = problem || 'unexpected quote in unquoted field';
        field += ch; i += 1; continue;
      }
      if (ch === ',') { fields.push(field); field = ''; atFieldStart = true; i += 1; continue; }
      if (ch === '\r' || ch === '\n') {
        if (ch === '\r' && text[i + 1] === '\n') i += 1;
        i += 1; line += 1; ended = true; continue;
      }
      field += ch; atFieldStart = false; i += 1;
    }
    if (inQuotes) problem = 'unterminated quoted field';
    fields.push(field);
    const rawLength = i - startIndex;
    if (rawLength > maxRecordChars) problem = `record exceeds ${maxRecordChars} characters`;
    if (problem) {
      errors.push({ line: startLine, message: problem });
    } else if (!(fields.length === 1 && fields[0] === '')) {
      records.push({ line: startLine, fields });
    }
  }
  return { records, errors };
}

module.exports = { parse, CsvError };
