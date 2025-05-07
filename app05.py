from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_teddynote.messages import AgentStreamParser
from langchain.tools.retriever import create_retriever_tool

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# ====================
# 문서 검색기
# ====================

# 단계 1: 문서 로드(Load Documents)
loader = PyMuPDFLoader('data/SPRI_AI_Brief_2023년12월호_F.pdf')
docs = loader.load()

# 단계 2: 문서 분할(Split Documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_documents = text_splitter.split_documents(docs)

# 단계 3: 임베딩(Embedding) 생성
embeddings = OpenAIEmbeddings(
    api_key=key,
    model='text-embedding-3-small'
)

# 단계 4: DB 생성(Create DB) 및 저장
# 벡터스토어 생성합니다.
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

# 단계 5: 검색기(Retriever) 생성
retriever = vectorstore.as_retriever()


# ====================
# 도구 만들기
# ====================

# 1. 문서검색 도구
retriever_tool = create_retriever_tool(
    retriever=retriever,        # 검색기(retriever)
    name='pdf_search',          # 도구의 이름
    description='use this tool to search information from the PDF document'
)

# 2. 웹 검색 도구
search = TavilySearchResults(k=2) 

# 3.도구 목록
tools = [retriever_tool, search]


# ====================
# Agent 생성
# ====================

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini'
)

prompt = ChatPromptTemplate.from_messages(                 
    [
        (
            'system',
            'You are a helpful assistant. '
            "Make sure to use the `pdf_search` tool for searching information from the PDF document. "
            "If you can't find the information from the PDF document, use the `search` tool for searching information from the web.",
        ),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}'),
    ]
)


agent = create_tool_calling_agent(llm, tools, prompt)

# ====================
# angent 실행기
# ====================
agent_executor = AgentExecutor(
    agent=agent,                # 계획 생성 및 결정하는 Agent               
    tools=tools,                # agent가 사용하는 도구
    verbose=False,              # 중간단계 출력하기
    max_iterations=10,          # 최대 반복 횟수
    max_execution_time=10,      # 최대 실행 시간
    handle_parsing_errors=True  # 에러 처리
)


store = {}                                  # 세션 기록 저장(딕셔너리)

def get_session_history(session_ids):       # 세션 기록을 가져오는 함수       
    if session_ids not in store:
        store[session_ids] = ChatMessageHistory()
    
    return store[session_ids]


# ====================
# 대화내용을 기억하는 angent 실행기
# ====================

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,                     # agent 실행기
    get_session_history,                # 세션 기록가져오는 함수
    input_messages_key='input',         # 사용자 질문
    history_messages_key='chat_history' # 대화 내용 기록
)

# 실행
response = agent_with_chat_history.stream(
    {'input': '삼성전자가 자체 개발한 생성형 AI에 대한 정보를 문서에서 검색해주세요.'},
    config={'configurable' : {'session_id': 'abc123'}}
)

for step in response:
    print(step)
    print()

