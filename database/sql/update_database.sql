-- Add state and updated columns to all existing tables

ALTER TABLE vehicle_make ADD COLUMN state TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE vehicle_make ADD COLUMN updated DATETIME NULL;

ALTER TABLE vehicle_model ADD COLUMN state TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE vehicle_model ADD COLUMN updated DATETIME NULL;

ALTER TABLE vehicle ADD COLUMN state TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE vehicle ADD COLUMN updated DATETIME NULL;
