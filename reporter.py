import os
import sys
import json
from datetime import datetime
from supabase import create_client, Client

def generate_consolidated_report(site_name, target_date):
    url = os.environ.get("SUPABASE_URL") or "https://zhvxjuhgfudavxrfsasn.supabase.co"
    key = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"
    
    supabase: Client = create_client(url, key)
    
    # Precise Measurement: PostgreSQL doesn't like 'LIKE' on Timestamps. 
    # Use GTE/LTE with explicit 00:00:00 to 23:59:59 bounds.
    start_bound = f"{target_date}T00:00:00+00:00"
    end_bound = f"{target_date}T23:59:59+00:00"
    
    res = supabase.table('audit_entries').select('*, devices(*)').eq('site_name', site_name).gte('audit_date', start_bound).lte('audit_date', end_bound).execute()
    data = res.data

    if not data:
        print(f"No records found for {site_name} on {target_date}.")
        sys.exit(1) # Critical for the watcher to know it failed

    # --- 1. Executive Summary Logic ---
    active_devices = [r for r in data if not r.get('ignore_flag')]
    missing_assets = [r for r in data if r.get('ignore_flag')]
    photo_breaches = [r for r in data if r.get('photos_count', 0) > 100]
    sync_failures = [r for r in data if r.get('onedrive_status') == 'Failed' or 'failed' in (r.get('notes') or '').lower()]

    report = []
    report.append(f"# {site_name}")
    report.append(f"Assessment Date: {target_date}")
    report.append("\n## Executive Summary")
    report.append(f"• {len(active_devices)} active devices currently recorded in use.")
    report.append(f"• {len(missing_assets)} devices currently marked missing and escalated for investigation.")
    if photo_breaches:
        report.append(f"• {len(photo_breaches)} devices exceed photo retention targets.")
    if sync_failures:
        report.append(f"• {len(sync_failures)} devices show password / OneDrive sync failures.")

    # --- 2. Critical Incidents & Immediate Actions ---
    report.append("\n## Critical Incidents & Immediate Actions")
    if missing_assets:
        report.append("### Missing Devices Requiring Immediate Investigation")
        for m in missing_assets:
            dev = m.get('devices') or {}
            report.append(f"- **Room: {dev.get('assigned_user_room', 'N/A')}** | {dev.get('device_type', 'N/A')} | {dev.get('brand_model', 'N/A')} | SN: {m['serial_number']}")
    
    if photo_breaches:
        report.append("\n### Photo Retention Breaches")
        for p in photo_breaches:
            dev = p.get('devices') or {}
            report.append(f"- **Room: {dev.get('assigned_user_room', 'N/A')}** | SN: {p['serial_number']} | Count: {p['photos_count']} | Total: {p.get('total_photos', 'N/A')}")

    # --- 3. Detailed Findings by Room / User ---
    report.append("\n## Detailed Findings by Room / User")
    for r in active_devices:
        dev = r.get('devices') or {}
        dtype = (dev.get('device_type') or "").lower()
        line = f"### {dev.get('assigned_user_room', 'Unassigned')}\n"
        line += f"- **Device:** {dev.get('brand_model')} (SN: {r['serial_number']})\n"
        
        if "tablet" in dtype or "phone" in dtype:
            line += f"  - **OS/Version:** iOS {r.get('ios_version') or 'N/A'}\n"
            line += f"  - **Photos:** {r.get('photos_count', 0)} (Total: {r.get('total_photos', 0)}) | Date: {r.get('photos_date') or 'N/A'}\n"
            line += f"  - **Sync:** Camera Sync Off: {'Yes' if r.get('camera_sync_off') else 'No'} | OneDrive Sync On: {'Yes' if r.get('onedrive_sync_on') else 'No'}\n"
        elif "laptop" in dtype or "desktop" in dtype:
            line += f"  - **OS:** Windows {r.get('windows_os') or 'N/A'}\n"
            line += f"  - **Updates:** {r.get('update_status') or 'N/A'}\n"
            line += f"  - **Compliance:** OneDrive Status: {r.get('onedrive_status') or 'N/A'} | Security Check: {r.get('security_check') or 'N/A'}\n"
        
        line += f"  - **Status/Notes:** {r.get('notes') or 'N/A'}"
        report.append(line)

    # --- 4. Missing Assets Register ---
    report.append("\n## Missing Assets Register")
    for m in missing_assets:
        report.append(f"- SN: {m['serial_number']} | Risk: {m.get('security_check', 'N/A')} | Action: {m.get('notes', 'N/A')}")

    final_report = "\n".join(report)
    filename = f"report_{site_name.replace(' ', '_')}_{target_date}.md"
    with open(filename, 'w') as f:
        f.write(final_report)
    print(f"Report saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 reporter.py <Site Name> <YYYY-MM-DD>")
    else:
        generate_consolidated_report(sys.argv[1], sys.argv[2])
