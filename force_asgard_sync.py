import os
import sys
import subprocess
import datetime
import requests

# 1. HARD-CODE CREDENTIALS & PATHS
SITE_URL = "https://cccex1.sharepoint.com/sites/bhelc-admin"
FOLDER_URL = "/sites/bhelc-admin/Shared Documents/Audit reports"
FED_AUTH = "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjE1LDBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwM2ZkNmEzYjZlQGxpdmUuY29tLDAjLmZ8bWVtYmVyc2hpcHxzeXNhZG1pbkBjY2NleC5jb20uYXUsMTM0MjI0MDQwNTAwMDAwMDAwLDEzMzc2MTA0MjIwMDAwMDAwMCwxMzQyMjU4NjA1NTAxNjUyMzUsMjAzLjIyMS44NC4yMTAsNjYsOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyLCwwMDRjZWY2YS1kYzVmLWIwMzMtYzAxYy1mODVhOGU4NjllY2QsOTI3MTEwYTItZjAyMS03MDAwLTgxNWUtMGU5ZDMyZGI3ZTcyLDk1Y2MxMGEyLTUwZDYtNzAwMC05Y2UxLTVjMGIyN2IyNmYyMCwsMCwxMzQyMjUwMzI1NTAwNjkxODcsMTM0MjI3NTg4NTUwMDY5MTg3LCwsZXlKNGJYTmZZMk1pT2lKYlhDSkRVREZjSWwwaUxDSjRiWE5mYzNOdElqb2lNU0lzSW5CeVpXWmxjbkpsWkY5MWMyVnlibUZ0WlNJNkluTjVjMkZrYldsdVFHTmpZMlY0TG1OdmJTNWhkU0lzSW5WMGFTSTZJbGxQV0UxTlkwd3lUVVZIVERCbGJGTm1WMVZGUVVFaUxDSmhkWFJvWDNScGJXVWlPaUl4TXpReU1qUXdOREExTURBd01EQXdNREFpZlE9PSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzNDIyNDA0MjE5MDAwMDAwMCw5ZmM5MmFhYi03MmMzLTRiZjgtODEwNC1mNzU3MmY2ZDE5MGMsLCwsLCwxMTUyOTIxNTA0NjA2ODQ5NTQzLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLGpsQk9ZUEtBM2txaWw1Z1lQRDJjTE5ZY0ZFNmNSaE15T29NcUwxcmpVWVpPbDg0M01YWmRLU3hYdm9nR0NxN3hRREk3b2l2blNmOCsvZ3lZZWtvYVV5OHFVQ25CajZwRTEzcVFqZk53S3liMUhVeFROMUJVbkszY3lnb3Zxb1EzV1JSREd3TVF5WC9meVZlQVZiK2JMNnBBenB0d2U5M2ZDNTZ2YzZaUDdKWWYwNExqV2FGQTBHRWVDc1dJYUhFWmNSb21MTFJ4ZFVUNE5pNytlSjVYNzJFSlVrZ1BHeXFXNTExdDFrcjJJTHArMVBJU3JTY2oxbHNhMk9vbnQ0ejg0bEJQZkJVZGRTV1ZLZDBQYloxYTlwNlhKZ29hUEE2RFZGOGsyS2R1di9iTVYwYjU0ZDRGVDVTK21xSDI3YkttZmh4RjROVW1aMnh1bnFkd2ZiWWJ1dz09PC9TUD4="
PYTHON_EXEC = "/data/workspace/venv/bin/python3"

def get_digest(site_url, fed_auth_cookie):
    endpoint = f"{site_url}/_api/contextinfo"
    headers = {
        "Accept": "application/json;odata=verbose",
        "Cookie": f"FedAuth={fed_auth_cookie}"
    }
    try:
        response = requests.post(endpoint, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()['d']['GetContextWebInformation']['FormDigestValue']
        else:
            print(f"Digest Failure: {response.status_code}")
    except Exception as e:
        print(f"Digest Exception: {e}")
    return None

def upload_file(file_path):
    file_name = os.path.basename(file_path)
    digest = get_digest(SITE_URL, FED_AUTH)
    if not digest:
        print("CRITICAL: Expired or invalid SharePoint session.")
        return False
    
    endpoint = f"{SITE_URL}/_api/web/GetFolderByServerRelativeUrl('{FOLDER_URL}')/Files/add(url='{file_name}',overwrite=true)"
    with open(file_path, 'rb') as f:
        content = f.read()

    headers = {
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/octet-stream",
        "X-RequestDigest": digest,
        "Cookie": f"FedAuth={FED_AUTH}"
    }

    print(f"Executing Upload: {file_name}...")
    res = requests.post(endpoint, data=content, headers=headers)
    if res.status_code in [200, 201]:
        print(f"SUCCESS: {file_name} is in SharePoint.")
        return True
    else:
        print(f"FAILED: {res.status_code}")
        print(res.text)
        return False

def force_sync(target_date):
    site = "Benowa ELC"
    md = f"report_Benowa_ELC_{target_date}.md"
    docx = f"report_Benowa_ELC_{target_date}.docx"

    print(f"Step 1: Generating MD for {target_date}...")
    subprocess.run([PYTHON_EXEC, "/data/workspace/reporter.py", site, target_date], check=True)
    
    if os.path.exists(md):
        print(f"Step 2: Converting to DOCX...")
        subprocess.run([PYTHON_EXEC, "/data/workspace/md_to_docx.py", md], check=True)
        
        if os.path.exists(docx):
            print(f"Step 3: Uploading {docx}...")
            upload_file(docx)
        else:
            print("ERROR: DOCX generation failed to produce file.")
    else:
        print(f"ERROR: No data found in Supabase for {target_date}.")

if __name__ == "__main__":
    # We force the date where we know the data exists (Melissa's entry)
    force_sync("2026-05-05")
