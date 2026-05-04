-- Version 3: Audit Compliance Schema (Historical Tracking)
CREATE TABLE IF NOT EXISTS devices (
    serial_number TEXT PRIMARY KEY,
    device_type TEXT,
    brand_model TEXT,
    date_of_purchase DATE,
    assigned_user_room TEXT,
    intended_use TEXT,
    connectivity TEXT,
    recording_storage_capabilities TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit_entries (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    serial_number TEXT REFERENCES devices(serial_number),
    audit_date TIMESTAMPTZ DEFAULT now(),
    security_settings_applied TEXT,
    onedrive_status TEXT,
    windows_updates TEXT,
    security_check TEXT,
    windows_os TEXT,
    ios_version TEXT,
    update_status TEXT,
    camera_sync_off BOOLEAN DEFAULT true,
    onedrive_sync_on BOOLEAN DEFAULT true,
    photos_count INTEGER DEFAULT 0,
    photos_date DATE,
    total_photos INTEGER DEFAULT 0,
    ignore_flag BOOLEAN DEFAULT false,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_history ON audit_entries(serial_number);
