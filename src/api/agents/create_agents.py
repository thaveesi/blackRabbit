from web3 import Web3
import json
import os
from api.web3_connection import get_web3_connection  # Adjust this based on your structure
import sys

# File to store agent wallet data
AGENTS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "agents.json"))

def create_agent_wallets(num_agents=5):
    print("Starting the agent wallet creation process...")
    sys.stdout.flush()

    # Get Web3 connection using your existing function
    web3 = get_web3_connection()

    # Check Web3 connection
    if not web3.is_connected():
        raise ConnectionError("Web3 connection failed.")
    else:
        print("Connected to Web3.")

    agent_wallets = []
    for i in range(num_agents):
        new_account = web3.eth.account.create()
        agent_wallets.append({
            'address': new_account.address,
            'private_key': new_account.key.hex()
        })
        print(f"Created wallet {i+1} with address: {new_account.address}")
        sys.stdout.flush()

    # Store agent wallet data in a JSON file
    print(f"Saving agent wallets to {AGENTS_FILE}")
    with open(AGENTS_FILE, 'w') as f:
        json.dump(agent_wallets, f, indent=4)

    print(f"Agent wallets successfully saved to {AGENTS_FILE}")
    print(f"Created {num_agents} agent wallets and saved to {AGENTS_FILE}")
    print(agent_wallets)
    sys.stdout.flush()

    return agent_wallets

if __name__ == "__main__":
    create_agent_wallets(5)
