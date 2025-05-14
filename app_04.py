from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
# from langchain.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader

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

# ===== PDF 문서 검색 도구 =====
# 단계 1: 문서 로드
loader = PyMuPDFLoader('data/SPRI_AI_Brief_2023년12월호_F.pdf')
docs = loader.load()

# 단계 2: 문서 자르기
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_documents = text_splitter.split_documents(docs)

# 단계 3: 임베딩 생성
embeddings = OpenAIEmbeddings(api_key=key, model='text-embedding-3-small')

# 단계 4 : DB 생성 및 저장
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

# 단계 5 : 검색기(retriever)
retriever = vectorstore.as_retriever()

# 단계 6 : 도구로 만들기
document_prompt = PromptTemplate.from_template(
    "<document><content>{page_content}</content><page>{page}</page><filename>{source}</filename></document>"
)

retriever_tool = create_retriever_tool(
    retriever,              # 우리가 만든 검색기
    name='pdf_search',      # 도구 이름을 지정
    description='use this tool to search for information in the PDF file.',
    document_prompt=document_prompt
)

# ===== 웹 검색 도구 =====
search = TavilySearchResults(k=2)

# ===== 파일 관리 도구 =====
if not os.path.exists('tmp'):
    os.mkdir('tmp')

working_directory = 'tmp'

# 사용할 도구들을 가져온다
file_tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=['write_file', 'read_file', 'list_directory']
).get_tools()

# 도구들을 리스에 모은다
tools = file_tools + [retriever_tool, search]

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini'
)

prompt = ChatPromptTemplate.from_messages(                  # 프롬프트
    [
        (
            'system',
            'You are a helpful assistant. '
            'You are a professional researcher. '
            'You can use the pdf_search tool to search for information in the PDF file. '
            'You can find further information by using search tool. '
            'You can use image generation tool to generate image from text. '
            'Finally, you can use file management tool to save your research result into files.'
        ),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}'),
    ]
)
