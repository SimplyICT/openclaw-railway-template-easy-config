import requests
import json
import urllib3

# Suppress insecure request warnings for SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WAZUH_URL = "https://securesocentral.com.au:55000"
USER = "wazuh-wui"
PASSWORD = "cdcxsOTW165Tqa2N9.0FW4L*Y6*0VK2T"

def get_token():
    auth_url = f"{WAZUH_URL}/security/user/authenticate"
    response = requests.get(auth_url, auth=(USER, PASSWORD), verify=False)
    if response.status_code == 200:
        return response.json()['data']['token']
    else:
        print(f"Auth Failed: {response.status_code} - {response.text}")
        return None

def get_agents(token):
    agents_url = f"{WAZUH_URL}/agents"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(agents_url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()['data']['affected_items']
    return []

if __name__ == "__main__":
    token = get_token()
    if token:
        agents = get_agents(token)
        print(json.dumps(agents, indent=2))
