from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader

from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import PromptTemplate

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.agent_toolkits import FileManagementToolkit

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_teddynote.messages import AgentStreamParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')


# 문서 검색 도구
# ====================
# 1. 문서 로드
loader = PyMuPDFLoader('data/SPRI_AI_Brief_2023년12월호_F.pdf')
docs = loader.load()

# 2. 문서 자르기
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_documents = text_splitter.split_documents(docs)

# 3. 임베딩 생성
embeddings = OpenAIEmbeddings(api_key=key, model='text-embedding-3-small')

# 4. 데이터베이스 생성 및 잘라 놓은 문서를 임베딩을 가지고 등록
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

# 5. 검색기(retriever)
retriever = vectorstore.as_retriever()

# 6. 검색 도구로 만들기
document_prompt = PromptTemplate.from_template(                         
    "<document><content>{page_content}</content><page>{page}</page><filename>{source}</filename></document>"
)


# 웹 검색 도구
# ====================

# 파일 관리 도구
# ====================


