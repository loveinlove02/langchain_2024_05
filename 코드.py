from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

class EmailSummary(BaseModel):
    person: str = Field(description='메일을 보낸 사람')
    email: str = Field(description='메일을 보낸 사람의 이메일 주소')
    subject: str = Field(description='메일 제목')
    summary: str = Field(description='메일 본문을 요약한 텍스트')

parser = PydanticOutputParser(pydantic_object=EmailSummary)


prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant. Please answer following questions in KOREAN.
    
    QUESTION:
    {question}
    
    EMAIL CONVERSATION:
    {email_conversation}
    
    FORMAT:
    {format}
    """
)
prompt = prompt.partial(format=parser.get_format_instructions())

email = """From: 이지완 (jiwan@naver.com)
To: Korea AI 팀장님 (korea_ai@naver.com)
Subject: RAG 솔루션 시연 관련 미팅 제안

안녕하세요, Korea AI 팀장님,

저는 소프트웨어놀이터의 이지완입니다. 최근 귀사에서 AI를 활용한 혁신적인 솔루션을 모색 중이라는 소식을 들었습니다. 

소프트웨어놀이터는 AI 및 RAG 솔루션 분야에서 다양한 경험과 노하우를 가진 기업으로, 귀사의 요구에 맞는 최적의 솔루션을 제공할 수 있다고 자부합니다.
저희 소프트웨어놀이터의 RAG 솔루션은 귀사의 데이터 활용을 극대화하고, 실시간으로 정확한 정보 제공을 통해 비즈니스 의사결정을 지원하는 데 탁월한 성능을 보입니다. 이 솔루션은 특히 다양한 산업에서의 성공적인 적용 사례를 통해 그 효과를 입증하였습니다.

귀사와의 협력 가능성을 논의하고, 저희 RAG 솔루션의 구체적인 기능과 적용 방안을 시연하기 위해 미팅을 제안드립니다. 

다음 주 월요일(12월 9일) 오후 3시에 귀사 사무실에서 만나 뵐 수 있을까요?
미팅 시간을 조율하기 어려우시다면, 편하신 다른 일정을 알려주시면 감사하겠습니다. Korea AI 팀장님과의 소중한 만남을 통해 상호 발전적인 논의가 이루어지길 기대합니다.

감사합니다.

이지완

소프트웨어놀이터 AI 솔루션팀
"""

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini'
)

chain = prompt | llm | parser

answer = chain.invoke({'question': '이메일 내용중 주요 내용을 추출해주세요.', 'email_conversation': email})

print(answer)
print(answer.person)
print(answer.email)
print(answer.subject)
print(answer.summary)


