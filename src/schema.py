from pymongo import MongoClient
from bson import ObjectId

# Assuming you have a MongoDB connection string
client = MongoClient('your_mongodb_connection_string_here')
db = client['your_database_name']

# Define collections
smart_contracts = db.smart_contracts
events = db.events
reports = db.reports

# Schema definitions (these are not enforced by MongoDB, but serve as a guide)

smart_contract_schema = {
    "_id": ObjectId,
    "addr": str,
    "source_code": str,
    "name": str
}

event_schema = {
    "_id": ObjectId,
    "agent_id": str,
    "created_at": datetime,
    "action": str,
    "smart_contract_id": ObjectId  # Reference to SmartContract
}

report_schema = {
    "_id": ObjectId,
    "text": str
}

# Example of how to insert a document
def insert_smart_contract(addr, source_code, name):
    return smart_contracts.insert_one({
        "addr": addr,
        "source_code": source_code,
        "name": name
    })

# Example of how to query documents
def get_smart_contract_by_id(contract_id):
    return smart_contracts.find_one({"_id": ObjectId(contract_id)})

# You can add more helper functions for CRUD operations as needed

