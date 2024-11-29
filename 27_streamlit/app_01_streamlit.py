import streamlit as st
from langchain_core.messages import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_teddynote.prompts import load_prompt
import requests
import urllib.request
import re
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

class EmailSummary(BaseModel):
    person: str = Field(description="메일을 보낸 사람")
    company: str = Field(description="메일을 보낸 사람의 회사 정보")
    email: str = Field(description="메일을 보낸 사람의 이메일 주소")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="메일 본문을 요약한 텍스트")
    date: str = Field(description="메일 본문에 언급된 미팅 날짜와 시간")


st.title('나만의 chatGPT')


if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
            st.write(chat_message.content)

def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))    


def create_email_parsing_chain():
    # PydanticOutputParser 생성
    output_parser = PydanticOutputParser(pydantic_object=EmailSummary)

    prompt = PromptTemplate.from_template(
        """
    You are a helpful assistant. Please answer the following questions in KOREAN.

    #QUESTION:
    다음의 이메일 내용 중에서 주요 내용을 추출해 주세요.

    #EMAIL CONVERSATION:
    {email_conversation}

    #FORMAT:
    {format}
    """
    )

    # format 에 PydanticOutputParser의 부분 포맷팅(partial) 추가
    prompt = prompt.partial(format=output_parser.get_format_instructions())

    # 체인 생성
    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | output_parser

    return chain


def create_report_chain():
    prompt = load_prompt("prompts/email.yaml", encoding="utf-8")
    output_parser = StrOutputParser()
    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | output_parser

    return chain


print_messages()


user_input = st.chat_input('궁금한 내용을 물어보세요')

if user_input:
    with st.chat_message('user'):
        st.write(user_input)
    
    # 1) 이메일을 파싱하는 chain 을 생성
    email_chain = create_email_parsing_chain()

    
    # email 에서 주요 정보를 추출하는 체인을 실행
    answer = email_chain.invoke({"email_conversation": user_input})

    
    # 3) 이메일 요약 리포트 생성
    report_chain = create_report_chain()

    report_chain_input = {
        "sender": answer.person,
        "company": answer.company,
        "email": answer.email,
        "subject": answer.subject,
        "summary": answer.summary,
        "date": answer.date,
    }


    # 스트리밍 호출
    response = report_chain.stream(report_chain_input)
    
    with st.chat_message("assistant"):
        container = st.empty()

        ai_answer = ""

        for token in response:
            ai_answer += token
            container.markdown(ai_answer)


    add_message("user", user_input)
    add_message("assistant", ai_answer)