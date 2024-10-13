from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv
load_dotenv()


def create_wrn():
    wrn_llm = ChatOpenAI(
        model="/models/WhiteRabbitNeo-33B-DeepSeekCoder",
        default_headers={"api-key":os.getenv("KINDO_API_KEY")},
        api_key=os.getenv("KINDO_API_KEY"),
        # temperature=0.8,
        base_url="https://llm.kindo.ai/v1",
    )
    return wrn_llm


def create_gpt_4():
    llm = ChatOpenAI(
        model="gpt-4o",
        # temperature=0.8,
        # model="azure/gpt-4o",
        # default_headers={"api-key": os.getenv("KINDO_API_KEY")},
        # api_key=os.getenv("KINDO_API_KEY"),
        api_key=os.getenv("OPENAI_API_KEY"),
        # base_url="https://llm.kindo.ai/v1",
    )
    return llm

def create_claude():
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        temperature=0.8,
        # max_tokens=1024,
        # default_headers={"api-key": os.getenv("KINDO_API_KEY")},
        # api_key=os.getenv("KINDO_API_KEY"),
        api_key=os.getenv("CLAUDE_API_KEY"),
        # base_url="https://llm.kindo.ai/v1",
    )
    return llm