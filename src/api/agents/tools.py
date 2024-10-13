from web3 import Web3
import json
import os

# Load the contract ABI from a file
def load_abi(abi_path):
    with open(abi_path, 'r') as f:
        return json.load(f)

# Call a read-only function on a smart contract (does not cost gas)
def call_function(w3, contract_address, abi, function_name, *args, from_address=None):
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)

    # Include 'from' address if provided
    call_params = {'from': from_address} if from_address else {}
    result = function(*args).call(call_params)
    return result

def send_transaction(w3, private_key, contract_address, abi, function_name, *args, value=0):
    account = w3.eth.account.from_key(private_key)
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)

    # Build the transaction for non-payable functions
    txn = function(*args).build_transaction({
        'from': account.address,
        'value': value,  # Sending ether if needed (0 by default)
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price + 2000000000,  # Increase gas price slightly to avoid underpriced replacement
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 11155111  # Sepolia chain ID
    })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    # Send the transaction
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return txn_hash.hex()


# Send a payable transaction (used when sending Ether along with a function call)
def send_payable_transaction(w3, private_key, contract_address, abi, function_name, *args, value=0):
    account = w3.eth.account.from_key(private_key)
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)

    # Build the transaction for payable functions
    txn = function(*args).build_transaction({
        'from': account.address,
        'value': value,  # Ether to send
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 11155111  # Sepolia chain ID
    })

    # Sign and send the transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return txn_hash.hex()

# Check the balance of an address in Ether
def check_balance(w3, address):
    balance = w3.eth.get_balance(Web3.to_checksum_address(address))
    return w3.from_wei(balance, 'ether')

# Retrieve multiple pieces of data from a contract
def retrieve_contract_data(w3, contract_address, abi, function_name, *args):
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)
    data = function(*args).call()
    return data

# Monitor contract events (useful for reflection agent)
def monitor_events(w3, contract_address, abi, event_name, from_block='latest'):
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    event_filter = contract.events.__dict__[event_name].createFilter(fromBlock=from_block)
    
    # Retrieve all past events
    events = event_filter.get_all_entries()
    return events

# Retry transaction with exponential backoff
def retry_transaction(w3, private_key, contract_address, abi, function_name, *args, retries=3):
    for attempt in range(retries):
        try:
            txn_hash = send_transaction(w3, private_key, contract_address, abi, function_name, *args)
            return txn_hash  # Return successful transaction hash
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            continue
    raise RuntimeError("All retry attempts failed")

# Submit multiple transactions in a single batch
def submit_batch_transactions(w3, private_key, contract_address, abi, function_names_and_args):
    try:
        account = w3.eth.account.from_key(private_key)
        txns = []
        for function_name, args in function_names_and_args:
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
            function = getattr(contract.functions, function_name)
            txn = function(*args).build_transaction({
                'chainId': 11155111,
                'from': account.address,
                'nonce': w3.eth.get_transaction_count(account.address),
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price,
            })
            signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
            txns.append(signed_txn)

        # Send transactions in parallel
        txn_hashes = [w3.eth.send_raw_transaction(txn.raw_transaction) for txn in txns]
        return [txn_hash.hex() for txn_hash in txn_hashes]
    except Exception as e:
        print(f"Error in batch transaction: {str(e)}")
        raise

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
    address_checksum = Web3.to_checksum_address(address)
    tx_filter = w3.eth.filter({
        'fromBlock': from_block,
        'toBlock': 'latest',
        'address': address_checksum
    })
    events = tx_filter.get_all_entries()
    return events

# Orchestrate multi-step exploit
def orchestrate_exploit(w3, private_key, contract_address, abi, steps):
    account = w3.eth.account.from_key(private_key)

    for step in steps:
        function_name, args = step
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
        function = getattr(contract.functions, function_name)

        txn = function(*args).build_transaction({
            'chainId': 11155111,
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"Executed step: {function_name}, Txn hash: {txn_hash.hex()}")

# Generic smart contract function call
def call_contract_function(w3, private_key, contract_address, abi, function_name, *args, value=0):
    account = w3.eth.account.from_key(private_key)
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)

    txn = function(*args).build_transaction({
        'chainId': 11155111,  # Sepolia Chain ID
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'value': value,  # If ETH is required
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    return txn_hash.hex()

def read_contract_function(w3, contract_address, abi, function_name, *args):
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    function = getattr(contract.functions, function_name)
    result = function(*args).call()
    return result

def retry_transaction(w3, private_key, contract_address, abi, function_name, *args, value=0, retries=3):
    for attempt in range(retries):
        try:
            txn_hash = call_contract_function(w3, private_key, contract_address, abi, function_name, *args, value=value)
            return txn_hash  # Return successful transaction hash
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            continue
    raise RuntimeError("All retry attempts failed")
