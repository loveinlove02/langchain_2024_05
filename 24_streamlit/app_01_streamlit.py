import streamlit as st
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('나만의 chatGPT')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []      

with st.sidebar:
    clear_btn = st.button('대화 다시')

def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):          # 이모티콘(assistant, 사용자)
            st.write(chat_message.content)   


def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))


def create_chain():
    prompt = load_prompt('./prompts/요약.yaml', encoding='utf-8')

    llm = ChatOpenAI(                                      # llm
        api_key=key, 
        model_name='gpt-4o-mini',  	
        temperature=0,			    
        max_tokens=2048,			
    )

    output_parser = StrOutputParser()                       # 출력 파서       
    chain = prompt | llm | output_parser                    # 체인
    return chain


if clear_btn:                                               # 버튼이 눌러지면
    st.session_state['messages'] = []

print_messages()                                            # 저장된 대화를 화면에 출력

user_input = st.chat_input('요약할 내용을 작성하세요')       # 사용자 입력

if user_input:                                              # 사용자 입력이 들어있으면
    with st.chat_message('user'):                           # 사용자 이모티콘
        st.write(user_input)
    
    chain = create_chain()                                  
    response = chain.stream({'question': user_input})       # 요약할 문장

    with st.chat_message('assistant'):                      
        container = st.empty()                              # 빈공간에 토큰을 스트리밍 출력한다.
        answer = ''

        for token in response:
            answer += token
            container.markdown(answer)

    add_message('user', user_input)                         # 대화 내용을 기록한다
    add_message('assistant', answer)                        