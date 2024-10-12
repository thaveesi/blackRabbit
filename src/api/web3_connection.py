from web3 import Web3

def get_web3_connection():
    alchemy_url = 'https://eth-sepolia.g.alchemy.com/v2/9yYPvzqaFmhxrKk7MhgRxNr4jRpt8KnO'
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    
    if w3.is_connected():  # Corrected the attribute name here
        print("Connected to Sepolia Testnet")
        return w3
    else:
        raise ConnectionError("Failed to connect to Sepolia Testnet")
