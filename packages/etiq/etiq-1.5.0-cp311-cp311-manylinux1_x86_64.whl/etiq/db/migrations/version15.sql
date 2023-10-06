
-- Table "user" is a reserved word in postgres.

-- Sqlalchemy will see the table "users" is missing and create it!

-- Remove existing demo user
DELETE FROM users;
-- Migrate data into new table
INSERT INTO users SELECT * FROM "user";
DROP TABLE user;
