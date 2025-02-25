import requests
import re
from bs4 import BeautifulSoup
from humanfriendly.terminal import ansi_width

from langchain.agents import tool
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word"""
    return len(word)

@tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def naver_news_crawl(news_url: str) -> str:
    """Crawls a 네이버(naver.com) news article and returns the body content"""

    response = requests.get(news_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h2', id='title_area').get_text()
        content = soup.find('div', id='contents').get_text()

        cleaned_title = re.sub(r'\n{2, }', '\n', title)
        cleaned_content = re.sub(r'\n{2, }', '\n', content)

        return f'{cleaned_title}\n{cleaned_content}'
    else:
        return f'HTTP 요청 실패 {response.status_code}'


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events."),
        ("user", "{input}"),
        # 에이전트가 검색하는 과정에서 중간 단계를 끄적이는 기능으로..
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# 도구 목록 리스트
tools = [get_word_length, multiply_numbers, naver_news_crawl]

# 에이전트
agent = create_tool_calling_agent(llm, tools, prompt)

# 에이전트 실행기
agent_executor = AgentExecutor(
    agent=agent,        # 에이전트
    tools=tools,        # 내가 만든 도구들 (리스트)
    verbose=True,       # 중간 단계들의 메시지
    handle_parsing_errors=True
)

answer = agent_executor.invoke({"input": "`안녕하세요` 의 길이는?"})
print(answer)
print(answer['output'])
