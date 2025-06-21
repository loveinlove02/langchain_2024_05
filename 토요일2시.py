from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from typing import List, Dict
from langchain.agents import tool
from langchain_teddynote.tools import GoogleNews

from langchain_teddynote.messages import AgentStreamParser
from langchain_teddynote.messages import AgentCallbacks

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
    """Look up news by keyword"""

    print(f'검색어: {query}')
    news_tool = GoogleNews()

    return news_tool.search_by_keyword(keyword=query, k=2)

tools = [add_numbers, multiply_numbers, search_keyword]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are a helpful assistant. '
            'Make sure to use the `search_news` tool for searching keyword related news.' 
            'Use the `add_numbers` tool to calculate the addition of two numbers.'
            'Use the `multiply_numbers` tool to calculate the multiplication of two numbers.'
        ),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}'),
    ]
)

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini'
)

agent = create_tool_calling_agent(llm, tools, prompt)

# agent 실행기
agent_executor = AgentExecutor(
    agent=agent,        # agent
    tools=tools,        # 도구
    verbose=False,      # 중간 단계 결과 안보이게
    max_iterations=10,  # 반복 10번
    max_execution_time=10,
    handle_parsing_errors=True
)

def tool_callback(tool) -> None:
    print(f'===== 도구 호출 =====')
    print(f'사용한 도구 : {tool.get("tool")}')
    print(f'====================')

def observation_callback(observation) -> None:
    print(f'===== 관찰 내용 =====')
    print(f'관찰 내용: {observation.get("observation")[0]}')
    print(f'====================')


def result_callback(result: str) -> None:
    print(f'===== 최종 결과 =====')
    print(result)
    print(f'====================')


agent_callbacks = AgentCallbacks(
    tool_callback=tool_callback,
    observation_callback=observation_callback,
    result_callback=result_callback
)

agent_stream_parser = AgentStreamParser(agent_callbacks)

result = agent_executor.stream({'input': 'AI 관련 뉴스를 검색해 주세요.'})

for step in result:
    agent_stream_parser.process_agent_steps(step)
