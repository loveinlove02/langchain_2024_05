import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from urllib import response
from requests import session

from dotenv import load_dotenv
import os


load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title("나만의 chatGPT 💬")

# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "store" not in st.session_state:
    st.session_state["store"] = {}


with st.sidebar:
    clear_btn = st.button("대화 초기화")
    session_id = st.text_input("세션 ID를 입력하세요.", "abc123")


# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids):
    if session_ids not in st.session_state["store"]:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state["store"][session_ids] = ChatMessageHistory()

    return st.session_state["store"][session_ids]  # 해당 세션 ID에 대한 세션 기록 반환


def create_chain():

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "당신은 Question-Answering 챗봇입니다. 주어진 질문에 대한 답변을 제공해주세요.",
            ),
            # 대화기록용 key 인 chat_history 는 가급적 변경 없이 사용하세요!
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "#Question:\n{question}"),  # 사용자 입력을 변수로 사용
        ]
    )

    llm = ChatOpenAI(model="gpt-4o-mini")

    output_parser = StrOutputParser()

    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | output_parser

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,                    # 세션 기록을 가져오는 함수
        input_messages_key="question",          # 사용자의 질문이 템플릿 변수에 들어갈 key
        history_messages_key="chat_history",    # 기록 메시지의 키
    )

    return chain_with_history


if clear_btn:
    st.session_state["messages"] = []


print_messages()

user_input = st.chat_input("궁금한 내용을 물어보세요!")

warning_msg = st.empty()        # 경고 메시지를 띄우기 위한 빈 영역

if "chain" not in st.session_state:
    st.session_state["chain"] = create_chain()

if user_input:
    chain = st.session_state["chain"]

    if chain is not None:
        response = chain.stream(
            {"question": user_input},                             # 질문 입력            
            config={"configurable": {"session_id": session_id}},  # 세션 ID 기준으로 대화를 기록합니다.
        )


        # 사용자의 입력
        with st.chat_message('user'):
            st.write(user_input)

        with st.chat_message("assistant"):
            container = st.empty()
            ai_answer = ""

            for token in response:
                ai_answer += token
                container.markdown(ai_answer)

            # 대화기록을 저장한다.
            add_message("user", user_input)
            add_message("assistant", ai_answer)
    else:
        warning_msg.error("에러")