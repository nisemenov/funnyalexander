from fastapi import FastAPI, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.models import Item, ItemCreate, User, UserCreate
from app.core.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


# User
@app.post('/users/', response_model=User)
def create_user(user: UserCreate, db: SessionDep):
    if db_user := crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400, detail='Email already registered'
        )
    return crud.create_user(db, user)

@app.get('/users/', response_model=list[User])
def list_users(
    db: SessionDep, skip: int = 0, limit: int = 100
):
    users = crud.get_users(db, skip, limit)
    return users

@app.get('/users/{user_id}', response_model=User)
def retrieve_user(user_id: int, db: SessionDep):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


# Item
@app.post('/users/{user_id}/items/', response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate, db: SessionDep
):
    return crud.create_user_item(db, item=item, user_id=user_id)


@app.get('/items/', response_model=list[Item])
def read_items(
    db: SessionDep, skip: int = 0, limit: int = 100
):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
