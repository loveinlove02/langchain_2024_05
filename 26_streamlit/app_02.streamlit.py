import streamlit as st
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_teddynote.prompts import load_prompt

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('나만의 chatGPT')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'chain' not in st.session_state:
    st.session_state['chain'] = None


# 저장된 대화를 화면에 출력(이전 대화를 출력)
def print_messages():                                     
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):          # 이모티콘(assistant, 사용자)
            st.write(chat_message.content)                # 내용(시스템 답변, 사용자 입력)    

# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))


st.cache_resource(show_spinner='업로드한 파일을 처리 중입니다...')
def embed_file():
    DB_PATH = "./chroma_db"     # 저장 경로

    # 디스크에서 문서를 로드합니다.
    persist_db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
        collection_name='my_db',
    )

    retriever = persist_db.as_retriever()

    return retriever


def create_chain(retriever):
    prompt = load_prompt('./prompts/pdf.yaml', encoding='utf-8')

    # 모델(LLM)
    llm = ChatOpenAI(
        api_key=key, 
        model_name='gpt-4o-mini',
        temperature=0,			    
        max_tokens=2048,			
    )

    # 체인(Chain)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}  
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


retriever = embed_file()                # 파일이 업로드되면 retriever 
chain = create_chain(retriever)         # retriever를 인자로 넘겨서 체인
st.session_state['chain'] = chain       # session_state에 체인을 등록


print_messages()

user_input = st.chat_input('궁금한 내용을 물어보세요')  

warning_msg = st.empty()                            # 경고 메시지 출력을 위한 빈 영역을 잡는다

if user_input:                                      # 사용자 입력이 들어있으면

    chain = st.session_state['chain']               # session_state에서 체인을 가져오기

    if chain is not None:                           # session_state에서 체인을 가져왔으면

        with st.chat_message('user'):               # 사용자 이모티콘
            st.write(user_input)                    # 사용자가 입력한 내용(질문)을 출력
            

        response = chain.stream(user_input)


        with st.chat_message('assistant'):          # assistant 이모티콘
            container = st.empty()                  # 빈공간을 만든다

            answer = ''

            for token in response:
                answer += token
                container.markdown(answer)

        add_message('user', user_input)             # 대화 내용을 기록한다
        add_message('assistant', answer)
    else:                                           # session_state에서 체인을 못 가져왔으면
        warning_msg.error('파일을 업로드 해주세요.')