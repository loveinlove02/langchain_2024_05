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

def save_graph_image(app, filename="state_graph.png"):
    try:
        # 스크립트 실행 위치 기반으로 'image' 폴더 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(script_dir, 'image')
        os.makedirs(image_dir, exist_ok=True)
        
        # 파일 경로 설정
        file_path = os.path.join(image_dir, filename)
        
        # 그래프 구조 시각화
        graph = app.get_graph()
        
        # Mermaid 다이어그램 PNG 생성
        png_data = graph.draw_mermaid_png()
        
        # 파일 저장
        with open(file_path, "wb") as f:
            f.write(png_data)

        print(f"✅ 그래프 이미지가 '{os.path.abspath(file_path)}' 경로에 저장되었습니다")
        
    except Exception as e:
        print(f"에러 발생: {str(e)}")

# 실행
save_graph_image(app, "state_graph.png")

