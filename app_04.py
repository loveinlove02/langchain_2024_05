from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

from app_02 import answer
from graph_image.draw_grpah_image_png import save_graph_image


from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

class State(TypedDict):
    messages: Annotated[list, add_messages]

# LLM
llm = ChatOpenAI(api_key=key,model='gpt-4o-mini')

# -------------------------------
# chatbot 함수 노드 : state 를 받아서 LLM 으로 실행
# -------------------------------
def chatbot(state: State):
    print('=====================')
    print('chatbot() 함수 시작')
    print(f"state['messages'] : {state['messages']}")
    answer = llm.invoke(state['messages'])
    print('chatbot() 함수 끝')
    print('=====================')

    return {'messages': [answer]}

# state1 = State(messages=[])
# print(state1)
