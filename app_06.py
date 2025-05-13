from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')


from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain.agents import create_tool_calling_agent, AgentExecutor


# 1단계: 문서 로드
loader = PyMuPDFLoader('./data/SPRI_AI_Brief_2023년12월호_F.pdf')
docs = loader.load()

# 2단계: 문서 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_documents = text_splitter.split_documents(docs)

# 3단계: Embedding
embeddings = OpenAIEmbeddings(api_key=key, model='text-embedding-3-small')

# 4단계: DB 생성 및 저장
vectore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

# 5단계: 검색기(retriever)
retriever = vectore.as_retriever()

# answer = retriever.invoke('삼성전자가 만든 생성형 AI')
# print(answer)

# agent가 사용할 수 있는 도구(문서 검색 도구)
retriever_tool = create_retriever_tool(
    retriever,              # 도구
    name='pdf_search',      # 도구 이름
    description='use this tool to search information from PDF document'
)


# agent가 사용할 수 있는 도구(웹 검색도구)
search = TavilySearchResults(k=2)

# 도구들을 리스트에 넣기
tools = [retriever_tool, search]

# llm
llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini'
)

# 프롬프트
prompt = ChatPromptTemplate.from_messages(                  # 프롬프트
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


# 도구를 실행 시킬수 있는 agent 만들기 
agent = create_tool_calling_agent(llm, tools, prompt)

# 위에서 만든 agent를 실행시키는 실행기
agent_executor = AgentExecutor(
    agent=agent,                # 에이전트
    tools=tools,                # 사용가능한 도구들
    verbose=False,              # 중간 단계 출력 안보이게
    max_iterations=10,          # 최대 실행 횟수
    max_execution_time=10,      # 실행되는데 소요되는 최대 시간
    handle_parsing_errors=True
)

answer = agent_executor.invoke({'input': '2025년 대선'})
print(answer)
