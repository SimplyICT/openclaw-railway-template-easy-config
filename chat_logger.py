import os
import sys
from supabase import create_client, Client

def log_chat_turn(summary):
    url = os.environ.get("SUPABASE_URL") or "https://zhvxjuhgfudavxrfsasn.supabase.co"
    key = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"
    if not url or not key:
        return

    supabase: Client = create_client(url, key)
    
    # We use a dedicated table for conversation continuity
    # This acts as our "External Memory" that survives workspace resets
    data = {
        "content": summary,
        "category": "chat_history",
        "importance": 5
    }
    
    try:
        supabase.table("agent_memories").insert(data).execute()
    except Exception as e:
        print(f"Failed to log chat to Supabase: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_chat_turn(sys.argv[1])
