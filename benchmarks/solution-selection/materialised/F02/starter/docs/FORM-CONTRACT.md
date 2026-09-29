# Settings form contract: renewal date

- The renewal date is a civil calendar date. It has no time and no time zone.
- The browser submits it as `YYYY-MM-DD`. An empty value means "no renewal date" and must be kept
  as an explicit absence.
- The server is the authority: it rejects anything that is not a real `YYYY-MM-DD` date, even when
  the client-side control was bypassed.
- The stored value and the value shown back in the form must be the same date for every user,
  whatever their UTC offset.
- The field must stay usable from the keyboard and by assistive technology: visible label,
  help text and error message programmatically associated with the control.
- Supported browsers all ship a native date control; the project avoids adding UI dependencies
  where the platform already provides the control.
