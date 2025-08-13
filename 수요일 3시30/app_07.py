from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Jinja2 Temlpate 생성. html 이 저장되는 경로
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float



# http://127.0.0.1:8002/items/2?q=hello
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None):
    item = Item(name='test_item', price=1000)
    item_dict= item.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={"id": id, "q": q, "item_dict": item_dict}
    )


# uvicorn app_06:app --port=8002 --reload 
