import requests
import re
from bs4 import BeautifulSoup

from langchain.agents import tool
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser

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

 # [{'args': {'word': '안녕하세요'}, 'type': 'get_word_length'}]
def execute_tool_calls(tool_call_results):
    """
    도구 호출 결과를 실행하는 함수
    :param tool_call_result: 도구 호출 결과 리스트
    :param tools: 사용 가능한 도구 리스트
    """
    print(f"tool_call_result: {tool_call_results}")
    print('=' * 100)

    for tool_call_result in tool_call_results:
        tool_name = tool_call_result['type']    # 도구(함수)의 이름
        tool_agrs = tool_call_result['args']    # 도구(함수)에 전달되는 인자

        matching_tool = None

        for tool in tools:      # tools 리스트 반복하면 실행할 실제 도구 찾을
            if tool.name == tool_name:
                matching_tool = tool
                break

        if matching_tool:      # 실행 도구를 찾았으면
            result = matching_tool.invoke(tool_agrs)
            print(f"[실행 도구]: {tool_name} [인자]: {tool_agrs}")
            print(f"[실행 결과]: {result}")
        else:
            print(f"경고: {tool_name}에 맞는 도구가 없음")


llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# 도구 목록 리스트
tools = [get_word_length, multiply_numbers, naver_news_crawl]

llm_with_tools = llm.bind_tools(tools)
chain = llm_with_tools | JsonOutputToolsParser(tools=tools)

tool_call_result = chain.invoke("10 x 20 은")

# tool_call_result = chain.invoke("`안녕하세요`의 길이는?")

# url = "https://n.news.naver.com/article/011/0004451835?cds=news_media_pc"
# tool_call_result = chain.invoke("다음의 url의 네이버 뉴스를 겁색해주세요:" + url)

execute_tool_calls(tool_call_result)
