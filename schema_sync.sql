-- RELATIONAL CLEANUP & SCHEMA SYNC
-- Run this if the schema cache is stale or column mismatches occur.

-- 1. Ensure the bridge between devices and audits is strictly via serial_number
-- 2. Explicitly remove any legacy columns if they accidentally leaked into the wrong table

-- Clear PostgREST Cache (Run this in Supabase SQL Editor if issue persists)
NOTIFY pgrst, 'reload schema';

DO $$ 
BEGIN
    -- Check if audit_entries has column brand_model (it shouldn't)
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='audit_entries' AND column_name='brand_model') THEN
        ALTER TABLE audit_entries DROP COLUMN brand_model;
    END IF;

    -- Check if audit_entries has column device_type (it shouldn't)
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='audit_entries' AND column_name='device_type') THEN
        ALTER TABLE audit_entries DROP COLUMN device_type;
    END IF;
END $$;
