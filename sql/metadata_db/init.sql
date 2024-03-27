CREATE TABLE IF NOT EXISTS snapshots_metadata
(
    id         SERIAL PRIMARY KEY,
    created_on TIMESTAMP,
    file_name  VARCHAR(1020)
);