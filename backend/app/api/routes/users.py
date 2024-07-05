from fastapi import APIRouter, HTTPException

from app.crud import create_user, create_user_item, get_user_by_email, get_user_by_id, get_users
from ..deps import SessionDep
from app import models, schemas

router = APIRouter()


@router.get('/', response_model=list[schemas.User])
def list_users(
    db: SessionDep, skip: int = 0, limit: int = 100
):
    return get_users(db, skip, limit)

@router.get('/{user_id}', response_model=schemas.User)
def retrieve(user_id: int, db: SessionDep):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@router.post('/', response_model=schemas.User)
def create(user: schemas.UserCreate, db: SessionDep):
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400, detail='Email already registered'
        )
    return create_user(db, user)

@router.post('/{user_id}/items/', response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: SessionDep
):
    return create_user_item(db, item=item, user_id=user_id)
