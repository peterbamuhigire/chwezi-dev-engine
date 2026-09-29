# Time windows

All reporting, roll-up and export code uses `core.time_windows.in_window`.

- Windows are half-open: `[start, end)`. The lower bound is included; the upper bound is not.
- `start == end` is an empty window and contains nothing.
- `end < start` raises `InvalidWindow`.
- Naive and aware datetimes must never be compared silently; mixing them raises.

Known issue (ticket OPS-412): events landing exactly on an hourly boundary appear in two
roll-up buckets, and the API and exports disagree with the documented contract.
