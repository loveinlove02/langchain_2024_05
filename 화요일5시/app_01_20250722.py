from fastapi import FastAPI

app = FastAPI()

# http://127.0.0.1:8002/
@app.get("/")
def root():
    return {"message" : "hello"}

# http://127.0.0.1:8002/items/
@app.get("/items")
def items():
    return {"item": "banana"}  

# http://127.0.0.1:8002/items/2
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# uvicorn 파일이름:객체이름 --port=포트번호 --reload 
# uvicorn app_01:app --port=8002 --reload 