from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import os
import json
from bson import ObjectId  # Import ObjectId
from schema import get_all_reports

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
# Enable CORS
CORS(app)

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

    # Fetch the contract source code from Etherscan
    sourcecode_response = requests.get(f"{ETHERSCAN_BASE_URL}?module=contract&action=getsourcecode&address={address}&apikey={ETHERSCAN_API_KEY}")
    sourcecode_data = sourcecode_response.json()

    if sourcecode_data.get("status") != "1":
        return jsonify({"error": "Unable to fetch source code"}), 400

    source_code_result = sourcecode_data.get("result", [{}])[0].get("SourceCode", "")

    # Insert contract details into the smart_contract collection
    contract_id = f"contract_{int(datetime.timestamp(datetime.now()))}"
    new_contract = {
        "contract_id": contract_id,
        "name": name,
        "addr": address,
        "abi": abi_parsed,  # Store the parsed ABI list
        "source_code": source_code_result,  # Store the verified source code
        "created_at": datetime.now()
    }
    db.smart_contract.insert_one(new_contract)

    # Insert contract details into the reports collection
    new_report = {
        "contract_id": contract_id,
        "contract_name": name,
        "created_at": datetime.now()
    }
    db.report.insert_one(new_report)

    # Convert ObjectIds to strings before returning
    new_contract = convert_objectid(new_contract)
    
    return jsonify({"message": "Contract and report created successfully", "contract": new_contract}), 201

# Route 4: GET /reports
@app.route('/reports', methods=['GET'])
def get_reports():
    try:
        # Fetch all reports from the database
        all_reports = get_all_reports()
        return jsonify(all_reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get report by contract ID
@app.route('/report/<contract_id>', methods=['GET'])
def get_report(contract_id):
    report = db.report.find_one({"contract_id": contract_id})
    if not report:
        return jsonify({"error": "Report not found"}), 404

    # Convert MongoDB ObjectId to string and return the report
    report = convert_objectid(report)
    return jsonify(report), 200
    
@app.route('/reports/append/<contract_id>', methods=['POST'])
def append_results(contract_id):
    try:
        # Get the new data from the request body (JSON format)
        data = request.json
        new_results = data.get("results", "")

        if not new_results:
            return jsonify({"error": "No results provided"}), 400

        # Find the report by contract_id
        report = db.report.find_one({"contract_id": contract_id})

        if not report:
            return jsonify({"error": "Report not found"}), 404

        # Append new results to the existing results
        updated_results = (report.get("results", "") + "\n" + new_results).strip()

        # Update the report's results field
        db.report.update_one(
            {"contract_id": contract_id},
            {"$set": {"results": updated_results}}
        )

        return jsonify({"message": "Results updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
