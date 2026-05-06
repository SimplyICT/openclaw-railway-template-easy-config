import requests
import json
import urllib3
from supabase import create_client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Wazuh/Supabase Config
WAZUH_URL = "https://securesocentral.com.au:55000"
USER = "wazuh-wui"
PASSWORD = "cdcxsOTW165Tqa2N9.0FW4L*Y6*0VK2T"
SUPABASE_URL = "https://zhvxjuhgfudavxrfsasn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"

def get_token():
    auth_url = f"{WAZUH_URL}/security/user/authenticate"
    response = requests.get(auth_url, auth=(USER, PASSWORD), verify=False)
    return response.json()['data']['token'] if response.status_code == 200 else None

def get_data(token, endpoint):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{WAZUH_URL}/{endpoint}", headers=headers, verify=False)
    return response.json()['data']['affected_items'] if response.status_code == 200 else []

def sync():
    token = get_token()
    if not token: 
        print("Auth failed")
        return
    
    # Increase limit to 100 to catch all client agents
    agents = get_data(token, "agents?limit=100")
    # Fetch higher volume of alerts to ensure we get counters right
    alerts = get_data(token, "alerts?limit=100&sort=-timestamp")
    
    enriched_agents = []
    for a in agents:
        # Get all alerts for this agent
        agent_raw_alerts = [al for al in alerts if str(al.get('agent', {}).get('id')) == str(a['id'])]
        
        # Count alerts by level
        level_counts = {}
        for al in agent_raw_alerts:
            lvl = al['rule']['level']
            level_counts[lvl] = level_counts.get(lvl, 0) + 1
            
        enriched_agents.append({
            "id": a['id'],
            "name": a['name'],
            "status": a['status'],
            "ip": a['ip'],
            "os": f"{a.get('os', {}).get('name', 'Unknown')} {a.get('os', {}).get('version', '')}",
            "alert_levels": level_counts,
            "top_alerts": [al['rule']['description'] for al in agent_raw_alerts[:3]]
        })

    active_agents = [a for a in enriched_agents if a['status'] == 'active']
    status_msg = f"SENTINEL SYNC: Alert Level Analysis complete."
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.table("agent_logs").insert({
        "agent_name": "Heimdal (Hunter)",
        "task_description": f"{status_msg} || DATA: {json.dumps(enriched_agents)}",
        "model_used": "Sentinel Sync v1.3",
        "status": "HEALTHY"
    }).execute()
    print(status_msg)

if __name__ == "__main__":
    sync()
