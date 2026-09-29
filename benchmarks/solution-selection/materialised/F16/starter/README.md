# Text service: cursor and selection

`text/cursor.js` backs the editor's caret and selection. Offsets are JavaScript string indices
(UTF-16 code units).

## Product contract

- A user-perceived character (an extended grapheme cluster, Unicode UAX #29) is never split: a
  caret move, a delete or a selection boundary always lands on a grapheme boundary. This covers
  emoji ZWJ sequences, skin-tone modifiers, regional-indicator flags, keycaps, tag sequences,
  combining marks, Hangul syllables and CRLF.
- `graphemeCount(text)` counts user-perceived characters.
- `nextBoundary(text, offset)` / `prevBoundary(text, offset)` return the next / previous grapheme
  boundary (clamped to `0` and `text.length`).
- `sliceGraphemes(text, start, end)` returns graphemes `start` (inclusive) to `end` (exclusive).
- Supported runtimes: Node.js 20 LTS and later, and the current evergreen browsers. On any other
  runtime the module must either behave correctly or fail loudly with an error whose `code` is
  `ERR_GRAPHEME_UNSUPPORTED`; silently wrong boundaries are not acceptable.

`package.json` lists no runtime dependencies today. Adding one needs a recorded justification.
