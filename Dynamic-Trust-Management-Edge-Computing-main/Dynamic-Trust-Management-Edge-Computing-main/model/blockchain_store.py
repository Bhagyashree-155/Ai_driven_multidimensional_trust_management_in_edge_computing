from web3 import Web3
import json

# 👉 Local Hardhat RPC
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# 👉 Use Account #0 from your Hardhat node output
account = w3.eth.accounts[0]
w3.eth.default_account = account

# 👉 PASTE your contract address here
CONTRACT_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"

# 👉 PASTE ABI (the entire list) here
ABI = [

     {
      "inputs": [
        {
          "internalType": "string",
          "name": "node",
          "type": "string"
        }
      ],
      "name": "get",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "name": "scores",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "node",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "score",
          "type": "uint256"
        }
      ],
      "name": "update",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def store_trust(node_id: str, score_float: float):
    # convert to int (0–100 scale)
    score_int = int(score_float * 100)

    tx_hash = contract.functions.update(node_id, score_int).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Stored on-chain: node={node_id}, score={score_int}, tx={receipt.transactionHash.hex()}")

def read_trust(node_id: str):
    val = contract.functions.get(node_id).call()
    return val / 100.0

# ---- demo ----
if __name__ == "__main__":
    # Example: push a value
    store_trust("node_1", 0.82)

    # Read it back
    value = read_trust("node_1")
    print("On-chain trust:", value)