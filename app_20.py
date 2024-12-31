import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('chatGPT 💬')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []


def add_message(role, message):  # 롤(user, assistant), 메시지(질문, 답변)
    st.session_state['messages'].append(
        ChatMessage(role=role, content=message)
    )

def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
            st.write(chat_message.content)

def create_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', '당신은 친절한 AI 어이스턴스입니다.'), 
            ('user', '#Question:\n{question}')
        ]
    )

    llm = ChatOpenAI(
        api_key=key, 
        model_name='gpt-4o-mini', 
        temperature=0
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain

print_messages()

user_input = st.chat_input('무엇을 도와드릴까요?')

if user_input:
    with st.chat_message('user'):
        st.write(user_input)

    # 사용자 질문을 처리할 chain
    chain = create_chain()

    # chain에 질물을 던져서 답변얻기(answer)
    answer = chain.invoke({'question': user_input})

    with st.chat_message('assistant'):
        st.write(answer)
    
    add_message('user', user_input)
    add_message('assistant', answer)

