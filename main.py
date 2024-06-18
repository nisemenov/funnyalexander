from enum import StrEnum
from typing import Annotated, Any
from fastapi import Body, Cookie, FastAPI, Path, Query
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class UserIn(User):
    password: str


class Image(BaseModel):
    url: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    image: Image | None = None


class ModelName(StrEnum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/items")
async def read_item(
    q: Annotated[
        list[str] | None, 
        Query(title='qqq', description='asas', min_length=4, deprecated=True)
    ],
    ads_id: Annotated[str | None, Cookie()] = None
):
    return q, ads_id

@app.post("/items/{item_id}", response_model=Item)
async def create_item(
    item: Item, 
    item_id: Annotated[int | None, Path(description='asdf')], 
    q: Annotated[str | None, Query(min_length=4)],
    user: User,
    importance: Annotated[int | None, Body()] = None
) -> Any:
    return item

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName, q: str | None = None):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!", 'q': q}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights

@app.get("/it/", response_model=list[Item] | Item)
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]

@app.post('/user/')
async def user(user: UserIn) -> User:
    user.model_dump
    return user
