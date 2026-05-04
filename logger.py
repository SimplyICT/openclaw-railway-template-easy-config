import os
from supabase import create_client

def log_task(agent_name, task_description, model_used, status):
    url = "https://zhvxjuhgfudavxrfsasn.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"
    
    supabase = create_client(url, key)
    data = {
        "agent_name": agent_name,
        "task_description": task_description,
        "model_used": model_used,
        "status": status
    }
    try:
        supabase.table("agent_logs").insert(data).execute()
        return True
    except Exception as e:
        print(f"Logging failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 5:
        log_task(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
