from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# 1. 문서 로드
loder = PyMuPDFLoader('./data/SPRI_AI_Brief_2023년12월호_F.pdf')
docs = loder.load()

# 2. 문서 자르기
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
split_documents = text_splitter.split_documents(docs)

# 3. 임베딩
embeddings = OpenAIEmbeddings(api_key=key, model='text-embedding-3-small')

# 4. 데이터베이스 생성 하고 임베딩을 사용해서 잘라놓은 문서를 저장
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

# 5. 리트리버
retriever = vectorstore.as_retriever()


prompt = PromptTemplate.from_template(
    """Yor are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Answer in Korean.
    
    #Context:
    {context}
    
    
    #Question:
    {question}
    
    #Answer:
    """
)
