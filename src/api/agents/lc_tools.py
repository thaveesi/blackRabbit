from langchain_core.tools import tool
import os
from api.agents.llms import create_gpt_4, create_wrn
from api.agents.tools import compile_solidity_contract, deploy_malicious_contract, get_abi_from_etherscan, get_source_code_from_etherscan, send_transaction, trigger_reentrancy_attack
from api.web3_connection import get_web3_connection
from schema import get_uploaded_malicious_contract_abi, insert_malicious_contract
from pydantic import Field
from typing import Annotated
from langchain.prompts import ChatPromptTemplate

@tool
def send_transaction_tool(
    contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")],
    function_name: Annotated[str, Field(description="The name of the function to call on the smart contract")],
    value: Annotated[int, Field(description="The amount of Ether to send with the transaction, in wei")] = 0,
    function_args: Annotated[list, Field(description="The arguments to pass to the function")] = []
) -> str:
    """
    Send a transaction to a smart contract.

    Args:
        contract_address (str): The address of the smart contract to interact with.
        function_name (str): The name of the function to call on the smart contract.
        value (int, optional): The amount of Ether to send with the transaction, in wei. Defaults to 0.
        function_args (list, optional): The arguments to pass to the function. Defaults to [].
    Returns:
        str: The transaction hash of the sent transaction.

    This function retrieves the Web3 connection, gets the private key from the environment,
    fetches the ABI for the given contract address, and then sends a transaction to the
    specified function of the smart contract.
    """
    w3 = get_web3_connection()
    pk = os.getenv("WALLET_PRIVATE_KEY") # agent's private key in wallet
    abi_from_contract_address = get_abi_from_etherscan(contract_address)
    txn_hash = send_transaction(w3=w3, private_key=pk, contract_address=contract_address, abi=abi_from_contract_address, function_name=function_name, value=value, function_args=function_args)
    return txn_hash

@tool
def send_transaction_to_malicious_contract_tool(
    contract_address: Annotated[str, Field(description="The address of the malicious contract to interact with")],
    function_name: Annotated[str, Field(description="The name of the function to call on the malicious contract")],
    value: Annotated[int, Field(description="The amount of Ether to send with the transaction, in wei")] = 0,
    function_args: Annotated[list, Field(description="The arguments to pass to the function")] = []
) -> str:
    """
    Send a transaction to a malicious smart contract.

    Args:
        contract_address (str): The address of the malicious smart contract to interact with.
        function_name (str): The name of the function to call on the malicious smart contract.
        value (int, optional): The amount of Ether to send with the transaction, in wei. Defaults to 0.
        function_args (list, optional): The arguments to pass to the function. Defaults to [].
    Returns:
        str: The transaction hash of the sent transaction.

    This function retrieves the Web3 connection, gets the private key from the environment,
    fetches the ABI for the given malicious contract address, and then sends a transaction to the
    specified function of the malicious smart contract. This tool is specifically designed for
    interacting with known malicious contracts, typically as part of security testing or
    vulnerability demonstration.
    """
    w3 = get_web3_connection()
    pk = os.getenv("WALLET_PRIVATE_KEY") # agent's private key in wallet
    abi_from_contract_address = get_uploaded_malicious_contract_abi(contract_address)
    txn_hash = send_transaction(w3=w3, private_key=pk, contract_address=contract_address, abi=abi_from_contract_address, function_name=function_name, value=value, function_args=function_args)
    return txn_hash


@tool
def trigger_reentrancy_attack_tool(contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")]) -> str:
    """
    Triggers a reentrancy on the target contract by calling the malicious contract.

    Parameters:
        contract_address (str): Address of the malicious contract.

    Returns:
        str: Transaction hash of the transaction.
    """
    w3 = get_web3_connection()
    pk = os.getenv("WALLET_PRIVATE_KEY")
    abi_from_contract_address = get_abi_from_etherscan(contract_address)
    print('abi_from_contract_address', abi_from_contract_address)
    txn_hash = trigger_reentrancy_attack(w3=w3, private_key=pk, contract_abi=abi_from_contract_address, contract_address=contract_address)
    return txn_hash

@tool
def deploy_malicious_contract_tool(
    source_code: Annotated[str, Field(description="The source code of the contract to deploy")],
    target_contract_address: Annotated[str, Field(description="The address of the target contract to attack")],
    contract_name: Annotated[str, Field(description="The name of the contract to deploy")],
) -> str:
    """
    Deploys a malicious contract to the blockchain.

    This function compiles the provided Solidity source code, deploys the resulting bytecode
    to the blockchain, and returns the transaction hash of the deployment transaction.

    Args:
        source_code (str): The Solidity source code of the malicious contract to deploy.
        target_contract_address (str): The address of the target contract that the malicious
                                       contract will interact with or attack.
        contract_name (str): The name of the contract to deploy.
    Returns:
        str: The transaction hash of the contract deployment transaction.

    Note:
        This function uses the WALLET_PRIVATE_KEY from the environment variables to sign
        the deployment transaction. Ensure that the account associated with this private key
        has sufficient funds for the deployment.
    """
    w3 = get_web3_connection()
    pk = os.getenv("WALLET_PRIVATE_KEY")
    compiled_sol = compile_solidity_contract(source_code, contract_name)
    bytecode = compiled_sol["bytecode"]
    abi = compiled_sol["abi"]
    addr = deploy_malicious_contract(w3=w3, private_key=pk, bytecode=bytecode, abi=abi, target_contract_address=target_contract_address)
    insert_malicious_contract(addr=addr, source_code=source_code, abi=abi, bytecode=bytecode)
    return addr


@tool
def get_uploaded_source_code_tool(contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")]) -> str:
    """
    Get the source code of a smart contract from Etherscan.

    Args:
        contract_address (str): The address of the smart contract to fetch the source code for.

    Returns:
        str: The source code of the smart contract.
    """
    return get_source_code_from_etherscan(contract_address)

@tool
def get_uploaded_abi_tool(contract_address: Annotated[str, Field(description="The address of the smart contract to interact with")]) -> str:
    """
    Get the ABI of a smart contract from Etherscan.

    Args:
        contract_address (str): The address of the smart contract to fetch the source code for.

    Returns:
        str: The source code of the smart contract.
    """
    return get_abi_from_etherscan(contract_address)

@tool
def generate_smart_contract_tool(query: Annotated[str, Field(description="A description of the smart contract to be generated")]) -> str:
    """
    Generate a smart contract based on a given query.

    Args:
        query (str): A description of the smart contract to be generated.

    Returns:
        str: The generated smart contract source code.
    """
    chat = create_gpt_4()
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert Solidity developer. Generate a smart contract based on the following description:

        {query}

        Please follow these guidelines:
        1. Provide only the Solidity code without any additional explanation.
        2. Name your contract 'Malicious'.
        3. Ensure the code is well-structured and follows Solidity best practices.
        5. Use clear and descriptive variable and function names.
        4. If you're writing a reentrancy attack contract, name your attack function as "attack".
        """
    )
    chain = prompt | chat
    result = chain.invoke({"query": query})
    return result.content
