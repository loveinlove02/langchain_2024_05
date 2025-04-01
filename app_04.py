from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from graph_image.draw_grpah_image_png import save_graph_image

class State(TypedDict):
    counter: int

# counter를 증가시키는 노드 함수
def increment(state: State):
    answer = state['counter'] + 1
    return {'counter': answer}


graph = StateGraph(State)
graph.add_node('increment', increment)

graph.add_edge(START, 'increment')
graph.add_edge('increment', END)

app = graph.compile()

state1 = State(counter=0)
result = app.invoke(state1)
print(result)

