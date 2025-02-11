from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

from langchain_community.tools.tavily_search import TavilySearchResults

tavily_key = os.getenv('TAVILY_API_KEY')

tool = TavilySearchResults(
    key = tavily_key,
    max_results=2,              # 검색 결과 수
    search_depth='advanced',    # Tavily 검색 API가 광범위한 검색
    include_raw_content=True,   # 검색 결과의 원본 내용 포함
    include_answer=True,        # 검색 결과를 바탕으로 생성된 답변 포함
    include_domains=['google.com', 'naver.com']
)

answer = tool.invoke({'query': '대한민국 2024년 계엄령'})

answer
