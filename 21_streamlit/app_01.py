import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('GhatGPT') 

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

with st.sidebar:
    btn = st.button('대화 다시')
    
    selected_prompt = st.selectbox(
        '프롬프트를 선택하세요', 
        ('기본모드', '게시글'), 
        index=0
    )

def print_mmessages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
           st.write(chat_message.content) 

def add_message(role, message):
    st.session_state['messages'].append(
        ChatMessage(role=role, content=message)
    )

def create_chain(prompt_type):
    if prompt_type=='기본모드':
        prompt = ChatPromptTemplate(
            [
                ('system', '당신은 친절한 AI 어시스턴트입니다. 다음의 질문에 간결하게 답변해주세요.'), 
                ('user', '#Qeustion:\n{question}')
            ]
        )
    elif prompt_type=='게시글':
        prompt = load_prompt('prompts/blog.yaml', encoding='utf-8')


    llm = ChatOpenAI(
        api_key=key, 
        model_name='gpt-4o-mini',
        temperature=0,
        max_toens=2048,
    )

    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    
    return chain


if btn:
    st.session_state['messages'] = []

print_mmessages()

user_input = st.chat_input('궁금한 내용을 물어보세요')

if user_input:
    with st.chat_message('user'):
        st.write(user_input)


    # 체인 만들기
    chain = create_chain(selected_prompt)  

    # 체인으로 invoke해서 답변
    response = ''

    with st.chat_message('assistant'):
        answer = '가짜 대답'

    
    add_message('user', user_input)
    add_message('assistant', answer)
