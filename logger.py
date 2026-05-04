import os
import sys
import datetime
from supabase import create_client, Client

def log_event():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Error: SUPABASE_URL or SUPABASE_KEY not set.")
        sys.exit(1)

    supabase: Client = create_client(url, key)
    
    # Using the 'agent_memories' table as confirmed by David
    data = {
        "content": "Conversation Update (2026-05-04): David confirmed IP mappings for simplyict.com.au. RMM is 208.87.135.69 (critical); Web fleet is 209.182.235.47.",
        "category": "infrastructure",
        "importance": 8
    }
    
    try:
        response = supabase.table("agent_memories").insert(data).execute()
        print(f"Logged to Supabase (agent_memories): {response}")
    except Exception as e:
        print(f"Failed to log to Supabase: {e}")

if __name__ == "__main__":
    log_event()
