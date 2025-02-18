import requests
import re
from bs4 import BeautifulSoup

# url = "https://n.news.naver.com/article/011/0004451835?cds=news_media_pc"
url = input('네이버 뉴스 주소: ')

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h2', id='title_area').get_text()
    content = soup.find('div', id='contents').get_text()

    cleaned_title = re.sub(r'\n{2, }', '\n', title)
    cleaned_content = re.sub(r'\n{2, }', '\n', content)

    print(f'제목: {cleaned_title}')
    print('본문')
    print('==' * 20)
    print(cleaned_content)

else:
    print(f'HTTP 요청 실패 {response.status_code}')
