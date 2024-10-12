from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")  # Get MongoDB URI from .env

client = MongoClient(MONGO_URI)
db = client.mydatabase

# Etherscan API details
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # Get Etherscan API key from .env
ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"

# Route 1: GET /contracts/recent
@app.route('/contracts/recent', methods=['GET'])
def get_recent_contracts():
    # Retrieve the 5 most recent smart contracts
    recent_contracts = list(db.smart_contract.find().sort("created_at", -1).limit(5))
    for contract in recent_contracts:
        contract['_id'] = str(contract['_id'])  # Convert ObjectId to string for JSON compatibility
    return jsonify(recent_contracts), 200

# Route 2: GET /contracts/<cid>
@app.route('/contracts/<cid>', methods=['GET'])
def get_contract_by_id(cid):
    # Find the contract by contract_id
    contract = db.smart_contract.find_one({"contract_id": cid})
    if contract:
        contract['_id'] = str(contract['_id'])  # Convert ObjectId to string for JSON compatibility
        # Fetch related events and reports for the contract
        events = list(db.events.find({"smart_contract_id": cid}))
        reports = list(db.report.find({"contract_id": cid}))
        return jsonify({
            "contract_info": contract,
            "events": events,
            "reports": reports
        }), 200
    else:
        return jsonify({"error": "Contract not found"}), 404

# Route 3: POST /contracts
@app.route('/contracts', methods=['POST'])
def create_contract():
    # Get data from the request body
    data = request.json
    name = data.get("name")
    address = data.get("address")

    if not name or not address:
        return jsonify({"error": "Name and address are required"}), 400

    # Fetch the contract ABI from Etherscan
    abi_response = requests.get(f"{ETHERSCAN_BASE_URL}?module=contract&action=getabi&address={address}&apikey={ETHERSCAN_API_KEY}")
    abi_data = abi_response.json()

    if abi_data.get("status") != "1":
        return jsonify({"error": "Unable to fetch ABI"}), 400

    # Insert contract details into the smart_contract collection
    new_contract = {
        "contract_id": f"contract_{int(datetime.timestamp(datetime.now()))}",
        "name": name,
        "addr": address,
        "source_code": abi_data.get("result"),  # Storing the ABI
        "created_at": datetime.now()
    }
    db.smart_contract.insert_one(new_contract)

    return jsonify({"message": "Contract created successfully", "contract": new_contract}), 201

if __name__ == '__main__':
    app.run(debug=True)