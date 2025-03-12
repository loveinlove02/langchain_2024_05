from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_teddynote.prompts import load_prompt

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

class ConverSationSummary_KOR(BaseModel):
    original_korean_sentence: str = Field(description='원문 한국어 문장')
    translated_english_sentence: str = Field(description='번역된 영어 문장')
    context_precautions_of_translation: str = Field(description='번역의 맥락이나 주의사항')

parser_kor = PydanticOutputParser(pydantic_object=ConverSationSummary_KOR)

prompt = load_prompt('./prompts/prompt_kor_to_eng.yaml', encoding='utf-8')
prompt = prompt.partial(format=parser_kor.get_format_instructions())

print(prompt)
