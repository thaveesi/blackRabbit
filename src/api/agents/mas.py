import functools
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from api.agents.lc_tools import deploy_malicious_contract_tool, get_uploaded_abi_tool, get_uploaded_source_code_tool, send_txn_tool, trigger_reentrancy_attack_tool
from api.agents.llms import create_gpt_4, create_wrn
from langchain_core.messages import AIMessage, ToolMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Annotated, Sequence, TypedDict
import operator
from api.agents.constants import planner_system_prompt, executor_system_prompt, smart_contract_writer_system_prompt, reflector_system_prompt, reporter_system_prompt

from langgraph.prebuilt import ToolNode

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str


def create_agent(llm, tools=None, system_message: str = ""):
    """Create an agent."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant, collaborating with other assistants."
                " {tool_instruction}"
                " If you are unable to fully answer, that's OK, another assistant with different tools "
                " will help where you left off. Execute what you can to make progress."
                " If you or any of the other assistants have the final answer or deliverable,"
                " prefix your response with FINAL ANSWER so the team knows to stop."
                "{tool_names}\n{system_message}"
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    
    if tools:
        tool_instruction = "Use the provided tools to progress towards answering the question."
        tool_names = " You have access to the following tools: " + ", ".join([tool.name for tool in tools]) + "."
        prompt = prompt.partial(tool_instruction=tool_instruction, tool_names=tool_names)
        return prompt | llm.bind_tools(tools)
    else:
        prompt = prompt.partial(tool_instruction="", tool_names="")
        return prompt | llm

# Helper function to create a node for a given agent
def agent_node(state, agent, name, msg_role = "ai"):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        if msg_role == "ai":
            result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
        else:
            result = HumanMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }

def router(state):
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        # The previous agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return "continue"


def create_graph():
    planner_tools = [get_uploaded_source_code_tool, get_uploaded_abi_tool, deploy_malicious_contract_tool, trigger_reentrancy_attack_tool, send_txn_tool]
    executor_tools = [send_txn_tool, deploy_malicious_contract_tool, trigger_reentrancy_attack_tool, get_uploaded_source_code_tool, get_uploaded_abi_tool]
    smart_contract_writer_tools = [
        get_uploaded_source_code_tool,
        get_uploaded_abi_tool,
    ]
    tools = planner_tools + executor_tools + smart_contract_writer_tools
    wrn = create_wrn()
    gpt4 = create_gpt_4()

    planner_agent = create_agent(llm=gpt4, tools=planner_tools, system_message=planner_system_prompt)
    executor_agent = create_agent(llm=gpt4, tools=executor_tools, system_message=executor_system_prompt)
    smart_contract_writer_agent = create_agent(llm=wrn, tools=smart_contract_writer_tools, system_message=smart_contract_writer_system_prompt)
    reflector_agent = create_agent(llm=gpt4, tools=planner_tools, system_message=reflector_system_prompt)
    reporter_agent = create_agent(llm=gpt4, tools=planner_tools, system_message=reporter_system_prompt)

    planner_node = functools.partial(agent_node, agent=planner_agent, name="planner")
    executor_node = functools.partial(agent_node, agent=executor_agent, name="executor")
    smart_contract_writer_node = functools.partial(agent_node, agent=smart_contract_writer_agent, name="smart_contract_writer")
    reflector_node = functools.partial(agent_node, agent=reflector_agent, name="reflector", msg_role="ai")
    reporter_node = functools.partial(agent_node, agent=reporter_agent, name="reporter")
    tools_node = ToolNode(tools=tools)


    graph_builder = StateGraph(State)
    graph_builder.add_node("planner", planner_node)
    graph_builder.add_node("executor", executor_node)
    graph_builder.add_node("smart_contract_writer", smart_contract_writer_node)
    graph_builder.add_node("reflector", reflector_node)
    graph_builder.add_node("reporter", reporter_node)
    graph_builder.add_node('call_tool', tools_node)

    graph_builder.add_edge(START, "planner")
    graph_builder.add_conditional_edges(
        "planner",
        router,
        {"continue": "executor", "call_tool": "call_tool", END: END},
    )
    graph_builder.add_conditional_edges(
        "executor",
        router,
        {"continue": "reflector", "call_tool": "call_tool", END: "reporter"},
    )
    graph_builder.add_conditional_edges(
        "smart_contract_writer",
        router,
        {"continue": "reflector", "call_tool": "call_tool", END: END},
    )
    graph_builder.add_conditional_edges(
        "reflector",
        router,
        {"continue": "executor", "call_tool": "call_tool", END: "reporter"},
    )
    graph_builder.add_conditional_edges(
        "reporter",
        router,
        {"continue":END, "call_tool": END, END: END},
    )

    graph_builder.add_conditional_edges(
        "call_tool",
        # Each agent node updates the 'sender' field
        # the tool calling node does not, meaning
        # this edge will route back to the original agent
        # who invoked the tool
        lambda x: x["sender"],
        {
            "planner": "planner",
            "executor": "executor",
            "smart_contract_writer": "smart_contract_writer",
            "reflector": "reflector",
        },
    )

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    return graph

def run(graph):
    addr = "0x8d4255bf30Ad54BAdcc672fAE977b9D3f15C3f18, 0xBf7446A56F00f88FF72A7C57Db945EE2132F421d, 0xD1A5c53E7F930248083597Ba88C84c1b087ED89e"
    user_input = f"Create a plan to find problems in this smart contract at these addresses: {addr}"
    config = {"configurable": {"thread_id": "1"}}
    # The config is the **second positional argument** to stream() or invoke()!
    events = graph.stream({"messages": [HumanMessage(content=user_input)]}, config, stream_mode="values")
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()
    


if __name__ == "__main__":
    graph = create_graph()
    run(graph)