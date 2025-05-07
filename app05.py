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
