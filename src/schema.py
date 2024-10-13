import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# Assuming you have a MongoDB connection string
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)
db = client['mydatabase']

# Define collections
smart_contracts = db.smart_contract
malicious_contracts = db.malicious_contract
events = db.events
reports = db.report

def create_id(object_type: str):
    return f'{object_type}_{int(datetime.timestamp(datetime.now()))}'

# Schema definitions (these are not enforced by MongoDB, but serve as a guide)

smart_contract_schema = {
    "_id": ObjectId,
    "addr": str,
    "source_code": str,
    "name": str
}

malicious_contract_schema = {
    "_id": ObjectId,
    "addr": str,
    "source_code": str,
    "abi": str,
    "bytecode": str,
}

event_schema = {
    "_id": ObjectId,
    "agent": str,
    "created_at": datetime, "action": str,
    "smart_contract_id": ObjectId  # Reference to SmartContract
}

report_schema = {
    "_id": ObjectId,
    "report_id": str,
    "text": str,
    "created_at": datetime
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
def get_all_reports():
    all_reports = list(reports.find())
    for report in all_reports:
        report['_id'] = str(report['_id'])
    return all_reports

def create_report(text: str, created_at: datetime):
    report_id = create_id('report')
    new_report = {
        "report_id": report_id,
        "text": text,
        "created_at": created_at
    }
    result = reports.insert_one(new_report)
    # Convert ObjectId to string for easier handling
    inserted_id = str(result.inserted_id)
    return {
        "_id": inserted_id,
        "report_id": report_id,
        "text": text,
        "created_at": created_at
    }

def get_uploaded_contract_address_abi(contract_address: str):
    contract = smart_contracts.find_one({"addr": contract_address})
    if contract and "abi" in contract:
        return contract["abi"]
    return None

def get_uploaded_malicious_contract_abi(contract_address: str):
    contract = malicious_contracts.find_one({"addr": contract_address})
    if contract and "abi" in contract:
        return contract["abi"]
    return None

def insert_malicious_contract(addr, source_code, abi, bytecode):
    return malicious_contracts.insert_one({
        "addr": addr,
        "source_code": source_code,
        "abi": abi,
        "bytecode": bytecode,
    })

def update_report(contract_id, final_result):
    reports.update_one(
        {"contract_id": contract_id},
        {"$set": {"results": final_result}}
    )

def insert_event(contract_id, agent, action):
    new_event = {
        "agent": agent,
        "smart_contract_id": contract_id,
        "action": action,
        "created_at": datetime.now()
    }
    return events.insert_one(new_event)
