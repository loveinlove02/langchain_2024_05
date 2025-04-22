from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')
tavily_key = os.getenv('TAVILY_API_KEY')

tool = TavilySearchResults(
    key=tavily_key,
    max_results=5,                      # 반환되는 최대 검색 결과 수(기본값: 5)
    include_answer=False,               # 원본 질문(쿼리)에 대한 짧은 답변 포함 여부
    include_raw_content=False,          # HTML 컨텐츠 여부
    include_domains=['www.naver.com', 'namu.wiki'],
    # exclude_domains=[]
)
answer = tool.invoke({'query': '농심 안성탕면'})
print(answer)

for data in answer:
    print(data['title'])
    print(data['url'])
    print(data['content'])
