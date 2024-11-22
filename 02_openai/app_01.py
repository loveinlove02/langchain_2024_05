from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=key, 
    model_name='gpt-4o-mini',	        # 모델 : 사용할 모델을 지정합니다.
    temperature=0.1,			        # 창의성 : (0.0 ~ 2.0) 
    max_tokens=300,			            # 최대 토큰 수
)

# 질문내용
question = '겔럭시 스마트폰은 어느 회사에서 개발한 제품인가요?'

# 요청
answer = llm.invoke(question)
print(answer)
print(answer.content)