CREATE TABLE kafka_data (
    time TIMESTAMPTZ NOT NULL,
    topic TEXT,
    value DOUBLE PRECISION
);
SELECT create_hypertable('kafka_data', 'time');