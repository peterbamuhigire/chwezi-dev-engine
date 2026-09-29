# Dependency decision: grapheme segmentation

**Decision:** use the native `Intl.Segmenter` (granularity `grapheme`); add no package.

## Requirement

The product contract needs extended grapheme clusters (UAX #29): ZWJ emoji sequences, skin-tone
modifiers, flags, keycaps, tag sequences, combining marks, Hangul and CRLF. Code-unit and
code-point slicing both split these.

## Alternatives considered

| Option | Result |
|---|---|
| Code-unit indices (current code) | Splits surrogate pairs; rejected. |
| `Array.from` code points | Splits ZWJ sequences, flags and combining marks; rejected. |
| Hand-written UAX #29 rules | Large, changes with every Unicode release; rejected (ad hoc Unicode logic). |
| Native `Intl.Segmenter` | Implements UAX #29 through the runtime's ICU; chosen. |
| npm grapheme-splitting package | Would work, but duplicates a native facility on every supported runtime; not needed. |

## Licence and version evidence

- Native facility: Node.js ships ICU (Unicode licence) with full data; checked on the fixture host
  with `node -p "process.versions.icu + ' / Unicode ' + process.versions.unicode"`. Node.js 20 LTS
  and later expose `Intl.Segmenter`; evergreen Chromium, Firefox and WebKit do too.
- No third-party package is added, so no new licence enters `package.json`.

## Support boundary

Supported: Node.js 20+ and evergreen browsers. A runtime without `Intl.Segmenter` gets an error
with `code: 'ERR_GRAPHEME_UNSUPPORTED'` on first use (tested), never code-point boundaries.

## Removal trigger

Revisit if a supported runtime lacks `Intl.Segmenter` or ships ICU data that fails the frozen
corpus, or if the support matrix adds such a runtime. At that point, evaluate a mature, maintained
UAX #29 package (licence, release cadence, Unicode version) and record it here.
