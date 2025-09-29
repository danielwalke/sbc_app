from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Example data model for POST request
class Item(BaseModel):
    name: str
    price: float

# GET request
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# POST request
@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price, "status": "created"}
