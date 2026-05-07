import os
import time
import requests
import sys
from supabase import create_client

# --- CONFIGURATION ---
WAZUH_URL = "https://securesocentral.com.au"
WAZUH_USER = "wazuh-wui"
WAZUH_PASS = "cdcxsOTW165Tqa2N9.0FW4L*Y6*0VK2T"
SUPABASE_URL = "https://zhvxjuhgfudavxrfsasn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"

# Disable SSL warnings for the self-signed native environments
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def log_to_supabase(agent, task, status):
    try:
        sb = create_client(SUPABASE_URL, SUPABASE_KEY)
        data = {
            "agent_name": agent,
            "task_description": task,
            "model_used": "Automated-SOC-Monitor",
            "status": status
        }
        sb.table("agent_logs").insert(data).execute()
        print(f"✅ Logged {agent} to Supabase with status {status}")
    except Exception as e:
        print(f"Failed to log to Supabase: {e}")

def get_wazuh_token():
    try:
        # Note: Wazuh API login endpoint is usually /security/user/authenticate
        res = requests.post(f"{WAZUH_URL}/wazuh-api/security/user/authenticate", auth=(WAZUH_USER, WAZUH_PASS), verify=False, timeout=10)
        token = res.json().get('data', {}).get('token')
        if token: return token
        
        # Fallback for different API versions
        res = requests.post(f"{WAZUH_URL}/security/user/authenticate", auth=(WAZUH_USER, WAZUH_PASS), verify=False, timeout=10)
        return res.json().get('data', {}).get('token')
    except Exception as e:
        print(f"Auth Error: {e}")
        return None

def monitor_alerts():
    print("🛡️ Asgard SOC Monitor: Starting automated alert listener...")
    
    while True:
        token = get_wazuh_token()
        if token:
            headers = {'Authorization': f'Bearer {token}'}
            try:
                # Polling for any level 10+ alerts in the stream
                res = requests.get(f"{WAZUH_URL}/wazuh-api/alerts?severity=high", headers=headers, verify=False, timeout=10)
                if res.status_code != 200:
                    res = requests.get(f"{WAZUH_URL}/alerts?severity=high", headers=headers, verify=False, timeout=10)
                
                alerts = res.json().get('data', {}).get('affected_items', [])
                print(f"Polled Wazuh: Found {len(alerts)} high alerts.")
                
                for alert in alerts:
                    rule = alert.get('rule', {})
                    rule_id = str(rule.get('id'))
                    description = rule.get('description', '')
                    
                    if rule_id == '40101' or "eicar" in description.lower():
                        print(f"🚨 MATCH: {description}")
                        log_to_supabase("Lady Sif", f"AUTO-DETECT: {description}", "RESPONDING")
                        log_to_supabase("Thor", f"AUTO-DETECT: Malware Signature Probe", "RESPONDING")
            except Exception as e:
                print(f"Monitoring error: {e}")
        else:
            print("❌ Failed to obtain Wazuh Token.")
        
        time.sleep(15) # Poll every 15 seconds

if __name__ == "__main__":
    print("LOGGING START")
    sys.stdout.flush()
    monitor_alerts()
