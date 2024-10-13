# from web3 import Web3
# import json
# import os
# from api.agents.tools import *
# from api.web3_connection import get_web3_connection

# # Load the ABI for the BasicVulnerableContract
# abi_path = os.path.join(os.path.dirname(__file__), "../abi/BasicVulnerableContractABI.json")
# with open(abi_path, 'r') as f:
#     basic_contract_abi = json.load(f)

# # Define contract address and private key
# my_contract_address = "0x8AdD1b01116cAcAE62D9bcCbF43aa002C47CF2e7"
# private_key = "a4af72ca5e6acefeea8593fd689892757bfd2df55bd7aff7b8d410cf4846a995"
# test_user_address = "0x13d6Fa5134AA6FC64E43679F9E24B7788c3Ab8E9"

# # Initialize Web3 connection
# w3 = get_web3_connection()

# # Function to check the balance of the interacting address
# def check_account_balance():
#     print("Checking account balance")
#     try:
#         account = w3.eth.account.from_key(private_key)
#         balance = w3.eth.get_balance(account.address)
#         balance_in_eth = w3.from_wei(balance, 'ether')
#         print(f"Account {account.address} has a balance of {balance_in_eth} ETH")
#         return balance_in_eth
#     except Exception as e:
#         print(f"Error in checking account balance: {str(e)}")
#         return None

# # Test the getContractBalance function
# def test_check_contract_balance():
#     print("Testing getContractBalance")
#     try:
#         # Define the account using your private key
#         account = w3.eth.account.from_key(private_key)
        
#         # Call the function with the 'from_address' parameter
#         contract_balance = call_function(
#             w3, my_contract_address, basic_contract_abi, "getContractBalance",
#             from_address=account.address
#         )
#         print(f"Contract balance: {contract_balance} wei")
#     except Exception as e:
#         print(f"Error in getContractBalance: {str(e)}")


# # Test the deposit function (with payable transaction)
# def test_deposit_funds():
#     print("Testing deposit function")
#     try:
#         txn_hash = send_payable_transaction(w3, private_key, my_contract_address, basic_contract_abi, "deposit", value=w3.to_wei(0.000001, 'ether'))
#         print(f"Deposit transaction hash: {txn_hash}")
#     except Exception as e:
#         print(f"Error in deposit: {str(e)}")

# # Test the withdraw function
# def test_withdraw_funds():
#     print("Testing withdraw function")
#     try:
#         withdraw_amount = w3.to_wei(0.5, 'ether')
#         txn_hash = send_transaction(w3, private_key, my_contract_address, basic_contract_abi, "withdraw", withdraw_amount)
#         print(f"Withdraw transaction hash: {txn_hash}")
#     except Exception as e:
#         print(f"Error in withdraw: {str(e)}")

# # Test checking a user's balance using the balances function
# def test_check_user_balance(user_address):
#     print(f"Testing balances function for user {user_address}")
#     try:
#         account = w3.eth.account.from_key(private_key)
#         user_balance = call_function(
#             w3, my_contract_address, basic_contract_abi, "balances",
#             user_address,
#             from_address=account.address
#         )
#         print(f"User balance: {user_balance} wei")
#     except Exception as e:
#         print(f"Error in checking user balance: {str(e)}")


# # Test the resetBalance function
# def test_reset_user_balance(user_address):
#     print(f"Testing resetBalance function for user {user_address}")
#     try:
#         txn_hash = send_transaction(w3, private_key, my_contract_address, basic_contract_abi, "resetBalance", user_address)
#         print(f"Reset balance transaction hash: {txn_hash}")
#     except Exception as e:
#         print(f"Error in resetBalance: {str(e)}")

# def main():
#     # Check the account balance first
#     balance_in_eth = check_account_balance()

#     # Proceed with the tests only if there is sufficient balance
#     if balance_in_eth is not None and balance_in_eth > 0:
#         test_check_contract_balance()
#         test_deposit_funds()
#         test_withdraw_funds()
#         test_check_user_balance(test_user_address)
#         test_reset_user_balance(test_user_address)
#     else:
#         print("Insufficient balance to perform transactions")

# if __name__ == "__main__":
#     main()


from web3 import Web3
import json
import os
from api.agents.tools import *
from api.web3_connection import get_web3_connection

# Load the ABI for the BasicVulnerableContract
abi_path = os.path.join(os.path.dirname(__file__), "../abi/BasicVulnerableContractABI.json")
with open(abi_path, 'r') as f:
    basic_contract_abi = json.load(f)

# Define contract address and private key
my_contract_address = "0x8AdD1b01116cAcAE62D9bcCbF43aa002C47CF2e7"
private_key = "a4af72ca5e6acefeea8593fd689892757bfd2df55bd7aff7b8d410cf4846a995"
test_user_address = "0x13d6Fa5134AA6FC64E43679F9E24B7788c3Ab8E9"

# Initialize Web3 connection
w3 = get_web3_connection()

# Function to check the balance of the interacting address
def check_account_balance():
    print("Checking account balance")
    try:
        account = w3.eth.account.from_key(private_key)
        balance = w3.eth.get_balance(account.address)
        balance_in_eth = w3.from_wei(balance, 'ether')
        print(f"Account {account.address} has a balance of {balance_in_eth} ETH")
        return balance_in_eth
    except Exception as e:
        print(f"Error in checking account balance: {str(e)}")
        return None

# Test the getContractBalance function
def test_check_contract_balance():
    print("Testing getContractBalance")
    try:
        # Define the account using your private key
        account = w3.eth.account.from_key(private_key)
        
        # Call the function with the 'from_address' parameter
        contract_balance = call_function(
            w3, my_contract_address, basic_contract_abi, "getContractBalance",
            from_address=account.address
        )
        print(f"Contract balance: {contract_balance} wei")
    except Exception as e:
        print(f"Error in getContractBalance: {str(e)}")


# Test the deposit function (with payable transaction)
def test_deposit_funds():
    print("Testing deposit function")
    try:
        txn_hash = send_payable_transaction(w3, private_key, my_contract_address, basic_contract_abi, "deposit", value=w3.to_wei(0.000001, 'ether'))
        print(f"Deposit transaction hash: {txn_hash}")
    except Exception as e:
        print(f"Error in deposit: {str(e)}")

# Test the withdraw function
def test_withdraw_funds():
    print("Testing withdraw function")
    try:
        withdraw_amount = w3.to_wei(0.5, 'ether')
        txn_hash = send_transaction(w3, private_key, my_contract_address, basic_contract_abi, "withdraw", withdraw_amount)
        print(f"Withdraw transaction hash: {txn_hash}")
    except Exception as e:
        print(f"Error in withdraw: {str(e)}")

# Test checking a user's balance using the balances function
def test_check_user_balance(user_address):
    print(f"Testing balances function for user {user_address}")
    try:
        account = w3.eth.account.from_key(private_key)
        user_balance = call_function(
            w3, my_contract_address, basic_contract_abi, "balances",
            user_address,
            from_address=account.address
        )
        print(f"User balance: {user_balance} wei")
    except Exception as e:
        print(f"Error in checking user balance: {str(e)}")


# Test the resetBalance function
def test_reset_user_balance(user_address):
    print(f"Testing resetBalance function for user {user_address}")
    try:
        txn_hash = send_transaction(w3, private_key, my_contract_address, basic_contract_abi, "resetBalance", user_address)
        print(f"Reset balance transaction hash: {txn_hash}")
    except Exception as e:
        print(f"Error in resetBalance: {str(e)}")

# Test the retrieve_contract_data function
def test_retrieve_contract_data():
    print("Testing retrieve_contract_data")
    try:
        result = retrieve_contract_data(w3, my_contract_address, basic_contract_abi, "getContractBalance")
        print(f"Retrieved contract data: {result} wei")
    except Exception as e:
        print(f"Error in retrieve_contract_data: {str(e)}")

# Test the monitor_events function
def test_monitor_events():
    print("Testing monitor_events")
    try:
        events = monitor_events(w3, my_contract_address, basic_contract_abi, "DepositEvent")
        print(f"Monitored events: {events}")
    except Exception as e:
        print(f"Error in monitor_events: {str(e)}")

# Test the retry_transaction function
def test_retry_transaction():
    print("Testing retry_transaction")
    try:
        txn_hash = retry_transaction(w3, private_key, my_contract_address, basic_contract_abi, "withdraw", w3.to_wei(0.1, 'ether'))
        print(f"Retry transaction hash: {txn_hash}")
    except Exception as e:
        print(f"Error in retry_transaction: {str(e)}")

# Test the submit_batch_transactions function
def test_submit_batch_transactions():
    print("Testing submit_batch_transactions")
    try:
        function_names_and_args = [("deposit", []), ("withdraw", [w3.to_wei(0.1, 'ether')])]
        txn_hashes = submit_batch_transactions(w3, private_key, my_contract_address, basic_contract_abi, function_names_and_args)
        print(f"Batch transaction hashes: {txn_hashes}")
    except Exception as e:
        print(f"Error in submit_batch_transactions: {str(e)}")

# Test the orchestrate_exploit function
def test_orchestrate_exploit():
    print("Testing orchestrate_exploit")
    try:
        steps = [("withdraw", [w3.to_wei(0.1, 'ether')]), ("resetBalance", [test_user_address])]
        orchestrate_exploit(w3, private_key, my_contract_address, basic_contract_abi, steps)
    except Exception as e:
        print(f"Error in orchestrate_exploit: {str(e)}")


def main():
    # Check the account balance first
    balance_in_eth = check_account_balance()

    # Proceed with the tests only if there is sufficient balance
    if balance_in_eth is not None and balance_in_eth > 0:
        test_check_contract_balance()
        test_deposit_funds()
        test_withdraw_funds()
        test_check_user_balance(test_user_address)
        test_reset_user_balance(test_user_address)
        test_retrieve_contract_data()
        test_monitor_events()
        test_retry_transaction()
        test_submit_batch_transactions()
        test_orchestrate_exploit()
    else:
        print("Insufficient balance to perform transactions")

if __name__ == "__main__":
    main()
