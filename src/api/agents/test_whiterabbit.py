from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    default_headers={"api-key":"c2b055eb-ca51-4e5d-a420-f056bba93b67-272414f9099e72b9" },
    model="/models/WhiteRabbitNeo-33B-DeepSeekCoder",
    temperature=0,
    api_key="c2b055eb-ca51-4e5d-a420-f056bba93b67-272414f9099e72b9",
    max_tokens=256,
    # timeout=None,
    # max_retries=2,
    base_url="https://llm.kindo.ai/v1",
)

messages = [
    (
        "system",
        """
### Your task:
For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps. 

### The objective: attack this smart contract using whatever apis/tools appropriate. 
        """,
    ),
    ("human", """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BasicVulnerableContract {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        (bool success, ) = msg.sender.call\{\value: _amount}(\"\");
        require(success, "Transfer failed");

        balances[msg.sender] -= _amount;
    }


    function resetBalance(address _user) public {
        balances[_user] = 0;
    }


    function decreaseBalance(uint256 _amount) public {
        balances[msg.sender] -= _amount; // Underflow if _amount > balances[msg.sender]
    }

    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
"""),
]
ai_msg = llm.invoke(messages)
print(ai_msg)