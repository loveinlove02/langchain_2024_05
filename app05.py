from langchain.tools import tool
from typing import List, Dict
from langchain_teddynote.tools import GoogleNews
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

from langchain_teddynote.messages import AgentStreamParser
from  langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.agent_toolkits import FileManagementToolkit


from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')


@tool
def lastest_news(k: int = 5) -> List[Dict[str, str]]:
    """Look up lastest news"""

    print('구글 뉴스 검색 (최근 뉴스)')
    news_tool = GoogleNews()
    
    return news_tool.search_latest(k=k)


# 폴더 생성하고 시작.
if not os.path.exists('tmp'):   # tmp 라는 폴더가 없으면
    os.mkdir('tmp')             # tmp 라는 이름의 폴더를 만든다


working_directory = 'tmp'

tools = FileManagementToolkit(
    root_dir=str(working_directory)
).get_tools()

# 파일 도구, 뉴스 검색 도구
tools.append(lastest_news)

llm = ChatOpenAI(
    api_key=key, 
    model='gpt-4o-mini'
)

prompt = ChatMessagePromptTemplate.format_messages(
    [
        (
            'system',
            'You are a helpful assistant. '
            'Make sure to use `lastest_news` tool to find lastest news. '
            'Make sure to use `file_management` tool to manage files. '
        ),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}')
    ]
)
