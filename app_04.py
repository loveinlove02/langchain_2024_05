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


# print(f'도구 이름: {search_keyword.name}')
# print(f'도구 설명: {search_keyword.description}')

# 2개의 도구를 리스트에 넣는다
tools = [search_keyword, add_function]

# Agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "             
            "Make sure to use the `search_news` tool for searching keyword related news."
        ),
        ("placeholder", "{chat_history}"),          # 이전 대화 내용을 넣을 곳을 잡아둔다.
        ("human", "{input}"),                       # 사용자 입력
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# llm 만들기
llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# 에이전트 생성 : llm + 도구들 + 프롬프트
agent = create_tool_calling_agent(llm, tools, prompt)

# 에이전트 실행기 생성
agent_executor = AgentExecutor(
    agent=agent,        # 각 단계에서 계획을 생성하고 행동을 결정하는 에이전트
    tools=tools,        # 에이전트가 사용할 도구 리스트(함수)
    verbose=False,      # 중단 단계 출력
    max_iterations=10,  # 최대 반복 횟수
    max_execution_time=10,  # 실행되는데 소요되는 최대 시간
    handle_parsing_errors=True
)

answer = agent_executor.invoke({'input': '10+20의 결과는?'})
print(answer)
