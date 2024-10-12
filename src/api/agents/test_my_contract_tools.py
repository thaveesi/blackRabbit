# src/api/agents/test_my_contract_tools.py
from web3 import Web3
import json
import os
from tools import *
from api.web3_connection import get_web3_connection

# Load the ABI for the BasicVulnerableContract
abi_path = os.path.join(os.path.dirname(__file__), "../abi/BasicVulnerableContractABI.json")
with open(abi_path, 'r') as f:
    basic_contract_abi = json.load(f)

# Define contract address and private key (Replace with actual values)
my_contract_address = "0xYourContractAddressHere"  # Replace with your deployed contract address
private_key = "YOUR_PRIVATE_KEY_HERE"  # Replace with your private key
test_user_address = "0xTestUserAddressHere"  # Replace with your test user address

# Initialize Web3 connection
w3 = get_web3_connection()

# Test the getContractBalance function
def test_check_contract_balance():
    print("Testing getContractBalance")
    contract_balance = call_function(w3, my_contract_address, basic_contract_abi, "getContractBalance")
    print(f"Contract balance: {contract_balance} wei")

# Test the deposit function
def test_deposit_funds():
    print("Testing deposit function")
    txn_hash = send_transaction(w3, private_key, my_contract_address, basic_contract_abi, "deposit", value=w3.toWei(1, 'ether'))
    print(f"Deposit transaction hash: {txn_hash}")

# Test the withdraw function
def test_withdraw_funds():
    print("Testing withdraw function")
    withdraw_amount = w3.toWei(0.5, 'ether')
    txn_hash = send_transaction(w3, private_key, my_contract_address, basic_contract_abi, "withdraw", withdraw_amount)
    print(f"Withdraw transaction hash: {txn_hash}")

# Test checking a user's balance using the balances function
def test_check_user_balance(user_address):
    print(f"Testing balances function for user {user_address}")
    user_balance = call_function(w3, my_contract_address, basic_contract_abi, "balances", user_address)
    print(f"User balance: {user_balance} wei")

# Test the resetBalance function
def test_reset_user_balance(user_address):
    print(f"Testing resetBalance function for user {user_address}")
    txn_hash = send_transaction(w3, private_key, my_contract_address, basic_contract_abi, "resetBalance", user_address)
    print(f"Reset balance transaction hash: {txn_hash}")

def main():
    # Test all the functions
    test_check_contract_balance()
    test_deposit_funds()
    test_withdraw_funds()
    test_check_user_balance(test_user_address)
    test_reset_user_balance(test_user_address)

if __name__ == "__main__":
    main()
