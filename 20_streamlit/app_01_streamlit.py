import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('나만의 chatGPT')

# 처음 1번만 실행
if 'messages' not in st.session_state:    
    st.session_state['messages'] = []       # 대화기록을 저장하기 위한 용도


# 저장된 대화를 화면에 출력(이전 대화를 출력)
def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
            st.write(chat_message.content)  

# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))

def create_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', '당신은 친절한 AI 어시스턴트입니다.'), 
            ('user', '#Questin:\n{question}'),
        ]
    )

    llm = ChatOpenAI(                       # 모델
        api_key=key, 
        model_name='gpt-4o-mini',
        temperature=0	    
    )

    output_parser = StrOutputParser()       # 출력 파서
    chain = prompt | llm | output_parser    # 체인

    return chain


print_messages()

user_input = st.chat_input('궁금한 내용을 물어보세요')  # 사용자 입력

if user_input:                                          
    with st.chat_message('user'):
        st.write(user_input)
    

    chain = create_chain()
    answer = chain.invoke({'question': user_input})

    with st.chat_message('assistant'):
        st.write(answer)


    # 대화 내용을 기록한다
    add_message('user', user_input)

    add_message('assistant', answer)