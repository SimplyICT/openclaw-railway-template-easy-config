-- Fix: Add missing columns to audit_entries for relational tracking
ALTER TABLE audit_entries 
ADD COLUMN IF NOT EXISTS assigned_user_room TEXT,
ADD COLUMN IF NOT EXISTS device_type TEXT,
ADD COLUMN IF NOT EXISTS brand_model TEXT;

-- Note: While these are technically in the 'devices' table, 
-- having them here as well can help with snapshots or 
-- simplify the initial bulk import logic if needed.
-- However, the error usually comes from the JS trying to insert them into the wrong table.

-- Re-run RLS policies for all tables to be safe
ALTER TABLE sites ENABLE ROW LEVEL SECURITY;
ALTER TABLE devices ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_entries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public Access Sites" ON sites FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Public Access Devices" ON devices FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Public Access Entries" ON audit_entries FOR ALL USING (true) WITH CHECK (true);
