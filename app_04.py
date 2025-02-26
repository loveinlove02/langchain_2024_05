from langchain_core.tools import tool
from typing import List, Dict
from langchain_teddynote.tools import GoogleNews

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""

    return a + b

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""

    print(f'검색어 : {query}')

    news_tool = GoogleNews()

    return news_tool.search_by_keyword(query, k=1)


# 실제로 도구를 실행 하는 함수
def execute_tool_calls(tool_call_results):
    """
    도구 호출 결과를 실행하는 함수

    :param tool_call_results: 도구 호출 결과 리스트
    :param tools: 사용 가능한 도구 리스트
    """


    for tool_call_result in tool_call_results:
        tool_name = tool_call_result['type']
        tool_agrs = tool_call_result['args']

        matching_tool = None

        for tool in tools:      # [add_numbers, search_keyword]
            if tool.name == tool_name:  # tool 리스트 이름 == 실행할 이름
                matching_tool = tool
                break

        if matching_tool:
            result = matching_tool.invoke(tool_agrs)
            print(result)
        else:
            print("경고: 실행할 도구를 찾을 수 없습니다.")



# llm (모델 gpt-4o-mini) 만들기
llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

# 우리가 만들어 놓은 도구(함수) : add_numbers, search_keyword
tools = [add_numbers, search_keyword]

# llm 에 도구를 쥐여 준다 (llm 에 도구를 바인딩)
llm_with_tools = llm.bind_tools(tools)

chain = llm_with_tools | JsonOutputToolsParser(tools=tools)

tool_call_result = chain.invoke('10 더하기 20은?')
execute_tool_calls(tool_call_result)

# print(tool_call_result)
# print(tool_call_result[0]['args'])  # 실행할 내용(인자)
# print(tool_call_result[0]['type'])  # 실행할 도구 이름(함수)
