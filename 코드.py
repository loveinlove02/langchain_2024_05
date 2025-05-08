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
template = '{product}는 어느 회사에서 만든 제품인가요?'
prompt = PromptTemplate.from_template(template)

# 3. 출력파서
output_parser = StrOutputParser()

# 실행기(chain)
chain = prompt | llm | output_parser

answer = chain.invoke({'product' : '겔럭시폰'})
print(answer)
