# 0001 Scheduling date input: reuse the range calendar, not the native date input

Status: accepted

## Options

1. Two native `<input type="date">` fields (first day, last day).
2. The existing accessible `components/range_calendar.py` component.

## Evaluation against docs/SCHEDULING-REQUIREMENTS.md

- Range semantics: native inputs are two unrelated fields; the component is one grid with
  `aria-multiselectable` and selected days.
- Blackout reasons: the native control cannot mark individual days as unavailable or explain why;
  `min`/`max` only bound the ends. The component keeps unavailable days focusable, marks them
  `aria-disabled` and links each to its visible reason.
- Keyboard exploration: the native picker differs by browser and hides reasons; the component has a
  roving tabindex with arrow keys, already tested on the rota screen.
- Locale: native inputs display in the browser locale; the product needs the account locale. The
  component formats labels and the range summary with `components/locale_format.py`.

## Decision

Reuse the range calendar. It adds no new dependency. The server still validates every range,
including ranges that span a blackout period.

## Revisit when

Browsers ship a native range picker that can annotate unavailable days accessibly.
