from langchain.tools import tool
from typing import List, Dict
from langchain_teddynote.tools import GoogleNews

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


res = search_keyword.invoke({'query': '김민석 의원'})
print(res)
