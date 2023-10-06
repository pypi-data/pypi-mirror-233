DROP TABLE chartsubmission;
CREATE TABLE chartsubmission (
    id INTEGER NOT NULL,
    hash VARCHAR,
    created TIMESTAMP,
    summary JSON,
    PRIMARY KEY (id)
)
