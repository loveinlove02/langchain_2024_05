from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

class MyState(TypedDict):
    counter: int

def increment(state: MyState):
    print('===== increment() 함수 시작 =====')
    answer = state['counter'] + 1
    print(f'실행 결과 : {answer}')
    print('===== increment() 함수  끝 =====')

graph = StateGraph(MyState)
graph.add_node('increment', increment)  # increment 노드 생성

graph.add_edge(START, 'increment')  # START 에서 increment
graph.add_edge('increment', END)    # increment 에서 END

# 여기서 다시

