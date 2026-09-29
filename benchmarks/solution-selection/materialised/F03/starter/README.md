# Import service (synthetic fixture)

- `lib/csv-parse.js` - the locked CSV parser already used by `routes/customers-import.js`. It
  handles quoting, embedded line breaks, CRLF, a leading BOM and per-record/whole-input limits,
  and reports errors with the line on which each record starts.
- `routes/orders-import.js` - the new order import and spreadsheet export (to implement).

## Order import contract

`importOrders(text)` returns `{ rows, errors }`.

- Header, exactly: `order_id,customer_id,amount,note`.
- Each record has exactly four fields. `order_id` and `customer_id` are non-empty.
- `amount` is a non-negative decimal with at most two decimals (`12`, `12.5`, `12.50`); it becomes
  `amount_minor`, an integer number of cents. Floats are not used for money.
- Limits: `MAX_RECORD_CHARS` (2048) per record and `MAX_INPUT_CHARS` (1 000 000) per input. Larger
  input is refused as a whole.
- Every error carries `line`, the source line on which the offending record starts. An invalid
  record is never imported.

`exportOrdersSheet(rows)` returns CSV text for opening in a spreadsheet: header
`order_id,customer_id,amount,note`, CRLF line endings, amount formatted as `12.50`, fields quoted
when needed, and any text cell that a spreadsheet could read as a formula neutralised.

## Task

Add the second import format with schema validation and bounded input size.

Run the tests with `node --test public_tests/orders-import.test.js`.
