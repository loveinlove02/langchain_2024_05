import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import ChatMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('chatbot')


if 'messages' not in st.session_state:
    st.session_state['messages'] = []

with st.sidebar:
    clear_btn = st.button('대화 다시')
    task_input = st.text_input('TASK 입력', '')

# 대화 내용 출력
def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
            st.write(chat_message.contnet)

# 대화 내용 추가
def add_messages(role, messages):
    st.session_state['messages'].append(
        ChatMessage(role=role, content=messages)
    )

# chain
def create_chain(task=''):
    prompt = load_prompt('./prompts/prompt-maker.yaml')

    if task:
        prompt = prompt.partial(task=task)

    llm = ChatOpenAI(
        api_key=key,
        model='gpt-4o-mini',
        temperature=0
    )

    output_parer = StrOutputParser()
    chain = prompt | llm| output_parer
    return  chain

if clear_btn:                           # 버튼을 클릭 하면
    st.session_state['messages'] = []   # 대화 내용 삭제

print_messages()

user_input = st.chat_input('궁긍한 내용을 물어 보세요')

if user_input:
    with st.chat_message('user'):
        st.write(user_input)

    chain = create_chain(task=task_input)
    response = chain.stream({'question': user_input})

    with st.chat_message('assistant'):
        container = st.empty()
        answer = ''

        for token in response:
            answer = answer + token
            container.markdown(answer)       # 화면에 따따따 출력


    add_messages('user', user_input)
    add_messages('assistant', answer)
