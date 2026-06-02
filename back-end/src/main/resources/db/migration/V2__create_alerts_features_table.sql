-- V2__create_alerts_features_table.sql
CREATE TABLE alerts_features (
    id                  BIGSERIAL PRIMARY KEY,
    alert_id            VARCHAR(36) NOT NULL UNIQUE REFERENCES alerts(alert_id) ON DELETE CASCADE,
    
    -- Time features
    hour_of_day         INT NOT NULL CHECK (hour_of_day BETWEEN 0 AND 23),
    day_of_week         INT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),  -- 0=Sunday
    is_weekend          BOOLEAN NOT NULL,
    
    -- One-hot encoded severity
    severity_low        BOOLEAN NOT NULL DEFAULT FALSE,
    severity_medium     BOOLEAN NOT NULL DEFAULT FALSE,
    severity_high       BOOLEAN NOT NULL DEFAULT FALSE,
    severity_critical   BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- One-hot top N event types (adjust N as needed)
    event_bruteforce    BOOLEAN NOT NULL DEFAULT FALSE,
    event_malware       BOOLEAN NOT NULL DEFAULT FALSE,
    event_ddos          BOOLEAN NOT NULL DEFAULT FALSE,
    event_phishing      BOOLEAN NOT NULL DEFAULT FALSE,
    event_scan          BOOLEAN NOT NULL DEFAULT FALSE,
    event_other         BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Numeric features (for future use)
    src_ip_entropy      DOUBLE PRECISION,
    description_length  INT NOT NULL,
    
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Critical indexes for ML queries
CREATE INDEX idx_alerts_features_hour ON alerts_features(hour_of_day);
CREATE INDEX idx_alerts_features_severity ON alerts_features USING btree(
    severity_low, severity_medium, severity_high, severity_critical
);
CREATE INDEX idx_alerts_features_event ON alerts_features USING btree(
    event_bruteforce, event_malware, event_ddos, event_phishing, event_scan, event_other
);