from fastapi import FastAPI

# ==============================
# Query Parameter (쿼리 파라미터)
# ==============================


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# ======================================================================
# http://127.0.0.1:8082/items?skip=0&limit=2
# 
# 함수에 개별 인자 값이 들어가 있는 경우 path 파라미터가 아닌 모든 인자는 query 파라미터
# ? 다음 부터 skip=0&limit=2 여기 까지 query 파라미터
# query 파라미터의 타입과 default 값을 함수인자로 설정할 수 있다.
# skip: int = 0  limit: int = 2 과 같이 default 값 0 으로 설정.
# 함수를 호출될 때 skip, limit 파리미터에 값이 안들어오면 default 값 0 
# ======================================================================
@app.get("/items")
async def read_item(skip: int = 0, limit: int = 2):
    return fake_items_db[skip : skip + limit]

# ======================================================================
# http://127.0.0.1:8082/items_nd/?skip=0&limit=2
# 함수를 호출될 때 skip, limit 파리미터에 값이 안들어오면 여기는 오류다 (반듯이 들어와야 됨)
# default 값을 설정하지 않았다.
# ======================================================================
@app.get("/items_nd/")
async def read_item_nd(skip: int, limit: int):
    return fake_items_db[skip : skip + limit]


# ======================================================================
# http://127.0.0.1:8082/items_op?skip=1&limit=2
# 
# 함수를 호출될 때 
# skip  파리미터에 값이 안들어오면 여기는 오류다. 반듯이 와야됨. 
# limit 파라미터에 값이 안들어 올수 도 있는데 default 값이 없으면 None이 설정. 
# ======================================================================
@app.get("/items_op/")
async def read_item_op(skip: int, limit: int | None = None):

    if limit:
        return fake_items_db[skip : skip + limit]
    else:
        return {"limit is not provided"}
    
# ======================================================================    
# http://127.0.0.1:8082/items/1?q='hello'
# path 파리미터와 query 파라미터 같이 사용
# ======================================================================
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    else:
        return {"item_id": item_id}
    
# uvicorn main_app_03:app --port=8082 --reload
