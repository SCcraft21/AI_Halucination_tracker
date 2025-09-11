from fastapi import FastAPI, HTTPException, Request
import hashlib, os, json
from verifier.python_verifier import verify_python_code
from ipfs.ipfs_client import upload_to_ipfs
from blockchain.contract_interface import store_snippet_on_chain, get_snippet_from_chain

app = FastAPI(title="Hallucination Tracker Backend (MVP)")

# Simple in-memory history for demo (persist in DB in prod)
HISTORY = []

@app.post("/submit")
async def submit(req: Request):
    data = await req.json()
    code = data.get("code", "")
    language = data.get("language", "python")

    if not code:
        raise HTTPException(status_code=400, detail="code required")

    if language != "python":
        raise HTTPException(status_code=400, detail="only python supported in MVP")

    report = verify_python_code(code)
    snippet_hash = "0x" + hashlib.sha256(code.encode()).hexdigest()
    # upload report + code to IPFS (mock or real token required)
    try:
        cid = upload_to_ipfs({"code": code, "report": report})
    except Exception as e:
        # if IPFS fails, continue with mock CID for local demo
        cid = os.getenv("MOCK_IPFS_CID", "bafybeiemockcid12345678")

    tx_hash = None
    try:
        tx_hash = store_snippet_on_chain(snippet_hash, cid, int(report.get("trust_score", 0)))
    except Exception as e:
        # log but don't fail MVP response
        tx_hash = None

    record = {"hash": snippet_hash, "score": report.get("trust_score", 0), "ipfs": cid, "report": report, "tx": tx_hash}
    HISTORY.append(record)
    return record

@app.get("/history")
async def history():
    return HISTORY

@app.get("/chain/{hash_hex}")
async def chain_lookup(hash_hex: str):
    if not hash_hex.startswith("0x"):
        hash_hex = "0x" + hash_hex
    try:
        res = get_snippet_from_chain(hash_hex)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
