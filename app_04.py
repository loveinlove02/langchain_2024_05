from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_teddynote.prompts import load_prompt

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

class ConverSationSummary_EN(BaseModel):
    original_english_sentence: str  = Field(description='원문 영어 문장')
    translated_korean_sentence: str = Field(description='번역된 한국어 문장')
    context_precautions_of_translation: str = Field(description='번역된 맥락이나 주의사항')

parser_en = PydanticOutputParser(pydantic_object=ConverSationSummary_EN)

prompt = load_prompt('./prompts/prompt_eng_to_kor.yaml')
prompt = prompt.partial(format=parser_en.get_format_instructions())

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

chain = prompt | llm

user_input = '학교 마치고 교문에서 만나자. 만나서 떡볶이 먹으러 같이 가자.'
response = chain.invoke({'question': user_input})
print(response)

