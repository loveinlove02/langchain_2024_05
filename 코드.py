from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
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
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '당신은 대화 요약에 특화된 AI 어시스턴트입니다. 주어진 대화에서 핵심 주제, 주요 인물, 중요한 사건이나 결론을 파악하여 간결하고 명확하게 요약하세요. 중립적인 톤을 유지하고, 불필요한 세부사항은 생략하세요.'
        ),
        (
            'human',
            '{conversation} 이 대화의 핵심 내용을 3문장으로 요약해 주세요. 각 문장은 명확하고 간결해야 하며, 독자가 전체 맥락을 빠르게 이해할 수 있도록 구성해 주세요.'
        )
    ]
)


# 3. 출력파서
output_paser = StrOutputParser()

chain = prompt | llm | output_paser

question = """
더불어민주당 이재명 대선 후보가 미국과의 관세 협상과 관련해 "서두르지 않는 게 중요하다"고 밝혔다.

이 후보는 8일 경제 유튜버들과의 연합 토크쇼인 '찐 리얼 경제 Talk, Talk! 라이브'에 출연해 미국 도널드 트럼프 대통령의 '관세 무기화'를 두고 한국의 협상 카드가 무엇이라고 보느냐는 질문에 이같이 답했다.

이 후보는 "민간 기업에도 개별적으로 미국과 협상하지 말라고 부탁하고 왔다"며 "나라 안에서 정부와 기업이 연합해야 하고, 비슷한 입장에 있는 국가들끼리도 공통 교섭을 하는 등 입장을 정리해볼 필요가 있다"고 설명했다.

주식 투자와 관련해선 "배당을 안 하는 기업들이 회사에 돈이 쌓이니 후에 상속세가 걱정돼 주가를 낮추려 한다. 그래서 다른 계열사를 만들어 일감을 몰아준다"며 "이런 부당거래로 자산을 빼돌리기 하는데 이는 엄정하게 책임을 물어야 한다"고 지적했다.

이어 "자본시장을 정상화해야 한다"며 "미국 같은 경우도 금융 자산 중에 주식이 많은데 우리나라도 국민의 투자 기회를 부동산만이 아니라 다른 수단으로도 만들어줘야 한다"고 강조했다.

스테이블코인에 대한 질문에는 "이 시장에 빨리 진출해야 하고 (투자자들이) 불안하지 않게 거래에 참여할 수 있게 관리하고 감시해야 한다"며 "원화 기반 스테이블코인 시장도 만들어놔야 소외되지 않고 국부 유출도 막을 수 있다"고 답했다.
"""
answer = chain.invoke({'conversation' : question})
print(answer)
