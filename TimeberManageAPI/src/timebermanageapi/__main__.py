from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="tinyfast")


class Item(BaseModel):
    name: str
    price: float


items: dict[int, Item] = {}


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return items.get(item_id, {"error": "not found"})


@app.put("/items/{item_id}")
def put_item(item_id: int, item: Item):
    items[item_id] = item
    return item
