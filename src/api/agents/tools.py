# src/api/agents/tools.py

from web3 import Web3
import json
import os

# Load the contract ABI from a file
def load_abi(abi_path):
    with open(abi_path, 'r') as f:
        return json.load(f)

# Call a read-only function on a smart contract (does not cost gas)
def call_function(w3, contract_address, abi, function_name, *args):
    contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)

    # Call the function without sending a transaction (readonly)
    result = function(*args).call()
    return result

# Send a transaction to invoke a function on the smart contract
def send_transaction(w3, private_key, contract_address, abi, function_name, *args, value=0):
    account = w3.eth.account.privateKeyToAccount(private_key)
    contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)

    # Build the transaction
    txn = function(*args).buildTransaction({
        'chainId': 11155111,  # Chain ID for Sepolia
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'value': value,  # If you're sending ETH with the transaction
    })

    # Sign the transaction
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
    # Send the transaction
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash.hex()

# Check the balance of an address in Ether
def check_balance(w3, address):
    balance = w3.eth.getBalance(Web3.toChecksumAddress(address))
    return w3.fromWei(balance, 'ether')

# Deploy a contract to the network
def deploy_contract(w3, private_key, contract_abi, contract_bytecode, constructor_args=()):
    account = w3.eth.account.privateKeyToAccount(private_key)

    # Create the contract object with bytecode and ABI
    contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

    # Build the transaction to deploy the contract
    txn = contract.constructor(*constructor_args).buildTransaction({
        'chainId': 11155111,  # Chain ID for Sepolia
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
    })

    # Sign and send the transaction
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined and return the contract address
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    return txn_receipt.contractAddress

# Monitor contract events (e.g., for Reflection agent)
def monitor_events(w3, contract_address, abi, event_name, from_block='latest'):
    contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
    event_filter = contract.events.__dict__[event_name].createFilter(fromBlock=from_block)
    
    # Retrieve all past events
    events = event_filter.get_all_entries()
    return events

# Create a new wallet
def create_wallet():
    w3 = Web3()
    new_account = w3.eth.account.create()
    return {
        'address': new_account.address,
        'private_key': new_account.key.hex()
    }

# Trigger a reentrancy attack (Example for Tier 1)
def trigger_reentrancy_attack(w3, private_key, contract_address, abi, reentrancy_function_name, attack_iterations=10):
    account = w3.eth.account.privateKeyToAccount(private_key)
    contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
    function = getattr(contract.functions, reentrancy_function_name)

    # Repeat the attack a number of times to exploit the reentrancy bug
    for i in range(attack_iterations):
        txn = function().buildTransaction({
            'chainId': 11155111,
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
        })

        signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(f"Iteration {i+1}: Transaction hash: {txn_hash.hex()}")

# Manipulate oracle price (Example for Tier 3)
def manipulate_oracle(w3, private_key, oracle_contract_address, oracle_abi, new_price):
    return send_transaction(
        w3=w3,
        private_key=private_key,
        contract_address=oracle_contract_address,
        abi=oracle_abi,
        function_name="updatePrice",
        args=(new_price,)
    )

# Flash loan exploit (Example for Tier 3)
def execute_flash_loan(w3, private_key, contract_address, abi, loan_amount):
    return send_transaction(
        w3=w3,
        private_key=private_key,
        contract_address=contract_address,
        abi=abi,
        function_name="flashLoan",
        args=(loan_amount,)
    )

# Retrieve multiple pieces of data from a contract
def retrieve_contract_data(w3, contract_address, abi, function_name, *args):
    contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)
    data = function(*args).call()
    return data

# Automatically retry a transaction with increased gas limits in case of failure
def retry_transaction(w3, private_key, contract_address, abi, function_name, *args, value=0, retries=3):
    account = w3.eth.account.privateKeyToAccount(private_key)
    contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)

    for attempt in range(retries):
        try:
            txn = function(*args).buildTransaction({
                'chainId': 11155111,
                'from': account.address,
                'nonce': w3.eth.getTransactionCount(account.address),
                'gas': 2000000 + (attempt * 500000),  # Increase gas with each retry
                'gasPrice': w3.eth.gas_price,
                'value': value,
            })

            signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
            txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            return txn_hash.hex()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            continue
    raise RuntimeError("All retry attempts failed")

# Tool to execute interactions between multiple contracts (cross-contract interaction)
def cross_contract_interaction(w3, private_key, contract1_address, contract2_address, contract1_abi, contract2_abi, function1_name, function2_name, *args):
    # Call function on the first contract
    send_transaction(w3, private_key, contract1_address, contract1_abi, function1_name, *args)

    # Call function on the second contract after the first
    send_transaction(w3, private_key, contract2_address, contract2_abi, function2_name, *args)


# Submit multiple transactions in a single batch
def submit_batch_transactions(w3, private_key, contract_address, abi, function_names_and_args):
    account = w3.eth.account.privateKeyToAccount(private_key)
    txns = []
    for function_name, args in function_names_and_args:
        contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
        function = getattr(contract.functions, function_name)
        txn = function(*args).buildTransaction({
            'chainId': 11155111,
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
        })
        signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
        txns.append(signed_txn)

    # Send transactions in parallel
    txn_hashes = [w3.eth.sendRawTransaction(txn.rawTransaction) for txn in txns]
    return [txn_hash.hex() for txn_hash in txn_hashes]


# Trigger self-destruct vulnerability
def trigger_self_destruct(w3, private_key, contract_address, abi):
    return send_transaction(
        w3=w3,
        private_key=private_key,
        contract_address=contract_address,
        abi=abi,
        function_name="selfDestruct"
    )

# Monitor account activity, such as Ether transfers in/out
def monitor_account_activity(w3, address, from_block='latest'):
    address_checksum = Web3.toChecksumAddress(address)
    tx_filter = w3.eth.filter({
        'fromBlock': from_block,
        'toBlock': 'latest',
        'address': address_checksum
    })
    events = tx_filter.get_all_entries()
    return events

# Orchestrate multi-step exploit
def orchestrate_exploit(w3, private_key, contract_address, abi, steps):
    account = w3.eth.account.privateKeyToAccount(private_key)

    for step in steps:
        function_name, args = step
        contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
        function = getattr(contract.functions, function_name)

        txn = function(*args).buildTransaction({
            'chainId': 11155111,
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
        })

        signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(f"Executed step: {function_name}, Txn hash: {txn_hash.hex()}")
