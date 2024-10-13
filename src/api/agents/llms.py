from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


def create_wrn():
    wrn_llm = ChatOpenAI(
        default_headers={"api-key":os.getenv("KINDO_API_KEY")},
        model="/models/WhiteRabbitNeo-33B-DeepSeekCoder",
        api_key=os.getenv("KINDO_API_KEY"),
        base_url="https://llm.kindo.ai/v1",
    )
    return wrn_llm


def create_gpt_4():
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return llm