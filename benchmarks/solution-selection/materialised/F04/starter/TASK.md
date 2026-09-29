# Catalogue service: saved filters

The catalogue lists and reads items through the query layer in `catalogue/query.py`.
Product has asked for persistent, per-user saved filters.

Interface the rest of the service (and its tests) will call:

- New module `catalogue/saved_filters.py` exposing:
  - `create_filter(q, user_id, name, spec) -> dict` returning `{"id", "user_id", "name", "spec"}`;
  - `list_filters(q, user_id) -> list[dict]` ordered by `id`;
  - `get_filter(q, user_id, filter_id) -> dict`;
  - `delete_filter(q, user_id, filter_id) -> None`;
  - exceptions `InvalidFilter` (a `ValueError`), `DuplicateFilter` and `FilterNotFound` (a `LookupError`).
- `q` is a `catalogue.query.QueryLayer`. Writes go through `QueryLayer.execute` inside
  `QueryLayer.transaction()`; rows live in a table named `saved_filters` created by
  `catalogue.db.init_schema`.
- `spec` is a non-empty object with only these optional keys: `category` (string), `text`
  (string), `min_price` and `max_price` (non-negative integers in minor units, with
  `min_price <= max_price` when both are present). A `name` is a non-empty string of at most
  80 characters.
- `(user_id, name)` is the create key: repeating a create with the same spec returns the
  original filter; the same name with a different spec raises `DuplicateFilter`.
- A user can never read or delete another user's filter; asking for one raises
  `FilterNotFound`, exactly as for a missing filter.
- When a user is deleted (`catalogue.users.delete_user`), that user's filters go with them.
