from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


# http://127.0.0.1:8002/item
@app.get("/item")
async def item():
    item = Item(name='바나나', 
                description='바나나입니다.', 
                price=1000, 
                text=1.0)
    
    return {"item": item}
    

# http://127.0.0.1:8002/users
@app.get("/users")
async def read_users():
    return [{"username":  '홍길동'}, {"username":  '김민정'}]


# uvicorn app_07:app --port=8082 --reload
