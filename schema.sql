CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    ip_address TEXT,
    timestamp TEXT,
    event_type TEXT,
    attempt_count INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flagged_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER,
    reason TEXT,
    ai_explanation TEXT,
    severity TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (log_id) REFERENCES logs(id)
);