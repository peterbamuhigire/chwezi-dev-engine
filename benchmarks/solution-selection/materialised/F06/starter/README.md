# Eligibility API (synthetic fixture)

`eligibility/rules.py` repeats the same policy checks in three functions. The public contract
is pinned: return values, exception types and messages, and the order of audit events
(`AuditLog.events`) must not change. Run the tests with
`python -m unittest discover -s public_tests -t .`.
