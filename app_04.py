from langchain.agents import tool
from typing import List, Dict, Annotated
from langchain_teddynote.tools import GoogleNews
from langchain_experimental.utilities import PythonREPL

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# muz.so/랭체인스터디5

@tool
def search_keyword(query: str) -> List[Dict[str, str]]:
    """Look up news by keyword"""
    news_tool = GoogleNews()
    return news_tool.search_by_keyword(query, k=2)

anwer = search_keyword.invoke({'query': '6월 선거'})
print(anwer)


@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""

    result = ""
    
    try:
        result = PythonREPL().run(code)
    except BaseException as e:
        print(f"Failed to execute. Error: {repr(e)}")
    finally:
        return result


# 프롬프트는 에이전트에게 모델이 수행할 작업을 설명하는 텍스트를 제공합니다. (도구의 이름과 역할을 입력)
prompt = ChatPromptTemplate.from_messages(
    [
        (                                           
            "system",
            "You are a helpful assistant. "             
            "Make sure to use the `search_news` tool for searching keyword related news."
        ),
        ("placeholder", "{chat_history}"),          # 이전 대화 내용을 넣을 곳을 잡아둔다.
        ("human", "{input}"),                       # 사용자 입력

        # 에이전트가 검색하는 과정들이나 내용 등을 끄적이는 메모장 같은 공간을 플레이스 홀더로 만들어준다
        ("placeholder", "{agent_scratchpad}"),       
    ]
)
