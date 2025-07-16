from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "자장면"}, {"item_name": "짬뽕"}, {"item_name": "탕수육"}]


# http://127.0.0.1:8002/items?skip=0&limit=2
@app.get("/items")
async def read_item(skip: int = 0, limit: int = 2):
    return fake_items_db[skip : skip + limit]

# http://127.0.0.1:8002/items_nd/?skip=0&limit=2
@app.get("/items_nd/")
async def read_item_nd(skip: int, limit: int):
    return fake_items_db[skip : skip + limit]

# uvicorn main_app_03:app --port=8082 --reload
