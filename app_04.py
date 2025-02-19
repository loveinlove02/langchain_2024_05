from langchain_core.tools import tool
from typing import List, Dict
from langchain_teddynote.tools import GoogleNews

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""

    return a + b

@tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers"""

    return a * b

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""

    print(f'검색어 : {query}')

    news_tool = GoogleNews()

    return news_tool.search_by_keyword(query, k=3)


answer = search_keyword.invoke({'query': '백종원'})
print(answer)

for i in range(0, len(answer), 1):
    print(answer[i]['url'])
    print(answer[i]['content'])
    print()
