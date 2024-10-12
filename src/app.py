from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Placeholder for contract data
contracts = []

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/contracts/recent', methods=['GET'])
def get_recent_contracts():
    # TODO: Implement logic to fetch recent contracts
    return jsonify({"message": "Recent contracts", "contracts": contracts[:5]})

@app.route('/contracts/<cid>', methods=['GET'])
def get_contract(cid):
    # TODO: Implement logic to fetch contract details
    contract = next((c for c in contracts if c['id'] == cid), None)
    if contract:
        return jsonify({
            "message": f"Contract details for {cid}",
            "contract": {
                "id": contract['id'],
                "name": contract['name'],
                "feed": "Sample feed data",
                "basic_info": "Sample basic info",
                "reports": "Sample reports"
            }
        })
    return jsonify({"error": "Contract not found"}), 404

@app.route('/contracts', methods=['POST'])
def create_contract():
    data = request.json
    if not data or 'name' not in data or 'address' not in data:
        return jsonify({"error": "Invalid request. Name and address are required."}), 400
    
    # TODO: Implement logic to create a new contract
    new_contract = {
        "id": str(len(contracts) + 1),
        "name": data['name'],
        "address": data['address']
    }
    contracts.append(new_contract)
    
    # TODO: Implement ABI fetching logic
    abi = "Sample ABI data"
    
    return jsonify({
        "message": "Contract created successfully",
        "contract": new_contract,
        "abi": abi
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
