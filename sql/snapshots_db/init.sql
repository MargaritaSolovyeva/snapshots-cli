CREATE TABLE IF NOT EXISTS snapshots
(
    user_id      INT PRIMARY KEY,
    name         VARCHAR(255),
    store_name   VARCHAR(255),
    credit_limit DECIMAL(10, 5)
);