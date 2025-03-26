from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

class MyState(TypedDict):
    counter: int


def increment(state: MyState) -> MyState:
    print(f"===== increment NODE =====")
    answer = state['counter'] + 1
    print(f"counter: {answer}")
    print(f"==========================")

    return {'counter': answer}



graph = StateGraph(MyState)

# 그래프 객체에 노드(함수) 추가
graph.add_node('increment', increment)

# START 에서 increment 으로 엣지
graph.add_edge(START, 'increment')

# increment 에서 END 로 엣지
graph.add_edge('increment', END)

app = graph.compile()

def save_graph_image(app, filename="./nggraph_state_graph.png"):
    png_data = app.get_graph().draw_mermaid_png()

    with open(filename, "wb") as f:
        f.write(png_data)
    
    print(f"그래프 이미지가 {filename} 파일로 저장되었습니다")

save_graph_image(app, "my_state_graph.png")  
