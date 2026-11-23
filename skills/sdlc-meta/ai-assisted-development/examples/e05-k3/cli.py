#!/usr/bin/env python3
"""Small SQLite ticket-import example for the K3 retry case."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys


class EventConflict(Exception):
    pass


class InjectedFailure(Exception):
    pass


def deliver(
    connection: sqlite3.Connection,
    event_id: str,
    ticket_id: str,
    status: str,
    implementation: str,
    fail_before_history: bool,
) -> dict[str, str]:
    connection.execute("BEGIN IMMEDIATE")
    try:
        ticket = connection.execute(
            "SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()
        if ticket is None:
            raise ValueError(f"unknown ticket: {ticket_id}")

        if implementation == "baseline":
            _record(connection, event_id, ticket_id, status, fail_before_history)
            outcome = "created"
        elif implementation == "ticket-level-dedupe":
            has_history = connection.execute(
                "SELECT 1 FROM history WHERE ticket_id = ? LIMIT 1", (ticket_id,)
            ).fetchone()
            if has_history:
                outcome = "suppressed"
            else:
                _record(connection, event_id, ticket_id, status, fail_before_history)
                outcome = "created"
        else:
            existing = connection.execute(
                "SELECT ticket_id, status FROM delivered_events WHERE event_id = ?",
                (event_id,),
            ).fetchone()
            if existing is not None:
                if existing != (ticket_id, status):
                    raise EventConflict(
                        f"event {event_id!r} was already used with a different payload"
                    )
                outcome = "replayed"
            else:
                connection.execute(
                    "INSERT INTO delivered_events(event_id, ticket_id, status) "
                    "VALUES (?, ?, ?)",
                    (event_id, ticket_id, status),
                )
                if fail_before_history:
                    raise InjectedFailure("injected failure before history insert")
                _write_history(connection, event_id, ticket_id, status)
                connection.execute(
                    "UPDATE tickets SET status = ? WHERE ticket_id = ?",
                    (status, ticket_id),
                )
                outcome = "created"
        connection.commit()
        return {
            "event_id": event_id,
            "implementation": implementation,
            "outcome": outcome,
            "status": status,
            "ticket_id": ticket_id,
        }
    except Exception:
        connection.rollback()
        raise


def _record(
    connection: sqlite3.Connection,
    event_id: str,
    ticket_id: str,
    status: str,
    fail_before_history: bool,
) -> None:
    if fail_before_history:
        raise InjectedFailure("injected failure before history insert")
    _write_history(connection, event_id, ticket_id, status)
    connection.execute(
        "UPDATE tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id)
    )


def _write_history(
    connection: sqlite3.Connection, event_id: str, ticket_id: str, status: str
) -> None:
    connection.execute(
        "INSERT INTO history(ticket_id, status, source_event_id) VALUES (?, ?, ?)",
        (ticket_id, status, event_id),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="path to an initialized SQLite fixture")
    parser.add_argument("--event", required=True, help="delivery event ID")
    parser.add_argument("--ticket", required=True, help="ticket ID")
    parser.add_argument("--status", required=True, help="requested ticket status")
    parser.add_argument(
        "--implementation",
        choices=("fixed", "baseline", "ticket-level-dedupe"),
        default="fixed",
        help="teaching variant (default: fixed)",
    )
    parser.add_argument(
        "--fail-before-history",
        action="store_true",
        help="inject a transactional failure after the fixed key insert",
    )
    args = parser.parse_args(argv)
    if not all((args.event.strip(), args.ticket.strip(), args.status.strip())):
        parser.error("--event, --ticket and --status must be non-empty")

    try:
        connection = sqlite3.connect(args.db, timeout=10.0)
        connection.execute("PRAGMA foreign_keys = ON")
        result = deliver(
            connection,
            args.event,
            args.ticket,
            args.status,
            args.implementation,
            args.fail_before_history,
        )
        print(json.dumps(result, sort_keys=True))
        return 0
    except EventConflict as exc:
        print(f"conflict: {exc}", file=sys.stderr)
        return 3
    except (InjectedFailure, sqlite3.Error, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 4
    finally:
        if "connection" in locals():
            connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
