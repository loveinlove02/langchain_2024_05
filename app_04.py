import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_teddynote.prompts import load_prompt

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# 스트림릿 앱 제목 설정
st.title("영어 -> 한국어 번역기")

class ConverSationSummary_EN(BaseModel):
    original_english_sentence: str  = Field(description='원문 영어 문장')
    translated_korean_sentence: str = Field(description='번역된 한국어 문장')
    context_precautions_of_translation: str = Field(description='번역된 맥락이나 주의사항')

parser_en = PydanticOutputParser(pydantic_object=ConverSationSummary_EN)

prompt = load_prompt('./prompts/prompt_eng_to_kor.yaml', encoding='utf-8')
prompt = prompt.partial(format=parser_en.get_format_instructions())

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

chain = prompt | llm

# 사용자로부터 영어 입력 받기
user_input = st.text_area("번역할 영어 문장을 입력하세요:")

# 번역 버튼 클릭 시 동작
if st.button("번역하기"):
    if user_input:
        response = chain.invoke({'question': user_input})
        structed_output = parser_en.parse(response.content)

        st.write(f"원문 문장: {structed_output.original_english_sentence}")
        st.write(f"번역 문장: {structed_output.translated_korean_sentence}")
        st.write(f"참고 사항: {structed_output.context_precautions_of_translation}")
    else:
        st.write("영어 문장을 입력해주세요.")
