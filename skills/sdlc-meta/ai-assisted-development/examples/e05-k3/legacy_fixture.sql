PRAGMA foreign_keys = ON;

CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY,
    status TEXT NOT NULL
);

CREATE TABLE history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id),
    status TEXT NOT NULL,
    source_event_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE delivered_events (
    event_id TEXT PRIMARY KEY,
    ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id),
    status TEXT NOT NULL
);

INSERT INTO tickets(ticket_id, status) VALUES ('T1', 'open');

-- This row predates event IDs. Its null source_event_id is intentional.
INSERT INTO history(ticket_id, status, source_event_id)
VALUES ('T1', 'open', NULL);
