import os
import time
import subprocess
from supabase import create_client, Client

def start_watcher():
    url = "https://zhvxjuhgfudavxrfsasn.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"
    supabase: Client = create_client(url, key)

    print("🛡️ Asgardian Report Watcher Online. Listening for triggers...")

    while True:
        try:
            # Poll for PENDING requests
            res = supabase.table('report_requests').select('*').eq('status', 'PENDING').execute()
            requests = res.data

            for req in requests:
                req_id = req['id']
                site = req['site_name']
                date = req['target_date']

                print(f"🚀 Trigger Detected: {site} for {date}")
                
                # Mark as PROCESSING
                supabase.table('report_requests').update({'status': 'PROCESSING'}).eq('id', req_id).execute()

                try:
                    # Run the Chain
                    subprocess.run(['python3', '/data/workspace/reporter.py', site, date], check=True)
                    # Note: We might need to handle the .md filename safely
                    md_file = f"report_{site.replace(' ', '_')}_{date}.md"
                    if os.path.exists('/data/workspace/md_to_docx.py'):
                        subprocess.run(['python3', '/data/workspace/md_to_docx.py', md_file], check=True)
                    
                    subprocess.run(['python3', '/data/workspace/sp_upload.py'], check=True)

                    # Mark as SUCCESS
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

            time.sleep(5) # Poll every 5 seconds
        except Exception as e:
            print(f"Watcher encountered an error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_watcher()
