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

    print(f"----------------------------")
    print(f"search_keyword 실행 시작")
    print(f"검색어: {query}")
    news_tool = GoogleNews()
    print(f"----------------------------")
    return news_tool.search_by_keyword(query, k=1)

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

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# 에이전트
agent = create_tool_calling_agent(llm, tools, prompt)

# 에이전트 실행기
agent_executor = AgentExecutor(
    agent=agent,        # 각 단계에서 계획을 생성하고 행동을 결정하는 agent
    tools=tools,        # agent 가 사용할 수 있는 도구 목록
    verbose=False,       # 중간 단계에서 실행되는 결과를 보고...
    max_iterations=10,  # 최대 10번까지 반복
    max_execution_time=10,
    handle_parsing_errors=True
)

result = agent_executor.stream({'input': '10 + 20을 출력하는 파이썬 코드'})

for step in result:
    if 'actions' in step:
        print('==' * 50)
        print(f'[actions]:')
        print(step['actions'])
        print('==' * 50)
    elif 'steps' in step:
        print('==' * 50)
        print(f'[steps]:')
        print(step['steps'])
        print('==' * 50)
    elif 'output' in step:
        print('==' * 50)
        print(f'[output]:')
        print(step['output'])
        print('==' * 50)

# i = 1
# for step in result:
#     print(f"실행 [{i}] :\n")
#     print(step)
#     print('=='*50)
#     i=i+1
