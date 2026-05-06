import os
import requests
from requests_ntlm import HttpNtlmAuth

def get_digest(site_url, fed_auth_cookie):
    endpoint = f"{site_url}/_api/contextinfo"
    headers = {
        "Accept": "application/json;odata=verbose",
        "Cookie": f"FedAuth={fed_auth_cookie}"
    }
    response = requests.post(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()['d']['GetContextWebInformation']['FormDigestValue']
    return None

def upload_to_sharepoint_rest(file_path, site_url, folder_url, fed_auth_cookie):
    file_name = os.path.basename(file_path)
    digest = get_digest(site_url, fed_auth_cookie)
    
    if not digest:
        print("Failed to get X-RequestDigest. Cookie might be expired.")
        return

    endpoint = f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_url}')/Files/add(url='{file_name}',overwrite=true)"
    
    with open(file_path, 'rb') as f:
        file_content = f.read()

    headers = {
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/octet-stream",
        "X-RequestDigest": digest,
        "Cookie": f"FedAuth={fed_auth_cookie}"
    }

    print(f"Attempting upload to: {endpoint}")
    response = requests.post(endpoint, data=file_content, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        print(f"Successfully uploaded {file_name}!")
    else:
        print(f"Upload failed. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Extracted from your provided link and curl headers
    SITE_URL = "https://cccex1.sharepoint.com/sites/bhelc-admin"
    FOLDER_URL = "/sites/bhelc-admin/Shared Documents/Audit reports"
    # This cookie was pulled from the 302 redirect header in our curl test
    FED_AUTH = "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjE1LDBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwM2ZkNmEzYjZlQGxpdmUuY29tLDAjLmZ8bWVtYmVyc2hpcHxzeXNhZG1pbkBjY2NleC5jb20uYXUsMTM0MjI0MDQwNTAwMDAwMDAwLDEzMzc2MTA0MjIwMDAwMDAwMCwxMzQyMjU4NjA1NTAxNjUyMzUsMjAzLjIyMS44NC4yMTAsNjYsOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyLCwwMDRjZWY2YS1kYzVmLWIwMzMtYzAxYy1mODVhOGU4NjllY2QsOTI3MTEwYTItZjAyMS03MDAwLTgxNWUtMGU5ZDMyZGI3ZTcyLDk1Y2MxMGEyLTUwZDYtNzAwMC05Y2UxLTVjMGIyN2IyNmYyMCwsMCwxMzQyMjUwMzI1NTAwNjkxODcsMTM0MjI3NTg4NTUwMDY5MTg3LCwsZXlKNGJYTmZZMk1pT2lKYlhDSkRVREZjSWwwaUxDSjRiWE5mYzNOdElqb2lNU0lzSW5CeVpXWmxjbkpsWkY5MWMyVnlibUZ0WlNJNkluTjVjMkZrYldsdVFHTmpZMlY0TG1OdmJTNWhkU0lzSW5WMGFTSTZJbGxQV0UxTlkwd3lUVVZIVERCbGJGTm1WMVZGUVVFaUxDSmhkWFJvWDNScGJXVWlPaUl4TXpReU1qUXdOREExTURBd01EQXdNREFpZlE9PSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzNDIyNDA0MjE5MDAwMDAwMCw5ZmM5MmFhYi03MmMzLTRiZjgtODEwNC1mNzU3MmY2ZDE5MGMsLCwsLCwxMTUyOTIxNTA0NjA2ODQ5NTQzLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLGpsQk9ZUEtBM2txaWw1Z1lQRDJjTE5ZY0ZFNmNSaE15T29NcUwxcmpVWVpPbDg0M01YWmRLU3hYdm9nR0NxN3hRREk3b2l2blNmOCsvZ3lZZWtvYVV5OHFVQ25CajZwRTEzcVFqZk53S3liMUhVeFROMUJVbkszY3lnb3Zxb1EzV1JSREd3TVF5WC9meVZlQVZiK2JMNnBBenB0d2U5M2ZDNTZ2YzZaUDdKWWYwNExqV2FGQTBHRWVDc1dJYUhFWmNSb21MTFJ4ZFVUNE5pNytlSjVYNzJFSlVrZ1BHeXFXNTExdDFrcjJJTHArMVBJU3JTY2oxbHNhMk9vbnQ0ejg0bEJQZkJVZGRTV1ZLZDBQYloxYTlwNlhKZ29hUEE2RFZGOGsyS2R1di9iTVYwYjU0ZDRGVDVTK21xSDI3YkttZmh4RjROVW1aMnh1bnFkd2ZiWWJ1dz09PC9TUD4="
    
    # Update to the file we just generated
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    FILE_TO_UPLOAD = f"report_Benowa_ELC_{today}.docx"
    
    if os.path.exists(FILE_TO_UPLOAD):
        upload_to_sharepoint_rest(FILE_TO_UPLOAD, SITE_URL, FOLDER_URL, FED_AUTH)
    else:
        print(f"File {FILE_TO_UPLOAD} not found for upload.")
