from fastapi import FastAPI

app = FastAPI()

# http://127.0.0.1:8002/items/all
@app.get("/items/all")
async def read_all_items():
    return {"message" : "all_items"}

# http://127.0.0.1:8002/items/2
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id" : item_id}


# uvicorn 파일이름:변수이름 --port=8002 --reload
# uvicorn app_02:app --port=8002 --reload
