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
    FED_AUTH = "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjE1LDBoLmZ8bWVtYmVyc2hpcHx1cm4lM2FzcG8lM2F0ZW5hbnRhbm9uIzhiZTIwMjJlLWI5NzktNDUzNi05MzViLTI2OGE0NjhlNzNhMiwwIy5mfG1lbWJlcnNoaXB8dXJuJTNhc3BvJTNhdGVuYW50YW5vbiM4YmUyMDIyZS1iOTc5LTQ1MzYtOTM1Yi0yNjhhNDY4ZTczYTIsMTM0MjI0MDU1NzcwMDAwMDAwLDAsMTM0MjI0OTE2ODUzNjU3MzcxLDAuMC4wLjAsMjU4LDhiZTIwMjJlLWI5NzktNDUzNi05MzViLTI2OGE0NjhlNzNhMiwsLDk0NzIxMGEyLTYwNzctNzAwMC04MTVlLTA4ODQ0ZjhmMDg5MSw5NDcyMTBhMi02MDc3LTcwMDAtODE1ZS0wODg0NGY4ZjA4OTEsTTFLUktZNWNlRStNd1VzdiszQXY5dywwLDAsMCwsLCwyNjUwNDY3NzQzOTk5OTk5OTk5LDAsLCwsLCwsMCwsMTk1NTc1LDRxLVo4eEFmUTdVSzFyNGpUZzlQYnNjNXBtVSwsMCwsai9hVVNwdHRiY1BUTC9ORzA4YmlkS29YV25obXRLK080WGtqQjAwempMQUtSUjI4K2V1dCswOFNVY0VWSFZQNjlRdUw4OGsxeVcya29zQ3NxR3RMOFoyZTNxK1prdm9DemRud3huc1FhRWJ3QUtvMFZwN3ZVbHQwWEhnT3NJVmdSSW5ObG9BQjJDZFVtL1NOS1g2VFIwenhIeWpmc0ZoTGo1eGo2N0FyTkhCQ0FGWlpaa1dBblhkT2xrV2I5amsyK042T2UxS0ZoSHNPTVphM2ErQkpQZlJubTQ2V2ZZd09tTjd6Tk1BRUhReWorQVNCMHNOVGdYdmZRN3pwTndLWVlFMk11dk9qdFM3N2M2VlczclhhWUpRT1R5d0RvMVNHbGxXcVNhVzhEcGJXbEZvdG1SZG56SndIZDAvREx2eG00S2h2cWt0MjkybVZ2aFdsZjdPdEt3PT08L1NQPg=="
    
    # Update to the file we just generated
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    FILE_TO_UPLOAD = f"report_Benowa_ELC_{today}.docx"
    
    if os.path.exists(FILE_TO_UPLOAD):
        upload_to_sharepoint_rest(FILE_TO_UPLOAD, SITE_URL, FOLDER_URL, FED_AUTH)
    else:
        print(f"File {FILE_TO_UPLOAD} not found for upload.")
