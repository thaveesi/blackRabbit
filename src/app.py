from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import json
from bson import ObjectId  # Import ObjectId

load_dotenv()

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.mydatabase

# Etherscan API details
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_BASE_URL = "https://api-sepolia.etherscan.io/api"

# Helper function to convert ObjectId to string
def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    if isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data

# Route 1: GET /contracts/recent
@app.route('/contracts/recent', methods=['GET'])
def get_recent_contracts():
    # Retrieve the 5 most recent smart contracts
    recent_contracts = list(db.smart_contract.find().sort("created_at", -1).limit(5))
    recent_contracts = convert_objectid(recent_contracts)  # Convert ObjectIds to strings
    return jsonify(recent_contracts), 200

# Route 2: GET /contracts/<cid>
@app.route('/contracts/<cid>', methods=['GET'])
def get_contract_by_id(cid):
    # Find the contract by contract_id
    contract = db.smart_contract.find_one({"contract_id": cid})
    if contract:
        contract = convert_objectid(contract)  # Convert ObjectIds to strings
        # Fetch related events and reports for the contract
        events = list(db.events.find({"smart_contract_id": cid}))
        reports = list(db.report.find({"contract_id": cid}))
        events = convert_objectid(events)
        reports = convert_objectid(reports)
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

    # Parse the ABI JSON string into a Python list
    try:
        abi_parsed = json.loads(abi_data.get("result"))
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse ABI"}), 400
    
    print(abi_data)

    # Insert contract details into the smart_contract collection
    new_contract = {
        "contract_id": f"contract_{int(datetime.timestamp(datetime.now()))}",
        "name": name,
        "addr": address,
        "source_code": abi_parsed,  # Store the parsed ABI list
        "created_at": datetime.now()
    }
    db.smart_contract.insert_one(new_contract)

    new_contract = convert_objectid(new_contract)  # Convert ObjectIds to strings before returning
    return jsonify({"message": "Contract created successfully", "contract": new_contract}), 201

if __name__ == '__main__':
    app.run(debug=True)