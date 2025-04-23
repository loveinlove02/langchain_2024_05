from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')


from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 1단계: 문서 로드
loader = PyMuPDFLoader('data/SPRI_AI_Brief_2023년12월호_F.pdf')
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

retriever.invoke('삼성전자가 만든 생성형 AI')


from langchain.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever,
    name='pdf_search',
    description='use this tool to search information from PDF document'
)

from langchain_teddynote.tools.tavily import TavilySearch

search = TavilySearch(
    max_results=5, 
    include_domains=['www.naver.com']
)



tools = [retriever_tool, search]

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini'
)

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


from langchain.agents import create_tool_calling_agent

agnet = create_tool_calling_agent(llm, tools, prompt)


from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(
    agent=agnet,
    tools=tools,
    verbose=False,
    max_iterations=10, 
    max_execution_time=10,
    handle_parsing_errors=True
)

answer = agent_executor.invoke({'input': '2024년 프로야구 우승팀?'})
answer





