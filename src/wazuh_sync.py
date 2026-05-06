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
    if not token: return
    
    agents = get_data(token, "agents")
    alerts = get_data(token, "alerts?limit=20&sort=-timestamp")
    
    # Enrich agents with their specific alerts
    enriched_agents = []
    for a in agents:
        agent_alerts = [al['rule']['description'] for al in alerts if al.get('agent', {}).get('id') == a['id']]
        enriched_agents.append({
            "id": a['id'],
            "name": a['name'],
            "status": a['status'],
            "ip": a['ip'],
            "os": f"{a.get('os', {}).get('name', 'Unknown')} {a.get('os', {}).get('version', '')}",
            "alerts": agent_alerts[:3]
        })

    status_msg = f"SENTINEL SYNC: {len([a for a in agents if a['status'] == 'active'])}/{len(agents)} Agents Online."
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.table("agent_logs").insert({
        "agent_name": "Heimdal (Hunter)",
        "task_description": status_msg,
        "model_used": "Sentinel Sync v1.0",
        "status": "HEALTHY",
        "metadata": {"raw_agents": enriched_agents}
    }).execute()
    print(status_msg)

if __name__ == "__main__":
    sync()
