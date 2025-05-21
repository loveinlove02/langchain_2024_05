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

retriever_tool = create_retriever_tool(
    retriever,
    name='pdf_search',
    description='use this tool to search for information in the PDF file',
    document_prompt=document_prompt
)


# 웹 검색 도구
# ====================
search = TavilySearchResults(k=2)

# 파일 관리 도구
# ====================
if not os.path.exists('temp'):
    os.makedirs('temp')

working_directory = 'temp'              # 작업 디렉토리(폴더)
file_tools = FileManagementToolkit(root_dir=str(working_directory),
                                   selected_tools=['write_file','read_file', 'list_directory'])
tools = file_tools.get_tools()

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

# 에이전트
agent = create_tool_calling_agent(llm, tools, prompt)

# 에이전트 실행기
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False, 
    max_iterations=10, 
    max_execution_time=10,
    handle_parsing_errors=True
)

# 채팅을 기록
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

# 출력 파서
agent_stream_parser = AgentStreamParser()

# 사용자 질문

# result = agent_with_chat_history.stream(
#     {
#         "input": "삼성전자가 개발한 `생성형 AI` 와 관련된 유용한 정보들을 `pdf_search` 도구를 사용해서 PDF 문서에서 찾아서 bullet point로 정리해 주세요. "
#         "한글로 작성해주세요."
#         "다음으로는 `report.md` 파일을 새롭게 생성하여 정리한 내용을 저장해주세요. \n\n"
#         "#작성방법: \n"
#         "1. markdown header 2 크기로 적절한 제목을 작성하세요. \n"
#         "2. 발췌한 PDF 문서의 페이지 번호, 파일명을 기입하세요(예시: page 10, filename.pdf). \n"
#         "3. 정리된 bullet point를 작성하세요. \n"
#         "4. 작성이 완료되면 파일을 `report.md` 에 저장하세요. \n"
#         "5. 마지막으로 저장한 `report.md` 파일을 읽어서 출력해 주세요. \n"
#     },
#     config={"configurable": {"session_id": "abc123"}},
# )

# for step in result:
#     agent_stream_parser.process_agent_steps(step)

result = agent_with_chat_history.stream(
    {
        "input": "report.md 파일을 열어서 내용을 출력하세요. "
        "출력된 내용을 바탕으로, 전문적인 수준의 보고서를 작성하세요. "
        "보고서는 총 3개의 섹션으로 구성되어야 합니다.\n"
        "1. 개요 : 보고서 abstract를 300자 내외로 작성하세요. \n"
        "2. 핵심내용 : 보고서의 핵심 내요을 작성하세요. "
        "3. 최종결론 : 보고서의 최종결론을 작성하세요. 출처(파일이름, url)등을 표시하세요."
        "마지막으로 작성된 결과물을 report2.md 파일에 저장하세요."
    },
    config={"configurable": {"session_id": "abc123"}},
)

for step in result:
    agent_stream_parser.process_agent_steps(step)
