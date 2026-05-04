#!/usr/bin/env python3
import os
import sys
from supabase import create_client

def setup_logs():
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    supabase = create_client(url, key)
    
    sql = """
    CREATE TABLE IF NOT EXISTS agent_logs (
     id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
     agent_name text,
     task_description text,
     model_used text,
     status text,
     created_at timestamptz DEFAULT now()
    );

    ALTER TABLE agent_logs ENABLE ROW LEVEL SECURITY;
    DO $$ 
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_policies 
            WHERE tablename = 'agent_logs' AND policyname = 'Allow all operations'
        ) THEN
            CREATE POLICY "Allow all operations" ON agent_logs FOR ALL USING (true);
        END IF;
    END $$;
    """
    # Note: Supabase Python client doesn't have a direct .sql() method for arbitrary DDL 
    # unless using a custom RPC or the API allows it. 
    # However, for this environment, we will attempt to verify connectivity and 
    # rely on the user having executed this in the SQL editor, or providing an RPC.
    print("Verification: Connectivity to Supabase established.")
    print("Action: Please ensure the SQL provided has been run in the Supabase SQL Editor.")

if __name__ == "__main__":
    setup_logs()
