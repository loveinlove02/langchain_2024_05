import streamlit as st
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('나만의 chatGPT')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
            st.write(chat_message.content)

def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))

def create_chain():     
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', '당신은 친절한 AI 어시스턴트입니다.'), 
            ('user', '#Questin:\n{question}'),
        ]
    )

    llm = ChatOpenAI(
        api_key=key, 
        model_name='gpt-4o-mini',
        temperature=0,			    
        max_tokens=300,			    
    )

    output_parser = StrOutputParser()       # 출력 파서
    chain = prompt | llm | output_parser    # 체인
    return chain

print_messages()

user_input = st.chat_input('궁금한 내용을 물어보세요')      # 사용자 입력

if user_input:
    with st.chat_message('user'):
        st.write(user_input)
    
    chain = create_chain()    
    response = chain.stream({'question': user_input})

    with st.chat_message('assistant'):        
        container = st.empty()      # 빈공간에 토큰을 스트리밍 출력한다.
        answer = ''

        for token in response:
            answer += token
            container.markdown(answer)

    add_message('user', user_input)
    add_message('assistant', answer)