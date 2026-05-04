-- Clean up the audit_entries table to follow strict relational rules
-- These fields belong in the 'devices' table, not 'audit_entries'
ALTER TABLE audit_entries DROP COLUMN IF EXISTS brand_model;
ALTER TABLE audit_entries DROP COLUMN IF EXISTS device_type;

-- Ensure the 'devices' table has the necessary columns
ALTER TABLE devices ADD COLUMN IF NOT EXISTS brand_model TEXT;
ALTER TABLE devices ADD COLUMN IF NOT EXISTS device_type TEXT;

-- Refresh the cache by re-applying the primary policy
DROP POLICY IF EXISTS "Public Access Entries" ON audit_entries;
CREATE POLICY "Public Access Entries" ON audit_entries FOR ALL USING (true) WITH CHECK (true);
