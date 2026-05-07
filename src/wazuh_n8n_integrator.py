#!/usr/bin/env python3
import sys
import json
import requests

# Wazuh Integration Script to send alert data to n8n Webhook
# Required in Wazuh: <integration><name>custom-n8n</name><hook_url>...</hook_url></integration>

if len(sys.argv) < 4:
    sys.exit(1)

alert_file = sys.argv[1]
hook_url = sys.argv[3]

with open(alert_file, 'r') as f:
    alert_json = json.load(f)

# Only send Level 12+ to n8n to save processing
if alert_json['rule']['level'] >= 12:
    msg = {
        "rule": {
            "level": alert_json['rule']['level'],
            "description": alert_json['rule']['description'],
            "id": alert_json['rule']['id']
        },
        "agent": {
            "id": alert_json['agent']['id'],
            "name": alert_json['agent']['name'],
            "ip": alert_json['agent'].get('ip', 'unknown')
        },
        "full_log": alert_json.get('full_log', '')
    }
    
    requests.post(hook_url, json=msg)
