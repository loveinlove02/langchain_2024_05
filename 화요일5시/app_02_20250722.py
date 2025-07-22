from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name":'짬뽕'}, {"item_name":'자장면'}, {"item_name":'군만두'}]


# http://127.0.0.1:8002/items?start=0&end=2
@app.get("/items")
def read_item(start: int=0, end: int=2):
    return fake_items_db[start : start + end]



# uvicorn 파일이름:객체이름 --port=포트번호 --reload 
# uvicorn app_02:app --port=8002 --reload 
# http://127.0.0.1:8002/docs
