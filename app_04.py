import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('나만의 GPT')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'store' not in st.session_state:
    st.session_state['store'] = {}

with st.sidebar:
    clear_btn = st.button('대화 초기화')
    session_id = st.text_input('세션 ID를 입력하세요', 'abc12')


def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
            st.write(chat_message.content)


def add_message(role, message):
    st.session_state['messages'].append(
        ChatMessage(role=role, content=message)
    )


def get_session_history(session_ids):
    if session_ids not in st.session_state['store']:
        st.session_state['store'][session_ids] = ChatMessageHistory()
    
    return st.session_state['store'][session_ids]


def create_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system', 
                '당신은 Question-Answering 챗봇입니다. 질문에 대한 답변을 제공해주세요'
            ), 
            MessagesPlaceholder(variable_name='chat_history'),
            ('human', '#Question: \n{question}')
        ]
    )

    llm = ChatOpenAI(
        api_key=key,
        model_name='gpt-4o-mini',
        temperature=0
    )

    output_parer = StrOutputParser()

    chain = prompt | llm | output_parer

    chain_with_history = RunnableWithMessageHistory(
        chain,                              # 체인
        get_session_history,                # 세션 기록을 가져오는 함수
        input_messages_key='question',      # 사용자 질문 
        history_messages_key='chat_history' # 기록 메시지 키
    )    
    
    return chain_with_history


if clear_btn:       
    st.session_state['messages'] = []

print_messages()

user_input = st.chat_input('궁금한 내용을 물어보세요')

# 빈 공간 변수
warning_msg = st.empty()

if 'chain' not in st.session_state:
    st.session_state['chain'] = create_chain()

if user_input:
    chain = st.session_state['chain']
    st.write(chain)
