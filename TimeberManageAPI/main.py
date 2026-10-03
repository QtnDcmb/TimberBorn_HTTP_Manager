from fastapi import FastAPI, Request
from pydantic import BaseModel
from timebermanageapi.timberborn import router as timberRouter


app = FastAPI(title="tinyfast")
app.include_router(timberRouter)


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

@app.api_route("/events/{name}/{state}", methods=["GET", "POST"])
async def timberborn_event(name: str, state: str, request: Request):
    body = (await request.body()).decode(errors="replace")
    print(f"[{request.method}] {name} {state} query={dict(request.query_params)} body={body!r}")
    return {"received": name}
