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

# muz.so/랭체인스터디5

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""
    news_tool = GoogleNews()
    return news_tool.search_by_keyword(query, k=2)

@tool
def python_repl_tool(code: Annotated[str, "The python code to execute to generate your chart."]):
    """Use this to execute python code. If you want to see the output of a value,
       you should print it out with `print(...)`. This is visible to the user."""

    result = ""

    try:
        result = PythonREPL().run(code)
    except BaseException as e:
        print(f"오류: {repr(e)}")
    finally:
        return result

tools = [search_keyword, python_repl_tool]

# 1. 에이전트 프롬프트
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are a helpful assistant. '
            'Make sure to use the `search_keyword` tool for searching keyword related news. '
            'Use the `python_repl_tool` when executing Python code'
        ),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}')
    ]
)

# 2. LLM
llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# 3.에이전트 생성
agent = create_tool_calling_agent(llm, tools, prompt)

# 4.에이전트 실행기(AgentExecutor)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

answer = agent_executor.invoke({'input': '선거'})
print(answer)

answer2 = agent_executor.invoke({'input': '1~100까지 합을 출력하는 파이썬 코드 작성 및 실행'})
print(answer2)
