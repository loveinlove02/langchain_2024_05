from langchain.tools import tool
from typing import List, Dict
from langchain_teddynote.tools import GoogleNews

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""

    return a+b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers"""

    return a*b

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up new by keyword"""

    print(f'검색어: {query}')
    news_tool = GoogleNews()

    return news_tool.search_by_keyword(keyword=query, k=2)


# 도구 목록 리스트
tools = [add_numbers, multiply_numbers, search_keyword]

# llm
llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# 도구를 가진 llm
llm_with_tools = llm.bind_tools(tools)

# chain
chain = llm_with_tools | JsonOutputToolsParser(tools=tools)
tool_call_result = chain.invoke('이스라엘 공격')

print(tool_call_result)
# [{'args': {'query': '이스라엘 공격'}, 'type': 'search_keyword'}]

print(tool_call_result[0])
# {'args': {'query': '이스라엘 공격'}, 'type': 'search_keyword'}

print(tool_call_result[0]['args'])
# {'query': '이스라엘 공격'}

print(tool_call_result[0]['type'])
# search_keyword
