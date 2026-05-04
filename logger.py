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
    
    # Protocol Confirmation Log
    data = {
        "content": "Protocol Confirmation (2026-05-04): Bruce confirmed primary rules and the four-step persistence protocol (Task, Memory, DB, Sync). Adherence is mandatory for the Claw Way.",
        "category": "protocol",
        "importance": 10
    }
    
    try:
        response = supabase.table("agent_memories").insert(data).execute()
        print(f"Logged to Supabase (agent_memories): {response}")
    except Exception as e:
        print(f"Failed to log to Supabase: {e}")

if __name__ == "__main__":
    log_event()
