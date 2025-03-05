from langchain_core.tools import tool
from typing import List, Dict, Annotated
from langchain_teddynote.tools import GoogleNews
from langchain_experimental.utilities import PythonREPL

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""

    print(f'검색어: {query}')
    news_tool = GoogleNews()

    return news_tool.search_by_keyword(query, k=2)

@tool
def python_repl_tool(
        code: Annotated[str, "The python code to execute to generate your chart."]
):
    """Use this to execute to python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""

    result = ""

    try:
        result = PythonREPL().run(code)
    except BaseException as e:
        print(f'실패 오류 : {repr(e)}')
    finally:
        return  result

a = """
for i in range(1, 6, 1):
    print(i)
"""
answer = python_repl_tool.invoke({'code' : a})
print(answer)

