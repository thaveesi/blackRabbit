import requests

# Multi-line markdown content stored in a variable
new_results = """
## Vulnerability Report

- **Issue 1:** Reentrancy vulnerability
  - Description: A reentrancy attack can allow malicious actors to drain funds.
  - Fix: Use `checks-effects-interactions` pattern.

- **Issue 2:** Integer underflow
  - Description: Integer underflow may cause unexpected behavior in contract logic.
  - Fix: Use SafeMath library to prevent underflow.
"""

# Define the API endpoint and payload
url = "http://127.0.0.1:5000/reports/append/contract_1728781838"
payload = {"results": new_results}

# Send the POST request with the JSON payload
response = requests.post(url, json=payload)

# Print the response
print(response.json())