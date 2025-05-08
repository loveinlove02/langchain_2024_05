from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# 1. LLM
llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini'
)

# 2. prompt
# template = '{product}는 어느 회사에서 만든 제품인가요?'
# prompt = PromptTemplate.from_template(template)

prompt = PromptTemplate(
    template='{country1}과 {country2}의 수도는 각각 어디인가요?',
    input_variables=['country1', 'country2']
)

# 3. 출력파서
output_parser = StrOutputParser()

# 실행기(chain)
chain = prompt | llm | output_parser

answer = chain.invoke({'country1' : '미국', 'country2': '일본'})
print(answer)
