-- SQL Schema for Offline Audit Database
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
    os_update_status TEXT, -- Windows/iOS Update Status
    camera_sync_status BOOLEAN DEFAULT false,
    onedrive_sync_status BOOLEAN DEFAULT false,
    photos_count INTEGER DEFAULT 0,
    photos_date DATE,
    total_photos_count INTEGER DEFAULT 0,
    notes TEXT
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_serial_number ON offline_audits(serial_number);
CREATE INDEX IF NOT EXISTS idx_device_type ON offline_audits(device_type);
