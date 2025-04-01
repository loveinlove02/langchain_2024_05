from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

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


from langchain_core.messages import HumanMessage

state1 = State(messages=[])
human = HumanMessage(content='대구 교보 문고에 대해서 알려줘', id='1')
state1['messages'] = add_messages(state1['messages'], human)
print(state1)

a = chatbot(state1)
print(a)
