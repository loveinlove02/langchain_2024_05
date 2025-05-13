from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')


from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain.tools.retriever import create_retriever_tool


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

# agent가 사용할 수 있는 검색 도구(문서 검색 도구)
retriever_tool = create_retriever_tool(
    retriever,              # 도구
    name='pdf_search',      # 도구 이름
    description='use this tool to search information from PDF document'
)
print(retriever_tool)
