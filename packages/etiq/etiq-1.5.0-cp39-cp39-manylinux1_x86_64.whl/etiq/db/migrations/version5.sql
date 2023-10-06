-- Add "parent_id" column to the segment table.
PRAGMA foreign_keys=off;
CREATE TABLE segment_new (
    id INTEGER NOT NULL,
    parent_id INTEGER,
    scan_id INTEGER,
    name VARCHAR,
    business_rule VARCHAR,
    volume FLOAT,
    volume_percent_total FLOAT,
    PRIMARY KEY (id),
    FOREIGN KEY(scan_id) REFERENCES scan (id),
    FOREIGN KEY(parent_id) REFERENCES segment (id)
);

-- SQLITE recommends this order:
INSERT INTO segment_new SELECT id,NULL,scan_id,name,business_rule,volume,volume_percent_total FROM segment;
DROP TABLE segment;
ALTER TABLE segment_new RENAME TO segment;
PRAGMA foreign_keys=on;
