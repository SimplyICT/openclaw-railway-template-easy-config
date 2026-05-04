import os
import sys
import json
from supabase import create_client, Client

def fetch_rules():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Error: SUPABASE_URL or SUPABASE_KEY not set.")
        sys.exit(1)

    supabase: Client = create_client(url, key)
    
    try:
        # Search for rules in the agent_memories table
        response = supabase.table("agent_memories").select("*").ilike("content", "%rule%").execute()
        print(json.dumps(response.data, indent=2))
        
        # Also try searching for "red lines" as mentioned in AGENTS.md
        response_red = supabase.table("agent_memories").select("*").ilike("content", "%red line%").execute()
        if response_red.data:
            print("\nRed Lines Found:")
            print(json.dumps(response_red.data, indent=2))
            
    except Exception as e:
        print(f"Failed to fetch from Supabase: {e}")

if __name__ == "__main__":
    fetch_rules()
