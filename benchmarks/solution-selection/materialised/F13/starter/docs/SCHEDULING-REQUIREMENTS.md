# Scheduling requirements

1. A booking is a date range: first day and last day, inclusive.
2. Blackout periods (`scheduling/blackouts.py`) cannot be booked, and a range may not include
   any blackout day. People must be able to find out *why* a day is unavailable before they
   submit, including keyboard and screen-reader users.
3. People explore the month with the keyboard to find a free range.
4. Dates are displayed in the account's locale (`en-GB`, `en-US`, `fr-FR`), which can differ
   from the browser's locale. The submitted values are ISO `YYYY-MM-DD`.
5. The server validates every range; the page is not trusted.
6. The team normally prefers native controls. For this feature, evaluate the native date input
   against these requirements instead of assuming it wins, and record the decision in
   `docs/decisions/`. `components/range_calendar.py` is the accessible range component already
   used and tested on the rota screen.
