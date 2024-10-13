from langchain_core.tools import tool
import os
from api.agents.tools import compile_solidity_contract, deploy_malicious_contract, get_abi_and_source_code_etherscan, send_transaction, trigger_reentrancy_attack
from api.web3_connection import get_web3_connection
from schema import get_uploaded_contract_address_abi
from pydantic import Field
from typing import Annotated

@tool
def send_txn_tool(
    contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")],
    function_name: Annotated[str, Field(description="The name of the function to call on the smart contract")],
    value: Annotated[int, Field(description="The amount of Ether to send with the transaction, in wei")] = 0
) -> str:
    """
    Send a transaction to a smart contract.

    Args:
        contract_address (str): The address of the smart contract to interact with.
        function_name (str): The name of the function to call on the smart contract.
        value (int, optional): The amount of Ether to send with the transaction, in wei. Defaults to 0.

    Returns:
        str: The transaction hash of the sent transaction.

    This function retrieves the Web3 connection, gets the private key from the environment,
    fetches the ABI for the given contract address, and then sends a transaction to the
    specified function of the smart contract.
    """
    w3 = get_web3_connection()
    pk = os.getenv("WALLET_PRIVATE_KEY") # agent's private key in wallet
    abi_from_contract_address = get_uploaded_contract_address_abi(contract_address)
    txn_hash = send_transaction(w3, pk, contract_address, abi_from_contract_address, function_name, value)
    return txn_hash

@tool
def trigger_reentrancy_attack_tool(contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")]) -> str:
    """
    Triggers a reentrancy on the target contract by calling the malicious contract.

    Parameters:
        contract_address (str): Address of the malicious contract.
        private_key (str): Private key of the account calling the attack.
        contract_abi (list): ABI of the deployed malicious contract.

    Returns:
        str: Transaction hash of the transaction.
    """
    w3 = get_web3_connection()
    pk = os.getenv("WALLET_PRIVATE_KEY")
    abi_from_contract_address = get_abi_and_source_code_etherscan(contract_address)[1]
    txn_hash = trigger_reentrancy_attack(w3=w3, private_key=pk, contract_abi=abi_from_contract_address, contract_address=contract_address)
    return txn_hash

@tool
def deploy_malicious_contract_tool(
    source_code: Annotated[str, Field(description="The source code of the contract to deploy")],
    target_contract_address: Annotated[str, Field(description="The address of the target contract to attack")]
) -> str:
    """
    Deploys a malicious contract to the blockchain.

    This function compiles the provided Solidity source code, deploys the resulting bytecode
    to the blockchain, and returns the transaction hash of the deployment transaction.

    Args:
        source_code (str): The Solidity source code of the malicious contract to deploy.
        target_contract_address (str): The address of the target contract that the malicious
                                       contract will interact with or attack.

    Returns:
        str: The transaction hash of the contract deployment transaction.

    Note:
        This function uses the WALLET_PRIVATE_KEY from the environment variables to sign
        the deployment transaction. Ensure that the account associated with this private key
        has sufficient funds for the deployment.
    """
    w3 = get_web3_connection()
    pk = os.getenv("WALLET_PRIVATE_KEY")
    compiled_sol = compile_solidity_contract(source_code)
    bytecode = compiled_sol["bytecode"]
    abi = compiled_sol["abi"]
    txn_hash = deploy_malicious_contract(w3=w3, private_key=pk, bytecode=bytecode, abi=abi, target_contract_address=target_contract_address)
    return txn_hash


@tool
def get_uploaded_source_code_tool(contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")]) -> str:
    """
    Get the source code of a smart contract from Etherscan.

    Args:
        contract_address (str): The address of the smart contract to fetch the source code for.

    Returns:
        str: The source code of the smart contract.
    """
    return get_abi_and_source_code_etherscan(contract_address)[0]

@tool
def get_uploaded_abi_tool(contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")]) -> str:
    """
    Get the ABI of a smart contract from Etherscan.

    Args:
        contract_address (str): The address of the smart contract to fetch the source code for.

    Returns:
        str: The source code of the smart contract.
    """
    return get_abi_and_source_code_etherscan(contract_address)[0]