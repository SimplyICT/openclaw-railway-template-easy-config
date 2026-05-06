import os
import requests

# 1. HARD-CODE CREDENTIALS
SITE_URL = "https://cccex1.sharepoint.com/sites/bhelc-admin"
FOLDER_URL = "/sites/bhelc-admin/Shared Documents/Audit reports"
FED_AUTH = "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjE1LDBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwM2ZkNmEzYjZlQGxpdmUuY29tLDAjLmZ8bWVtYmVyc2hpcHxzeXNhZG1pbkBjY2NleC5jb20uYXUsMTM0MjI0MDQwNTAwMDAwMDAwLDEzMzc2MTA0MjIwMDAwMDAwMCwxMzQyMjU4NjA1NTAxNjUyMzUsMjAzLjIyMS44NC4yMTAsNjYsOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyLCwwMDRjZWY2YS1kYzVmLWIwMzMtYzAxYy1mODVhOGU4NjllY2QsOTI3MTEwYTItZjAyMS03MDAwLTgxNWUt0GU5ZDMyZGI3ZTcyLDk1Y2MxMGEyLTUwZDYtNzAwMC05Y2UxLTVjMGIyN2IyNmYyMCwsMCwxMzQyMjUwMzI1NTAwNjkxODcsMTM0MjI3NTg4NTUwMDY5MTg3LCwsZXlKNGJYTmZZMk1pT2lKYlhDSkRVREZjSWwwaUxDSjRiWE5mYzNOdElqb2lNU0lzSW5CeVpXWmxjbkpsWkY5MWMyVnlibUZ0WlNJNkluTjVjMkZrYldsdVFHTmpZMlY0TG1OdmJTNWhkU0lzSW5WMGFTSTZJbGxQV0UxTlkwd3lUVVZIVERCbGJGTm1WMVZGUVVFaUxDSmhkWFJvWDNScGJXVWlPaUl4TXpReU1qUXdOREExTURBd01EQXdNREFpZlE9PSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzNDIyNDA0MjE5MDAwMDAwMCw5ZmM5MmFhYi03MmMzLTRiZjgtODEwNC1mNzU3MmY2ZDE5MGMsLCwsLCwxMTUyOTIxNTA0NjA2ODQ5NTQzLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLGpsQk9ZUEtBM2txaWw1Z1lQRDJjTE5ZY0ZFNmNSaE15T29NcUwxcmpVWVpPbDg0M01YWmRLU3hYdm9nR0NxN3hRREk3b2l2blNmOCsvZ3lZZWtvYVV5OHFVQ25CajZwRTEzcVFqZk53S3liMUhVeFROMUJVbkszY3lnb3Zxb1EzV1JSREd3TVF5WC9meVZlQVZiK2JMNnBBenB0d2U5M2ZDNTZ2YzZaUDdKWWYwNExqV2FGQTBHRWVDc1dJYUhFWmNSb21MTFJ4ZFVUNE5pNytlSjVYNzJFSlVrZ1BHeXFXNTExdDFrcjJJTHArMVBJU3JTY2oxbHNhMk9vbnQ0ejg0bEJQZkJVZGRTV1ZLZDBQYloxYTlwNlhKZ29hUEE2RFZGOGsyS2R1di9iTVYwYjU0ZDRGVDVTK21xSDI3YkttZmh4RjROVW1aMnh1bnFkd2ZiWWJ1dz09PC9TUD4="
RTFA = "B4ofbd21wWO4oXxYEed88GDIVnskg9orl3xNXHYsaYwmOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyIzEzNDIyNDA0MjE5NTkxMzgwMSM5MjcxMTBhMi1mMDIxLTcwMDAtODE1ZS0wZTlkMzJkYjdlNzIjc3lzYWRtaW4lNDBjY2NleC5jb20uYXUsMTM0MjI0MDQwNTAwMDAwMDAwLDEzMzc2MTA0MjIwMDAwMDAwMCwxMzQyMjU4NjA1NTAxNjUyMzUsMjAzLjIyMS44NC4yMTAsNjYsOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyLCwwMDRjZWY2YS1kYzVmLWIwMzMtYzAxYy1mODVhOGU4NjllY2QsOTI3MTEwYTItZjAyMS03MDAwLTgxNWUtMGU5ZDMyZGI3ZTcyLDk1Y2MxMGEyLTUwZDYtNzAwMC05Y2UxLTVjMGIyN2IyNmYyMCwsMCwxMzQyMjUwMzI1NTAwNjkxODcsMTM0MjI3NTg4NTUwMDY5MTg3LCwsZXlKNGJYTmZZMk1pT2lKYlhDSkRVREZjSWwwaUxDSjRiWE5mYzNOdElqb2lNU0lzSW5CeVpXWmxjbkpsWkY5MWMyVnlibUZ0WlNJNkluTjVjMkZrYldsdVFHTmpZMlY0TG1OdmJTNWhkU0lzSW5WMGFTSTZJbGxQV0UxTlkwd3lUVVZIVERCbGJGTm1WMVZGUVVFaUxDSmhkWFJvWDNScGJXVWlPaUl4TXpReU1qUXdOREExTURBd01EQXdNREFpZlE9PSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzNDIyNDA0MjE5MDAwMDAwMCw5ZmM5MmFhYi03MmMzLTRiZjgtODEwNC1mNzU3MmY2ZDE5MGMsLCwsLCwxMTUyOTIxNTA0NjA2ODQ5NTQzLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLGpsQk9ZUEtBM2txaWw1Z1lQRDJjTE5ZY0ZFNmNSaE15T29NcUwxcmpVWVpPbDg0M01YWmRLU3hYdm9nR0NxN3hRREk3b2l2blNmOCsvZ3lZZWtvYVV5OHFVQ25CajZwRTEzcVFqZk53S3liMUhVeFROMUJVbkszY3lnb3Zxb1EzV1JSREd3TVF5WC9meVZlQVZiK2JMNnBBenB0d2U5M2ZDNTZ2YzZaUDdKWWYwNExqV2FGQTBHRWVDc1dJYUhFWmNSb21MTFJ4ZFVUNE5pNytlSjVYNzJFSlVrZ1BHeXFXNTExdDFrcjJJTHArMVBJU3JTY2oxbHNhMk9vbnQ0ejg0bEJQZkJVZGRTV1ZLZDBQYloxYTlwNlhKZ29hUEE2RFZGOGsyS2R1di9iTVYwYjU0ZDRGVDVTK21xSDI3YkttZmh4RjROVW1aMnh1bnFkd2ZiWWJ1dz09PC9TUD4=="

COOKIE = f"FedAuth={FED_AUTH}; rtFa={RTFA}"

def get_digest():
    endpoint = f"{SITE_URL}/_api/contextinfo"
    headers = {"Accept": "application/json;odata=verbose", "Cookie": COOKIE}
    resp = requests.post(endpoint, headers=headers)
    if resp.status_code == 200:
        return resp.json()['d']['GetContextWebInformation']['FormDigestValue']
    print(f"Digest Error {resp.status_code}: {resp.text}")
    return None

def upload(filename):
    digest = get_digest()
    if not digest: return
    endpoint = f"{SITE_URL}/_api/web/GetFolderByServerRelativeUrl('{FOLDER_URL}')/Files/add(url='{filename}',overwrite=true)"
    headers = {
        "X-RequestDigest": digest,
        "Cookie": COOKIE,
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/octet-stream"
    }
    with open(filename, 'rb') as f: content = f.read()
    res = requests.post(endpoint, data=content, headers=headers)
    if res.status_code in [200, 201]:
        print(f"SUCCESS: {filename} uploaded.")
    else:
        print(f"UPLOAD FAILED {res.status_code}: {res.text}")

if __name__ == "__main__":
    target = "report_Benowa_ELC_2026-05-05.docx"
    if os.path.exists(target):
        upload(target)
    else:
        print(f"File {target} not found.")
