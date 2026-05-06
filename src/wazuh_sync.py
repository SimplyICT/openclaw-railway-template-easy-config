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
    if response.status_code == 200:
        return response.json().get('data', {}).get('affected_items', [])
    return []

def sync():
    token = get_token()
    if not token: return
    
    agents = get_data(token, "agents?limit=100")
    
    enriched_agents = []
    for a in agents:
        # Get SCA policy summary
        sca_summary = get_data(token, f"sca/{a['id']}")
        fail_count = 0
        policy_id = ""
        detailed_fails = []
        
        if sca_summary:
            fail_count = sca_summary[0].get('fail', 0)
            policy_id = sca_summary[0].get('policy_id', '')
            
            # If there are failures, reach into the checks for the top 5 practical failures
            if fail_count > 0:
                checks = get_data(token, f"sca/{a['id']}/checks/{policy_id}?status=fail&limit=5")
                detailed_fails = [{"title": c.get('title'), "reason": c.get('description')} for c in checks]

        # Use the density distribution for levels 10-15
        level_map = {
            "15": int(fail_count * 0.02),
            "14": int(fail_count * 0.05),
            "13": int(fail_count * 0.10),
            "12": int(fail_count * 0.15),
            "11": int(fail_count * 0.20),
            "10": int(fail_count * 0.48)
        }
        
        enriched_agents.append({
            "id": a['id'],
            "name": a['name'],
            "status": a['status'],
            "ip": a['ip'],
            "os": f"{a.get('os', {}).get('name', 'Unknown')} {a.get('os', {}).get('version', '')}",
            "alert_levels": level_map,
            "detailed_alerts": detailed_fails,
            "total_fails": fail_count
        })

    status_msg = f"SENTINEL SYNC: Drill-down data enabled for {len(enriched_agents)} agents."
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.table("agent_logs").insert({
        "agent_name": "Heimdal (Hunter)",
        "task_description": f"{status_msg} || DATA: {json.dumps(enriched_agents)}",
        "model_used": "Sentinel Sync v1.6",
        "status": "HEALTHY"
    }).execute()
    print(status_msg)

if __name__ == "__main__":
    sync()
