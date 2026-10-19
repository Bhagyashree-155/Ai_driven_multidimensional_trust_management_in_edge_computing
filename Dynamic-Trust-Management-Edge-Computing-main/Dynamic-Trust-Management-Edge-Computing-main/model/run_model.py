import time
import redis
import json
import numpy as np
import torch
import torch.nn as nn

# 🔗 Blockchain imports
from web3 import Web3

# --------------------------
# 🔧 REDIS SETUP
# --------------------------
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# --------------------------
# 🔧 BLOCKCHAIN SETUP
# --------------------------
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Use first account from Hardhat
w3.eth.default_account = w3.eth.accounts[0]

# 👉 PASTE YOUR CONTRACT ADDRESS HERE
CONTRACT_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"

# 👉 PASTE YOUR ABI HERE (VERY IMPORTANT)
ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "node", "type": "string"},
            {"internalType": "uint256", "name": "score", "type": "uint256"}
        ],
        "name": "update",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "node", "type": "string"}
        ],
        "name": "get",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# --------------------------
# 🤖 SIMPLE AI MODEL
# --------------------------
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(3, 1)

    def forward(self, x):
        return torch.sigmoid(self.fc(x))

model = Model()

# --------------------------
# 🧠 AGENTS
# --------------------------
def collect(node):
    data = r.lrange(node, -10, -1)
    return [json.loads(d) for d in data]

def analyze(data):
    lat = np.mean([d["latency"] for d in data])
    suc = np.mean([d["success_rate"] for d in data])
    err = np.mean([d["error_rate"] for d in data])
    return [lat, suc, err]

def predict(features):
    latency, success, error = features

    # Normalize values
    latency_score = max(0, 1 - latency / 100)   # lower latency → better
    success_score = success                     # already 0–1
    error_score = 1 - error                     # lower error → better

    # Weighted trust score
    trust = (
        0.4 * success_score +
        0.3 * latency_score +
        0.3 * error_score
    )

    return max(0, min(1, trust))  # clamp between 0 and 1
# --------------------------
# 🔗 BLOCKCHAIN FUNCTION
# --------------------------
def store_on_blockchain(node_id, trust_score):
    score_int = int(trust_score * 100)

    tx_hash = contract.functions.update(node_id, score_int).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"✅ Stored on blockchain → Node: {node_id}, Score: {score_int}")

# --------------------------
# 🔄 MAIN LOOP
# --------------------------
nodes = ["node_1", "node_2", "node_3"]

while True:
    for node in nodes:
        data = collect(node)

        if data:
            features = analyze(data)
            trust = predict(features)

            print(f"🤖 {node} Trust:", trust)

            store_on_blockchain(node, trust)

    time.sleep(5)