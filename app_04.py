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

@tool()
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""

    print(f"검색어: {query}")
    news_tool = GoogleNews()

    return news_tool.search_by_keyword(query, k=2)

'''
answer = search_keyword.invoke({'query': '트럼프'})
for i in answer:
    print(i)
'''
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
        print(f"코드 실행 실패 : {repr(e)}")
    finally:
        return  result

# 테스트
'''
answer = python_repl_tool.invoke({'code': 'print(1+2)'})
print(answer)
'''

# 에이전트 프롬프트
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant."
            "Make sure to use the `search_keyword` tool for searching keyword related news."
            "Be sure to use the `python_repl_tool` tool when make python code."
        ),
        ('placeholder', '{chat_history}'),       # 대화 내용들 집어 넣을 공간
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}')
    ]
)


tools = [search_keyword, python_repl_tool]
