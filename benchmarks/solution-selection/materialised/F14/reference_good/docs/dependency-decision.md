# Dependency decision: keep vetted_crypto

Decision: retain `vetted_crypto` 3.2.1. The proposal to remove it is rejected.

Reason: removing it would mean hand-writing password hashing (salted, memory-hard scrypt with a
constant-time comparison) and token verification (algorithm allow-list that refuses `none` and
algorithm confusion, key-id lookup for rotation, issuer, audience, expiry and not-before checks).
Each of those is a known source of security defects when re-implemented, and the saving is one
line in `requirements.lock`.

What was simplified instead: the forwarding adapters, the factory and the duplicated username
normalisers in `auth/service.py`, and the validator/runner classes in `auth/user_import.py`. The
stdlib `csv` module stays as the CSV parser because hand splitting breaks quoted fields.

Removal trigger: revisit only if the platform provides an audited equivalent with the same policy
checks, or if `vetted_crypto` loses maintenance or security support.
