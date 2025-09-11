import os, json, requests
WEB3_STORAGE_TOKEN = os.getenv("WEB3_STORAGE_TOKEN", "")

def upload_to_ipfs(payload: dict) -> str:
    # If WEB3_STORAGE_TOKEN is present, upload; otherwise return mock CID for local demo
    if not WEB3_STORAGE_TOKEN:
        return "bafybeiemockcid12345678"
    url = "https://api.web3.storage/upload"
    headers = {"Authorization": f"Bearer {WEB3_STORAGE_TOKEN}"}
    files = {'file': ('report.json', json.dumps(payload).encode('utf-8'), 'application/json')}
    resp = requests.post(url, headers=headers, files=files, timeout=30)
    if resp.status_code in (200, 202):
        obj = resp.json()
        return obj.get("cid")
    else:
        raise RuntimeError(f"IPFS upload failed: {resp.status_code} {resp.text}")
