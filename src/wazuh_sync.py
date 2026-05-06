import requests
import json
import urllib3
from supabase import create_client

# Suppress insecure request warnings for SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Wazuh Config
WAZUH_URL = "https://securesocentral.com.au:55000"
USER = "wazuh-wui"
PASSWORD = "cdcxsOTW165Tqa2N9.0FW4L*Y6*0VK2T"

# Supabase Config
SUPABASE_URL = "https://zhvxjuhgfudavxrfsasn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"

def get_token():
    auth_url = f"{WAZUH_URL}/security/user/authenticate"
    response = requests.get(auth_url, auth=(USER, PASSWORD), verify=False)
    if response.status_code == 200:
        return response.json()['data']['token']
    return None

def get_agents(token):
    agents_url = f"{WAZUH_URL}/agents"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(agents_url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()['data']['affected_items']
    return []

def get_alerts(token):
    # Fetching top alerts
    alerts_url = f"{WAZUH_URL}/alerts?limit=10&sort=-timestamp"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(alerts_url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()['data']['affected_items']
    return []

def sync_to_mission_control():
    token = get_token()
    if not token:
        print("Failed to authenticate with Wazuh")
        return

    agents = get_agents(token)
    alerts = get_alerts(token)

    active_count = len([a for a in agents if a['status'] == 'active'])
    total_count = len(agents)
    
    # Store high-fidelity data in a new table 'wazuh_alerts' if available, 
    # but for now, we post a tactical update to agent_logs so Mission Control sees it.
    
    status_msg = f"WAZUH INTEGRATION: {active_count}/{total_count} Agents Active. Latest alerts processed."
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    data = {
        "agent_name": "Heimdal (Hunter)",
        "task_description": status_msg,
        "model_used": "Wazuh API v4.14.4",
        "status": "HEALTHY" if active_count > (total_count / 2) else "CRITICAL"
    }
    
    try:
        supabase.table("agent_logs").insert(data).execute()
        print(f"Mission Control Updated: {status_msg}")
    except Exception as e:
        print(f"Supabase Sync Failed: {e}")

if __name__ == "__main__":
    sync_to_mission_control()
