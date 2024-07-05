from fastapi import APIRouter

from app import crud
from ..deps import SessionDep
from app.schemas import Item

router = APIRouter()


@router.get('/', response_model=list[Item])
def read_items(
    db: SessionDep, skip: int = 0, limit: int = 100
):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
