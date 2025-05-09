from langchain.tools import tool
from typing import List, Dict
from langchain_teddynote.tools import GoogleNews
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
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

prompt = ChatPromptTemplate.from_messages(
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


agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,            # 각 단계에서 계획을 생성하고 행동을 결정하는 agent
    tools=tools,            # agent가 사용가능한 도구 리스트
    verbose=False,          # 중간 단계 출력
    max_iterations=10,      # 최대 10번까지 반복
    max_execution_time=10,  # 실행되는데 소요되는 최대 시간
    handle_parsing_errors=True
)

store = {}

def get_session_history(session_ids):
    if session_ids not in store:
        store[session_ids] = ChatMessageHistory()
    
    return store[session_ids]

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)

# result = agent_with_chat_history.stream(
#     {
#         'input': '최근 뉴스 5개를 검색하고, 각 뉴스의 제목을 파일명으로 하는 파일을 생성하고(.txt) '
#         '파일의 뉴스 내용은 뉴스의 내용과 url을 추가하세요.'
#     },
#     config={'configurable' : {'session_id': 'abc123'}}
# )

result = agent_with_chat_history.stream(
    {
        'input': '이전에 생성한 파일 제목 맨 앞에 어울리는 emoji를 추가해서 파일 명을 변경하세요. '
        '파일도 깔끔하게 변경하세요.'
    },
    config={'configurable' : {'session_id': 'abc123'}}
)

agnet_stream_parser = AgentStreamParser()

for step in result:
    agnet_stream_parser.process_agent_steps(step)
