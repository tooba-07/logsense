CREATE DATABASE logsense;
USE logsense;

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    ip_address VARCHAR(45),
    timestamp DATETIME,
    event_type VARCHAR(50),
    attempt_count INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flagged_incidents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_id INT,
    reason TEXT,
    ai_explanation TEXT,
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (log_id) REFERENCES logs(id)
);