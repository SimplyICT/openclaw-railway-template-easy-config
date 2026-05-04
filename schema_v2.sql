-- Updated SQL Schema for Offline Audit Database
CREATE TABLE IF NOT EXISTS offline_audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    device_type TEXT,
    brand_model TEXT,
    date_of_purchase DATE,
    serial_number TEXT UNIQUE,
    assigned_user_room TEXT,
    intended_use TEXT,
    connectivity TEXT,
    recording_storage_capabilities TEXT,
    security_settings_applied TEXT,
    notes TEXT,
    ignore_flag BOOLEAN DEFAULT false,
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
    total_photos INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_serial_number ON offline_audits(serial_number);
