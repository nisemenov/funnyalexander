from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


# User
def get_user(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)

def get_user_by_email(db: Session, email) -> models.User | None:
    model = models.User
    return db.execute(select(model).where(model.email == email)).scalar_one()

def get_users(db:Session, skip: int = 0, limit: int = 100) -> Session.query:
    return db.execute(select(models.User)).all()

def create_user(db: Session, user: models.UserCreate) -> models.User:
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Item
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(
    db: Session, item: models.ItemCreate, user_id: int
) -> models.Item:
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
