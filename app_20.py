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

user_input = st.chat_input('무엇을 도와드릴까요?')

if user_input:
    with st.chat_message('user'):
        st.write(user_input)

    with st.chat_message('assistant'):
        pass
    

    add_message('user', user_input)
