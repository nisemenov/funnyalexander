from sqlalchemy.orm import Session

from .models import Item, ItemCreate, User, UserCreate


# User
def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def get_user_by_email(db: Session, email) -> User | None:
    model = User
    return db.query(model).filter(model.email == email).first()

def get_users(db:Session, skip: int = 0, limit: int = 100) -> Session.query:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = User(
        email=user.email, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Item
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def create_user_item(
    db: Session, item: ItemCreate, user_id: int
) -> Item:
    db_item = Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
