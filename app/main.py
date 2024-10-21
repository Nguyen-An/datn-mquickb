from fastapi import FastAPI
from app.users.router import router_users

app = FastAPI()

app.include_router(router_users)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}