import requests
import re
from bs4 import BeautifulSoup
from langchain.agents import tool

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

url = "https://n.news.naver.com/article/011/0004451835?cds=news_media_pc"
answer = naver_news_crawl.invoke({'news_url': url})
print(answer)

