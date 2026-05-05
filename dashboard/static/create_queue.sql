-- Create the Report Requests Queue
CREATE TABLE IF NOT EXISTS report_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    site_name TEXT NOT NULL,
    target_date DATE NOT NULL,
    status TEXT DEFAULT 'PENDING', -- PENDING, PROCESSING, SUCCESS, ERROR
    message TEXT,
    agent_name TEXT DEFAULT 'Bruce'
);

-- Enable Realtime for this table so the Watcher can see it instantly
ALTER PUBLICATION supabase_realtime ADD TABLE report_requests;
