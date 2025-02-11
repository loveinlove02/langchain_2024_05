from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_experimental.tools import PythonAstREPLTool

def print_and_execute(code, debug=True):
    python_tool = PythonAstREPLTool()

    if debug==True:
        print('코드:')
        print(code)
    
    return python_tool.invoke(code)

prompt = ChatPromptTemplate.from_messages(      # 파이썬 코드 작성을 지시하는 프롬프트
    [
        (
            "system",
            "You are Raymond Hetting, an expert python programmer, well versed in meta-programming and elegant, concise and short but well documented code. You follow the PEP8 style guide. "
            "Return only the code, no intro, no explanation, no chatty, no markdown, no code block, no nothing. Just the code.",
        ),
        ("human", "{input}"),
    ]
)

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini', 
    temperature=0
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser | RunnableLambda(print_and_execute)


answer = chain.invoke({'input': '피보나치 수열의 10항까지 출력해주세요.'})
print(answer)

