import os
import sys

# --- ASGARDIAN REMEDIATION PLAYBOOK ---
# This library stores actionable scripts that agents can "propose" in the drill-down modals.

PLAYBOOKS = {
    "WIN_ISOLATE_HOST": {
        "title": "Isolate Endpoint (Defender)",
        "description": "Uses Microsoft Defender XDR to isolate the machine from the network except for security comms.",
        "script_type": "powershell",
        "danger_level": "HIGH",
        "action": "Invoke-MgSecurityIncidentAction -IncidentId {id} -Action isolate"
    },
    "WIN_TERMINATE_PROCESS": {
        "title": "Terminate Malicious Process",
        "description": "Kills a specific process by name or ID to stop a persistent foothold.",
        "script_type": "powershell",
        "danger_level": "MEDIUM",
        "action": "Stop-Process -Name {process_name} -Force"
    },
    "WIN_REMOVE_SCHEDULED_TASK": {
        "title": "Delete Persistence Task",
        "description": "Removes a malicious scheduled task identified as a persistent foothold.",
        "script_type": "powershell",
        "danger_level": "MEDIUM",
        "action": "Unregister-ScheduledTask -TaskName {task_name} -Confirm:$false"
    },
    "LINUX_BLOCK_IP": {
        "title": "Block IP (iptables)",
        "description": "Blocks a specific malicious IP address at the firewall level.",
        "script_type": "bash",
        "danger_level": "MEDIUM",
        "action": "iptables -A INPUT -s {ip} -j DROP"
    }
}

def get_remediation_text(playbook_key, **kwargs):
    """Generates the text for the 'Remediation' section of the Asgard Drill-down."""
    pb = PLAYBOOKS.get(playbook_key)
    if not pb:
        return "Manual Investigation Required || No automated playbook found for this event."
    
    try:
        command = pb['action'].format(**kwargs)
    except:
        command = pb['action']
        
    return f"REMEDIATION: {pb['title']} || {pb['description']} || PROPOSED_COMMAND: {command}"

if __name__ == "__main__":
    # Test logic
    print("🦞 Asgard Remediation Playbook initialized.")
    test_text = get_remediation_text("WIN_REMOVE_SCHEDULED_TASK", task_name="MalwareUpdater")
    print(f"Sample Output: {test_text}")
