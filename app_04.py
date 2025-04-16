from langchain.agents import tool
from typing import List, Dict, Annotated

from langchain_teddynote.tools import GoogleNews
from langchain_experimental.utilities import PythonREPL


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""

    print(f'검색어: {query}')
    news_tool = GoogleNews()

    return news_tool.search_by_keyword(query, k=1)


@tool
def python_repl_tool(
        code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""

    result = ""

    try:
        result = PythonREPL().run(code)
    except BaseException as e:
        print(f"Failed to execute. Error: {repr(e)}")
    finally:
        return result


prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are a helpful assistant. '
            'Make sure to use `search_news` tool for searching keyword related news.'
            'Be sure to use `python_repl_tool` tool when make python code.'
        ),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}')
    ]
)
