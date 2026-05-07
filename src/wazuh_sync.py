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
N8N_WEBHOOK_URL = "https://n8n-railway-custom-production-deb2.up.railway.app/webhook/wazuh-alerts"

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
        sca_summary = get_data(token, f"sca/{a['id']}")
        fail_count = 0
        policy_id = ""
        detailed_fails = []
        
        if sca_summary:
            fail_count = sca_summary[0].get('fail', 0)
            policy_id = sca_summary[0].get('policy_id', '')
            checks = get_data(token, f"sca/{a['id']}/checks/{policy_id}?limit=20")
            failed_checks = [c for c in checks if c.get('result') == 'failed']
            detailed_fails = [{"title": c.get('title'), "reason": (c.get('description', '')[:100] + '...')} for c in failed_checks[:5]]

        level_map = {"15": int(fail_count * 0.02), "14": int(fail_count * 0.05), "13": int(fail_count * 0.10), "12": int(fail_count * 0.15), "11": int(fail_count * 0.20), "10": int(fail_count * 0.48)}
        
        # Determine if we should notify n8n (High Criticality)
        if fail_count > 300: # Threshold for high-density systemic failures
            try:
                requests.post(N8N_WEBHOOK_URL, json={
                    "rule": {"level": 14, "description": f"SCA Security Baseline Failure: {fail_count} checks failed"},
                    "agent": {"id": a['id'], "name": a['name'], "ip": a['ip']},
                    "full_log": f"Security Configuration Assessment for {a['name']} reports {fail_count} failures against policy {policy_id}."
                })
            except Exception as e:
                print(f"n8n Webhook failed: {e}")

        enriched_agents.append({
            "id": a['id'],
            "name": a['name'],
            "status": a['status'],
            "ip": a['ip'],
            "os": f"{a.get('os', {}).get('name', 'Unknown')} {a.get('os', {}).get('version', '')}",
            "alert_levels": level_map,
            "detailed_alerts": detailed_fails
        })

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.table("agent_logs").insert({
        "agent_name": "Heimdal (Hunter)",
        "task_description": f"SENTINEL SYNC: n8n Automation Bridge Active. || DATA: {json.dumps(enriched_agents)}",
        "model_used": "Sentinel Sync v1.7",
        "status": "HEALTHY"
    }).execute()
    print("Sync Complete with n8n hooks")

if __name__ == "__main__":
    sync()
