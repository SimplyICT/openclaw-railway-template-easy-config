import os
import time
import subprocess
import sys

# 1. HARD-CODE PATHS
VENV_PYTHON = "/data/workspace/venv/bin/python3"
VENV_SITE_PACKAGES = "/data/workspace/venv/lib/python3.11/site-packages"

# 2. ENSURE SYS PATH IS MODIFIED BEFORE IMPORTING SUPABASE
if VENV_SITE_PACKAGES not in sys.path:
    sys.path.insert(0, VENV_SITE_PACKAGES)

from supabase import create_client, Client

def start_watcher():
    url = "https://zhvxjuhgfudavxrfsasn.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"
    supabase: Client = create_client(url, key)

    print(f"🛡️ Asgardian Report Watcher Online (PID {os.getpid()}). Listening...")

    while True:
        try:
            # Poll for PENDING
            res = supabase.table('report_requests').select('*').eq('status', 'PENDING').execute()
            requests = res.data

            for req in requests:
                req_id = req['id']
                site = req['site_name']
                date = req['target_date']

                print(f"🚀 Trigger Detected: {site} for {date}")
                supabase.table('report_requests').update({'status': 'PROCESSING'}).eq('id', req_id).execute()

                try:
                    # 3. FORCE ENVIRONMENT FOR SUBPROCESSES
                    env = os.environ.copy()
                    env["PYTHONPATH"] = VENV_SITE_PACKAGES
                    
                    # Run Chain
                    print(f"Executing reporter...")
                    subprocess.run([VENV_PYTHON, '/data/workspace/reporter.py', site, str(date)], check=True, env=env)
                    
                    md_file = f"report_{site.replace(' ', '_')}_{date}.md"
                    if os.path.exists('/data/workspace/md_to_docx.py'):
                        print(f"Executing converter...")
                        subprocess.run([VENV_PYTHON, '/data/workspace/md_to_docx.py', md_file], check=True, env=env)
                    
                    print(f"Executing upload...")
                    subprocess.run([VENV_PYTHON, '/data/workspace/sp_upload.py'], check=True, env=env)

                    supabase.table('report_requests').update({
                        'status': 'SUCCESS', 
                        'message': 'Report shipped to SharePoint!'
                    }).eq('id', req_id).execute()
                    print(f"✅ Finished: {site}")

                except Exception as e:
                    print(f"❌ Error during processing: {e}")
                    supabase.table('report_requests').update({
                        'status': 'ERROR', 
                        'message': str(e)
                    }).eq('id', req_id).execute()

            time.sleep(5)
        except Exception as e:
            print(f"Watcher Loop Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_watcher()
