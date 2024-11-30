import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.utils import ConfigurableFieldSpec
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


# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))



# sqlite.db에서 대화 내용을 가져오는 함수를 만듭니다.
def get_chat_history(user_id, conversation_id):
    return SQLChatMessageHistory(
        table_name=user_id,
        session_id=conversation_id,             
        connection="sqlite:///sqlite.db",       
    )

config_fields = [
    ConfigurableFieldSpec(
        id="user_id",			#  get_chat_history 함수의 파라미터 이름과 같아야 한다.
        annotation=str,
        name="User ID",			
        description="Unique identifier for a user.",
        default="",
        is_shared=True,
    ),
    
    ConfigurableFieldSpec(
        id="conversation_id",	#  get_chat_history 함수의 파라미터 이름과 같아야 한다.
        annotation=str,
        name="Conversation ID",
        description="Unique identifier for a conversation.",
        default="",
        is_shared=True,
    ),
]


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
        
        # 대화 기록을 가져오는 함수를 설정합니다.
        get_chat_history,  
        
        # 입력 메시지의 키를 "question"으로 설정.프롬프트의 question와 맵핑.
        input_messages_key="question", 
        
        # 대화 기록 메시지의 키를 "history"로 설정. MessagesPlaceholder의 chat_history 맵핑.
        history_messages_key="chat_history",
        
        # 대화 기록 조회시 참고할 파라미터를 설정합니다.
        history_factory_config=config_fields,
    )


    return chain_with_history


print_messages()

user_input = st.chat_input("궁금한 내용을 물어보세요!")

warning_msg = st.empty()        # 경고 메시지를 띄우기 위한 빈 영역

if "chain" not in st.session_state:
    st.session_state["chain"] = create_chain()

if user_input:
    chain = st.session_state["chain"]

    if chain is not None:
        # "configurable" 키 아래에 "user_id", "conversation_id" key-value 쌍을 설정합니다.
        config = {
            "configurable": {
                "user_id": "user1", 
                "conversation_id": "conversation1"
            }
        }

        response = chain.stream(
            {"question": user_input},                             # 질문 입력            
            config=config,  
        )

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