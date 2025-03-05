from langchain_core.tools import tool
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


tools = [search_keyword, python_repl_tool]

# 프롬 프트
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are a helpful assistant. '
            'Make sure to use the `search_keyword` tool for searching keyword related news.'
            'Make sure to use the `python_repl_tool` tool when make python code.'
        ),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}')
    ]
)

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# tools 도구 리스트, prompt, llm 을 가지고 에이전트를 만들기
agent = create_tool_calling_agent(llm, tools, prompt)

# 에이전트 실행기
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    max_iterations=10,
    max_execution_time=10,
    handle_parsing_errors=True
)

result = agent_executor.stream({'input': '피보나치 수열 5번째 항까지 출력하는 파이썬 코드'})

i = 1
for step in result:
    print('============================================================')
    print(f'[{i}] step')
    print(step)
    i=i+1
    print('============================================================')
