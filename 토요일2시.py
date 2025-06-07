from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from langchain_experimental.tools import PythonAstREPLTool

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

def print_and_execute(code):
    python_tool = PythonAstREPLTool()
    print('코드:')
    print(code)

    return python_tool.invoke(code)

# 1.프롬프트
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '당신은 Raymond Hetting으로, 메타프로그래밍에 능숙하고 우아하며 간결하고 짧지만 문서화가 잘 된 코드를 작성하는 파이썬 전문가 입니다.'
            'PEP8 스타일 가이드를 준수합니다. 소개, 설명, 잡담, 마크다운, 코드 불록 등은 모두 없이 코드만 출력하세요.'
        ),
        ('human', '{input}')
    ]
)

'''
(
    'system',
    'You are Raymond Hetting, an expert python programmer, well versed in meta-programming and elegant, concise and short but well documented code. You follow the PEP8 style guide. '
    'Return only the code, no intro, no explanation, no chatty, no markdown, no code block, no nothing. Just the code.',
)
'''
