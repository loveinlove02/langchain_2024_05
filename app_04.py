from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.agents import tool
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from langchain_teddynote.tools import GoogleNews
from typing import List, Dict, Annotated

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

@tool
def add_function(a:float, b:float) -> float:
    """Adds two numbers together."""
    return a+b

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""

    print(f'검색어 : {query}')
    news_tool = GoogleNews()        # 구글 뉴스 검색 객체
    answer = news_tool.search_by_keyword(query, k=3)

    return answer

