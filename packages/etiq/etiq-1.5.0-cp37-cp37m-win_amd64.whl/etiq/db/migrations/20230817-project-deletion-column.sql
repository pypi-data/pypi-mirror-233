
ALTER TABLE project ADD COLUMN deleted BOOLEAN;
UPDATE project SET deleted = false;
