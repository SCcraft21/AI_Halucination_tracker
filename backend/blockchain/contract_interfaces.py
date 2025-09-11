import os, json
from web3 import Web3
from pathlib import Path

HARDHAT_URL = os.getenv("HARDHAT_URL", "http://hardhat:8545")
w3 = Web3(Web3.HTTPProvider(HARDHAT_URL))

# deployed.json will be written by the contracts deploy script into /contracts/deployment/deployed.json
DEPLOY_PATH = "/contracts/deployment/deployed.json"

ABI = None
CONTRACT_ADDRESS = None

def _load_artifact_abi():
    global ABI
    # Attempt to load ABI from compiled artifact (optional); fallback to none
    possible = Path("/contracts/artifacts/contracts/SnippetRegistry.sol/SnippetRegistry.json")
    if possible.exists():
        try:
            data = json.loads(possible.read_text())
            ABI = data.get("abi")
        except Exception:
            ABI = None

def _load_deployed_address():
    global CONTRACT_ADDRESS
    if os.path.exists(DEPLOY_PATH):
        try:
            with open(DEPLOY_PATH) as f:
                deployed = json.load(f)
                CONTRACT_ADDRESS = deployed.get("address")
        except Exception:
            CONTRACT_ADDRESS = None

_load_artifact_abi()
_load_deployed_address()

contract = None
if CONTRACT_ADDRESS and ABI:
    contract = w3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=ABI)

def store_snippet_on_chain(hash_hex: str, ipfs_cid: str, trust_score: int):
    # For local MVP, we just print; if contract & ABI available perform tx (requires unlocked account)
    if not CONTRACT_ADDRESS:
        print("No contract address found; skipping on-chain submit for MVP")
        return None
    if not ABI:
        print("No ABI found; can't call contract")
        return None
    # Note: for a true TX you'd need an account/private key; for local Hardhat you can use unlocked accounts via Web3 provider
    # This function intentionally does not perform signing for safety in MVP.
    print(f"Would submit to chain: {hash_hex}, {ipfs_cid}, score={trust_score}")
    return None

def get_snippet_from_chain(hash_hex: str):
    if not CONTRACT_ADDRESS or not ABI:
        raise RuntimeError("Contract not available in backend container (deploy to generate deployment file and compile artifacts)")
    c = w3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=ABI)
    res = c.functions.getSnippet(Web3.toBytes(hexstr=hash_hex)).call()
    return {
        "hash": Web3.toHex(res[0]),
        "ipfsCID": res[1],
        "trustScore": res[2],
        "timestamp": res[3],
        "submitter": res[4]
    }
