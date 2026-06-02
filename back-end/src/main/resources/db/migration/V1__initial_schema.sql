CREATE TABLE alerts (
    alert_id VARCHAR(36) PRIMARY KEY,
    source VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    severity VARCHAR(50) NOT NULL,
    description VARCHAR(2000) NOT NULL,
    src_ip VARCHAR(255) NOT NULL,
    dest_ip VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    event_type VARCHAR(255) NOT NULL,
    raw_data JSONB,
    score DOUBLE PRECISION,
    model_version VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_alert_severity ON alerts(severity);
CREATE INDEX idx_alert_timestamp ON alerts(timestamp);
CREATE INDEX idx_alert_source ON alerts(source);