CREATE TABLE IF NOT EXISTS balance (
    id INTEGER NOT NULL,
    value INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    comment VARCHAR(30) DEFAULT '',
    PRIMARY KEY (id),
    FOREIGN KEY (account_id) REFERENCES account(id)
);

