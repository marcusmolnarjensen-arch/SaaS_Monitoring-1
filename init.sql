CREATE TABLE IF NOT EXISTS monitoring_results (
    id SERIAL PRIMARY KEY,
    website_url TEXT NOT NULL,
    status_code INTEGER,
    is_online BOOLEAN,
    response_time_ms INTEGER,
    is_healthy BOOLEAN,
    checked_at TIMESTAMPTZ DEFAULT now()
);