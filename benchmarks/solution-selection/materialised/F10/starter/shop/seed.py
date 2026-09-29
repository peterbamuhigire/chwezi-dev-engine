"""Small synthetic data set with the legacy data problems found in production."""
from __future__ import annotations

import sqlite3

CUSTOMERS = [
    (1, "ACME", "Acme Traders"),
    (2, "BETA", "Beta Stores"),
    (3, "acme ", "Acme Traders (duplicate record)"),
    (4, "GAMMA", "Gamma Ltd"),
]
ORDERS = [
    (1, "BETA", 12000),
    (2, " beta", 5000),
    (3, "ACME", 7000),
    (4, "ZETA", 3000),
    (5, None, 1500),
    (6, "GAMMA", 9900),
    (7, "", 100),
]


def seed(conn: sqlite3.Connection) -> None:
    conn.executemany("INSERT INTO customers (id, code, name) VALUES (?, ?, ?)", CUSTOMERS)
    conn.executemany("INSERT INTO orders (id, legacy_customer_code, amount_minor) VALUES (?, ?, ?)", ORDERS)
