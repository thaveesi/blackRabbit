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

# Test retry_transaction tool
def test_retry_transaction():
    print("Testing retry_transaction")
    try:
        # Set a small amount for withdrawal
        withdraw_amount = w3.to_wei(0.0005, 'ether')
        txn_hash = retry_transaction(
            w3, private_key, my_contract_address, basic_contract_abi, "withdraw", withdraw_amount, retries=3
        )
        print(f"Withdraw transaction hash (retry_transaction): {txn_hash}")
    except Exception as e:
        print(f"Error in retry_transaction: {str(e)}")

def test_submit_batch_transactions():
    print("Testing submit_batch_transactions")
    try:
        # Prepare multiple transactions (deposit and withdraw)
        function_names_and_args = [
            ("deposit", []),  # Deposit without arguments
            ("withdraw", [w3.to_wei(0.0005, 'ether')]),  # Withdraw 0.0005 ether
        ]

        # Get the initial nonce
        account = w3.eth.account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(account.address)
        
        txns = []
        for i, (function_name, args) in enumerate(function_names_and_args):
            contract = w3.eth.contract(address=Web3.to_checksum_address(my_contract_address), abi=basic_contract_abi)
            function = getattr(contract.functions, function_name)
            txn = function(*args).build_transaction({
                'from': account.address,
                'nonce': nonce + i,  # Increment nonce for each transaction
                'gas': 2000000,
                'maxPriorityFeePerGas': w3.to_wei(5, 'gwei'),  # Further increased priority fee
                'maxFeePerGas': w3.eth.gas_price + w3.to_wei(15, 'gwei'),  # Further increase max fee
                'chainId': 11155111  # Sepolia chain ID
            })
            txns.append(txn)

        # Sign and send all transactions
        signed_txns = [w3.eth.account.sign_transaction(txn, private_key=private_key) for txn in txns]
        txn_hashes = [w3.eth.send_raw_transaction(signed_txn.raw_transaction).hex() for signed_txn in signed_txns]

        print(f"Batch transaction hashes: {txn_hashes}")
    except Exception as e:
        print(f"Error in submit_batch_transactions: {str(e)}")




def main():
    # Check the account balance first
    balance_in_eth = check_account_balance()

    # Proceed with the tests only if there is sufficient balance
    if balance_in_eth is not None and balance_in_eth > 0.0005:
        test_retry_transaction()  # Test the retry_transaction function
        test_submit_batch_transactions()  # Test the submit_batch_transactions function
    else:
        print("Insufficient balance to perform transactions")


if __name__ == "__main__":
    main()
