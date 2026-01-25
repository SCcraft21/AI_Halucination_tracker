import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import nltk
from celery import Celery
from web3 import Web3
import hashlib
from dotenv import load_dotenv

nltk.download('punkt', quiet=True)
load_dotenv()

app = FastAPI()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# Load NLI model (at startup)
tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-base")
model = AutoModelForSequenceClassification.from_pretrained("MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli").eval()

# Blockchain setup
w3 = Web3(Web3.HTTPProvider(os.getenv('RPC_URL')))
contract_address = os.getenv('CONTRACT_ADDRESS')
abi = [  # From compiled contract; paste full ABI here
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "uint256", "name": "queryHash", "type": "uint256"}, {"indexed": False, "internalType": "uint8", "name": "score", "type": "uint8"}, {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}, {"indexed": False, "internalType": "string", "name": "modelVersion", "type": "string"}], "name": "LogEntry", "type": "event"},
    {"inputs": [{"internalType": "uint256[]", "name": "queryHashes", "type": "uint256[]"}, {"internalType": "uint8[]", "name": "scores", "type": "uint8[]"}, {"internalType": "string[]", "name": "modelVersions", "type": "string[]"}], "name": "logBatch", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "queryHash", "type": "uint256"}, {"internalType": "uint8", "name": "score", "type": "uint8"}, {"internalType": "string", "name": "modelVersion", "type": "string"}], "name": "logSingle", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]
contract = w3.eth.contract(address=contract_address, abi=abi)
private_key = os.getenv('PRIVATE_KEY')

class Query(BaseModel):
    text: str

# Mock RAG functions (replace with real impl)
def retrieve_context(query: str) -> str:
    # Mock: In real, use vector DB
    return "The capital of France is Paris. It has famous landmarks like the Eiffel Tower."

def generate_response(context: str, query: str) -> str:
    # Mock: In real, use LLM API
    return f"Based on {query}, the answer is: Paris is the capital, known for beaches."  # Intentional partial hallucination

def calculate_hallucination_score(context: str, response: str) -> float:
    response_sentences = nltk.sent_tokenize(response)
    scores = []
    for sent in response_sentences:
        inputs = tokenizer(context, sent, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=1).numpy()[0]
            entailment_prob = probs[0]  # 0=entailment
            scores.append(entailment_prob)
    return np.mean(scores) * 100 if scores else 100.0

@celery_app.task
def run_validation_and_log(query: str, context: str, response: str):
    score = int(calculate_hallucination_score(context, response))
    # Log to blockchain (single for simplicity; batch in prod)
    query_hash = int(hashlib.sha256(query.encode()).hexdigest(), 16)
    account = w3.eth.account.from_key(private_key)
    tx = contract.functions.logSingle(query_hash, score, "v1.0").build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Logged tx: {tx_hash.hex()}")
    return score

@app.post("/query")
async def handle_query(query: Query, background_tasks: BackgroundTasks):
    context = retrieve_context(query.text)
    response = generate_response(context, query.text)
    background_tasks.add_task(run_validation_and_log.delay, query.text, context, response)
    return {"response": response, "status": "Validation queued"}

# Run: uvicorn app:app --reload