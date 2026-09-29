# Customer reporting service (synthetic fixture)

- `core/identifiers.py` owns customer-identifier normalisation (`canonical_id`). It is the shared
  contract; `billing/invoices.py` and `crm/lookup.py` already call it.
- `reports/customer_report.py` builds the monthly customer balance report.

Run the tests with `python -m unittest discover -s public_tests -t .`.
