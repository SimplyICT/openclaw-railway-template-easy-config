import os
import json
import requests
import time
from supabase import create_client

# --- MULTI-TENANT CONFIGURATION ---
# This will eventually move to a secure database table, but for now, we define the structure.
TENANTS = [
    {
        "client_name": "Client_Alpha",
        "tenant_id": "TENANT_ID_HERE",
        "client_id": "CLIENT_ID_HERE",
        "client_secret": "CLIENT_SECRET_HERE"
    },
    # Add other 9 clients here
]

SUPABASE_URL = "https://zhvxjuhgfudavxrfsasn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"

def get_access_token(tenant):
    url = f"https://login.microsoftonline.com/{tenant['tenant_id']}/oauth2/v2.0/token"
    data = {
        "client_id": tenant['client_id'],
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": tenant['client_secret'],
        "grant_type": "client_credentials",
    }
    try:
        res = requests.post(url, data=data, timeout=10)
        return res.json().get('access_token')
    except Exception as e:
        print(f"Token Error for {tenant['client_name']}: {e}")
        return None

def fetch_defender_incidents(tenant, token):
    # MS Defender XDR Incidents Endpoint
    url = "https://graph.microsoft.com/v1.0/security/incidents?$filter=status eq 'active'"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        return res.json().get('value', [])
    except Exception as e:
        print(f"API Error for {tenant['client_name']}: {e}")
        return []

def log_alert_to_squad(client_name, incident):
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    severity = incident.get('severity', 'informational')
    title = incident.get('title', 'Unknown Defender Alert')
    
    # Alert Thor
    data = {
        "agent_name": "Thor",
        "task_description": f"DEFENDER XDR [{client_name}]: {severity.upper()} - {title}",
        "status": "RESPONDING" if severity.lower() in ['high', 'medium'] else "ACTIVE",
        "model_used": "Defender-XDR-Monitor"
    }
    sb.table("agent_logs").insert(data).execute()

def monitor_all_tenants():
    print(f"🛡️ Asgard Multi-Tenant XDR Watcher active. Monitoring {len(TENANTS)} clients...")
    while True:
        for tenant in TENANTS:
            # Skip if keys are placeholders
            if "HERE" in tenant['tenant_id']: continue
            
            token = get_access_token(tenant)
            if token:
                incidents = fetch_defender_incidents(tenant, token)
                for inc in incidents:
                    log_alert_to_squad(tenant['client_name'], inc)
        
        time.sleep(300) # Check every 5 minutes

if __name__ == "__main__":
    monitor_all_tenants()
