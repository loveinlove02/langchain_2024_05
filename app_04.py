from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader

from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# 웹 검색
search = TavilySearchResults(k=5)

# 문서 검색

# 1.문서 로드
loader = PyMuPDFLoader('./data/SPRI_AI_Brief_2023년12월호_F.pdf')
docs = loader.load()

# 2.문서 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_document = text_splitter.split_documents(docs)

# 3.임베딩 생성
embeddings = OpenAIEmbeddings(
    api_key=key,
    model='text-embedding-3-small'
)

# 4. DB 생성 및 저장
vectorstore = FAISS.from_documents(documents=split_document, embedding=embeddings)

# 5.벡터스토어에 들어가서 검색해오는 검색기(Retriever) 생성
retriever = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,               # 리트리버
    name='pdf_search',       # 도구의 이름
    description='여기서 도구에 대한 설명....'
)

# answer = retriever.invoke('삼성전자가 개발한 생성형 AI이름?')
# # print(answer)
#
# for data in answer:
#     print(data)
